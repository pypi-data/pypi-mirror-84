#! env python
import json
import os
import sys
import semantic_version
import git
import requests
import getpass
import re
from requests.auth import HTTPBasicAuth
import requests.exceptions
from time import sleep
from .config.common_site_config import get_config
import click
import gitlab
import datetime

app_map = {
	'frappe': 'dodock',
	'erpnext': 'dokos'
}

branches_to_update = {
	'develop': [],
	'staging': [],
	'hotfix': []
}

releasable_branches = ['master']

def release(bench_path, app, bump_type, from_branch, to_branch,
		remote='upstream', owner='dokos', prerelease=False, prerelease_date=None, repo_name=None, frontport=True):

	confirm_testing()
	config = get_config(bench_path)

	if not config.get('release_bench'):
		print('bench not configured to release')
		sys.exit(1)


	if config.get('branches_to_update'):
		branches_to_update.update(config.get('branches_to_update'))

	if config.get('releasable_branches'):
		releasable_branches.extend(config.get('releasable_branches',[]))

	gitlab = authenticate(bench_path, config)

	bump(gitlab, bench_path, app, bump_type, from_branch=from_branch, to_branch=to_branch, owner=owner,
		prerelease=prerelease, prerelease_date=prerelease_date, repo_name=repo_name, remote=remote, frontport=frontport)

def authenticate(bench_path, config):
	gitlab_token = config.get('gitlab_token')

	if not gitlab_token:
		gitlab_token = click.prompt('Gitlab Token', type=str)

	return gitlab.Gitlab('https://gitlab.com', private_token=gitlab_token)

def confirm_testing():
	print('')
	print('================ CAUTION ==================')
	print('Never miss this, even if it is a really small release!!')
	print('')
	print('')
	click.confirm('Is manual testing done ?', abort = True)
	click.confirm('Have you added a change log ?', abort = True)

def bump(gitlab, bench_path, app, bump_type, from_branch, to_branch, remote, owner, \
	prerelease=False, prerelease_date=None, repo_name=None, frontport=True):
	assert bump_type in ['minor', 'major', 'patch', 'stable', 'prerelease']

	repo_path = os.path.join(bench_path, 'apps', app)
	push_branch_for_old_major_version(bench_path, bump_type, app, repo_path, from_branch, to_branch, remote, owner)
	update_branches_and_check_for_changelog(repo_path, from_branch, to_branch, remote=remote)
	message = get_release_message(repo_path, from_branch=from_branch, to_branch=to_branch, remote=remote)

	if not message:
		print('No commits to release')
		return

	print('')
	print(message)
	print('')

	click.confirm('Do you want to continue?', abort=True)

	try:
		new_version = bump_repo(repo_path, bump_type, from_branch=from_branch, to_branch=to_branch, prerelease=prerelease)
		commit_changes(repo_path, new_version, to_branch)
		tag_name = create_release(repo_path, new_version, from_branch=from_branch, to_branch=to_branch, frontport=frontport)
		push_release(repo_path, from_branch=from_branch, to_branch=to_branch, remote=remote)
		prerelease = True if 'beta' in new_version else False
		create_gitlab_release(gitlab, repo_path, tag_name, message, remote=remote, owner=owner, repo_name=repo_name, prerelease=prerelease, prerelease_date=prerelease_date)
		print('Released {tag} for {repo_path}'.format(tag=tag_name, repo_path=repo_path))
	except Exception as e:
		print(e)

def update_branches_and_check_for_changelog(repo_path, from_branch, to_branch, remote='upstream'):

	update_branch(repo_path, to_branch, remote=remote)
	update_branch(repo_path, from_branch, remote=remote)

	for branch in branches_to_update[from_branch]:
		update_branch(repo_path, branch, remote=remote)

	git.Repo(repo_path).git.checkout(from_branch)
	check_for_unmerged_changelog(repo_path)

def update_branch(repo_path, branch, remote):
	print("updating local branch of", repo_path, 'using', remote + '/' + branch)

	repo = git.Repo(repo_path)
	g = repo.git
	g.fetch(remote)
	g.checkout(branch)
	g.reset('--hard', remote+'/'+branch)

def check_for_unmerged_changelog(repo_path):
	current = os.path.join(repo_path, os.path.basename(repo_path), 'change_log', 'current')
	if os.path.exists(current) and [f for f in os.listdir(current) if f != "readme.md"]:
		raise Exception("Unmerged change log! in " + repo_path)

def get_release_message(repo_path, from_branch, to_branch, remote='upstream'):
	print('getting release message for', repo_path, 'comparing', to_branch, '...', from_branch)

	repo = git.Repo(repo_path)
	g = repo.git
	log = g.log('{remote}/{to_branch}..{remote}/{from_branch}'.format(
		remote=remote, to_branch=to_branch, from_branch=from_branch), '--format=format:%s', '--no-merges')

	if log:
		return "* " + log.replace('\n', '\n* ')

def bump_repo(repo_path, bump_type, from_branch, to_branch, prerelease):
	current_version = get_current_version(repo_path, to_branch)
	new_version = get_bumped_version(current_version, bump_type, prerelease)

	print('bumping version from', current_version, 'to', new_version)

	set_version(repo_path, new_version, to_branch)
	return new_version

def get_current_version(repo_path, to_branch):
	# TODO clean this up!
	version_key = '__version__'

	if to_branch.lower() in releasable_branches:
		filename = os.path.join(repo_path, os.path.basename(repo_path), '__init__.py')
	else:
		filename = os.path.join(repo_path, os.path.basename(repo_path), 'hooks.py')
		version_key = 'staging_version'

	with open(filename) as f:
		contents = f.read()
		match = re.search(r"^(\s*%s\s*=\s*['\\\"])(.+?)(['\"])(?sm)" % version_key,
				contents)
		return match.group(2)

def get_bumped_version(version, bump_type, prerelease=False):
	v = semantic_version.Version(version)
	if prerelease:
		if v.prerelease == ():
			v.prerelease = ('beta', '1')

		elif len(v.prerelease) == 2:
			v.prerelease = ('beta', str(int(v.prerelease[1]) + 1))

		else:
			raise ("Something wen't wrong while doing a prerelease")

	if bump_type == 'major':
		v.major += 1
		v.minor = 0
		v.patch = 0

	elif bump_type == 'minor':
		v.minor += 1
		v.patch = 0

	elif bump_type == 'patch':
		v.patch += 1

	elif bump_type == 'stable':
		# remove pre-release tag
		v.prerelease = None

	elif bump_type == 'prerelease':
		pass

	else:
		raise ("bump_type not amongst [major, minor, patch, prerelease]")

	click.confirm('Do you want to create version {version}?'.format(version=str(v)), abort=True)

	return str(v)

def set_version(repo_path, version, to_branch):
	if to_branch.lower() in releasable_branches:
		set_filename_version(os.path.join(repo_path, os.path.basename(repo_path),'__init__.py'), version, '__version__')
	else:
		set_filename_version(os.path.join(repo_path, os.path.basename(repo_path),'hooks.py'), version, 'staging_version')

	# TODO fix this
	# set_setuppy_version(repo_path, version)
	# set_versionpy_version(repo_path, version)
	# set_hooks_version(repo_path, version)

# def set_setuppy_version(repo_path, version):
# 	set_filename_version(os.path.join(repo_path, 'setup.py'), version, 'version')
#
# def set_versionpy_version(repo_path, version):
# 	set_filename_version(os.path.join(repo_path, os.path.basename(repo_path),'__version__.py'), version, '__version__')
#
# def set_hooks_version(repo_path, version):
# 	set_filename_version(os.path.join(repo_path, os.path.basename(repo_path),'hooks.py'), version, 'app_version')

def set_filename_version(filename, version_number, pattern):
	changed = []

	def inject_version(match):
		before, dummy, after = match.groups()
		changed.append(True)
		return before + version_number + after

	with open(filename) as f:
		contents = re.sub(r"^(\s*%s\s*=\s*['\\\"])(.+?)(['\"])(?sm)" % pattern,
				inject_version, f.read())

	if not changed:
		raise Exception('Could not find %s in %s', pattern, filename)

	with open(filename, 'w') as f:
		f.write(contents)

def commit_changes(repo_path, new_version, to_branch):
	print('committing version change to', repo_path)

	repo = git.Repo(repo_path)
	app_name = os.path.basename(repo_path)

	if to_branch.lower() in releasable_branches:
		repo.index.add([os.path.join(app_name, '__init__.py')])
	else:
		repo.index.add([os.path.join(app_name, 'hooks.py')])

	repo.index.commit('bumped to version {}'.format(new_version))

def create_release(repo_path, new_version, from_branch, to_branch, frontport=True):
	print('creating release for version', new_version)
	repo = git.Repo(repo_path)
	g = repo.git
	g.checkout(to_branch)
	try:
		g.merge(from_branch, '--no-ff')
	except git.exc.GitCommandError as e:
		handle_merge_error(e, source=from_branch, target=to_branch)

	tag_name = 'v' + new_version
	repo.create_tag(tag_name, message='Release {}'.format(new_version))
	g.checkout(from_branch)

	try:
		g.merge(to_branch)
	except git.exc.GitCommandError as e:
		handle_merge_error(e, source=to_branch, target=from_branch)

	if frontport:
		for branch in branches_to_update[from_branch]:
			print ("Front porting changes to {}".format(branch))
			print('merging {0} into'.format(to_branch), branch)
			g.checkout(branch)
			try:
				g.merge(to_branch)
			except git.exc.GitCommandError as e:
				handle_merge_error(e, source=to_branch, target=branch)

	return tag_name

def handle_merge_error(e, source, target):
	print('-'*80)
	print('Error when merging {source} into {target}'.format(source=source, target=target))
	print(e)
	print('You can open a new terminal, try to manually resolve the conflict/error and continue')
	print('-'*80)
	click.confirm('Have you manually resolved the error?', abort=True)

def push_release(repo_path, from_branch, to_branch, remote='upstream'):
	print('pushing branches', to_branch, from_branch, 'of', repo_path)
	repo = git.Repo(repo_path)
	g = repo.git
	args = [
		'{to_branch}:{to_branch}'.format(to_branch=to_branch),
		'{from_branch}:{from_branch}'.format(from_branch=from_branch)
	]

	for branch in branches_to_update[from_branch]:
		print('pushing {0} branch of'.format(branch), repo_path)
		args.append('{branch}:{branch}'.format(branch=branch))

	args.append('--tags')

	print(g.push(remote, *args))

def create_gitlab_release(gitlab, repo_path, tag_name, message, remote='upstream', owner='frappe',
		repo_name=None, prerelease=False, prerelease_date=None):

	data = {
		'tag_name': tag_name,
		'name': 'Release ' + tag_name,
		'description': message,
		'released_at': datetime.datetime.strptime(prerelease_date, "%Y-%m-%d").isoformat() if prerelease and prerelease_date else None
	}

	print('')
	click.echo(data)
	print('')

	click.confirm('Do you want to create a release with the above data ?', abort=True)
	print('creating release on gitlab')

	repo_name = repo_name or os.path.basename(repo_path)
	for i in range(3):
		try:
			project = gitlab.projects.get('dokos/{repo_name}'.format(repo_name=app_map.get(repo_name)))
			project.releases.create(data)
			break
		except requests.exceptions.HTTPError:
			print('request failed, retrying....')
			sleep(3*i + 1)
			if i !=2:
				continue
			else:
				print(release)
				raise
	return release

def push_branch_for_old_major_version(bench_path, bump_type, app, repo_path, from_branch, to_branch, remote, owner):
	if bump_type != 'major':
		return

	current_version = get_current_version(repo_path, to_branch)
	old_major_version_branch = "v{major}.x.x".format(major=current_version.split('.')[0])

	click.confirm('Do you want to push {branch}?'.format(branch=old_major_version_branch), abort=True)

	update_branch(repo_path, to_branch, remote=remote)

	g = git.Repo(repo_path).git
	g.checkout(b=old_major_version_branch)

	args = [
		'{old_major_version_branch}:{old_major_version_branch}'.format(old_major_version_branch=old_major_version_branch),
	]

	print("Pushing {old_major_version_branch} ".format(old_major_version_branch=old_major_version_branch))
	print(g.push(remote, *args))

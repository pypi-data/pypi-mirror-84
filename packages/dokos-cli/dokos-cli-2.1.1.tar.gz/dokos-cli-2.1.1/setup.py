from setuptools import find_packages, setup

from bench import PROJECT_NAME, VERSION

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

setup(
	name=PROJECT_NAME,
	description='Command line tools for Dodock/Dokos',
	url='https://dokos.io',
	author='Dokos SAS',
	author_email='hello@dokos.io',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	version=VERSION,
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
	entry_points='''
[console_scripts]
docli=bench.cli:cli
bench=bench.cli:cli
''',
)

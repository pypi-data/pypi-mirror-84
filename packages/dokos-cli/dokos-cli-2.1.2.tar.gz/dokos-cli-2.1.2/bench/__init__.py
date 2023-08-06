VERSION = "2.1.2"
PROJECT_NAME = "dokos-cli"
FRAPPE_VERSION = None

def set_frappe_version(bench_path='.'):
	from .app import get_current_frappe_version
	global FRAPPE_VERSION
	if not FRAPPE_VERSION:
		FRAPPE_VERSION = get_current_frappe_version(bench_path=bench_path)

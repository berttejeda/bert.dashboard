from btdashboard.logger import Logger

import os
import sys

logger = Logger().init_logger(__name__)
is_frozen = getattr(sys, 'frozen', False)
if is_frozen:
  my_file_name = os.path.basename(sys.executable)
  # If the MEIPASS attribute is available in the sys module, 
  # this indicates a single-file executable created by pyinstaller
  # If MEIPASS attribute is not detected, fallback to the path of the frozen executable
  sys_executable_path = os.path.dirname(os.path.abspath(sys.executable))
  project_root = getattr(sys, '_MEIPASS', sys_executable_path)
else:
  my_file_name = __file__
  project_root = os.path.dirname(my_file_name)

def do_if_frozen():

  logger.debug('Detected installation type is "frozen"')
  static_folder_relative = './%s' % gui_dirname
  static_folder = os.path.join(project_root, static_folder_relative)
  logger.info('Checking %s' % static_folder)
  if os.path.exists(static_folder):
    logger.info('Found %s' % static_folder)
    return static_folder
  else: # Check for frozen py2app
    static_folder_relative = '../Resources/%s' % gui_dirname
    static_folder = os.path.join(project_root, static_folder_relative)
    logger.info('Checking %s' % static_folder)
    if os.path.exists(static_folder):
      logger.info('Found %s' % static_folder)
      return static_folder_relative
    else:
      logger.error('%s not found' % static_folder)
      return None

def do_if_not_frozen():

  import re
  import site
  import sysconfig
  root_package_name = __name__.split('.')[0]
  site_packages_path = sysconfig.get_paths().get('purelib', 'DNE')
  site_packages_data_path = sysconfig.get_paths().get('data', 'DNE')
  user_scripts_paths = [p for p in site.getsitepackages() if 'site-packages' in p]
  if len(user_scripts_paths) > 0:
    user_scripts_path = user_scripts_paths[0]
    user_package_path = os.path.realpath(os.path.join(user_scripts_path, root_package_name))
  else:
    user_scripts_path = user_package_path = 'DNE'
  root_package_path = os.path.realpath(os.path.join(site_packages_path, root_package_name))
  logger.debug(f'Root Package Name: {root_package_name}')
  logger.debug(f'Root Package Path: {root_package_path}')
  logger.debug(f'Site Packages Path: {site_packages_path}')
  logger.debug(f'User Scripts Path: {user_scripts_paths}')
  logger.debug(f'Site Packages Data Path: {site_packages_data_path}')
  try:
    import btdashboard
    pip_package_path = ''.join(btdashboard.__path__)
    logger.debug(f'Pip Package Path: {pip_package_path}')
    if re.search('dist-packages|site-packages', pip_package_path):
      logger.debug('Found pip package path at %s' % pip_package_path)
      if os.name == 'nt':
        package_path = root_package_path if os.path.isdir(root_package_path) else user_package_path
      else:
        pattern = re.compile('/lib/.*')
        logger.debug('Platform is POSIX-compliant')
        package_path_base_dir = pattern.sub('', ''.join(pip_package_path))
        package_path = os.path.join(package_path_base_dir, 'bin')
        logger.debug('Using pip package path of %s' % package_path)
    else:
      package_path = 'DNE'
      logger.debug('pip package does not exist')
  except Exception as e:
    logger.debug(f'pip package does not exist: {e}')
    pass
  asset_paths = [
      os.getcwd(),
      os.path.realpath(os.path.expanduser('~')),
      os.path.join(os.path.abspath(os.sep), 'etc'),
      package_path,
      os.path.join(site_packages_data_path,'bin'),
      os.path.abspath(os.path.join(package_path, os.pardir, 'scripts')),
      os.path.abspath(os.path.join(package_path, os.pardir, 'Scripts')),
      os.path.abspath(os.path.join(project_root, os.pardir))
  ] + [p[1] for p in sysconfig.get_paths().items()]
  return asset_paths

def get_asset_search_paths():
  logger.info('Determining search paths to application assets')
  logger.debug(f'Is Frozen?: {is_frozen}')
  logger.debug(f'Detected file name: {my_file_name}')
  logger.debug(f'Detected project root: {project_root}')
  asset_search_paths = []
  if is_frozen: # Check for frozen pyinstaller app
    asset_search_paths = do_if_frozen()
  else: # Check for unfrozen development app
    asset_search_paths = do_if_not_frozen()
  return asset_search_paths

# def get_dashboard_config_path():
#   logger.info('Determining path to dashboard config')
#   logger.debug(f'Is Frozen?: {is_frozen}')
#   logger.debug(f'Detected file name: {my_file_name}')
#   logger.debug(f'Detected project root: {project_root}')
#   if is_frozen: # Check for frozen pyinstaller app
#     dashboard_config_path = do_if_frozen()
#   else: # Check for unfrozen development app
#     dashboard_config_path = do_if_not_frozen()
#   if dashboard_config_path:
#     return dashboard_config_path
#   else:
#     raise Exception('No config file found for dashboard settings')
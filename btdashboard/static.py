import os

from btdashboard.defaults import gui_dirname
from btdashboard.logger import Logger

logger = Logger().init_logger(__name__)

def get_static_folder_path(search_paths):

  static_folder_found = False

  static_folder_paths = [
      os.path.expanduser(os.path.join(p, gui_dirname))
      for p in search_paths
  ]

  for static_folder_path in static_folder_paths:
      logger.debug(f'Checking {static_folder_path}')
      if os.path.exists(static_folder_path):
          logger.info(f'Found {static_folder_path}')
          return static_folder_path

  if not static_folder_found:
    raise Exception(f'Could not find static assets folder in any of the expected locations')

# from btdashboard.defaults import default_settings
from btdashboard.logger import Logger
import os
from btconfig import Config

logger = Logger().init_logger(__name__)

class AppConfig():

  def __init__(self, **kwargs):
    pass

  def initialize(self, **kwargs):

    logger.info("Initializing config")
    args = kwargs.get('args', {})
    verify_tls = kwargs.get('verify_tls')
    # Initialize App Config
    initial_data = {
    'environment': os.environ
    }  

    config_file_uri = kwargs.get('config_file') or \
                      args.get('config_file')
    if config_file_uri:
      logger.info(f"Config file URI is {config_file_uri}")
      # Initialize App Config
      config = Config(
          config_file_uri=config_file_uri,
          initial_data=initial_data,
          args=args,
          verify_tls=verify_tls
      )

      settings = config.read()

      return settings
    else:
      return {}

  @staticmethod
  def get_config_path(search_paths, config_file_name):

    config_found = False

    config_file_paths = [
      os.path.expanduser(os.path.join(p, 'etc', config_file_name))
      for p in search_paths
    ]

    config_file_paths_adjacent = [
      os.path.expanduser(os.path.join(p, config_file_name))
      for p in search_paths
    ]

    config_file_paths.extend(config_file_paths_adjacent)

    for config_file_path in config_file_paths:
      logger.debug(f'Checking {config_file_path}')
      if os.path.exists(config_file_path):
        logger.info(f'Found {config_file_path}')
        return config_file_path

    if not config_found:
      logger.error(f'Could not find {config_file_name} config file in any of the expected locations')
      return None

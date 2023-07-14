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
from btdashboard.config import AppConfig
from btdashboard.defaults import default_sidebar_config_file_name
from btdashboard.defaults import default_verify_tls
from btdashboard.logger import Logger

logger = Logger().init_logger(__name__)

class SideBar():

  def __init__(self, **kwargs):
    args = kwargs['args']
    config_search_paths = kwargs['config_search_paths']
    verify_tls = args.no_verify_tls or default_verify_tls

    if args.sidebar_config_file:
      sidebar_config_file = args.sidebar_config_file
    else:
      sidebar_config_file = AppConfig.get_config_path(
        config_search_paths,
        default_sidebar_config_file_name
      )
    sidebar_config = AppConfig().initialize(
      args=vars(kwargs['args']),
      config_file=sidebar_config_file,
      verify_tls=verify_tls
    )
    self.settings = sidebar_config

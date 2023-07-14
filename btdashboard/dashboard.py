import base64
import json
from btdashboard.config import AppConfig
from btdashboard.defaults import default_dashboard_config_file
from btdashboard.defaults import default_verify_tls
from btdashboard.logger import Logger
from subprocess import run

logger = Logger().init_logger(__name__)

class Dashboard():

  def __init__(self, **kwargs):
    args = kwargs['args']
    verify_tls = args.no_verify_tls or default_verify_tls
    dashboard_config = AppConfig().initialize(
    args=vars(args),
    config_file=args.dashboard_config_file or default_dashboard_config_file,
    verify_tls=verify_tls
    )
    self.settings = dashboard_config
    self.make_data()

  def make_data(self, **kwargs):
    logger.info('Rendering dashboard data ...')
    for dk, dv in self.settings.dashboard.items():
      if hasattr(self.settings.dashboard[dk], 'items'):
        for ck,cv in list(self.settings.dashboard[dk].items()):
          for k, v in list(self.settings.dashboard[dk][ck].items()):
            data = self.settings.dashboard[dk][ck].get('data', {})
            data_exec = data.get('exec')
            if data_exec:
              try:
                command = data_exec.command
                command_args = ' '.join(data_exec.args)
                exec_command = f"{command} {command_args}"
                exec_result = run(['/bin/bash', '-c', exec_command], capture_output=True, text=True)
                exec_result_decoded = base64.b64decode(exec_result.stdout)
                json_result = json.loads(exec_result_decoded)
              except Exception as e:
                logger.error(f'Encountered an error rending Dashboard data - {e}')
                json_result = json.loads('{"error":"%s"}' % e)
              self.settings.dashboard[dk][ck]['data'] = json_result
              break
    logger.info('Dashboard data rendering complete')

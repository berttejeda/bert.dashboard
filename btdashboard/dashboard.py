import base64
import json
from btdashboard.config import AppConfig
from btdashboard.defaults import default_dashboard_config_file
from btdashboard.defaults import default_dashboard_throttle
from btdashboard.defaults import default_dashboard_backoff_num_retries
from btdashboard.defaults import default_dashboard_backoff_sleep_time
from btdashboard.defaults import default_verify_tls
from btdashboard.logger import Logger
from schema import Schema, SchemaError
from subprocess import run
from time import sleep
import math

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
    self.throttle = dashboard_config.get('processing.throttle', default_dashboard_throttle)
    self.num_retries = dashboard_config.get('processing.backoff.num_retries', default_dashboard_backoff_num_retries)
    self.sleep_time = dashboard_config.get('processing.backoff.sleep_time', default_dashboard_backoff_sleep_time)
    self.make_data()

  def make_data(self, **kwargs):
    logger.info('Rendering dashboard data ...')
    for dk, dv in self.settings.dashboard.items():
      if dk != 'cards':
        continue
      if hasattr(self.settings.dashboard[dk], 'items'):
        for ck,cv in list(self.settings.dashboard[dk].items()):
          logger.info(f"Processing dashboard object '{ck}'")
          for k, v in list(self.settings.dashboard[dk][ck].items()):
            data = self.settings.dashboard[dk][ck].get('data', {})
            data_exec = data.get('exec')
            data_schema = data.get('schema')
            if data_exec:
              try:
                command = data_exec.command
                command_args = ' '.join(data_exec.args)
                exec_command = f"{command} {command_args}"
                shell_command = data_exec.get('shell', ['/bin/bash', '-c'])
                exec_result = run([*shell_command, exec_command], capture_output=True, universal_newlines=True, text=True)
                exec_result_decoded = '{"error": "Data failed decoding"}'
                logger.info(f'Decoding dashboard data for {ck}')
                exec_result_to_decode = exec_result.stdout
                decode_err = None
                for x in range(0, self.num_retries):
                  try:
                    exec_result_decoded = base64.b64decode(exec_result_to_decode)
                  except Exception as e:
                    try:
                      logger.warning(f'Fixed base64 padding {ck} data result')
                      exec_result_decoded = base64.b64decode(exec_result_to_decode + '===').decode("utf-8", "ignore")
                    except Exception as e:
                      decode_err = str(e)
                  if decode_err:
                    logger.warn(f'Failed to decode dashboard data for {ck} ({decode_err})... reattempting in {self.sleep_time}s ')
                    sleep(self.sleep_time)  # wait before trying to fetch the data again
                    self.sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
                  else:
                    break
                json_result = json.loads(exec_result_decoded)
                if not decode_err and data_schema:
                  logger.info(f'{ck} - validating data schema')
                  if isinstance(data_schema, dict):
                    for validation in data_schema.get('validations', []):
                      data_schema_obj = eval(validation)
                      schema = Schema(data_schema_obj)
                      try:
                        schema.validate(json_result)
                        logger.info(f"Schema validation passed for '{ck}'")
                      except SchemaError as e:
                        json_result = {"error": json.dumps(e.args)}
              except Exception as e:
                logger.error(f'Encountered an error rending Dashboard data - {e}')
                json_result = {"error": f'{e}'}
              self.settings.dashboard[dk][ck]['data'] = json_result
              break
          logger.info(f'Waiting {self.throttle} seconds ...')
          sleep(self.throttle)
    logger.info('Dashboard data rendering complete')

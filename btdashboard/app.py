"""
Application entrypoint. This module initializes the API and, optionally, forks shell processes
for the Webterminal UI element.

Components:

-   [`app`][btdashboard.app.main], the application's main function. Invokes the Flask module
    to initialize the API and serve up the static assets built from the React [source](src) code. 
    If the `-aio` flag is specified, the main function will invoke the multiprocessing module
    to spawn a websocket that handles forking of shell sessions for attachment by the WebTerminal
    UI element. 
    The code for this was taken from [spyder-terminal](https://github.com/spyder-ide/spyder-terminal).
"""

from btconfig.configutils import AttrDict
from btdashboard.args import parse_args
from btdashboard.config import AppConfig
from btdashboard.defaults import default_app_port, \
default_app_config, \
default_app_config_file_name, \
default_app_host_address, \
default_footer_websocket_address, \
default_webterminal_listen_host , \
default_webterminal_listen_port, \
default_rightpane_websocket_address, \
default_verify_tls
from btdashboard.entrypoint import get_asset_search_paths
from btdashboard.static import get_static_folder_path
from btdashboard.logger import Logger
from btdashboard.dashboard import Dashboard
from btdashboard.sidebar import SideBar
from btdashboard.topics import Topics
from btdashboard.lessons import Lessons
from btdashboard.webterminal import WebTerminal
from btdashboard.websocket import WebSocket
from flask import Flask, jsonify, make_response, request, send_from_directory
from flask_cors import CORS
import json
import os
import requests
import threading
import webbrowser
import mimetypes

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')

# Read command-line args
args = parse_args()

# Initialize logging facility
logger_obj = Logger(logfile_path=args.logfile_path, logfile_write_mode=args.logfile_write_mode)
logger = logger_obj.init_logger('app')

global app_config

def start_webterminal(app_config_input):
  app_config = json.loads(app_config_input)
  webterminal_listen_host  = args.webterminal_listen_host or default_webterminal_listen_host
  webterminal_listen_port = args.webterminal_listen_port or default_webterminal_listen_port
  WebTerminal(app_config, args).start(host=webterminal_listen_host , port=webterminal_listen_port)

def start_api(app_config_input, asset_search_paths):
  """

  API functions
  
  This function defines the API routes and starts the API Process.

  """
  app_config = AttrDict(json.loads(app_config_input))

  # Initialize Lessons
  lessons = Lessons(args=args, config_search_paths=asset_search_paths)

  if args.api_only:
      static_assets_folder = None
  else:
      static_assets_folder = args.static_assets_folder or get_static_folder_path(asset_search_paths)
      logger.info(f'Static assets folder is {static_assets_folder}')

  # Initialize Topics
  topics = Topics(
      settings=lessons.settings,
      args=args)

  # Initialize Dashboard
  dashboard = Dashboard(args=args, config_search_paths=asset_search_paths)

  # Initialize Sidebar
  sidebar = SideBar(args=args, config_search_paths=asset_search_paths)

  # Initialize Websocket handler
  websocket = WebSocket()

  if static_assets_folder:
      app = Flask(__name__, static_url_path='', static_folder=static_assets_folder)
      if args.cors_origin:
          CORS(app, resources={r"*": {"origins": args.cors_origin}})
      else:
          logger.warning('CORS Policy effectively disabled, as no Origin Pattern specified')
          CORS(app, resources={r"*": {"origins": "*"}})
  else:
      logger.info('Serving API Only, no static assets')
      app = Flask(__name__)
      if args.cors_origin:
          CORS(app, resources={r"*": {"origins": args.cors_origin}})
      else:
          logger.warning('CORS Policy effectively disabled, as no Origin Pattern specified')
          CORS(app, resources={r"*": {"origins": "*"}})

  @app.route('/', defaults={'path': ''})
  @app.route('/<path:path>')
  def serve(path=""):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

  @app.route('/api/sendToWebsocket', methods=['POST'])
  def send_to_websocket():
    try:
      wsURL = request.json.get('wsURL')
      data = request.json.get('data')
      websocket.send_to_websocket(wsURL, data)
      resp = jsonify(success=True)
    except Exception as e:
      resp = jsonify(error=True)
    return resp

  @app.route('/api/loadLesson', methods=['POST'])
  def load_lesson():
    lesson_uri = request.json.get('uri')
    encoded_lesson_obj = lessons.load_lesson(lesson_uri)
    return encoded_lesson_obj

  @app.route('/api/getRightPaneWebSocketAddress')
  def get_rightpane_websocket_address():
    default_address = app_config.get('webterminal.rightpane.address', default_rightpane_websocket_address)
    effective_address = default_address
    response_obj = {'address': effective_address}
    return response_obj

  @app.route('/api/terminals/<terminalPID>/size', methods = ['POST'])
  def resize_terminal(**kwargs):
    if args.webterminal_host:
        footer_websocket_address = args.webterminal_host
    else:
        footer_websocket_address = app_config.get('webterminal.footer.address', default_footer_websocket_address)
    footer_http_address = footer_websocket_address.replace('ws', 'http')
    cols = request.json.get('cols')
    rows = request.json.get('rows')
    data = {'rows': rows, 'cols': cols}
    terminal_pid = kwargs.get('terminalPID')
    resize_url = f'{footer_http_address}/api/terminals/{terminal_pid}/size?cols={cols}&rows={rows}'
    resize_request = requests.post(resize_url, json=data)
    if resize_request.status_code == 200:
      return {}
    else:
      resp = make_response("Failed to resize terminal", 500)
      return resp

  @app.route('/api/getFooterWebSocketAddress')
  def get_footer_websocket_address():
    if args.webterminal_host:
        footer_websocket_address = args.webterminal_host
    else:
        footer_websocket_address = app_config.get('webterminal.footer.address', default_footer_websocket_address)
    footer_http_address = footer_websocket_address.replace('ws', 'http')
    footer_query = f'{footer_http_address}/api/terminals?cols=256&rows=50'
    footer_request = requests.post(footer_query)
    if footer_request.status_code == 200:
        footer_websocket_address = f'{footer_websocket_address}/terminals/{footer_request.text}'
    logger.debug(f'Footer websocket address: {footer_websocket_address}')
    response_obj = {'address': footer_websocket_address}
    return response_obj

  @app.route('/api/getDashboardSettings')
  def get_dashboard_settings():
    return {'settings': dashboard.settings}

  @app.route('/api/getSideBarSettings')
  def get_sidebar_settings():
    return {'settings': sidebar.settings}

  @app.route('/api/getTopics')
  def get_topics():
    available_topics = topics.get()
    return available_topics

  @app.route('/api/getAppData')
  def get_app_id():
    app_data = app_config
    logger.debug(f'app_data is {app_data}')
    return {'settings': app_data}

  @app.route('/api/ping')
  def ping():
    return {'message': "pong"}

  logger.info("Start API")

  app_port = args.port or default_app_port
  app_host_address = args.host_address or default_app_host_address

  local_url = f"http://localhost:{app_port}"
  if 'WERKZEUG_RUN_MAIN' not in os.environ and not all([args.api_only or args.no_browser]):
    threading.Timer(args.open_browser_delay, lambda: webbrowser.open(local_url)).start()

  app.run(host=app_host_address, port=app_port)

  logger.info("Stop API")

def main():
    """The main entrypoint
    """
    verify_tls = args.no_verify_tls or default_verify_tls

    # Get asset search paths
    asset_search_paths = get_asset_search_paths()

    # Initialize App Configuration

    if args.app_config_file:
      app_config_file = args.app_config_file
    else:
      app_config_file = AppConfig.get_config_path(
        asset_search_paths,
        default_app_config_file_name
      )

    if app_config_file:
        app_config = AppConfig().initialize(
            args=vars(args),
            config_file=app_config_file,
            verify_tls=verify_tls
        )
    else:
        app_config = default_app_config

    app_config_data = json.dumps(app_config)

    if args.webterminal_only:
      start_webterminal()
    elif args.all_in_one:
      import multiprocessing as mp
      if hasattr(os, 'getppid'):  # only available on Unix
          logger.info(f'parent process: {os.getppid()}')
      logger.info('========================================')

      proc_api = mp.Process(target=start_api, args=(app_config_data,asset_search_paths))
      proc_api.deamon = True
      proc_api.start()

      proc_webterminal = mp.Process(target=start_webterminal, args=(json.dumps(app_config),))
      proc_webterminal.deamon = True
      proc_webterminal.start()

      proc_api.join()
      proc_webterminal.join()

    else:
        start_api(app_config_data, asset_search_paths)

if __name__ == '__main__':
  main()



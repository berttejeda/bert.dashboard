import os

# SSL Requests
default_verify_tls = True

# Websocket Settings
default_webterminal_listen_port = 10001
default_webterminal_listen_host  = '0.0.0.0'
default_websocket_address = f'ws://127.0.0.1:{default_webterminal_listen_port}'
default_footer_websocket_address = default_websocket_address
default_rightpane_websocket_address = default_websocket_address
default_webterminal_shell = '/bin/bash'
default_webterminal_shell_command = '-l'
default_webterminal_env = {
  "SHELL": 'bash',
  "TERM": 'xterm',
  "WEBTERMINAL": 'True',
  "TESTING": 'True',
}

# Flask app settings
gui_dirname = 'dashboard.gui'
default_app_name = "Bert's Dashboard"
default_app_port = 10000
default_open_browser_delay = 1.25
default_app_host_address = '0.0.0.0'
default_app_config_file = 'etc/app.yaml'
default_lessons_config_file = 'etc/lessons.yaml'
default_dashboard_throttle = 5
default_dashboard_backoff_sleep_time = 2
default_dashboard_backoff_num_retries = 4
default_dashboard_config_file = 'etc/dashboard.yaml'
default_sidebar_config_file = 'etc/sidebar.yaml'
default_app_id = 'btDashboard'
default_app_user = os.environ.get('USER') or os.environ.get('USERNAME') or 'Anonymous'

default_app_config = {
  "app_id": default_app_id,
  "app_user": default_app_user,
  "terminals": {
    "default": {
      "address": default_websocket_address
    },
    "footer": {
      "address": default_footer_websocket_address
    },
    "rightpane": {
      "address": default_rightpane_websocket_address
    }
  },
  "external_configs": [
    {
      "name": "bert.lessons",
      "uri": "https://raw.githubusercontent.com/berttejeda/bert.lessons/main/lessons.yaml"
    }
  ]
}


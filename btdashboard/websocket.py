from ws4py.client.threadedclient import WebSocketClient
import json
from btdashboard.logger import Logger

logger = Logger().init_logger(__name__)

class WebSocket():

    def __init__(self):
      pass
      
    def opened(self):
        pass

    def closed(self, code, reason):
        self.logger.info(("Closed", code, reason))

    def received_message(self, m):
        self.logger.info(("Message", json.loads(m.data.decode('utf-8'))))

    def send_to_websocket(self, wsUrl, data):
      logger.info(f'Sending data to socket at {wsUrl}: "{data}"')
      if len(wsUrl) > 0:
        websocket = WebSocketClient(wsUrl)
        websocket.daemon = False
        websocket.connect()
        msg = '''echo hello
        '''
        websocket.send(msg)
        websocket.close()
      else:
        logger.warning('Empty websocket URL!')
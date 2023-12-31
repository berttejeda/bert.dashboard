# -*- coding: iso-8859-15 -*-

"""Basic static index.html HTTP handler."""
import tornado.web
import tornado.escape
from os import getcwd
from urllib.parse import quote
from pathlib import Path


class MainHandler(tornado.web.RequestHandler):
    """Handles index request."""

    def initialize(self, db=None):
        """Stump initialization function."""
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        """Get static index.html page."""
        cwd = self.get_argument('path', getcwd())
        # We need to do percent encoding for sending the cwd through a cookie
        # For further information see spyder-ide/spyder-terminal#225
        self.set_cookie('cwd', quote(cwd))
        index_html_path = Path('../static/build/index.html').resolve().as_posix()
        self.render(index_html_path)

    @tornado.gen.coroutine
    def post(self):
        """POST verb: Forbidden."""
        self.set_status(403)

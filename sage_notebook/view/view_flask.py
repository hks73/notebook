"""
The View Component in Flask

This is the Gtk3 implementation of :mod:`view`.
"""

##############################################################################
#  Sage Notebook: A Graphical User Interface for Sage
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

import os
from flask import Flask

from .view import ViewABC
from .window_flask import WindowFlask
from sage_notebook.misc.cached_property import cached_property



class ViewFlask(ViewABC):
    
    def __init__(self, presenter):
        super(ViewFlask, self).__init__(presenter)
        static = os.path.join('flask', 'static')
        template = os.path.join('flask', 'templates')
        self._app = app = Flask(__name__, static_folder=static, template_folder=template) 
        app.config['DEBUG'] = True
        self._init_routes()

    def _init_routes(self):
        """
        Set up the Flask URL routing
        """
        self.notebook_window.add_url_rule_to(self.flask_app)

    @property
    def flask_app(self):
        """
        Return the Flask application object
        """
        return self._app

    @cached_property
    def about_window(self):
        raise NotImplementedError

    @cached_property
    def notebook_window(self):
        from .notebook_window_flask import NotebookWindowFlask
        return NotebookWindowFlask(self.presenter)

    @cached_property
    def preferences_window(self):
        raise NotImplementedError

    def new_notification_dialog(self, parent, text):
        raise NotImplementedError

    def new_error_dialog(self, parent, title, text):
        raise NotImplementedError
        
    def new_setup_assistant(self, parent, sage_root, callback):
        raise NotImplementedError


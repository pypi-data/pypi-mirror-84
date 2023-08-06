import logging
from threading import Thread

from flask import Flask

from telecom_coworker.recorder import Recorder
from telecom_coworker.web.config import Config
from telecom_coworker.web.db import Record
from telecom_coworker.web.zk import client

log = logging.getLogger('telecom_coworker.web')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from . import api
    app.register_blueprint(api.bp)
    from . import pages
    app.register_blueprint(pages.bp)

    app.add_url_rule('/', 'index', pages.index)

    from telecom_coworker.web.db import init_app as init_app_for_db
    init_app_for_db(app)

    if app.config['ENABLED_RECORDER']:
        with app.app_context():
            zk_namespace = app.config['ZK_NAMESPACE']
            recorder = Recorder(client(), zk_namespace, app)
            Thread(target=recorder).start()

    register_shell_context(app)
    register_commands(app)

    return app


def register_shell_context(app: Flask):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'Record': Record
        }

    app.shell_context_processor(shell_context)


def register_commands(app: Flask):
    from telecom_coworker.web import commands
    app.cli.add_command(commands.recorder)

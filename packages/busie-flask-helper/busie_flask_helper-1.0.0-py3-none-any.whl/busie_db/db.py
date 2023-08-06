from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import force_auto_coercion
from .loaders import Loader


class DBHelper(SQLAlchemy):
    """
    Helper class that extends sqlalchemy
    and exposes custom methods for ease of
    use in the Application Factory pattern
    """
    def __init__(self, root_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.migrate = Migrate()
        self.loader = Loader(root_dir=root_dir)

    def init_db(self, app=None, models_dir=None):
        """Init the global db object used by the application"""
        if isinstance(app, Flask):
            force_auto_coercion()
            self.loader.load_models(models_dir)
            self.init_app(app)
        else:
            raise ValueError('Cannot init DB without a Flask application')

    def init_migrate(self, app=None):
        """ initialize the global migration object"""
        if isinstance(app, Flask):
            self.migrate.init_app(app, self)
import pytest
from busie_db.db import DBHelper

def test_db_helper_init(mocker, mock_sql_alchemy):
    """
    - sets migrate attr to instance of Migrate
    - sets loader attr to instance of Loader
    """

    class Migrate(mocker.MagicMock):
        """Mock Migrate Class"""
        pass
    class Loader(mocker.MagicMock):
        """Mock Loader Class"""
        pass

    orm_mock = mocker.patch('busie_db.db.SQLAlchemy.__init__')
    migrate_mock = mocker.patch('busie_db.db.Migrate')
    migrate_mock.return_value = Migrate()
    loader_mock = mocker.patch('busie_db.db.Loader')
    loader_mock.return_value = Loader()
    db = DBHelper(root_dir='foo')
    orm_mock.assert_called_once()
    migrate_mock.assert_called_once()
    loader_mock.assert_called_once_with(root_dir='foo')
    assert hasattr(db, 'migrate')
    assert isinstance(getattr(db, 'migrate'), Migrate)
    assert hasattr(db, 'loader')
    assert isinstance(getattr(db, 'loader'), Loader)

def test_init_db__invalid_app(mocker, mock_flask, mock_sql_alchemy):
    """
    - Throws if provided app is not instance of Flask application
    """
    class Flask(mocker.MagicMock):
        pass
    mock_flask('busie_db.db', new=Flask)
    mock_sql_alchemy('busie_db.db')

    db = DBHelper(root_dir='foo')
    class InvalidClass:
        pass
    test_calls = [lambda: db.init_db(), lambda: db.init_db(app=InvalidClass())]
    for call in test_calls:
        with pytest.raises(ValueError):
            call()

def test_init_db(mocker, mock_flask, mock_sql_alchemy):
    """
    - forces auto coercion
    - loads models
    - inits app with app
    """
    class Flask(mocker.MagicMock):
        pass

    mock_loader = mocker.patch('busie_db.db.Loader')
    mock_force_auto_coercion = mocker.patch('busie_db.db.force_auto_coercion')
    mock_flask('busie_db.db', new=Flask)
    mock_init_app = mocker.patch('busie_db.db.SQLAlchemy.init_app')
    
    db = DBHelper(root_dir='foo')
    mock_app = Flask()
    models_dir = 'foo'
    db.init_db(app=mock_app, models_dir=models_dir)
    mock_force_auto_coercion.assert_called_once()
    mock_loader.return_value.load_models.assert_called_once_with(models_dir)
    mock_init_app.assert_called_once_with(mock_app)

def test_init_migrate(mocker, mock_sql_alchemy, mock_flask):
    """
    - migrate.init_app with app and db
    """
    class SQLAlchemy(mocker.MagicMock):
        pass
    class Migrate(mocker.MagicMock):
        pass
    class Flask(mocker.MagicMock):
        pass

    mock_sql_alchemy('busie_db.db', new=SQLAlchemy)
    mock_flask('busie_db.db', new=Flask)
    mocker.patch('busie_db.db.Migrate', new=Migrate)

    db = DBHelper(root_dir='foo')
    mock_app = Flask()

    db.init_migrate(app=mock_app)
    db.migrate.init_app.assert_called_once_with(mock_app, db)  # pylint: disable=no-member
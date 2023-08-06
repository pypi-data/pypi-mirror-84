# Busie Flask Helper

A package to help with common initialization code across Busie Flask projects

Helpful for use with the application factory pattern.
Allows for modularization of initialization code, such that factories are not cluttered with boilerplate initialization

## Installation

`pip install busie-flask-helper`

## Usage

```python
# in app.py, or wherever application initialization lives
from busie_flask import FlaskHelper
helper = FlaskHelper('abs/path/to/project/')
db = helper.db
auth = helper.auth
cache = helper.cache

# Other Initialization Code omitted

def create_app():
    app = Flask(__name__)
    # Other App Factory initialization omitted

    # this invocation initializes all of the helper objects with the application
    # this includes migration commands, models, views, auth, cache client, orm
    helper.init_app(app, 'relative/path/to/models', '/relative/path/to/views')

    return app

# in some module, maybe an API View
from flask import request
from src.app import auth

class SomeView(MethodView):
    def get(self):
        decoded_token = auth.handle_auth_header(auth_header=request.headers.get('Authorization'))
        # Rest of application api view code
```

## API

### FlaskHelper

#### Public Properties
* `db` <[SQLAlchemy] (https://flask-sqlalchemy.palletsprojects.com/en/2.x/)>
* `auth` <[AuthHelper] (#authhelper)>
* `cache` <[CacheClient] (#cacheclient)>

#### Public Methods
* `FlaskHelper(root_dir, app=None, models_dir=None, views_dir=None)`
    * param `root_dir`: The root directory of the project, best practice to pass an abspath here. if your application lives in src/app then your root dir should be src/
    * See `init_app` method documentation for specifics on the other params
* `init_app(self, app, models_dir, views_dir)`
    * param `app`: A Flask application instance
    * param `models_dir`: Relative path to the models directory, with respect to the root_dir that the helper was initialized with
    * param `views_dir`: same as `models_dir`, but for views


### AuthHelper

#### Public Properties
* `JWTPayload` <[JWTPaylaod] (#jwtpayload)>: Custom Payload for JWT with validation and defaults
* `AuthenticationSignException` <Exception>
* `AuthenticationVerificationException` <Exception>

#### Public Methods
* `AuthHelper(app=None)`: Constructor
* `init_app(self, app)`: Initialize the AuthHelper with a Flask application
    * param `app`: A Flask application instance. app.config _must_ have `AUTH_SECRET`

### JWTPayload

#### Public Properties
* `sub`: _REQUIRED_ The subject of the jwt, should be a `string` in most cases
* `role`: _REQUIRED_ The subjects 'role' within the system _(i.e superadmin, user, etc.)_
* `org`: _REQUIRED_ The subject's organization
* `iat`: _DEFAULT SUPPLIED_ POSIX timestamp (seconds) of issue date, defaults to utcnow
* `exp`: _DEFAULT SUPPLIED_ POSIX timestamp (seconds) of expiration date (defaults to 15 minutes from `iat`)

#### Public Methods
* `json(self)`: _JSON-ifies_ the JWT Payload claims.

### CacheClient

#### Public Properties
* `redis`: The redis instance. Allows for direct interation with the python Redis API

#### Public Methods
* `CacheClient(app=None)`: Constructor
* `init_app(self, app)`: Initialize the redis client with application.
    * param `app`: A Flask application instance. app.config _must_ have `REDIS_HOST` `REDIS_PORT` and `REDIS_DB`. **NOTE** `REDIS_PASSWORD` is also used, but this method _will not_ throw without it
* `get`: Alias for redis.get
* `set`: Alias for redis.set
 

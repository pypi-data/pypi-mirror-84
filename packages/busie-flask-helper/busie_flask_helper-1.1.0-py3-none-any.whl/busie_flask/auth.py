"""Authentication Lib"""
import jwt
from arrow import utcnow

class AuthHelper:
    """Methods for signing, verifying, and decoding tokens"""
    def __init__(self, app=None):
        self.__secret = None
        self.__issuer = None

        if app is not None:
            self.init_app(app)

    class JWTPayload:
        """Custom Payload for JWT with validation and defaults"""
        def __init__(self, sub=None, role=None, org=None, **kwargs):
            if not (sub and role and org):
                raise TypeError('sub, role, and org must all be provided')
            now = utcnow()
            self.iat = kwargs.pop('iat', now.int_timestamp)  # time in seconds
            self.exp = kwargs.pop('exp', now.shift(minutes=15).int_timestamp)
            self.sub = sub
            self.role = role
            self.org = org
            self.iss = kwargs.pop('iss', None)
            if not self.iss:
                del self.iss
            for key, value in kwargs.items():
                setattr(self, key, value)

        def json(self):
            """return jsonified jwt payload"""
            return vars(self)

    def sign(self, **payload):
        """
        Sign a token using the instances private secret key.

        :param **payload: claims for the JSON Web Token. Must include sub, role, org
        """
        try:
            payload['iss'] = self.__issuer
            payload = self.JWTPayload(**payload)
            token = jwt.encode(payload.json(), self.__secret, algorithm='HS256')
            return token.decode()
        except TypeError as ex:
            raise self.AuthenticationSignException(f'Cant sign payload -> {ex}') from ex

    def verify(self, token=None):
        """
        Verify a JSON Web Token using the instance's secret key.

        :param token: The JWT to be verified/decoded
        :return: decoded JWT claims (JWTPayload)
        """
        ERR_MSG = 'Can\'t verify token ->'
        try:
            decoded = jwt.decode(
                token,
                self.__secret,
                algorithms=['HS256'],
                options=dict(verify_iss=True, verify_exp=True),
                issuer=self.__issuer
            )
            return self.JWTPayload(**decoded)
        except jwt.ExpiredSignatureError as ex:
            raise self.AuthenticationVerificationException(f'{ERR_MSG} token expired') from ex
        except jwt.InvalidTokenError as ex:
            raise self.AuthenticationVerificationException(f'{ERR_MSG} token invalid') from ex

    def init_app(self, app):
        """
        Initialize a Flask application, setting the __secret property and adding self to
        app extensions

        :param app: A Flask application
        """

        self.__secret = app.config.get('AUTH_SECRET')
        self.__issuer = app.config.get('AUTH_ISSUER')
        if not (self.__secret and self.__issuer):
            raise RuntimeError('AUTH_SECRET and AUTH_ISSUER must be in application config.')

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['auth'] = self

    class AuthenticationSignException(Exception):
        """Something went wrong when signing"""

    class AuthenticationVerificationException(Exception):
        """Something went wrong when verifying"""

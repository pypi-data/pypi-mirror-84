"""Test Authentication Lib"""
import pytest
from busie_flask.auth import AuthHelper

@pytest.fixture
def mock_app(mocker):
    app = mocker.MagicMock()
    app.config.get.return_value = 'secret'
    return app

def test_authentication_helper_init(mocker):
    """
    - Sets _secret to None
    - Calls self.init_app with app if app provided
    """
    mock_init_app = mocker.patch('busie_flask.auth.AuthHelper.init_app')

    res = AuthHelper()
    mock_init_app.assert_not_called()
    assert hasattr(res, '_AuthHelper__secret')
    assert getattr(res, '_AuthHelper__secret') is None
    assert hasattr(res, '_AuthHelper__issuer')
    assert getattr(res, '_AuthHelper__issuer') is None

    res = AuthHelper(app='foo')
    mock_init_app.assert_called_once_with('foo')

def test_jwtpayload():
    """
    - Throws if a required arg not provided
    - has json method which returns a dict of the class's properties
    - sets defaults for iat, exp
    - sets issuer if provided
    - does not have issuer attr if not provided
    - sets additional kwargs to instance attributes
    """
    JWTPayload = AuthHelper.JWTPayload
    invalid_calls = [
        dict(),
        dict(sub='foo'),
        dict(sub='foo', role='foo'),
        dict(sub='foo', org='foo'),
        dict(role='foo', org='foo')
    ]
    for call in invalid_calls:
        with pytest.raises(TypeError):
            JWTPayload(**call)

    valid = JWTPayload(sub='foo', org='foo', role='foo', iss='some-issuer', foo='bar')
    assert valid.iat and valid.exp and valid.sub and valid.role and valid.org and valid.iss
    assert valid.foo == 'bar'                                                                # pylint: disable=no-member
    assert valid.json
    assert isinstance(valid.json(), dict)

    valid = JWTPayload(sub='foo', org='bar', role='foobar')
    with pytest.raises(AttributeError):
        valid.iss

def test_sign(mocker, mock_jwt, mock_app):
    """
    - makes a JWTPayload from provided payload
    - converts the payload to json
    - calls jwt.encode on JWTPayload.json, with AuthHelper instance secret property
      and algorithm = HS256
    - returns the a decoded string from the byte string of the token
    - raises exception on invalid jwt payload
    """
    jwt_mock = mock_jwt('busie_flask.auth')
    mock_jwt_payload = mocker.patch('busie_flask.auth.AuthHelper.JWTPayload')
    jwt_mock.encode.return_value = b'hereisatoken'
    authenticator = AuthHelper(mock_app)
    payload = dict(foo='bar')

    token = authenticator.sign(**payload)
    payload['iss'] = authenticator._AuthHelper__issuer

    mock_jwt_payload.assert_called_once_with(**payload)
    mock_jwt_payload.return_value.json.assert_called_once()
    jwt_mock.encode.assert_called_once_with(
        mock_jwt_payload.return_value.json.return_value,
        authenticator._AuthHelper__secret,
        algorithm='HS256'
    )
    assert isinstance(token, str)

    mock_jwt_payload.side_effect = TypeError
    with pytest.raises(AuthHelper.AuthenticationSignException):
        authenticator.sign(**payload)

def test_verify(mocker, mock_jwt, mock_app):
    """
    - Decode a token using the secret key
    - returns JWTPayload
    - Raises exceptions on invalid token or token expired
    """
    jwt_mock = mock_jwt('busie_flask.auth')
    mock_jwt_payload = mocker.patch('busie_flask.auth.AuthHelper.JWTPayload')
    jwt_mock.decode.return_value = dict(foo='bar')
    mock_token = 'sometokenstringdoesntmatter.here'

    authenticator = AuthHelper(mock_app)
    decoded = authenticator.verify(token=mock_token)

    mock_jwt_payload.assert_called_once_with(**jwt_mock.decode.return_value)
    jwt_mock.decode.assert_called_once_with(
        mock_token,
        authenticator._AuthHelper__secret,
        algorithms=['HS256'],
        options=dict(verify_iss=True, verify_exp=True),
        issuer=authenticator._AuthHelper__issuer
    )
    assert decoded == mock_jwt_payload.return_value

    jwt_mock.ExpiredSignatureError = ValueError
    jwt_mock.decode.side_effect = jwt_mock.ExpiredSignatureError
    with pytest.raises(AuthHelper.AuthenticationVerificationException):
        authenticator.verify(token=mock_token)

    jwt_mock.InvalidTokenError = AssertionError
    jwt_mock.decode.side_effect = jwt_mock.InvalidTokenError
    with pytest.raises(AuthHelper.AuthenticationVerificationException):
        authenticator.verify(token=mock_token)

def test_init_app(mock_app, mocker):
    """
    - Throws RuntimeError if app.config does not have AUTH_SECRET
    - Adds self to app.extensions as `auth`
    """
    del mock_app.extensions

    auth = AuthHelper()
    auth.init_app(mock_app)
    mock_app.config.get.assert_has_calls([mocker.call('AUTH_SECRET'), mocker.call('AUTH_ISSUER')])
    assert mock_app.extensions
    assert mock_app.extensions.get('auth') == auth

    mock_app.config.get.return_value = None
    with pytest.raises(RuntimeError):
        auth.init_app(mock_app)

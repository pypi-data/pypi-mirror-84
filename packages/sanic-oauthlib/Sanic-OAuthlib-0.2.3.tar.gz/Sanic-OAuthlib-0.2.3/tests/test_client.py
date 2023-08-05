from pytest import raises
from sanic import Sanic
from spf import SanicPluginsFramework

from sanic_oauthlib.client import encode_request_data
from sanic_oauthlib.client import OAuthRemoteApp, oauthclient
from sanic_oauthlib.client import parse_response
from asynctest import patch

class Response(object):
    def __init__(self, content, headers=None):
        self._content = content
        self.content = None
        self.headers = headers or {}

    @property
    def text(self):
        c = self.content
        if isinstance(c, bytes):
            c = c.decode('utf-8')
        return c

    async def aread(self):
        self.content = self._content

    async def aclose(self):
        pass

    @property
    def status(self):
        return self.headers.get('status-code', 500)

    @property
    def code(self):
        return self.status

    @property
    def status_code(self):
        return self.status

    def read(self):
        return self.content

    def close(self):
        return self


def test_encode_request_data():
    data, _ = encode_request_data('foo', None)
    assert data == 'foo'

    data, f = encode_request_data(None, 'json')
    assert data == '{}'
    assert f == 'application/json'

    data, f = encode_request_data(None, 'urlencoded')
    assert data == ''
    assert f == 'application/x-www-form-urlencoded'


def test_app():
    app = Sanic(__name__)
    spf = SanicPluginsFramework(app)
    oauth = spf.register_plugin(oauthclient)
    remote = oauth.remote_app(
        'dev',
        consumer_key='dev',
        consumer_secret='dev',
        request_token_params={'scope': 'email'},
        base_url='http://127.0.0.1:5000/api/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='http://127.0.0.1:5000/oauth/token',
        authorize_url='http://127.0.0.1:5000/oauth/authorize'
    )
    plugin = app.extensions['oauthlib.client']
    client = spf.get_plugin_assoc(plugin)
    assert client.dev.name == 'dev'


async def test_parse_xml():
    resp = Response(
        '<foo>bar</foo>', headers={
            'status-code': 200,
            'content-type': 'text/xml'
        }
    )
    await resp.aread()
    parse_response(resp, resp.content)



def test_raise_app():
    with raises(AttributeError):
        app = Sanic(__name__)
        spf = SanicPluginsFramework(app)
        oauth = spf.register_plugin(oauthclient)
        plugin = app.extensions['oauthlib.client']
        client = spf.get_plugin_assoc(plugin)
        assert client.demo.name == 'dev'


class TestOAuthRemoteApp(object):

    def test_raise_init(self):
        with raises(TypeError):
            OAuthRemoteApp('oauth', 'twitter')

    def test_not_raise_init(self):
        OAuthRemoteApp('oauth', 'twitter', app_key='foo')

    def test_lazy_load(self):
        twitter = oauthclient.remote_app(
            'twitter',
            base_url='https://api.twitter.com/1/',
            app_key='twitter'
        )
        assert twitter.base_url == 'https://api.twitter.com/1/'
        app = Sanic(__name__)
        app.config.update({
            'twitter': dict(
                request_token_params={'realms': 'email'},
                consumer_key='twitter key',
                consumer_secret='twitter secret',
                request_token_url='request url',
                access_token_url='token url',
                authorize_url='auth url',
            )
        })
        spf = SanicPluginsFramework(app)
        spf.register_plugin(oauthclient)
        assert twitter.consumer_key == 'twitter key'
        assert twitter.consumer_secret == 'twitter secret'
        assert twitter.request_token_url == 'request url'
        assert twitter.access_token_url == 'token url'
        assert twitter.authorize_url == 'auth url'
        assert twitter.content_type is None
        assert 'realms' in twitter.request_token_params

    def test_lazy_load_with_plain_text_config(self):
        twitter = oauthclient.remote_app('twitter', app_key='TWITTER')

        app = Sanic(__name__)
        app.config['TWITTER_CONSUMER_KEY'] = 'twitter key'
        app.config['TWITTER_CONSUMER_SECRET'] = 'twitter secret'
        app.config['TWITTER_REQUEST_TOKEN_URL'] = 'request url'
        app.config['TWITTER_ACCESS_TOKEN_URL'] = 'token url'
        app.config['TWITTER_AUTHORIZE_URL'] = 'auth url'

        spf = SanicPluginsFramework(app)
        spf.register_plugin(oauthclient)

        assert twitter.consumer_key == 'twitter key'
        assert twitter.consumer_secret == 'twitter secret'
        assert twitter.request_token_url == 'request url'
        assert twitter.access_token_url == 'token url'
        assert twitter.authorize_url == 'auth url'

    @patch('httpx._client.AsyncClient.send')
    async def test_http_request(self, sender):
        sender.return_value = Response(
            b'{"foo": "bar"}', headers={'status-code': 200}
        )

        resp, content = await OAuthRemoteApp.http_request('http://example.com')
        assert resp.status == 200
        assert 'foo' in content
        resp, content = await OAuthRemoteApp.http_request(
            'http://example.com/',
            method='GET',
            data={'wd': 'sanic-oauthlib'}
        )
        assert resp.status == 200
        assert 'foo' in content

        resp, content = await OAuthRemoteApp.http_request(
            'http://example.com/',
            data={'wd': 'sanic-oauthlib'}
        )
        assert resp.status == 200
        assert 'foo' in content

    # @patch('httpx._client.AsyncClient.request')
    # async def test_raise_http_request(self, urlopen):
    #     error = aiohttp.HTTPError(
    #         'http://example.com/', 404, 'Not Found', None, None
    #     )
    #     error.read = lambda: b'o'
    #
    #     class _Fake(object):
    #         def close(self):
    #             return 0
    #
    #     class _Faker(object):
    #         _closer = _Fake()
    #
    #     error.file = _Faker()
    #
    #     urlopen.side_effect = error
    #     resp, content = await OAuthRemoteApp.http_request('http://example.com')
    #     assert resp.status == 404
    #     assert 'o' in content

    def test_token_types(self):
        oauth = oauthclient
        remote = oauth.remote_app('remote',
                                  consumer_key='remote key',
                                  consumer_secret='remote secret')

        client_token = {'access_token': 'access token'}

        str_token = 'access token'
        client = remote.make_client(token=str_token)
        assert client.token == client_token

        list_token = ['access token']
        client = remote.make_client(token=list_token)
        assert client.token == client_token

        tuple_token = ('access token',)
        client = remote.make_client(token=tuple_token)
        assert client.token == client_token

        dict_token = {'access_token': 'access token'}
        client = remote.make_client(token=dict_token)
        assert client.token == client_token

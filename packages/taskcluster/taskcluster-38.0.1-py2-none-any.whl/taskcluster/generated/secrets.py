# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from ..client import BaseClient
from ..client import createApiClient
from ..client import config
from ..client import createTemporaryCredentials
from ..client import createSession
_defaultConfig = config


class Secrets(BaseClient):
    """
    The secrets service provides a simple key/value store for small bits of secret
    data.  Access is limited by scopes, so values can be considered secret from
    those who do not have the relevant scopes.

    Secrets also have an expiration date, and once a secret has expired it can no
    longer be read.  This is useful for short-term secrets such as a temporary
    service credential or a one-time signing key.
    """

    classOptions = {
    }
    serviceName = 'secrets'
    apiVersion = 'v1'

    def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    def set(self, *args, **kwargs):
        """
        Set Secret

        Set the secret associated with some key.  If the secret already exists, it is
        updated instead.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["set"], *args, **kwargs)

    def remove(self, *args, **kwargs):
        """
        Delete Secret

        Delete the secret associated with some key. It will succeed whether or not the secret exists

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["remove"], *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Read Secret

        Read the secret associated with some key.  If the secret has recently
        expired, the response code 410 is returned.  If the caller lacks the
        scope necessary to get the secret, the call will fail with a 403 code
        regardless of whether the secret exists.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["get"], *args, **kwargs)

    def list(self, *args, **kwargs):
        """
        List Secrets

        List the names of all secrets.

        By default this end-point will try to return up to 1000 secret names in one
        request. But it **may return less**, even if more tasks are available.
        It may also return a `continuationToken` even though there are no more
        results. However, you can only be sure to have seen all results if you
        keep calling `listTaskGroup` with the last `continuationToken` until you
        get a result without a `continuationToken`.

        If you are not interested in listing all the members at once, you may
        use the query-string option `limit` to return fewer.

        This method is ``stable``
        """

        return self._makeApiCall(self.funcinfo["list"], *args, **kwargs)

    funcinfo = {
        "get": {
            'args': ['name'],
            'method': 'get',
            'name': 'get',
            'output': 'v1/secret.json#',
            'route': '/secret/<name>',
            'stability': 'stable',
        },
        "list": {
            'args': [],
            'method': 'get',
            'name': 'list',
            'output': 'v1/secret-list.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/secrets',
            'stability': 'stable',
        },
        "ping": {
            'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable',
        },
        "remove": {
            'args': ['name'],
            'method': 'delete',
            'name': 'remove',
            'route': '/secret/<name>',
            'stability': 'stable',
        },
        "set": {
            'args': ['name'],
            'input': 'v1/secret.json#',
            'method': 'put',
            'name': 'set',
            'route': '/secret/<name>',
            'stability': 'stable',
        },
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Secrets']

from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class Log(EntityBase):
    """Audit Logs

    Access Vidispine Audit Logs.

    :vidispine_docs:`Vidispine doc reference <audit-trail>`

    """
    entity = 'log'

    def list(self, params: dict = None) -> BaseJson:
        """Retrieves log entries according to the specified filtering criteria.

        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        return self.client.get(self.entity, params=params)

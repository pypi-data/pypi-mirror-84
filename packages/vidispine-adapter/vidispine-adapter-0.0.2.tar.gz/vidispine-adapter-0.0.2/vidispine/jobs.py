from vidispine.base import EntityBase
from vidispine.typing import BaseJson


class Job(EntityBase):
    """Jobs

    Manages Vidispine Jobs.

    :vidispine_docs:`Vidispine doc reference <job>`

    """

    entity = 'job'

    def __init__(self, client) -> None:
        self.client = client

    def get(self, job_id: str) -> BaseJson:
        """Return information about specified job.

        :param job_id: The ID of the job to get.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        endpoint = self._build_url(job_id)
        return self.client.get(endpoint)

    def list_problems(self) -> BaseJson:
        """Returns a list of unresolved problems.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        endpoint = self._build_url('problem')
        return self.client.get(endpoint)

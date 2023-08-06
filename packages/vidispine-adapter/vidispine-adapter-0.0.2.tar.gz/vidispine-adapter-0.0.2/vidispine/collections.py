from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Collection(EntityBase):
    """Collections

    A collection is an ordered logical set of items, libraries and
    other collections.

    :vidispine_docs:`Vidispine doc reference <collection>`

    """
    entity = 'collection'

    def create(self, params: dict = None) -> str:
        """Creates a new collection.

        :param params: Optional query parameters.

        :return: id associated with the collection.
        :rtype: str.

        """

        if params is None:
            params = {}

        response = self.client.post(self.entity, params=params)

        return response['id']

    def get(self, collection_id: str, params: dict = None) -> BaseJson:
        """Return the ids of the objects contained within the collection

        :param collection_id: The id of the collection to get.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """

        if params is None:
            params = {}

        endpoint = self._build_url(collection_id)

        return self.client.get(endpoint, params=params)

    def delete(self, collection_id: str) -> None:
        """Delete specified collection.

        :param collection_id: The id of the collection to delete.

        """

        endpoint = self._build_url(collection_id)

        self.client.delete(endpoint)

    def delete_multiple(self, collection_ids: list) -> None:
        """Delete multiple collections.

        :param collection_ids: A list of collection ids to delete.

        """

        if not collection_ids:
            raise InvalidInput('Please supply Vidispine IDs to delete.')

        params = {'id': ','.join(collection_ids)}

        self.client.delete(self.entity, params=params)

    def update_metadata(self, collection_id: str, metadata: dict) -> BaseJson:
        """Sets or updates the metadata of a collection.

        :param collection_id: The id of the collection to update.
        :param metadata: The metadata to update the collection with.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        :vidispine_docs:`update_metadata Vidispine doc reference
        <metadata/metadata.html#
        put-%7Bmetadata-entity%7D-(entity-id)-metadata>`

        """

        endpoint = self._build_url(f'{collection_id}/metadata')

        return self.client.put(endpoint, json=metadata)

    def list(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:
        """Retrieves a list of all known collections.

        :param params: Optional query parameters.
        :param matrix_params: Optional matrix parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """

        endpoint = self._build_url(matrix_params=matrix_params)

        return self.client.get(endpoint, params=params)

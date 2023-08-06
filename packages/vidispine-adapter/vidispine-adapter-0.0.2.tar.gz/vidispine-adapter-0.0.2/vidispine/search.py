from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class Search(EntityBase):
    """Search

    Search Vidispine objects.

    :vidispine_docs:`Vidispine doc reference <collection>`

    """
    entity = 'search'

    def __call__(self, *args, **kwargs) -> BaseJson:
        """Browses items and collections

        :param metadata: Optional metadata (search document) supplied
            to perform a shared search query.
        :param params: Optional query parameters.
        :param matrix_params: Optional matrix parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self._search(*args, **kwargs)

    def _search(
        self,
        metadata: dict = None,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if metadata is None:
            return self._search_without_search_doc(params, matrix_params)
        else:
            return self._search_with_search_doc(
                metadata, params, matrix_params
            )

    def _search_with_search_doc(
        self,
        metadata: dict,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if not metadata:
            raise InvalidInput('Please supply metadata.')

        if params is None:
            params = {}

        endpoint = self._build_url(matrix_params=matrix_params)

        return self.client.put(endpoint, json=metadata, params=params)

    def _search_without_search_doc(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if params is None:
            params = {}

        endpoint = self._build_url(matrix_params=matrix_params)

        return self.client.get(endpoint, params=params)

    def shape(
        self,
        metadata: dict = None,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:
        """Searches shapes

        :param metadata: Optional metadata (shape document) supplied
            to perform a search query.
        :param params: Optional query parameters.
        :param matrix_params: Optional matrix parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if metadata is None:
            return self._search_shapes_without_search_doc(
                params, matrix_params
            )
        else:
            return self._search_shapes_with_search_doc(
                metadata, params, matrix_params
            )

    def _search_shapes_without_search_doc(
        self,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if params is None:
            params = {}

        endpoint = self._build_url('shape', matrix_params=matrix_params)

        return self.client.get(endpoint, params=params)

    def _search_shapes_with_search_doc(
        self,
        metadata: dict,
        params: dict = None,
        matrix_params: dict = None
    ) -> BaseJson:

        if not metadata:
            raise InvalidInput('Please supply metadata.')

        if params is None:
            params = {}

        endpoint = self._build_url('shape', matrix_params=matrix_params)

        return self.client.put(endpoint, json=metadata, params=params)

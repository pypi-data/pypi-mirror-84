from vidispine.base import EntityBase
from vidispine.errors import InvalidInput
from vidispine.typing import BaseJson


class MetadataFieldGroup(EntityBase):
    """Metadata field groups

    Field groups are named sets of fields and groups.

    :vidispine_docs:`Vidispine doc reference <metadata/field-group>`

    """
    entity = 'metadata-field/field-group'

    def get(self, field_group_name: str, params: dict = None) -> BaseJson:
        """Retrieves the specified metadata field group.

        :param field_group_name: The name of the field group to get.
        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(field_group_name)

        return self.client.get(endpoint, params=params)

    def create(self, field_group_name: str, params: dict = None) -> None:
        """Creates a new group with the given name.

        :param field_group_name: The name of the field group to create.
        :param params: Optional query parameters.

        """
        if params is None:
            params = {}

        endpoint = self._build_url(field_group_name)

        self.client.put(endpoint, params=params)

    def list(self, params: dict = None) -> BaseJson:
        """Retrieves all groups known by the system.

        :param params: Optional query parameters.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        return self.client.get(self.entity, params=params)

    def add_field_to_group(
        self,
        field_group_name: str,
        field_name: str
    ) -> None:
        """Adds the field with the specified name to the group.

        :param field_group_name: The name of the field group to
            add the field to.
        :param field_name: The name of the field to add.
        :param params: Optional query parameters.

        """
        endpoint = self._build_url(f'{field_group_name}/{field_name}')
        self.client.put(endpoint)

    def remove_field_from_group(
        self,
        field_group_name: str,
        field_name: str
    ) -> None:
        """Removes the field with the specified name from the group.

        :param field_group_name: The name of the field group with
            the field to be deleted.
        :param field_name: The name of the field to delete.

        """
        endpoint = self._build_url(f'{field_group_name}/{field_name}')
        self.client.delete(endpoint)

    def add_group_to_group(
        self,
        parent_group_name: str,
        child_group_name: str
    ) -> None:
        """Adds the group with the specified name to the group.

        :param parent_group_name: The name of the parent group.
        :param child_group_name: The name of the child group to add.

        """
        endpoint = self._build_url(
            f'{parent_group_name}/group/{child_group_name}'
        )
        self.client.put(endpoint)

    def delete(self, field_group_name: str) -> None:
        """Deletes the group with the given name.

        :param field_group_name: The name of the field group to be deleted.

        """
        endpoint = self._build_url(field_group_name)
        self.client.delete(endpoint)

    def remove_group_from_group(
        self,
        parent_group_name: str,
        child_group_name: str
    ) -> None:
        """Removes the group with the specified name from the group.

        :param parent_group_name: The name of the parent group.
        :param child_group_name: The name of the child group to remove.

        """
        endpoint = self._build_url(
            f'{parent_group_name}/group/{child_group_name}'
        )
        self.client.delete(endpoint)


class MetadataField(EntityBase):
    """Metadata fields

    Metadata fields define name and type of fields for metadata.

    :vidispine_docs:`Vidispine doc reference <metadata/field>`

    """
    entity = 'metadata-field'

    def create(self, metadata: dict, field_name: str) -> BaseJson:
        """Creates a metadata field.

        :param metadata: The metadata to create the field with.
        :param params: The name of the field to create.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self._update(metadata, field_name)

    def update(self, metadata: dict, field_name: str) -> BaseJson:
        """Updates a metadata field.

        :param metadata: The metadata to update the field with.
        :param params: The name of the field to update.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        return self._update(metadata, field_name)

    def _update(self, metadata: dict, field_name: str) -> BaseJson:
        if not metadata:
            raise InvalidInput('Please supply metadata.')

        endpoint = self._build_url(field_name)

        return self.client.put(endpoint, json=metadata)

    def get(self, field_name: str, params: dict = None) -> BaseJson:
        """Returns information about a specific metadata field.

        :param field_name: The name of the metadata field to get.
        :param params: Optional query params.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if not field_name:
            raise InvalidInput('Please supply a field name.')

        if params is None:
            params = {}

        endpoint = self._build_url(field_name)

        return self.client.get(endpoint, params=params)

    def list(self, params: dict = None) -> BaseJson:
        """Returns a list of all defined fields.

        :param params: Optional query params.

        :return: JSON response from the request.
        :rtype: vidispine.typing.BaseJson.

        """
        if params is None:
            params = {}

        return self.client.get(self.entity)

    def delete(self, field_name: str) -> None:
        """Deletes a metadata field.

        :param field_name: The name of the metadata field to delete.

        """
        if not field_name:
            raise InvalidInput('Please supply a field name.')

        endpoint = self._build_url(field_name)
        self.client.delete(endpoint)

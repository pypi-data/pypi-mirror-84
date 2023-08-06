from vidispine.utils import create_matrix_params_query


class EntityBase:

    entity = ''

    def __init__(self, client) -> None:
        self.client = client

    def _build_url(
        self,
        endpoint: str = '',
        matrix_params: dict = None
    ) -> str:

        if not self.entity:
            raise NotImplementedError('Do not use Base class directly.')

        if matrix_params:
            matrix_string = create_matrix_params_query(matrix_params)
        else:
            matrix_string = ''

        if endpoint:
            return f'{self.entity}/{endpoint}{matrix_string}'
        else:
            return f'{self.entity}{matrix_string}'

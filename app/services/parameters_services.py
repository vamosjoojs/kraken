from typing import List

from app.db.repositories.parameters_repository import ParametersRepository
from app.models.schemas.kraken import ParametersResponse, CreateParameters
from app.models.entities import Parameters


class ParametersServices:
    def __init__(self, parameter_repo: ParametersRepository):
        self.parameter_repo = parameter_repo

    def get_parameter(self) -> List[ParametersResponse]:
        parameters_orm = self.parameter_repo.get_parameters()
        result = []
        for parameter in parameters_orm:
            parameter_response = ParametersResponse(
                id=parameter.id,
                name=parameter.name,
                activated=parameter.activated,
                value=parameter.value,
                bool_value=parameter.bool_value,
                int_value=parameter.int_value
            )
            result.append(parameter_response)

        return result

    def edit_parameter(self, id: int, edit_parameter: CreateParameters) -> int:
        orm_model = Parameters(**edit_parameter.dict())
        id = self.parameter_repo.update_parameter(id, orm_model)
        return id

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.kraken import get_parameters_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.kraken import ParametersResponse, CreateParameters
from app.services.parameters_services import ParametersServices

router = APIRouter()


@router.get(
    "/get_parameters",
    name="Kraken: Get parameters",
    status_code=200,
    response_model=List[ParametersResponse],
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_parameters(
        parameter_service: ParametersServices = Depends(get_parameters_service),
):
    parameters = parameter_service.get_parameter()
    return parameters


@router.put(
    "/edit_parameter/{id}",
    name="Kraken: Edit parameter",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def edit_parameter(
        id: int,
        edit_parameter: CreateParameters,
        parameter_service: ParametersServices = Depends(get_parameters_service)):
    return parameter_service.edit_parameter(id, edit_parameter)

from typing import Literal, Union, Optional
from typing_extensions import Annotated

from pydantic import Field, StringConstraints

from middlewared.api.base import (
    BaseModel, ForUpdateMetaclass, NonEmptyString,
    single_argument_args,
)


class VirtGlobalEntry(BaseModel):
    id: int
    pool: str | None = None
    dataset: str | None = None
    bridge: str | None = None
    state: str | None = None


@single_argument_args('virt_global_update')
class VirtGlobalUpdateArgs(BaseModel):
    pool: str | None = None
    bridge: str | None = None


class VirtGlobalUpdateResult(BaseModel):
    result: VirtGlobalEntry


class VirtGlobalBridgeChoicesArgs(BaseModel):
    pass


class VirtGlobalBridgeChoicesResult(BaseModel):
    result: dict


class VirtGlobalPoolChoicesArgs(BaseModel):
    pass


class VirtGlobalPoolChoicesResult(BaseModel):
    result: dict


class VirtInstancesImageChoicesArgs(BaseModel):
    pass


class VirtInstancesImageChoicesResult(BaseModel):
    result: dict


class VirtInstanceEntry(BaseModel):
    id: str
    name: Annotated[NonEmptyString, StringConstraints(max_length=200)]
    type: Literal['CONTAINER', 'VM'] = 'CONTAINER'
    status: str
    cpu: str | None
    memory: int
    autostart: bool
    environment: dict
    raw: dict


@single_argument_args('virt_instance_create')
class VirtInstancesCreateArgs(BaseModel):
    name: Annotated[NonEmptyString, StringConstraints(max_length=200)]
    image: Annotated[NonEmptyString, StringConstraints(max_length=200)]
    instance_type: Literal['CONTAINER', 'VM'] = 'CONTAINER'
    environment: dict | None = None
    autostart: bool | None = None
    cpu: str | None = None
    memory: int | None = None


class VirtInstancesCreateResult(BaseModel):
    result: dict


class VirtInstancesUpdate(BaseModel, metaclass=ForUpdateMetaclass):
    environment: dict | None = None
    autostart: bool | None = None
    cpu: str | None = None
    memory: int | None = None


class VirtInstancesUpdateArgs(BaseModel):
    id: str
    virt_instance_update: VirtInstancesUpdate


class VirtInstancesUpdateResult(BaseModel):
    result: VirtInstanceEntry


class VirtInstancesDeleteArgs(BaseModel):
    id: str


class VirtInstancesDeleteResult(BaseModel):
    result: Literal[True]


class VirtInstancesDeviceListArgs(BaseModel):
    id: str


class VirtInstancesDeviceListResult(BaseModel):
    result: dict


class Device(BaseModel):
    name: str
    dev_type: Literal['USB', 'TPM', 'DISK']


class Disk(Device):
    source: Optional[str] = None
    destination: Optional[str] = None


class USB(Device):
    bus: Optional[int] = None
    dev: Optional[int] = None


class TPM(Device):
    path: Optional[str] = None
    pathrm: Optional[str] = None


class VirtInstancesDeviceAddArgs(BaseModel):
    id: str
    device: Union[USB, TPM, Disk] = Field(..., descriminator='dev_type')


class VirtInstancesDeviceAddResult(BaseModel):
    result: dict


class VirtInstancesDeviceDeleteArgs(BaseModel):
    id: str
    name: str


class VirtInstancesDeviceDeleteResult(BaseModel):
    result: dict


class VirtInstancesStateArgs(BaseModel):
    id: str
    action: Literal['START', 'STOP']
    force: bool = False


class VirtInstancesStateResult(BaseModel):
    result: bool

from typing import Literal, TypeAlias
from typing_extensions import Annotated

from pydantic import StringConstraints

from middlewared.api.base import BaseModel, Excluded, excluded_field, ForUpdateMetaclass, NonEmptyString, Private


class ContainerEntry(BaseModel):
    id: str
    name: Annotated[NonEmptyString, StringConstraints(max_length=200)]


class ContainerCreate(BaseModel):
    name: Annotated[NonEmptyString, StringConstraints(max_length=200)]
    image: Annotated[NonEmptyString, StringConstraints(max_length=200)]


class ContainerCreateArgs(BaseModel):
    container_create: ContainerCreate


class ContainerCreateResult(BaseModel):
    result: int


class ContainerUpdate(BaseModel, metaclass=ForUpdateMetaclass):
    limits_config: str


class ContainerUpdateArgs(BaseModel):
    id: str
    container_update: ContainerUpdate


class ContainerUpdateResult(BaseModel):
    result: ContainerEntry


class ContainerDeleteArgs(BaseModel):
    id: str


class ContainerDeleteResult(BaseModel):
    result: Literal[True]


class ContainerStateArgs(BaseModel):
    id: str
    action: str
    force: bool


class ContainerStateResult(BaseModel):
    result: bool

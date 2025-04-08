from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field, field_validator, ConfigDict, HttpUrl
from datetime import date
from enum import Enum
from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date
)


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str


    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, value: str) -> str:
        return validate_name(value)

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, value: GenderEnum) -> GenderEnum:
        return validate_gender(value)

    @field_validator('date_of_birth')
    @classmethod
    def validate_birth_date(cls, value: date) -> int:
        return validate_birth_date(value)


class ProfileCreateRequest(ProfileBase):
    avatar: UploadFile = Field(..., description="User avatar image")

    @classmethod
    def from_form(
            cls,
            first_name: str = Form(...),
            last_name: str = Form(...),
            gender: str = Form(...),
            date_of_birth: date = Form(...),
            info: str = Form(...),
            avatar: UploadFile = File(...)
    ) -> "ProfileCreateSchema":
        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=avatar
        )

    @field_validator('avatar')
    @classmethod
    def validate_avatar(cls, value: UploadFile) -> None:
        try:
            return validate_image(value)
        except ValueError as e:
            raise ValueError(str(e)) from e


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    avatar: HttpUrl

    model_config = ConfigDict(from_attributes=True)
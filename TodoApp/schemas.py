from pydantic import BaseModel, Field
# import typing as t


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Some Title",
                    "description": "Some Author",
                    "priority": 1,
                    "complete": False,
                },
            ]
        }
    }


class CreateUserRequest(BaseModel):
    email: str = Field()
    username: str = Field()
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    password: str = Field(min_length=8)
    role: str = Field(min_length=4)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "someemail@gmail.com",
                    "username": "someusername",
                    "first_name": "John",
                    "last_name": "Doe",
                    "password": "password",
                    "role": "admin"
                },
            ]
        }
    }


class UpdateUserPasswordRequest(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "old_password": "old_password",
                    "new_password": "new_password"
                },
            ]
        }
    }


class UpdateUserDetailsRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=10)
    address: str = Field(min_length=10, max_length=80)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "phone_number": "phone_number",
                    "address": "address"
                },
            ]
        }
    }


class LoginUserRequest(BaseModel):
    email: str = Field()
    password: str = Field(min_length=8)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "someemail@gmail.com",
                    "password": "password"
                },
            ]
        }
    }


class JwtToken(BaseModel):
    access_token: str
    token_type: str


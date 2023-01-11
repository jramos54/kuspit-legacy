# Librerias Estandar
import typing

# engine
from api.engine.use_cases.ports.secondaries import repository_users as repository
from api.engine.use_cases.factory import orm_mapper
from api.engine.domain.entities import entities_users as entity

# orm
from apps.backoffice.models import users as models_users

# Librerías de Terceros
from django.contrib.gis.geos import Point


class User(repository.UserDyPRepository):
    def __init__(self, users_orm_model: models_users.User):
        self._users_orm_model = users_orm_model

    def list_users(self) -> typing.List[entity.UserDyP]:
        return [
            orm_mapper.constructor_user_entities(user)
            for user in self._users_orm_model.objects.all()
        ]

    def get_user(self, user_id: int) -> entity.UserDyP:
        user = self._users_orm_model.objects.get(id=user_id)
        return orm_mapper.constructor_user_entities(user)

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        is_persona_fisica: bool,
        is_persona_moral: bool,
           ) -> entity.UserDyP:
        user = self._users_orm_model.objects.create(
            username=username,
            email=email,
            password=password,
            is_persona_fisica=is_persona_fisica,
            is_persona_moral=is_persona_moral,
            )
        return orm_mapper.constructor_user_entities(user)

    def update_user(
        self,
        id: int,
        is_active: typing.Optional[bool],
        is_staff: typing.Optional[bool],
        is_superuser: typing.Optional[bool],
        is_customer: typing.Optional[bool],
        is_persona_fisica: typing.Optional[bool],
        is_persona_moral: typing.Optional[bool],
    ) -> entity.UserDyP:
        user = self._users_orm_model.objects.get(id=id)
        # if location:
        #     valid_location = self.valid_location(
        #         latitude=location[0],
        #         longitude=location[1],
        #     )
        #     location = Point(location[0], location[1])
        #     if not valid_location:
        #         raise ValueError("Invalid location")

        # Implementacion de openfin create_persona_fisica -> id
        user.is_active = is_active if is_active else user.is_active
        user.is_staff = is_staff if is_staff else user.is_staff
        user.is_superuser = is_superuser if is_superuser else user.is_superuser
        user.is_customer = is_customer if is_customer else user.is_customer
        user.is_persona_fisica = (
            is_persona_fisica if is_persona_fisica else user.is_persona_fisica
        )
        user.is_persona_moral = (
            is_persona_moral if is_persona_moral else user.is_persona_moral
        )

        user.save(
            update_fields=[
                "is_active",
                "is_staff",
                "is_superuser",
                "is_customer",
                "is_persona_fisica",
                "is_persona_moral",
            ]
        )
        return orm_mapper.constructor_user_entities(user)

    def delete_user(self, user_id: int) -> None:
        user = self._users_orm_model.objects.get(id=user_id)
        user.delete()

    def valid_location(self, latitude: float, longitude: float) -> bool:
        point_location = Point(latitude, longitude)
        print(point_location)
        return True

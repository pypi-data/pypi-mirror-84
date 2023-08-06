from aiohttp import web
from aiohttp_apispec import docs
from colibris.views import ModelView

from colibris import app
from colibris import views
from colibris.conf import settings
from colibris.authentication import get_account
from colibris.views.generic import RetrieveUpdateDestroyModelView, ListCreateModelView

from __packagename__ import constants
from __packagename__ import models
from __packagename__ import schemas


# Here are some examples of views. Just remove what you don't need.
from colibris.views.mixins import UpdateMixin, RetrieveMixin


class HomeView(views.View):
    # Show the API docs when visiting the index of the service
    async def get(self):
        raise web.HTTPFound(settings.API_DOCS_URL)


class HealthView(views.View):
    @docs(tags=['Service'],
          summary='The health check endpoint')
    async def get(self):
        h = await app.get_health()
        return web.json_response(h)


class MeView(ModelView, RetrieveMixin, UpdateMixin):
    authentication_required = True
    body_schema_class = schemas.UserSchema
    model = models.User

    async def get_object(self):
        user = get_account(self.request)
        return user


class UsersView(ListCreateModelView):
    permissions = {constants.ROLE_ADMIN}
    body_schema_class = schemas.UserSchema
    model = models.User

    @docs(tags=['Users'], summary='List all users')
    async def get(self):
        return await super().get()

    @docs(tags=['Users'], summary='Add a new user')
    async def post(self):
        return await super().post()


class UserView(RetrieveUpdateDestroyModelView):
    permissions = {constants.ROLE_ADMIN}
    body_schema_class = schemas.UserSchema
    model = models.User

    @docs(tags=['Users'], summary='Reveal details about a specific user')
    async def get(self):
        return await super().get()

    @docs(tags=['Users'], summary='Update an existing user')
    async def patch(self):
        return await super().patch()

    @docs(tags=['Users'], summary='Update an existing user')
    async def put(self):
        return await super().put()

    @docs(tags=['Users'], summary='Delete a user')
    async def delete(self):
        return await super().delete()

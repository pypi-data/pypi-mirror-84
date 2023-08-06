
from colibris import utils

from .base import AuthorizationBackend


class ModelBackend(AuthorizationBackend):
    def __init__(self, model, account_field, **kwargs):
        self.model = model
        if isinstance(model, str):
            self.model = utils.import_member(self.model)

        self.account_field = account_field

        super().__init__(**kwargs)

    def get_account_field(self):
        return getattr(self.model, self.account_field)

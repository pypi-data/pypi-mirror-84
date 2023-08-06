from typing import Type, Tuple

from django.db.models.base import Model


def obj_model_name_with_app_name(obj: Type[Model]) -> Tuple[str, str]:
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()

    return app_label, model_name

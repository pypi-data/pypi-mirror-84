from typing import Type

from django.db.models.base import Model
from django.urls import reverse

from .utils import obj_model_name_with_app_name

__all__ = (
    'admin_add_url',
    'admin_change_url',
    'admin_delete_url',
    'admin_index_url',
)


def admin_add_url(model: Type[Model], namespace: str = 'admin'):
    """Returns admin add url for a given model
    """
    app_label, model_name = obj_model_name_with_app_name(model)

    return reverse(f"{namespace}:{app_label}_{model_name}_add")


def admin_change_url(obj: Type[Model], namespace: str = 'admin'):
    """Returns admin change url for a given object
    """
    app_label, model_name = obj_model_name_with_app_name(obj)

    return reverse(f"{namespace}:{app_label}_{model_name}_change", args=(obj.pk,))


def admin_delete_url(obj: Type[Model], namespace: str = 'admin'):
    """Returns admin delete url for a given object
    """
    app_label, model_name = obj_model_name_with_app_name(obj)

    return reverse(f"{namespace}:{app_label}_{model_name}_delete", args=(obj.pk,))


def admin_index_url(namespace: str = 'admin'):
    """Returns admin dashboard url
    """
    return reverse(f"{namespace}:index")

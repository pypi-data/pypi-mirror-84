from contextlib import suppress
from typing import Type

from django.urls.exceptions import NoReverseMatch
from django_jinja import library
from django.db.models.base import Model

from dj_admin_urls import admin_change_url, admin_index_url


@library.global_function
def object_admin_url(obj: Type[Model]):
    """Returns object's admin url.
    """
    if obj:
        with suppress(NoReverseMatch):
            return admin_change_url(obj)


@library.global_function
def admin_url():
    """Returns admin dashboard url.
    """
    return admin_index_url()

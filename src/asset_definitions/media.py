import django.forms
from typing import *  # noqa


__all__ = (
    "Media",
)


# noinspection PyProtectedMember
# noinspection PyMissingConstructor
class Media(django.forms.Media):

    def __init__(self, **kwargs):
        self._media = django.forms.Media(**kwargs)
        self._combined_with = []

    def add_js(self, data):
        # type: (Iterable) -> None
        self._media.add_js(data)

    def add_css(self, data):
        # type: (Dict[str, Iterable]) -> None
        self._media.add_css(data)

    @property
    def _js(self):
        media = django.forms.Media()
        media.add_js(self._media._js)
        for other_media in self._combined_with:
            media.add_js(other_media._js)
        return media._js

    @property
    def _css(self):
        media = django.forms.Media()
        media.add_css(self._media._css)
        for other_media in self._combined_with:
            media.add_css(other_media._css)
        return media._css

    def __add__(self, other):
        # type: (django.forms.Media) -> Media
        media = Media(js=self._media._js, css=self._media._css)
        media._combined_with = self._combined_with + [other]
        return media

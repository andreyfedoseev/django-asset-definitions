import asset_definitions
import django.forms  # noqa
from typing import *  # noqa


__all__ = (
    "MediaDefiningView",
)


class MediaDefiningView(object):

    @property
    def media(self):
        return self.get_media()

    def get_media(self):
        # type: () -> asset_definitions.Media
        media = asset_definitions.Media()
        media_from_class_definition = self._get_media_from_definition()
        if media_from_class_definition:
            media += media_from_class_definition
        form_media = self._get_form_media()
        if form_media:
            media += form_media
        return media

    def _get_media_from_definition(self):
        # type: () -> Optional[asset_definitions.Media]
        definition = getattr(self.__class__, "Media", None)
        if definition:
            return asset_definitions.Media(media=definition)

    def _get_form_media(self):
        # type: () -> Optional[django.forms.Media]
        if hasattr(self, "get_form"):
            return self.get_form().media

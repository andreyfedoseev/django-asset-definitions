from typing import Optional

import django.forms

import asset_definitions

__all__ = ("MediaDefiningView",)


class MediaDefiningView(asset_definitions.MediaDefiningClass):
    def get_media(self) -> asset_definitions.Media:
        media = super(MediaDefiningView, self).get_media()
        form_media = self._get_form_media()
        if form_media:
            media += form_media
        return media

    def _get_form_media(self) -> Optional[django.forms.Media]:
        if hasattr(self, "get_form"):
            return self.get_form().media

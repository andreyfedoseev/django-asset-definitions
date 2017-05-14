import asset_definitions
import django.forms


class MediaDefinitionView(object):

    class Media:
        js = ("media.js",)
        css = {"all": ("media.css",)}


class Form(django.forms.Form):

    class Media:
        js = ("form.js",)
        css = {"all": ("form.css",)}


class FormView(object):

    def get_form(self):
        return Form()


def test_media_from_definition():

    class View(
        MediaDefinitionView,
        asset_definitions.MediaDefiningView
    ):
        pass

    view = View()
    assert view.media.render() == (
        """<link href="/static/media.css" type="text/css" media="all" rel="stylesheet" />\n"""
        """<script type="text/javascript" src="/static/media.js"></script>"""
    )


def test_form_media():

    class View(
        FormView,
        asset_definitions.MediaDefiningView
    ):
        pass

    view = View()
    assert view.media.render() == (
        """<link href="/static/form.css" type="text/css" media="all" rel="stylesheet" />\n"""
        """<script type="text/javascript" src="/static/form.js"></script>"""
    )


def test_combined():

    class View(
        MediaDefinitionView,
        FormView,
        asset_definitions.MediaDefiningView
    ):
        pass

    view = View()
    assert view.media.render() == (
        """<link href="/static/media.css" type="text/css" media="all" rel="stylesheet" />\n"""
        """<link href="/static/form.css" type="text/css" media="all" rel="stylesheet" />\n"""
        """<script type="text/javascript" src="/static/media.js"></script>\n"""
        """<script type="text/javascript" src="/static/form.js"></script>"""
    )

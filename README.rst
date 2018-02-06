========================
django-asset-definitions
========================

.. image:: https://circleci.com/gh/andreyfedoseev/django-asset-definitions.svg?style=shield
    :target: https://circleci.com/gh/andreyfedoseev/django-asset-definitions
    :alt: Build Status

.. image:: https://codecov.io/github/andreyfedoseev/django-asset-definitions/coverage.svg?branch=master
    :target: https://codecov.io/github/andreyfedoseev/django-asset-definitions?branch=master
    :alt: Code Coverage

Asset definitions are collections of static files (JavaScript, CSS) defined in Python code and (re)used in Django views
and templates.

An example of asset definition is ``Media`` class that you can
`define in Django forms <https://docs.djangoproject.com/en/1.11/topics/forms/media/>`_.

``django-asset-definitions`` aim to extend the application of asset definitions beyond forms and use them as the main
way to describe and organize JavaScript and CSS files.

Installation
============

.. code-block:: sh

    pip install django-asset-definitions


Usage
=====

Define:
-------

.. code-block:: python

  import asset_definitions

  my_media = asset_definitions.Media(
      js=(
          "media.js",
          """<script>window.addEventListener("load", function() {console.log("Loaded!");});</script>""",
      ),
      css={
          "all": (
              "media.css",
          ),
      }
  )

Combine:
--------

.. code-block:: python

  extended_media = my_media + asset_definitions.Media(
      js=("extension.js", )
  )


Define in views:
----------------

.. code-block:: python

  import asset_definitions

  class MyView(asset_definitions.MediaDefiningView, ...):

      class Media:
          js=(
              "media.js",
          ),
          css={
              "all": (
                  "media.css",
              ),
          }

      ...

Form media is added to view media automatically:

.. code-block:: python

  import asset_definitions
  from django.views.generic import FormView

  class MyFormView(asset_definitions.MediaDefiningView, FormView):
      ...

Use in templates:
-----------------

.. code-block:: django

  {{ view.media.render }}

Or:

.. code-block:: django

  {{ view.media.js.render }}
  {{ view.media.css.render }}


See an extended example below.


``asset_definitions.Media`` and ``django.forms.Media``
======================================================

1. ``asset_definitions.Media`` provides the same API as ``django.forms.Media``. In fact, it is inherited from
   ``django.forms.Media``.
2. It is safe to combine ``asset_definitions.Media`` with ``django.forms.Media``.
3. ``asset_definitions.Media`` objects are lazy. If two or more instances of ``asset_definitions.Media`` are combined
   together the result is computed only when media is rendered. It is safe to use ``reverse_lazy()`` with
   ``asset_definitions.Media``. It is important if you define your assets on module level.
4. ``Media`` class in ``MediaDefiningView`` does not support ``extend`` option. To add to the media defined in parent
   view class you should override ``get_media`` method and use ``super(MyView, self).get_media()``.

Example:
========

``myapp/urls.py``:

.. code-block:: python

  urlpatterns = (
      url("/", MyView.as_view()),
      url("/global-variables.js", global_js_variables, name="global_js_variables"),
  )


``myapp/views.py``:

.. code-block:: python

  import asset_definitions
  from . import assets


  class MyView(assets_definition.MediaDefiningView, TemplateView):

      template_name = "template.html"

      class Media:
          js = ("media.js", )
          css = {"all": ("media.css", media)

      def get_media():
          return (
            assets.global_js_variables +
            assets.jquery +
            super(MyView, self).get_media()
          )

  def global_js_variables(request):
      js_content = 'const CURRENT_USER="{}";'.format(request.user)
      return HttpResponse(js_content, content_type="application/javascript")

``myapp/assets.py``:

.. code-block:: python

  import asset_definitions
  from django.core import urlresolvers


  global_js_variables = asset_definition.Media(
      js=urlresolvers.reverse_lazy("global_js_variables"),
  )


  jquery = asset_definitions.Media(
      js="jquery.js"
  )


``myapp/templates/template.html``:

.. code-block:: django

  <html>
    <head>
      {{ view.media.css.render }}
    </head>
    <body>
      ...
      {{ view.media.js.render }}
    </body>
  </html>



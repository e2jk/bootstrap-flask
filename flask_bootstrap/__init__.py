# -*- coding: utf-8 -*-
"""
    flask_bootstrap
    ~~~~~~~~~~~~~~
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
from flask import current_app, Markup, Blueprint, url_for

try:
    from wtforms.fields import HiddenField
except ImportError:

    def is_hidden_field_filter(field):
        raise RuntimeError('WTForms is not installed.')
else:

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)


class Bootstrap(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['bootstrap'] = self

        blueprint = Blueprint('bootstrap', __name__, template_folder='templates',
                              static_folder='static', static_url_path='/bootstrap' + app.static_url_path)
        app.register_blueprint(blueprint)

        app.jinja_env.globals['bootstrap'] = self
        app.jinja_env.globals['bootstrap_is_hidden_field'] = \
            is_hidden_field_filter
        app.jinja_env.add_extension('jinja2.ext.do')
        # default settings
        app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', False)

    @staticmethod
    def load_css(version='4.1.0'):
        """Load Bootstrap's css resources with given version.

        .. versionadded:: 0.1.0

        :param version: The version of Bootstrap.
        """
        css_filename = 'bootstrap.min.css'
        serve_local = current_app.config['BOOTSTRAP_SERVE_LOCAL']

        if serve_local:
            css = '<link rel="stylesheet" href="%s" type="text/css">\n' % \
                  url_for('bootstrap.static', filename='css/' + css_filename)
        else:
            css = '<link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/%s/css/%s"' \
                  ' type="text/css">\n' % (version, css_filename)
        return Markup(css)

    @staticmethod
    def load_js(version='4.1.0', jquery_version='3.3.1', popper_version='1.14.0', with_jquery=True, with_popper=True):
        """Load Bootstrap and related library's js resources with given version.

        .. versionadded:: 0.1.0

        :param version: The version of Bootstrap.
        :param jquery_version: The version of jQuery.
        :param popper_version: The version of Popper.js.
        :param with_jquery: Include jQuery or not.
        :param with_popper: Include Popper.js or not.
        """
        js_filename = 'bootstrap.min.js'
        jquery_filename = 'jquery.min.js'
        popper_filename = 'popper.min.js'

        serve_local = current_app.config['BOOTSTRAP_SERVE_LOCAL']

        if serve_local:
            js = '<script src="%s"></script>' % url_for('bootstrap.static', filename='js/' + js_filename)
        else:
            js = '<script src="//cdn.bootcss.com/bootstrap/%s/js/%s">' \
                 '</script>' % (version, js_filename)

        if with_jquery:
            if serve_local:
                jquery = '<script src="%s"></script>' % url_for('bootstrap.static', filename=jquery_filename)
            else:
                jquery = '<script src="//cdn.bootcss.com/jquery/%s/%s">' \
                 '</script>' % (jquery_version, jquery_filename)
        else:
            jquery = ''

        if with_popper:
            if serve_local:
                popper = '<script src="%s"></script>' % url_for('bootstrap.static', filename=popper_filename)
            else:
                popper = '<script src="//cdn.bootcss.com/popper.js/%s/umd/%s">' \
                     '</script>' % (popper_version, popper_filename)
        else:
            popper = ''
        return Markup('%s\n%s\n%s\n' % (jquery, js, popper))

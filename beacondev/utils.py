import os
import jinja2

from os.path import dirname, join

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(join(dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

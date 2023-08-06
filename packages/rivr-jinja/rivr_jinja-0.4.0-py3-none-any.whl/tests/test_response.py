import unittest

from jinja2 import DictLoader, Environment
from rivr.http import Request

from rivr_jinja.response import JinjaResponse


class JinjaResponseTests(unittest.TestCase):
    def test_rendering_content_without_environment_raises(self):
        response = JinjaResponse(None, 'index.html', {})

        with self.assertRaises(Exception):
            response.content

    def test_rendering_content_with_environment(self):
        environment = Environment(loader=DictLoader({'index.html': 'Hello {{ name }}'}))
        response = JinjaResponse(
            request=None,
            template_names=['index.html'],
            context={'name': 'World'},
            environment=environment,
        )

        self.assertEqual(response.content, b'Hello World')

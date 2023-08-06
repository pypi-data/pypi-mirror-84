from jinja2 import Environment
from rivr.http import Request, Response
from rivr.middleware import Middleware

from rivr_jinja.response import JinjaResponse


class JinjaMiddleware(Middleware):
    def __init__(self, environment: Environment, *args, **kwargs):
        super(JinjaMiddleware, self).__init__(*args, **kwargs)
        self.environment = environment

    def process_response(self, request: Request, response: Response) -> Response:
        if isinstance(response, JinjaResponse):
            response.environment = self.environment

        return response

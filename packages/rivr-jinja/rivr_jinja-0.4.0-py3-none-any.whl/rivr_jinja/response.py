from typing import List, Optional, Sequence, Union, cast

from jinja2 import Environment, Template
from rivr.http import Request, Response


class JinjaResponse(Response):
    def __init__(
        self,
        request: Request,
        template_names: Sequence[str],
        context,
        environment: Environment = None,
        *args,
        **kwargs
    ):
        super(JinjaResponse, self).__init__(*args, **kwargs)
        self.request = request
        self.template_names = template_names
        self.context = context
        self._content: Optional[bytes] = None
        self.environment = environment

        if 'request' not in self.context:
            self.context['request'] = request

    def get_environment(self) -> Environment:
        if self.environment:
            return self.environment

        raise Exception(
            'JinjaResponse is improperly configured' 'and requires a jinja environment'
        )

    def render(self) -> str:
        environment = self.get_environment()
        # workaround for https://github.com/python/typeshed/pull/4677
        template_names = cast(List[Union[str, Template]], self.template_names)
        template = environment.select_template(template_names)
        return template.render(self.context)

    def get_content(self) -> bytes:
        if not self._content:
            self._content = self.render().encode('utf-8')

        return self._content

    def set_content(self, value: bytes):
        pass

    content = property(get_content, set_content)

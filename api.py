import inspect
import os.path

from jinja2 import Environment, FileSystemLoader
from parse import parse
from webob import Request, Response
from whitenoise import WhiteNoise


class API:
    def __init__(self, templates_dir='templates', static_dir="static"):

        self.__routes = {}
        self.__templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)


    def template(self, template_name, context: dict = None):
        if context is None:
            context = {}
        return self.__templates_env.get_template(template_name).render(**context)


    def add_route(self, path, handler):
        assert path not in self.__routes, "Such route already registered"
        self.__routes[path] = handler


    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        return wrapper


    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)


    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)


    def handle_request(self, request: Request):

        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                assert handler is not None, "Sorry, method not allowed"

                handler(request, response, **kwargs)

            handler(request, response, **kwargs)
            return response

        self.not_found_handler(response)
        return response


    def find_handler(self, request_path):
        for path, handler in self.__routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None


    @staticmethod
    def not_found_handler(response: Response):
        response.status = "404"
        response.text = "Sorry, Not Found"
        return response



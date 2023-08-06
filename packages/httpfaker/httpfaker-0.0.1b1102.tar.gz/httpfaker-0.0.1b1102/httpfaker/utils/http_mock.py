from flask import Flask
from flask import request
import os
from httpfaker.utils.logic import ResolveYaml
from flask import Response
import json
from httpfaker.utils.generator import MGenerator
from httpfaker.utils.faker_date_time import Provider as DateTimeProvider
from httpfaker.utils.faker_tool import Provider as ToolProvider
from faker import Faker
import importlib
import sys

faker = Faker(locale='zh_CN', generator=MGenerator(locale='zh_CN'))


def import_module(module_path='script'):
    if not os.path.exists(module_path):
        return
    pys = [x for x in list(os.walk(module_path))[0][-1] if x.endswith(".py")]
    modules = []
    for py in pys:
        if module_path.endswith('/'):
            module_path = module_path[:-1]
        module = importlib.import_module('{}.{}'.format(module_path.replace('/', '.'), py.split(".")[0]))
        for class_name in dir(module):
            provider = getattr(module, class_name)
            if isinstance(provider, type):
                modules.append(provider)
    return modules


class HttpMock(Flask):
    def __init__(self, target='apis', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function_object = self._find_api(target)

    def function(self, *args, **kwargs):
        func = self.function_object['_'.join([x for x in request.path.split('/') if x]) + '_{}'.format(request.method)]
        response_data = func.start()
        return Response(
            response=json.dumps(response_data['body']),
            status=response_data['status_code'],
            headers=response_data['headers']
        )

    def m_route(self, rules: list):
        for rule in rules:
            for key, value in rule.items():
                self.route(key, methods=value)(self.function)

    @staticmethod
    def _find_api(path, topdown=False):
        api_files = []
        for root, dirs, files in os.walk(path, topdown):
            for file in files:
                if os.path.splitext(file)[-1] in ('.yml', '.yaml', '.json'):
                    api_files.append(os.path.join(root, file))
        obj = {}
        for f in api_files:
            key = os.path.split(f)[-1].split('.')[0]
            obj[key] = ResolveYaml(meta=f, faker=faker, request=request)
        return obj


def start_server(api_path='apis', listen='0.0.0.0', port=9001, script_path='script'):
    cur_dir = os.path.abspath(os.curdir)
    sys.path.append(cur_dir)
    sys.path.append(script_path)
    faker.add_provider(DateTimeProvider, offset=0)
    faker.add_provider(ToolProvider, )
    modules = import_module(script_path)
    if modules:
        for module in modules:
            faker.add_provider(module)
    http = HttpMock(import_name=__name__, target=api_path)
    rule = []
    for h in http.function_object.values():
        print(h.request_data)
        rule.append({h.request_data['path']: h.request_data['method']})
    http.m_route(rule)
    http.run(host=listen, port=port)


if __name__ == '__main__':
    start_server()

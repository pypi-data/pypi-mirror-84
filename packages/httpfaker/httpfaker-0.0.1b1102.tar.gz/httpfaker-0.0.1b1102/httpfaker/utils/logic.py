from httpfaker.utils.resolve import ResolveBase
from httpfaker.common.setting import get_yaml
import copy

class ResolveYaml(ResolveBase):
    def __init__(self, meta, faker=None, request=None):
        super().__init__(faker)
        self.meta_data = get_yaml(meta)
        self.request_data = {}
        self.request = {}
        self.logic = {}
        self.response = {}
        self.import_package()
        self.resolve_env()
        self.resolve_request(request)

    def import_package(self):
        self._import_package(packages=self.meta_data.get('import'))

    def resolve_env(self):
        """
        环境变量预处理
        :param condition:
        :return:
        """
        env = self.meta_data.get('env')
        if not env:
            return
        self.env_data['env'] = self._field_handle(**env)

    def resolve_request(self, request):
        self.request_data = self.dict_resolve(self.meta_data.get('request'))
        self.request = request
        self.env_data['request'] = request

    def resolve_logic(self):
        logic = self.dict_resolve(self.meta_data.get('logic'))
        _logic = {}
        for key, value in logic.items():
            _logic[key] = self._gen_field(**value)
        self.env_data['logic'] = copy.deepcopy(_logic)

    def resolve_response(self):
        response = self.dict_resolve(self.meta_data.get('response'))
        _response = {}
        for key, value in response.items():
            if not isinstance(value, dict):
                _response[key] = value
            else:
                _response[key]= self._field_handle(**value)
        self.response= _response

    def start(self):
        self.resolve_logic()
        self.resolve_response()
        return self.response

from httpfaker.utils.resolve import ResolveBase
from httpfaker.common.setting import get_yaml



class ResolveYaml(ResolveBase):
    def __init__(self, meta, faker=None, request=None):
        super().__init__(faker)
        self.meta_data = self.check_api_file(meta)
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
        self.env_data['logic'] = self._field_handle(**logic)

    def resolve_response(self):
        response = self.dict_resolve(self.meta_data.get('response'))
        _response = {}
        self.response = self._field_handle(**response)

    def start(self):
        self.resolve_logic()
        self.resolve_response()
        return self.response

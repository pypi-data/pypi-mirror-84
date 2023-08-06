from httpfaker.utils.faker_tool import Provider

class MyProvider(Provider):
    def verify_account(self, username, password):
        return {"code": 200, "msg": "请求成功"}

    def gen_token(self, username):
        return {"token": self.uuid()}
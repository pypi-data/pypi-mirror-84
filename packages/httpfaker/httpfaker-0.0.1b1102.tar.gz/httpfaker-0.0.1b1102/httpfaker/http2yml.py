from flask import Flask
from flask import request
from httpfaker.utils.constant import HTTP_TEMPLATE
from httpfaker.utils.constant import __version__
import sys
import json
import os
import argparse
import jinja2
import yaml

app = Flask(__name__)

DEFAULT_BODY = 'null'
DEFAULT_STATUS = 200
DEFAULT_PATH = 'apis'
HIDE_DATA = False
FORMAT = 'yaml'


def save_file(request, data, format):
    if not os.path.exists(DEFAULT_PATH):
        os.mkdir(DEFAULT_PATH)
    filename = '_'.join([x for x in request.path.split('/') if x]) + '_{}'.format(request.method) + format
    with open(os.path.join(DEFAULT_PATH, filename), 'w', encoding='utf-8', ) as f:
        f.write(data)


@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def save_params(path):
    def render(**kwargs):
        tp = jinja2.Template(HTTP_TEMPLATE)
        data = tp.render(kwargs)
        if FORMAT == 'json':
            data_str = json.dumps(yaml.load(data, Loader=yaml.FullLoader), ensure_ascii=False, indent='  ')
            save_file(request, data_str, '.json')
        else:
            data_str = yaml.dump(yaml.load(data, Loader=yaml.FullLoader), encoding='utf-8', allow_unicode=True,
                                 default_flow_style=False, sort_keys=False).decode()
            save_file(request, data_str, '.yml')

        return yaml.load(data, Loader=yaml.FullLoader)

    data = 'null'
    args = 'null'
    if not HIDE_DATA:
        data = request.json if request.content_type == 'application/json' else 'null'
        args = request.args.to_dict()
    return render(CONTENT_TYPE=request.content_type, PATH=request.path, METHOD=request.method,
                  RESPONSE_BODY=DEFAULT_BODY, RESPONSE_STATUS=DEFAULT_STATUS, DATA=data, ARGS=args)


def start(**kwargs):
    global DEFAULT_BODY, DEFAULT_STATUS, DEFAULT_PATH, HIDE_DATA, FORMAT
    default_body = kwargs.get('default_body')
    if default_body:
        if os.path.isfile(default_body):
            with open(default_body, encoding='utf-8') as f:
                try:
                    _body = f.read()
                    DEFAULT_BODY = json.loads(_body)
                except json.JSONDecodeError:
                    DEFAULT_BODY = yaml.load(_body, Loader=yaml.FullLoader)
                except Exception:
                    DEFAULT_BODY = _body

        else:
            raise ValueError('“default-body” must be the file path of a json or yaml format file')
    default_status = kwargs.get('default_status')
    if default_status:
        DEFAULT_STATUS = default_status
    DEFAULT_PATH = kwargs.get('path', 'apis')
    HIDE_DATA = kwargs.get('hide_data', False)
    FORMAT = kwargs.get('out_format', 'yaml')
    app.run(host=kwargs.get('listen'), port=kwargs.get('port'))


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='调用接口生成mock描述文件')
    parser.add_argument('--default-body', nargs='?', action='store',
                        help='Response默认的返回体，指定后生成的Response中的body字段将按照此定义来生成。用法：指定文件路径，文件内容格式可以是json或者yaml！')
    parser.add_argument('--default-status', nargs='?', action='store', default=200,
                        help='Response中status_code返回值，默认为200')
    parser.add_argument('--path', nargs='?', action='store', default='apis', help='输出的配置文件存放路径, 默认当前目录下的apis目录')
    parser.add_argument('--hide-data', action='store_true', help='不转换Request中的请求体和请求参数数据（请求参数和请求体数据仅做参考，不参与实际逻辑）')
    parser.add_argument('--out-format', nargs='?', action='store', default='yml', help='转换的配置文件的格式；可选yml和json，默认yml格式')
    parser.add_argument('--listen', nargs='?', action='store', default='0.0.0.0', help='启动服务默认监听地址，默认0.0.0.0')
    parser.add_argument('--port', nargs='?', action='store', default='9000', help='启动服务默认监听端口，默认9000')
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    start(**args.__dict__)


if __name__ == '__main__':
    main()

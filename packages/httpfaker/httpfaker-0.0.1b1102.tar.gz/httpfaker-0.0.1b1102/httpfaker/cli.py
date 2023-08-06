from httpfaker import start_server
import sys
import argparse
from httpfaker.utils.constant import __version__


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='启动mock服务')
    parser.add_argument('--api_path', nargs='?', action='store', default='yaml_api', help='api描述文件所在路径， 默认apis')
    parser.add_argument('--script_path', nargs='?', action='store', default='script', help='自定义方法脚本所在目录, 默认script')
    parser.add_argument('--listen', nargs='?', action='store', default='0.0.0.0', help='启动服务默认监听地址，默认0.0.0.0')
    parser.add_argument('--port', nargs='?', action='store', default='9001', help='启动服务默认监听端口，默认9001')
    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    start_server(**args.__dict__)


if __name__ == '__main__':
    main()
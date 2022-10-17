import argparse
from BocchiLink import Bocchi


def get_args():
    parser = argparse.ArgumentParser(description='BocchiLink')
    parser.add_argument('username', help='school card id')
    parser.add_argument('password', help='password of ehall.szu.edu.cn')
    parser.add_argument('-l', '--log-path', help='log file path', default='bocchi_link.log')
    return parser.parse_args()


def main():
    args = get_args()
    bocchi_link = Bocchi(args.username, args.password, args.log_path)
    bocchi_link.loop()


if __name__ == '__main__':
    main()

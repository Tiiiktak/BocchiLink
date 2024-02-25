import argparse
from BocchiLink import Bocchi


def get_args():
    parser = argparse.ArgumentParser(description='BocchiLink')
    parser.add_argument('username', help='school card id')
    parser.add_argument('password', help='password of ehall.szu.edu.cn')
    parser.add_argument('-l', '--log-path', help='log file path', default='bocchi_link.log')
    parser.add_argument('-tt', '--trying-times', help='loop trying times', default=-1, type=int)
    return parser.parse_args()


def main():
    args = get_args()
    bocchi_link = Bocchi(args.username, args.password, args.trying_times, log_path=args.log_path)
    if args.trying_times == -1:
        bocchi_link.loop()
    else:
        bocchi_link.trying()


if __name__ == '__main__':
    main()

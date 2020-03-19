import argparse

import sys

import chat_server


def define_args(arg_vec):
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', type=str, default="0.0.0.0")
    parser.add_argument('--port', type=int, default="33333")

    _args = parser.parse_args(arg_vec)
    return _args


if __name__ == "__main__":
    args = define_args(arg_vec=sys.argv[1:])

    chat_server.service.serve((args.host, args.port))

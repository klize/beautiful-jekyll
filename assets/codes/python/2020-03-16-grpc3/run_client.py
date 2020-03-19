import argparse

import sys

from chat_client.client import ChatClient


def define_args(arg_vec):
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', type=str)
    parser.add_argument('--host', type=str, default="localhost")
    parser.add_argument('--port', type=int, default="33333")

    _args = parser.parse_args(arg_vec)
    return _args


if __name__ == "__main__":
    args = define_args(arg_vec=sys.argv[1:])

    c = ChatClient(user_id=args.id, config=(args.host, args.port))

    c.start()

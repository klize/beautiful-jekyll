import logging
from queue import Queue
from typing import Tuple

import sys
import threading

import grpc

import chat_proto.chat_message_pb2
import chat_proto.chat_message_pb2_grpc

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


class ChatClient:

    def __init__(self, user_id: str, config: Tuple[str, int]):
        self._id = user_id
        self._config = config

        channel = grpc.insecure_channel(":".join(list(map(str, config))))
        self._connection = chat_proto.chat_message_pb2_grpc.ChatStub(channel)

        self._get_cmsg_stream_task = self._create_task("_get_cmsg_stream")

        self._cmsg_q = Queue()

        logging.info(f"Client<{self._id}> generated")


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

    @property
    def config(self):
        return self._config

    @property
    def connection(self):
        return self._connection

    def _make_req(self, msg):
        """

        Make a chat_proto.chat_message_pb2.ChatRequest to use as input to server's send method

        :param msg:
        :return:
        """
        chat_req = chat_proto.chat_message_pb2.ChatRequest()
        chat_req.cmsg.text.owner = self.id  # "" not works, Must feed None
        chat_req.cmsg.text.msg = msg
        return chat_req

    def send_msg(self, msg):
        """

        Make a request, then call server's send method with request.

        :param msg:
        :return:
        """
        req = self._make_req(msg)
        resp = self.connection.send(req)
        return resp

    def _get_cmsg_stream(self):
        """

        As you can see from chat_server.service, `recv` method is a blocking by outer while loop.
        def recv(...):
            while True:
                while ...:
                    c = ...

                    yield  c

        But if you send any message to the server, then server's message list will be updated
        ,thus the length of current list gets different from cached latest length, _last_idx_cmsgs.

        As a result of updates, server yields the updated messages and client who called this method
        gets cmsg in the for-loop.

        Since the method is basically blocking, this will be started on other thread.

        :return:
        """
        for cmsg in self.connection.recv(chat_proto.chat_message_pb2.Empty()):
            print(f"{cmsg.text.owner} > {cmsg.text.msg}")
            self._cmsg_q.put(cmsg)

    def _create_task(self, task: str):
        th = threading.Thread(target=getattr(self, task), daemon=True)
        th.start()
        return th

    @staticmethod
    def get_id_from_terminal():
        _id = input("id ? ")
        return _id

    def start(self):
        while True:
            try:
                msg = input("message >> ")
                if msg == "q":
                    sys.exit(0)
                else:
                    resp = self.send_msg(msg)
                    if not resp:
                        raise Exception # @TODO exception based on resp
            except Exception as e:
                logging.warning(e)
                self.id = self.get_id_from_terminal()








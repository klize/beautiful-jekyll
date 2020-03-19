import logging

from typing import Tuple, List
from concurrent import futures

import grpc
import chat_proto.chat_message_pb2
import chat_proto.chat_message_pb2_grpc


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


class ChatService(chat_proto.chat_message_pb2_grpc.ChatServicer):
    """Chat Service

        :param config: tuple of (ip, port)
    """
    def __init__(self, config: Tuple[str, int]):
        self._config = config

        self._cmsgs: List[chat_proto.chat_message_pb2.ChatMessage] = []
        self._last_idx_cmsgs = 0

    @property
    def config(self):
        return self._config

    def send(self, request: chat_proto.chat_message_pb2.ChatRequest, context)\
            -> chat_proto.chat_message_pb2.ChatResponse:
        """Send a message

        Clients are supposed to call this method to say their words.
        They make a request including chat_proto.chat_message_pb2.ChatMessage and put their
        message into the request.

        :param request:
        :param context:
        :return:
        """
        _cmsg = request.cmsg

        _owner = _cmsg.text.owner
        _text = _cmsg.text.msg

        # server debugging
        logging.info("Message from {%s} : {%s}" % (_owner, _text))

        _success = True
        if _owner == "":
            # If the sender has no its own id, server respond with False, which means
            # the client sends a message but server rejects it.
            _success = False

        if _success:
            self._cmsgs.append(_cmsg)

        resp = chat_proto.chat_message_pb2.ChatResponse()
        resp.success = _success

        return resp

    def recv(self, request: chat_proto.chat_message_pb2.Empty, context):
        """recieve messages from other clients

        Since gRPC has no concepts of `broadcast`, I tried seems like a broadcasting method
        as possible as I can. In the gRPC manner, client calls this method and server yields
        the latest messages. Client will iterate over this latest messages and print them out
        onto somewhere called a window.

        :param request:
        :param context:
        :return:
        """
        while True:
            while len(self._cmsgs) > self._last_idx_cmsgs:
                cmsg = self._cmsgs[self._last_idx_cmsgs]

                self._last_idx_cmsgs += 1
                yield cmsg


def serve(config: tuple):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = ChatService(config=config)

    chat_proto.chat_message_pb2_grpc.add_ChatServicer_to_server(servicer=servicer, server=server)

    server.add_insecure_port('[::]:'+str(config[1]))
    server.start()
    server.wait_for_termination()

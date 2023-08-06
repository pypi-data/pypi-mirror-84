import atexit
import faulthandler
import os
from typing import Any, Callable

from dynabuffers.Dynabuffers import Dynabuffers
from interstate_py.interstate import Interstate
from interstate_py.log_factory import LogFactory
from interstate_py.serialization.serialization import Serialization


class DynabufferSerialization(Serialization):

    def __init__(self, schema: str):
        self._dynabuffers = Dynabuffers.parse(schema)

    def serialize(self, value: Any) -> bytes:
        if isinstance(value, dict):
            has_annotated_keys = next(filter(lambda k: '@' in k, value.keys()), None) is not None
            if has_annotated_keys:
                return self._unpack_and_serialize(value)
            return self._dynabuffers.serialize(value, "outgoing")
        raise Exception("Only dictionary serialization is supported")

    def deserialize(self, bb: bytes) -> Any:
        return self._dynabuffers.deserialize(bytearray(bb))

    def _unpack_and_serialize(self, d: dict) -> bytes:
        keys = d.keys()
        if len(keys) > 1:
            raise Exception("Only one namespace annotated key is allowed - you provided: '{}'".format(keys))
        (key, v) = d.popitem()
        namespace = key[1:]  # get the one and only key and strip the @ namespace indicator
        return self._dynabuffers.serialize(v, "{}.outgoing".format(namespace))


class SkillTest:
    def __init__(self, eval: Callable, on_started: Callable, contract: str):
        self._eval = eval
        self._on_started = on_started
        self._context = {}
        self._contract = contract

    def initialize(self):
        skill_name = "test"
        faulthandler.enable()
        if self._contract is None:
            raise Exception("Could not load dynabuffers contract")

        serialization = DynabufferSerialization(self._contract)

        log = LogFactory.get_logger(skill_name)
        port = os.environ.get("PORT")
        if port is None or not port:
            port = 8077
        else:
            port = int(port)

        log.info("Starting %s", skill_name)
        # init hook
        self.load_on_started_hook()
        # register shutdown hook:
        atexit.register(self.load_on_stopped)

        # start server

        Interstate.request_response_server(self.pre_evaluate, port, serialization)

    def pre_evaluate(self, payload: dict) -> dict:
        """
        Wraps the evaluate function supplied by the skill developer to enhance the context with namespace information
        """
        context = {}
        namespace = payload.pop(':namespace')
        context['namespace'] = namespace
        return self._eval(payload, {**self._context, **context})

    def load_on_started_hook(self):
        self._on_started(self._context)

    def load_on_stopped(self):
        pass

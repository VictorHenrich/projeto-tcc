from typing import Optional
from socketio import Namespace, AsyncNamespace


class Controller(Namespace):
    event_name: str = ""
    room_name: Optional[str] = None


    def __init__(self):
        self.__event_name: str = self.__class__.event_name
        self.__room_name: str = self.__class__.room_ or self.__event_name

        super().__init__(self.__event_name)

    @property
    def event_name(self) -> str:
        return self.__event_name

    @property
    def room_name(self) -> str:
        return self.__room_name

    def on_connect(self, sid, environ) -> None:
        pass

    def on_disconnect(self, sid) -> None:
        pass
    

class AsyncController(AsyncNamespace):
    event_name: str = ""
    room_name: Optional[str] = None


    def __init__(self):
        self.__event_name: str = self.__class__.event_name
        self.__room_name: str = self.__class__.room_ or self.__event_name

        super().__init__(self.__event_name)

    @property
    def event_name(self) -> str:
        return self.__event_name

    @property
    def room_name(self) -> str:
        return self.__room_name

    def on_connect(self, sid, environ) -> None:
        raise NotImplementedError()

    def on_disconnect(self, sid) -> None:
        raise NotImplementedError()
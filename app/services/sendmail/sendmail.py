


from typing import Any, Mapping, Union, Optional, Sequence, Type
from smtplib import SMTP, SMTP_SSL
from ssl import create_default_context


class Sendmail:
    def __init__(
        self,
        host: str,
        port: Union[str, int],
        credentials: Optional[tuple[str, str]] = None,
        ssl: bool = False,
        tls: bool = False
    ) -> None:
        self.__host: str = host
        self.__port: Union[str, int] = port
        self.__credentials: Optional[tuple[str, str]] = credentials
        self.__ssl: bool = ssl
        self.__tls: bool = tls
        self.__server: Optional[Union[SMTP, SMTP_SSL]] = None

    def connect(self) -> None:
        time_out_seconds: int = 15

        if not self.__server:
            self.__server = SMTP(timeout=time_out_seconds) \
                if not self.__ssl \
                else SMTP_SSL(timeout=time_out_seconds, context=create_default_context())

            self.__server.connect(self.__host, self.__port)

            if self.__credentials:
                self.__server.login(*self.__credentials)

            if self.__tls:
                self.__server.starttls()
                self.__server.helo()

    def disconnect(self) -> None:
        if self.__server:
            self.__server.close()
            self.__server = None

    def __enter__(self) -> None:
        self.connect()

    def __exit__(self, exception_type: Type[Exception], exception_value: Exception, exception_traceback: str) -> None:
        self.disconnect()

    def send(
        self,
        from_: str,
        to: Union[str, Sequence],
        title: str,
        content: Union[str, bytes],
        attachments: Optional[Sequence[Mapping]] = None,
        enconding: str = "utf-8"
    ) -> None:
        pass
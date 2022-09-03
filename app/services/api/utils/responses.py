from typing import Any, Mapping, Optional, Union
from io import IOBase
from flask import Response
import json


__content_type_default__: Mapping[str, str] = \
    {
        'Content-Type': 'application/json'
    }


class ResponseSuccess(Response):
    def __init__(
        self,
        message: str = "OK",
        data: Optional[Any] = None,
        status_code: int = 200,
        headers: Mapping[str, str] = __content_type_default__
    ) -> None:

        response: Mapping[str, Any] = {
            "message": message,
            "status": status_code,
        }

        if data:
            response['result'] = data

        response_json: str = json.dumps(response)

        super().__init__(
            response=response_json,
            headers=headers,
            status=status_code
        )


class ResponseFailure(Response):
    def __init__(
        self,
        message: str = "ERRO",
        data: Optional[Any] = None,
        status_code: int = 500,
        headers: Mapping[str, str] = __content_type_default__
    ) -> None:

        response: Mapping[str, Any] = {
            "message": message,
            "status": status_code,
        }

        if data:
            response['result'] = data

        response_json: str = json.dumps(response)

        super().__init__(
            response=response_json,
            headers=headers,
            status=status_code
        )


class ResponseNotFound(Response):
    def __init__(
        self,
        message: str = "NOT FOUND",
        data: Optional[Any] = None,
        status_code: int = 404,
        headers: Mapping[str, str] = __content_type_default__
    ) -> None:

        response: Mapping[str, Any] = {
            "message": message,
            "status": status_code,
        }

        if data:
            response['result'] = data

        response_json: str = json.dumps(response)

        super().__init__(
            response=response_json,
            headers=headers,
            status=status_code
        )


class ResponseUnauthorized(Response):
    def __init__(
        self,
        message: str = "UNAUTHORIZED",
        data: Optional[Any] = None,
        status_code: int = 401,
        headers: Mapping[str, str] = __content_type_default__
    ) -> None:

        response: Mapping[str, Any] = {
            "message": message,
            "status": status_code,
        }

        if data:
            response['result'] = data

        response_json: str = json.dumps(response)

        super().__init__(
            response=response_json,
            headers=headers,
            status=status_code
        )


class ResponseMedia(Response):
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

    __file_types: Mapping[str, str] = {
        'aac': 'audio/aac',
        'abw': 'application/x-abiword',
        'arc': 'application/x-freearc',
        'avif': 'image/avif',
        'avi': 'video/x-msvideo',
        'azw': 'application/vnd.amazon.ebook',
        'bin': 'application/octet-stream',
        'bmp': 'image/bmp',
        'bz': 'application/x-bzip',
        'bz2': 'application/x-bzip2',
        'cda': 'application/x-cdf',
        'csh': 'application/x-csh',
        'css': 'text/css',
        'csv': 'text/csv',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'eot': 'application/vnd.ms-fontobject',
        'epub': 'application/epub+zip',
        'gz': 'application/gzip',
        'gif': 'image/gif',
        'html': 'text/html',
        'ico': 'image/vnd.microsoft.icon',
        'ics': 'text/calendar',
        'jar': 'application/java-archive',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'js': 'text/javascript',
        'json': 'application/json',
        'mid': 'audio/midi',
        'midi': 'audio/x-midi',
        'mp3': 'audio/mpeg',
        'mp4': 'video/mp4',
        'mpeg': 'video/mpeg',
        'odp': 'application/vnd.oasis.opendocument.presentation',
        'ods': 'application/vnd.oasis.opendocument.spreadsheet'
    }


    def __init__(
        self,
        file: Union[str, bytes, IOBase],
        file_type: str,
        filename: str,
        status: int = 200,
        stream: bool = True
    ) -> None:

        content_type: str = [
            value
            for prop, value in ResponseMedia.__file_types.items()
            if file_type == prop
        ] [0]

        headers: Mapping[str, str] = {
            'Content-Type': content_type,
            'Content-Disposition': f'attachment; filename="{filename}"'
        }

        response_attachment: Union[str, bytes, list[bytes], list[str]] = self.__handle_file(file, stream)

        super().__init__(
            response=response_attachment,
            headers=headers,
            status=status
        )

    def __handle_file(self, file: Union[str, bytes, IOBase], stream: bool) -> Union[str, bytes, list[bytes], list[str]]:
        if isinstance(file, IOBase):
            return self.__handle_io(file, stream)

        else:
            return self.__handle_byte_or_str(file, stream)

    def __handle_io(self, file: IOBase, stream: bool) -> Union[str, bytes, list[bytes], list[str]]:
        if not file.readable():
            raise Exception('IO file is not readable type')

        file.seek(0)

        content: Union[str, bytes, list[bytes], list[str]] = \
            file.readlines() if stream else file.read()

        file.close()

        return content

    def __handle_byte_or_str(self, file: Union[str, bytes], stream: bool) -> Union[str, bytes, list[bytes], list[str]]:
        return list(file) if stream else file

        

            


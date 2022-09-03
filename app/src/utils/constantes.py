

from typing import Any, Mapping, Sequence


__NAME_SESSION_USER__: str = "session_user_osplus"

__ALGORITHMS_JWT__ : Sequence[str] = 'HS256',

__PAYLOAD_AUTHENTICATION_USER__: Mapping[str, Any] = {
    'uuid_company': "",
    'uuid_user': "",
    'expired': 0
}

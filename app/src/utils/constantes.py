

from typing import Any, Mapping, Sequence


__NAME_SESSION_USER__: str = "session_user_osplus"

__ALGORITHMS_JWT__ : list[str] = ['HS256']

__PAYLOAD_AUTHENTICATION_USER__: Mapping[str, Any] = {
    'uuid_company': "",
    'uuid_user': "",
    'expired': 0
}

__TIPOS_CONTAS_RECEBER_PAGAR__: Sequence[str] = 'PAG', 'REC'

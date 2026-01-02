"""
Log defines
Mostafa Rasouli
mostafarasooli54@gmail.com
2023-11-29
"""

from log.models import Log
from utils.defines import get_client_ip


def save_log(request, l_type=None, log=None, body=None):
    try:
        Log(
            l_type=l_type,
            endpoint=request.build_absolute_uri(),
            body=body,
            log=log,
            ip=get_client_ip(request)
        ).save()
    except Exception:
        pass

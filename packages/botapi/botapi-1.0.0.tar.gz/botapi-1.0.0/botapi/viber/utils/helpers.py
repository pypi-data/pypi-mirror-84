from .constants import ALL_STATUS_CODES


def get_status_description(status_code: int) -> dict:
    """
    returns description of response code.

    :param status_code: int - status code from response
    :return: dict with status code, message, description
    """
    status = ALL_STATUS_CODES.get(status_code)
    return {
        "code": status_code,
        "message": "General error" if status is None else status[0],
        "description": "General error" if status is None else status[1],
    }

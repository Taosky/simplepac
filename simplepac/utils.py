import base64


def is_base64(text):
    try:
        base64.b64decode(text)
    except ValueError:
        return False
    return True


__all__ = ['is_base64']

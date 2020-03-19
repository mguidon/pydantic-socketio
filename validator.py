from pydantic import ValidationError

def validate(cls, err_callback):
    def outer(func):
        def inner(data, **kwargs):
            try:
                m = cls(**data)
                return func(m, **kwargs)
            except ValidationError as e:
                err_callback(e.json())
        return inner
    return outer


def validate_asyn(cls, err_callback):
    def outer(func):
        async def inner(sid, data, **kwargs):
            try:
                m = cls(**data)
                return await func(sid, m, **kwargs)
            except ValidationError as e:
                return await err_callback(sid, e.json())
        return inner
    return outer
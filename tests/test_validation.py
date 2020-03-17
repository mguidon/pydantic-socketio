import pytest
from pydantic import ValidationError

from model.model import MouseInput, Quality


def validate(cls):
    def outer(func):
        def inner(data, **kwargs):
            try:
                m = cls(**data)
                return func(m, **kwargs)
            except ValidationError as e:
                print(e.json())
        return inner
    return outer

@validate(MouseInput)
def on_mouseInput(data: MouseInput):
    assert type(data) == MouseInput

def test():
    data = { "button": 0, "delta" : 100, "modifiers" : 1, "pos" : { "x": 1, "y": 2}, "type" : "wheel"}
    m = MouseInput(**data)
    on_mouseInput(data)
    data = { "quality" : 100}
    q = Quality(**data)

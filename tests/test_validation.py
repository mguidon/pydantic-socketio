import pytest

from model.model import MouseInput, Quality
from validator import validate

def on_error(err: str):
    print("error_callback")
    print(err)

@validate(MouseInput, on_error)
def on_mouseInput(data: MouseInput):
    assert type(data) == MouseInput

def test():
    data = { "button": 0, "delta" : 100, "modifiers" : 1, "pos" : { "x": 1, "y": 2}, "type" : "a"}
    on_mouseInput(data)
    data = { "quality" : 100}
    q = Quality(**data)

from pytest import mark


# content of test_sample.py
def func(x):
    return x + 1

@mark.smoke
def test_answer():
    assert func(3) == 5

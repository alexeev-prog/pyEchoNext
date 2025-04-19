from echonextdi.providers.callable_provider import CallableProvider


def function(a: int, b: int = 2):
    return a**b


def test_callable():
    cp = CallableProvider(function)
    result = cp(a=2)
    assert result == 4

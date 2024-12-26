from echonextdi.containers.container import Container
from echonextdi.depends import Depends
from echonextdi.providers.callable_provider import CallableProvider


def sqrt(a: int, b: int = 2):
	return a**b


class SQRT_Dependency:
	def __init__(self, sqrt):
		self.sqrt = sqrt


container = Container()
container.register("sqrt", CallableProvider(sqrt))


def calculate(number: int, depend: Depends = Depends(container, SQRT_Dependency)):
	return depend().sqrt(number)


def test_depend():
	res = calculate(3)
	assert res == 9

	assert container._providers.keys() == {"sqrt"}

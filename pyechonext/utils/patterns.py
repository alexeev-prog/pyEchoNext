class Singleton(type):
	"""
	A metaclass that implements the Singleton pattern.

	This metaclass ensures that a class has only one instance, and provides a
	global point of access to it.
	"""

	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

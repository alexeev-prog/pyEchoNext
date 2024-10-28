from dataclasses import dataclass


@dataclass
class Settings:
	"""
	This class describes settings.
	"""

	BASE_DIR: str
	TEMPLATES_DIR: str

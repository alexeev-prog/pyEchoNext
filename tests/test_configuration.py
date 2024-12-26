from echonextdi.providers.configuration_provider import ConfigurationProvider


def test_json():
	cp = ConfigurationProvider("example.json")
	instance = cp().get_loaded_config()
	assert instance == {
		"config_name": "example.json",
		"config": {"id": 0, "is_file": True},
	}


def test_yaml():
	cp = ConfigurationProvider("example.yaml")
	instance = cp().get_loaded_config()
	assert instance == {
		"metadata": {
			"name": "pyBurnBuild",
			"version": "0.1.0",
			"description": "build system written in python for projects in C, C++, Python, ASM",
			"language": "python",
			"use_cmake": True,
			"cache_file": "cache.json",
			"features": ["pyechonext"],
		},
		"compiler": {"name": "gcc", "base_compiler_flags": ["-c"]},
	}


def test_toml():
	cp = ConfigurationProvider("example.toml")
	instance = cp().get_loaded_config()
	assert instance == {
		"metadata": {
			"name": "pyBurnBuild",
			"version": "0.1.0",
			"description": "build system written in python for projects in C, C++, Python, ASM",
			"language": "python",
			"use_cmake": True,
			"cache_file": "cache.json",
			"features": ["pyechonext"],
		},
		"compiler": {"name": "gcc", "base_compiler_flags": "-c"},
	}

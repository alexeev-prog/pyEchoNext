import os

from pyechonext.config import Settings
from pyechonext.static import StaticFile, StaticFilesManager

settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)),
	TEMPLATES_DIR="templates",
	SECRET_KEY="secret-key",
)


def test_static():
	file = StaticFile(settings, "styles.css")
	manager = StaticFilesManager([file])

	assert file.get_content_type() == "text/css"
	assert manager.get_file_type("/static/styles.css") == "text/css"

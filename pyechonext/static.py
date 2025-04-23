import mimetypes
import os
from pathlib import Path
from typing import List, Optional

from pyechonext.utils import prepare_url
from pyechonext.config import Settings
from pyechonext.logging import logger
from pyechonext.utils.exceptions import StaticFileNotFoundError
from pyechonext.cache import InMemoryCache


class StaticFile:
    """
    This class describes a static file.
    """

    def __init__(self, settings: Settings, filename: str, update_timeout: Optional[int] = 3600, precache: Optional[bool] = False):
        """Constructs a Static File

        Args:
            settings (Settings): settings of webapp.
            filename (str, optional): static filename without static dir.
            update_timeout (int, optional): timeout to update inmemory-cache file content. Defaults to 3600.
            precache (bool, optional): preload a file content flag. Defaults to False.

        Raises:
            StaticFileNotFoundError: static file at static dir not found
        """
        self.settings: Settings = settings
        self.filename: str = f"/{settings.STATIC_DIR}/{filename}".replace("//", "/")
        self.abs_filename: Path = Path(
            os.path.join(self.settings.BASE_DIR, self.settings.STATIC_DIR, filename)
        )

        if not self.abs_filename.exists():
            raise StaticFileNotFoundError(
                f'Static file "{self.abs_filename}" not found.'
            )
            
        self.content_cache: InMemoryCache = InMemoryCache(timeout=update_timeout)
        
        self.precache: bool = precache
        self.preloaded_value: Optional[str] = None
        
        if self.precache:
            self.preloaded_value = self.caching_static_file()

    def caching_static_file(self):
        """Set and save static file to cache
        """
        content = self._load_content()
        
        item = self.content_cache.get(self.filename)
        
        if item is None:
            logger.debug(f'Caching static file: {self.filename}')
            self.content_cache.set(self.filename, content)
            item = content
        else:
            logger.debug(f'Load static file from cache: {self.filename}')
        
        return item

    def _load_content(self) -> str:
        """
        Loads a content.

        :returns:	static file content
        :rtype:		str
        """
        with open(self.abs_filename, "r") as file:
            return file.read().strip()

    def get_content_type(self) -> str:
        """
        Gets the content type.

        :returns:	The content type.
        :rtype:		str
        """
        content_type, _ = mimetypes.guess_type(str(self.abs_filename))

        return content_type or "application/octet-stream"

    def get_file_size(self) -> int:
        """
        Gets the file size.

        :returns:	The file size.
        :rtype:		int
        """
        return self.abs_filename.stat().st_size


class StaticFilesManager:
    """
    This class describes a static files manager.
    """

    def __init__(self, static_files: List[StaticFile]):
        """
        Constructs a new instance.

        :param		static_files:  The static files
        :type		static_files:  List[StaticFile]
        """
        self.static_files = static_files

    def get_file_type(self, url: str) -> str | None:
        """
        Gets the file type.

        :param		url:  The url
        :type		url:  str

        :returns:	The file type.
        :rtype:		str
        """
        for static_file in self.static_files:
            if static_file.filename == url:
                return static_file.get_content_type()

    def get_file_size(self, url: str) -> int | None:
        """
        Gets the file size.

        :param		url:  The url
        :type		url:  str

        :returns:	The file size.
        :rtype:		str
        """
        for static_file in self.static_files:
            if static_file.filename == url:
                return static_file.get_file_size()

    def serve_static_file(self, url: str) -> str | bool:
        """
        Server static file by url

        :param		url:  The url
        :type		url:  str

        :returns:	static file content
        :rtype:		str
        """
        url = prepare_url(url)
        
        for static_file in self.static_files:
            if static_file.filename == url:
                logger.info(f"Found static file: {static_file.filename}")
                if static_file.precache:
                    logger.debug(f'Use preloaded value of static file {static_file}')
                    return static_file.preloaded_value
                else:
                    return static_file.caching_static_file()

        logger.warning(f'Static file "{url}" not found.')
        return False

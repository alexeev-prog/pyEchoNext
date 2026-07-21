import re
from typing import Dict

CYRILLIC_TO_LATIN: Dict[str, str] = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}

SLUG_MAX_LENGTH = 512


def _transliterate_cyrillic(text: str) -> str:
    """Transliterate cyrillic to latin

    Args:
        text (str): text

    Returns:
        str: transliterated text
    """
    return "".join(CYRILLIC_TO_LATIN.get(char.lower(), char) for char in text)


class SlugGenerator:
    """
    This class describes a slug generator.
    """

    def generate_slug(self, phrase: str) -> str:
        """Generate slug

        Args:
            phrase (str): phrase

        Returns:
            str: slug
        """
        slug = self._convert_to_slug(phrase)
        return slug

    def _convert_to_slug(self, phrase: str) -> str:
        """Convert phrase to slug

        Args:
            phrase (str): phrase for converting

        Returns:
            str: converted slug
        """
        slug = phrase.lower()
        slug = self._replace_spaces_with_hyphens(slug)
        slug = _transliterate_cyrillic(slug)
        slug = self._remove_non_alphanumeric_chars(slug)
        slug = self._remove_consecutive_hyphens(slug)
        slug = self._limit_length(slug)
        return slug

    def _remove_non_alphanumeric_chars(self, text: str) -> str:
        """Removes non alphanumeric chars

        Args:
            text (str): text

        Returns:
            str: cleaned text
        """
        return re.sub(r"[^a-z0-9_-]", "", text, flags=re.UNICODE)

    def _replace_spaces_with_hyphens(self, text: str) -> str:
        """Replace space with hyphens

        Args:
            text (str): text

        Returns:
            str: cleaned text
        """
        return text.replace(" ", "-")

    def _remove_consecutive_hyphens(self, text: str) -> str:
        """Remove consecutive hyphens

        Args:
            text (str): text of slug

        Returns:
            str: cleaned text
        """
        return re.sub(r"-+", "-", text)

    def _limit_length(self, slug: str) -> str:
        """Split slug by length limit

        Args:
            slug (str): slug phrase

        Returns:
            str: splitted slug
        """
        return slug[:SLUG_MAX_LENGTH]

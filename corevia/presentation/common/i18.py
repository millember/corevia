import json
from importlib.resources import files

from PySide6.QtCore import QObject, Signal

class I18n(QObject):
    language_changed = Signal(str)

    DEFAULT_LANGUAGE = "en"
    SUPPORTED_LANGUAGES = {"en", "ru"}

    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__()

        self._language = language
        self._translations: dict[str, str] = {}

        self._validate_language(language)
        self._load()

    @property
    def language(self) -> str:
        return self._language

    def tr(self, key: str) -> str:
        return self._translations.get(
            key,
            key
        )

    def set_language(
        self,
        language: str,
    ) -> None:
        self._validate_language(language)

        if language == self._language:
            return

        self._language = language
        self._load()
        self.language_changed.emit(language)

    def _load(self) -> None:
        locale_file = (
            files("corevia.locales")
            .joinpath(f"{self._language}.json")
        )
        self._translations = json.loads(
            locale_file.read_text(
                encoding="utf-8"
            )
        )

    @classmethod
    def _validate_language(
        cls,
        language: str,
    ) -> None:
        if language not in cls.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

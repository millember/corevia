from collections.abc import Callable

from PySide6.QtWidgets import QMenu, QToolButton

from corevia.presentation.common.i18 import I18n

class LanguageButton(QToolButton):
    def __init__(
        self,
        i18n: I18n,
        on_language_selected: Callable[[str], None],
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._i18n = i18n
        self._on_language_selected = on_language_selected

        self.setText("🌐")
        self.setAutoRaise(True)

        self._menu = QMenu(self)
        self.setMenu(self._menu)
        self.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        self._i18n.language_changed.connect(
            self._apply_translations
        )

        self._apply_translations()

    def _apply_translations(
        self,
        *_args,
        ) -> None:
        self.setToolTip(
            self._i18n.tr("language.change")
        )

        self._menu.clear()

        english_action = self._menu.addAction(
            self._i18n.tr("language.english")
        )
        russian_action = self._menu.addAction(
            self._i18n.tr("language.russian")
        )

        english_action.triggered.connect(
            lambda _checked=False: self._on_language_selected("en")
        )
        russian_action.triggered.connect(
            lambda _checked=False: self._on_language_selected("ru")
        )

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from corevia.presentation.common.i18 import I18n
from corevia.presentation.desktop.widgets.language_button import (
    LanguageButton,
)

class MainWindow(QMainWindow):
    def __init__(
        self,
        i18n: I18n,
        ) -> None:
        super().__init__()

        self._i18n = i18n
        self._welcome_label = QLabel()

        self._language_button = LanguageButton(
            i18n=self._i18n,
            on_language_selected=self._change_language,
            parent=self,
        )

        layout = QVBoxLayout()
        layout.addWidget(self._language_button)
        layout.addWidget(self._welcome_label)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.resize(900, 600)

        self._i18n.language_changed.connect(
            self._apply_translations
        )
        self._apply_translations()

    def _change_language(
        self,
        language: str,
    ) -> None:
        self._i18n.set_language(language)

    def _apply_translations(
        self,
        *_args,
    ) -> None:
        self.setWindowTitle(
            self._i18n.tr("app.title")
        )
        self._welcome_label.setText(
            self._i18n.tr("app.welcome")
        )


def run_desktop() -> int:
    app = QApplication([])

    i18n = I18n()

    window = MainWindow(
        i18n=i18n
    )
    window.show()

    return app.exec()

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "Corevia"
        )

        self.resize(
            900,
            600,
        )

        self.setCentralWidget(
            QLabel(
                "Corevia"
            )
        )

def run_desktop() -> int:
    app = QApplication([])

    window = MainWindow()
    window.show()

    return app.exec()
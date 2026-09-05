from corevia.presentation.common.i18n import I18n


def test_i18n_switches_language() -> None:
    i18n = I18n()

    assert i18n.language == "en"
    assert i18n.tr("app.welcome") == "Welcome to Corevia"

    i18n.set_language("ru")

    assert i18n.language == "ru"
    assert i18n.tr("app.welcome") == "Добро пожаловать в Corevia"

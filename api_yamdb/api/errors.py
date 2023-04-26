"""Модуль содержит описание ошибок в приложении api."""


class ErrorMessage:
    """Определяет описание ошибок, возвращаемых пользователю."""

    ME_AS_USERNAME_ERROR = (
        "Нельзя использовать me в качестве имени пользователя."
    )
    EXISTS_USERNAME_ERROR = (
        "Нельзя использовать существующеe имя пользователя."
    )
    EXISTS_EMAIL_ERROR = (
        "Нельзя использовать email существующего пользователя."
    )
    INVALID_CONFIRMATION_CODE_ERROR = "Некорректный confirmation code."

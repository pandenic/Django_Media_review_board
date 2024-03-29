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
    INVALID_YEAR_ERROR = (
        "Год выпуска не может быть больше текущего."
    )
    MAX_SCORE_ERROR = "Максимальная оценка не может быть выше: "
    MIN_SCORE_ERROR = "Минимальная оценка не может быть ниже: "
    ONLY_ONE_REVIEW_ERROR = "Можно написать только один отзыв!"
    NO_VIEW_IN_CONTEXT_ERROR = "Ошибка при обработке запроса"

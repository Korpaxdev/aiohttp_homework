INCORRECT_REQUEST_BODY = "Неправильное тело запроса"
REQUIRED_FIELD = "Поле обязательно для заполнения"
TOO_LONG_FIELD = "Поле должно быть не более {0} символов"
UNIQUE_FIELD = "Запись с таким значением уже существует"
NOT_FOUND = "Такой записи не существует"
MESSAGE_DELETED = "Запись успешно удалена"
PASSWORD_TOO_SHORT = "Пароль должен быть не менее 8 символов"
WRONG_EMAIL_OR_PASS = "Неверный email адрес или пароль"
USER_NOT_FOUND = "Такого пользователя не существует"
LOGOUT_SUCCESS = "Вы успешно вышли из системы"
TOKEN_NOT_FOUND = "Такой токен не существует в системе"
NOT_AUTHORIZED = "Вы не авторизованы"
NOT_OWNER_ADVERTISEMENT = "Вы не являетесь создателем объявления"


def error_message(message):
    return {"errors": message}


def success_message(message):
    return {"success": message}

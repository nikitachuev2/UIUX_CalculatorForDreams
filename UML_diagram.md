@startuml
title UML-диаграмма последовательности действий клиента — Сайт "Управление финансами"

actor Пользователь
participant "Интерфейс\n(браузер)" as UI
participant "Сервер Flask" as Server
participant "AuthService"
participant "UserService"
participant "FinanceService"
participant "GoalService"
participant "CreditService"
database "БД (SQL)" as DB

== Регистрация ==
Пользователь -> UI : Открывает форму регистрации
UI -> Пользователь : Отображает поля (email, пароль)
Пользователь -> UI : Вводит email и пароль
UI -> Server : POST /register(email, password)

alt Некорректный email
    Server -> AuthService : validateEmail()
    AuthService -> Server : Ошибка "Неверный email"
    Server -> UI : Показывает ошибку "Введите корректный email"
else Email уже зарегистрирован
    AuthService -> DB : SELECT * FROM users WHERE email=email
    DB --> AuthService : Уже существует
    Server -> UI : Показывает ошибку "Email уже зарегистрирован"
else Успешная регистрация
    AuthService -> AuthService : hashPassword()
    AuthService -> DB : INSERT INTO users(email, hashed_password)
    DB --> AuthService : OK
    Server -> UI : Перенаправление на /login
end

== Вход ==
Пользователь -> UI : Вводит email и пароль
UI -> Server : POST /login(email, password)
alt Неверные учетные данные
    Server -> AuthService : checkCredentials()
    AuthService -> DB : SELECT * FROM users WHERE email=email
    DB --> AuthService : user data
    AuthService -> Server : Сравнение паролей (не совпало)
    Server -> UI : Ошибка "Неверный email или пароль"
else Успешный вход
    Server -> UI : redirect /home
end

== Главная страница ==
UI -> Server : GET /home
Server -> UserService : getBalance(user_id)
UserService -> DB : SELECT доходы и расходы WHERE user_id
DB --> UserService : данные баланса
Server -> UI : Отображает баланс и меню функций

== Добавить покупку ==
Пользователь -> UI : Нажимает "Добавить покупку"
UI -> Server : GET /add_purchase
UI -> Пользователь : Форма ввода суммы и категории
Пользователь -> UI : Вводит данные
UI -> Server : POST /add_purchase

alt Отрицательная сумма
    Server -> UI : Ошибка "Сумма не может быть отрицательной"
else Некорректные данные
    Server -> UI : Ошибка валидации формы
else Успех
    FinanceService -> DB : INSERT INTO purchases
    DB --> FinanceService : OK
    Server -> UI : Покупка добавлена
end

== Установить цель ==
Пользователь -> UI : Нажимает "Установить цель"
UI -> Server : GET /set_goal
UI -> Пользователь : Вводит цель и сумму
Пользователь -> UI : подтверждает
UI -> Server : POST /set_goal

alt Нулевая или отрицательная сумма
    Server -> UI : Ошибка "Цель должна быть больше 0"
else Успех
    GoalService -> DB : INSERT INTO goals
    DB --> GoalService : OK
    Server -> UI : Цель установлена
end

== Кредитный калькулятор ==
Пользователь -> UI : Вводит сумму, срок, процент
UI -> Server : POST /calculate_credit
alt Ошибочные параметры
    Server -> UI : Ошибка "Введите положительные значения"
else Успех
    CreditService -> CreditService : calculate()
    CreditService -> Server : Платёж, переплата, ставка
    Server -> UI : Отображает расчёты
end

== Добавить доход ==
Пользователь -> UI : Вводит сумму
UI -> Server : POST /add_income
alt Некорректный ввод
    Server -> UI : Ошибка "Некорректные данные, ввод должен быть числом."
else Успешное добавление
    FinanceService -> DB : INSERT INTO income
    DB --> FinanceService : OK
    Server -> UI : Баланс обновлён
end

== Распределение дохода ==
Пользователь -> UI : Переходит к распределению
UI -> Server : GET /income_distribution
Server -> FinanceService : getIncome(user_id)
FinanceService -> DB : SELECT total income
DB --> FinanceService : сумма
FinanceService -> Server : расчёт 20/50/30
Server -> UI : Отображает доли

== Анализ расходов ==
Пользователь -> UI : Переходит к анализу расходов
UI -> Server : GET /expense_analysis
Server -> FinanceService : getExpenses(user_id)
FinanceService -> DB : SELECT * FROM purchases
DB --> FinanceService : список
FinanceService -> Server : Сгруппировать по категориям за последний месяц
Server -> UI : График и список расходов

== Выход ==
Пользователь -> UI : Нажимает "Выйти"
UI -> Server : GET /logout
Server -> AuthService : logout()
Server -> UI : Перенаправление на /login

@enduml

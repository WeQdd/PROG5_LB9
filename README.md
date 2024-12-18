# Лабораторная работа 9. Задание
## Описание задачи
Реализуйте REST-сервис для просмотра текущего уровня бонусной программы, который дает определенный кешбэк пользователю и следующего уровня ("серебряный", "золотой", "платиновый" уровень при определенном объеме трат). Поскольку эти данные являются важными и критичными, каждый пользователь может видеть только информацию о своем кэшбеке. Для обеспечения безопасности потребуется реализовать метод, который по логину и паролю сотрудника будет выдавать секретный токен, действующий в течение определенного времени. Запрос данных о бонусной программе должен выдаваться только при предъявлении валидного токена пользователем. В модели данных и в интерфейсе соответственно должны быть отображены. Уровень трат и границы бонусных уровней 

## Требования к решению
- в качестве токена использовать JWT;
- код размещен и доступен в публичном репозитории на GitHub / GitLab;
- оформлена инструкция по запуску сервиса и взаимодействию с проектом (Markdown-файл с использованием конструкций разметки по необходимости);
- сервис реализован на FastAPI или Django Rest Framework, Flask, Eve.

### Получаем токен

```bash
curl -X POST -d "username=admin&password=admin" http://localhost:8000/token
```

* username - имя пользователя
* password - пароль

### Получаем информацию об уровне бонусной программы


```bash
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczNDU0Nzk4MX0.CI8FlnWXL-yyUuiFvaMZQtbHtzznsRInnsRvB3tIlRw" http://localhost:8000/bonus
```

Полученный результат:

{"current_level":{"level":"Серебро","min_spending":0.0,"cashback":0.01},"next_level":{"level":"Золото","min_spending":10000.0,"cashback":0.02}}


![image](https://github.com/user-attachments/assets/ec858a40-fe55-4a6d-8ae7-22893189910d)

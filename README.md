# Тестовое задание для кандидата на вакансию Automation QA Engineer

Описание задания:
Необходимо разработать автоматизированные тесты для открытого API Petstore (Swagger Petstore).
Цель задания — продемонстрировать ваши навыки в области автоматизации тестирования, включая написание тестов, работу с API, использование фреймворков для тестирования и генерации отчетов. Задание является простым, но нужно продемонстрировать реализацию на должном уровне с использованием необходимого инструментария. (Показать свои best practice)


# How to run:

Install requirements.txt (pip install -r requirements.txt)

Run tests: pytest -v -rP ./tests

Run tests with docs html: pytest --html=reports/report.html -v -rP ./tests
To view the documentation you need to open the file report.html

Run tests with docs allure: pytest --alluredir=reports/allure-results -v -rP ./tests
Generate docs: allure serve reports/allure-results


# Небольшое Summary

Я добавил основную структуру проекта и вынес файлы по PageObject.
Написаны тесты на 4 метода из ТЗ с позитивными и негативными проверками.
Так же добавлена возможность просмотра результатов в нескольких отчетах.

# Дефекты в апи

1. В методе PUT есть документация:
Responses
Code	Description
400	    Invalid ID supplied

404	    Pet not  found

405	    Validation exception

Но при некорректном ID отдается ошибка:
E       AssertionError: Ожидался статус ошибки 400, но получен 500
E       assert 500 == 400
E        +  where 500 = <Response [500]>.status_code

Тот же самый код отдается на ошибки Pet not  found и Validation exception

2. Если передать в метод Put пустую строку, то отдается 200 код

3. В методе DELETE не отдается сообщение об ошибке, если передан не существующий ID
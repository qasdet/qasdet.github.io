---
title: Как защитить ваш API С помощью Аутентификации JWT в Django И Django Rest Framework
layout: page
---

![2023-06-15-your-title.md
](https://images.unsplash.com/photo-1531771686035-25f47595c87a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MzB8fGNvbXB1dGVyfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=1600&q=60)

JWT (Json Web Token) - одна из самых популярных систем аутентификации на основе токенов. Сторонним пакетом для аутентификации JWT является djangorestframework-simple jwt, который используется для реализации jwt auth в проекте django.

Установка

Сначала нам нужно установить простой пакет jwt в нашу систему, просто выполнив эту команду в терминале.

`pip install djangorestframework-simplejwt`

Настройка простого пакета JWT

Открытый settings.py файл и добавить просто добавьте rest_framework_simplejwt в INSTALLED_APPS.


```
INSTALLED_APPS = [
     ...
     'rest_framework_simplejwt',
     ...
]
```

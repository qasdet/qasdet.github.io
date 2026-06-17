#!/usr/bin/env python3
"""Генератор HTML-справочника по Python на русском языке."""

import os

OUT = r'C:\Users\win11\Documents\GIT\qasdet.github.io\pytestru'

PAGE_TPL = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Справочник Python</title>
  <link rel="stylesheet" href="pytestru-style.css">
</head>
<body>
<div class="wrapper">
  <header>
    <h1><a href="index.html">Справочник Python</a></h1>
    <p class="subtitle">Полное руководство по языку на русском</p>
  </header>
  <div class="layout">
    <nav class="sidebar">
      <h3>Разделы</h3>
      <ul>
{nav_items}
      </ul>
    </nav>
    <main>
      <h2>{title}</h2>
{content}
    </main>
  </div>
  <footer>
    <p>Справочник Python на русском — создан для тестировщиков и разработчиков</p>
  </footer>
</div>
</body>
</html>'''

INDEX_TPL = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Справочник Python</title>
  <link rel="stylesheet" href="pytestru-style.css">
</head>
<body>
<div class="wrapper">
  <header>
    <h1>Справочник Python</h1>
    <p class="subtitle">Полное руководство по языку на русском</p>
  </header>
  <div class="layout">
    <nav class="sidebar">
      <h3>Разделы</h3>
      <ul>
{nav_items}
      </ul>
    </nav>
    <main>
      <h2>Все разделы справочника</h2>
      <div class="card-grid">
{cards}
      </div>
    </main>
  </div>
  <footer>
    <p>Справочник Python на русском — создан для тестировщиков и разработчиков</p>
  </footer>
</div>
</body>
</html>'''

CSS = '''/* pytestru-style.css — светлая тема для справочника Python */
:root {
  --bg: #f8f9fc;
  --text: #1e1b4b;
  --accent: #7c3aed;
  --accent-light: #ede9fe;
  --card-bg: #ffffff;
  --border: #e0e7ff;
  --sidebar-bg: #ffffff;
  --header-bg: linear-gradient(135deg, #7c3aed, #a78bfa);
  --header-text: #ffffff;
  --code-bg: #f3f4f6;
  --hover: #f0e7ff;
  --footer-bg: #1e1b4b;
  --footer-text: #c7d2fe;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}

.wrapper {
  max-width: 1300px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
header {
  background: var(--header-bg);
  color: var(--header-text);
  padding: 28px 36px;
  border-radius: 16px;
  margin-bottom: 24px;
}
header h1 { font-size: 28px; font-weight: 700; }
header h1 a { color: #fff; text-decoration: none; }
header .subtitle { opacity: 0.85; margin-top: 6px; font-size: 15px; }

/* Layout */
.layout {
  display: flex;
  gap: 24px;
  flex: 1;
}

/* Sidebar */
.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: var(--sidebar-bg);
  border-radius: 12px;
  padding: 20px 0;
  border: 1px solid var(--border);
  height: fit-content;
  position: sticky;
  top: 20px;
}
.sidebar h3 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--accent);
  padding: 0 20px 12px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 8px;
}
.sidebar ul { list-style: none; }
.sidebar li a {
  display: block;
  padding: 7px 20px;
  color: var(--text);
  text-decoration: none;
  font-size: 14px;
  transition: background 0.2s;
  border-left: 3px solid transparent;
}
.sidebar li a:hover,
.sidebar li a.active {
  background: var(--hover);
  border-left-color: var(--accent);
  color: var(--accent);
}

/* Main */
main {
  flex: 1;
  min-width: 0;
  background: var(--card-bg);
  border-radius: 12px;
  padding: 32px;
  border: 1px solid var(--border);
}
main h2 {
  font-size: 24px;
  color: var(--accent);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--accent-light);
}
main h3 {
  font-size: 18px;
  color: var(--text);
  margin: 24px 0 12px;
}
main h4 {
  font-size: 16px;
  color: var(--text);
  margin: 20px 0 10px;
}
main p { margin: 10px 0; }
main ul, main ol { margin: 10px 0 10px 24px; }
main li { margin: 4px 0; }

/* Code */
code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9em;
}
pre {
  background: var(--code-bg);
  padding: 16px 20px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
  border: 1px solid var(--border);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 14px;
  line-height: 1.5;
}
pre code { background: none; padding: 0; }

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}
th, td {
  border: 1px solid var(--border);
  padding: 10px 14px;
  text-align: left;
}
th { background: var(--accent-light); font-weight: 600; }

/* Card grid for index */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 20px;
}
.card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
  text-decoration: none;
  color: var(--text);
}
.card:hover {
  border-color: var(--accent);
  box-shadow: 0 4px 20px rgba(124,58,237,0.1);
  transform: translateY(-2px);
}
.card h3 { font-size: 16px; margin: 0 0 8px; color: var(--accent); }
.card p { font-size: 13px; margin: 0; opacity: 0.75; }

/* Footer */
footer {
  margin-top: 24px;
  background: var(--footer-bg);
  color: var(--footer-text);
  padding: 18px 28px;
  border-radius: 12px;
  text-align: center;
  font-size: 13px;
}

/* Responsive */
@media (max-width: 768px) {
  .layout { flex-direction: column; }
  .sidebar { width: 100%; position: static; }
  .card-grid { grid-template-columns: 1fr; }
}

/* Info blocks */
.info {
  background: #ede9fe;
  border-left: 4px solid var(--accent);
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
  margin: 12px 0;
}
.warn {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
  margin: 12px 0;
}
'''

# ── Структура разделов ──
SECTIONS = [
    {
        'slug': 'intro',
        'title': 'Введение в Python',
        'desc': 'История, особенности, области применения Python',
        'html': '''
<p>Python — это высокоуровневый, интерпретируемый язык программирования, созданный Гвидо ван Россумом в 1991 году. Название языка происходит от британского комедийного шоу «Monty Python's Flying Circus».</p>

<h3>Ключевые особенности</h3>
<ul>
  <li><strong>Простота и читаемость</strong> — синтаксис Python интуитивно понятен, код выглядит как псевдокод</li>
  <li><strong>Интерпретируемость</strong> — код выполняется построчно, не требует компиляции</li>
  <li><strong>Динамическая типизация</strong> — тип переменной определяется автоматически во время выполнения</li>
  <li><strong>Автоматическое управление памятью</strong> — сборщик мусора освобождает неиспользуемую память</li>
  <li><strong>Мультипарадигмальность</strong> — поддерживает процедурное, ООП и функциональное программирование</li>
  <li><strong>Обширная стандартная библиотека</strong> — батарейки входят в комплект (batteries included)</li>
</ul>

<h3>Области применения</h3>
<ul>
  <li><strong>Веб-разработка</strong> — Django, Flask, FastAPI</li>
  <li><strong>Тестирование</strong> — pytest, Selenium, Playwright</li>
  <li><strong>Data Science</strong> — NumPy, Pandas, Matplotlib</li>
  <li><strong>Машинное обучение</strong> — TensorFlow, PyTorch, scikit-learn</li>
  <li><strong>Автоматизация</strong> — скрипты, парсинг, CI/CD</li>
  <li><strong>DevOps</strong> — Ansible, Terraform (провайдеры)</li>
</ul>

<h3>Версии Python</h3>
<table>
  <tr><th>Версия</th><th>Год</th><th>Особенности</th></tr>
  <tr><td>2.x</td><td>2000</td><td>Классическая версия (завершена в 2020)</td></tr>
  <tr><td>3.6</td><td>2016</td><td>f-строки, type hints</td></tr>
  <tr><td>3.7</td><td>2018</td><td>dataclasses, asyncio improvements</td></tr>
  <tr><td>3.8</td><td>2019</td><td>walrus operator :=, positional-only params</td></tr>
  <tr><td>3.9</td><td>2020</td><td>dict union, type hint generics</td></tr>
  <tr><td>3.10</td><td>2021</td><td>match/case, union types X | Y</td></tr>
  <tr><td>3.11</td><td>2022</td><td>exception groups, улучшение скорости</td></tr>
  <tr><td>3.12</td><td>2023</td><td>f-строки с неограниченной вложенностью</td></tr>
  <tr><td>3.13</td><td>2024</td><td>JIT-компиляция, улучшенный интерактивный режим</td></tr>
</table>

<div class="info">Python 2.x официально завершил поддержку 1 января 2020. Все новые проекты следует писать на Python 3.x.</div>
'''
    },
    {
        'slug': 'setup',
        'title': 'Установка и настройка',
        'desc': 'Установка Python, настройка окружения, pip, venv',
        'html': '''
<h3>Установка Python</h3>

<h4>Windows</h4>
<ol>
  <li>Скачайте установщик с <a href="https://python.org">python.org</a></li>
  <li>Запустите .exe, обязательно отметьте «Add Python to PATH»</li>
  <li>Проверьте: <code>python --version</code></li>
</ol>

<h4>macOS / Linux</h4>
<pre><code># macOS (Homebrew)
brew install python

# Ubuntu/Debian
sudo apt install python3 python3-pip

# Проверка
python3 --version</code></pre>

<h3>Виртуальное окружение (venv)</h3>
<p>Виртуальное окружение изолирует зависимости проекта.</p>
<pre><code># Создание
python -m venv .venv

# Активация (Windows)
.venv\\Scripts\\activate

# Активация (macOS/Linux)
source .venv/bin/activate

# Выход
deactivate</code></pre>

<h3>pip — менеджер пакетов</h3>
<pre><code># Установка пакета
pip install requests

# Установка версии
pip install pytest==7.4.0

# Установка из requirements.txt
pip install -r requirements.txt

# Создание requirements.txt
pip freeze > requirements.txt

# Список установленных
pip list</code></pre>

<h3>Интерактивный режим</h3>
<p>Запустите <code>python</code> без аргументов — откроется REPL (Read-Eval-Print Loop).</p>
<pre><code>Python 3.11.9 (main, ...)
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello, World!")
Hello, World!
>>> 2 + 2
4</code></pre>

<h3>IDE и редакторы</h3>
<ul>
  <li><strong>VS Code</strong> — лёгкий редактор с расширениями Python, Pylance, Jupyter</li>
  <li><strong>PyCharm</strong> — мощная IDE от JetBrains (Community — бесплатно)</li>
  <li><strong>IDLE</strong> — базовый редактор в составе Python</li>
  <li><strong>Jupyter Notebook</strong> — интерактивные блокноты для data science</li>
</ul>
'''
    },
    {
        'slug': 'syntax',
        'title': 'Основы синтаксиса',
        'desc': 'Отступы, комментарии, операторы, соглашения об именовании',
        'html': '''
<h3>Отступы и блоки кода</h3>
<p>Python использует отступы (пробелы или табуляцию) для обозначения блоков кода. Стандарт — 4 пробела.</p>
<pre><code>if age >= 18:
    print("Совершеннолетний")
    can_vote = True
else:
    print("Несовершеннолетний")
    can_vote = False</code></pre>

<h3>Комментарии</h3>
<pre><code># Однострочный комментарий

# Многострочный комментарий
# Каждая строка начинается с #

"""
Docstring — многострочный комментарий,
используется для документации функций и классов
"""</code></pre>

<h3>Операторы</h3>
<table>
  <tr><th>Тип</th><th>Операторы</th></tr>
  <tr><td>Арифметические</td><td><code>+ - * / // % **</code></td></tr>
  <tr><td>Сравнения</td><td><code>== != &lt; &gt; &lt;= &gt;=</code></td></tr>
  <tr><td>Логические</td><td><code>and or not</code></td></tr>
  <tr><td>Присваивания</td><td><code>= += -= *= /= //= %= **=</code></td></tr>
  <tr><td>Побитовые</td><td><code>& | ^ ~ &lt;&lt; &gt;&gt;</code></td></tr>
  <tr><td>Принадлежности</td><td><code>in not in</code></td></tr>
  <tr><td>Тождества</td><td><code>is is not</code></td></tr>
</table>

<h3>Соглашения об именовании (PEP 8)</h3>
<table>
  <tr><th>Элемент</th><th>Стиль</th><th>Пример</th></tr>
  <tr><td>Переменные</td><td>snake_case</td><td><code>user_name</code></td></tr>
  <tr><td>Функции</td><td>snake_case</td><td><code>get_user()</code></td></tr>
  <tr><td>Классы</td><td>PascalCase</td><td><code>UserProfile</code></td></tr>
  <tr><td>Константы</td><td>UPPER_CASE</td><td><code>MAX_SIZE</code></td></tr>
  <tr><td>Приватные</td><td>_префикс</td><td><code>_internal()</code></td></tr>
  <tr><td>Магические</td><td>__dunder__</td><td><code>__init__</code></td></tr>
</table>

<h3>Ввод и вывод</h3>
<pre><code>name = input("Введите имя: ")
print(f"Привет, {name}!")

# Форматированный вывод
print(f"Число: {value:.2f}")
print(f"Шестнадцатеричное: {value:#x}")
print(f"Проценты: {percent:.1%}")</code></pre>
'''
    },
    {
        'slug': 'variables',
        'title': 'Переменные и типы данных',
        'desc': 'Объявление переменных, базовые типы, приведение типов',
        'html': '''
<h3>Переменные</h3>
<p>Python — язык с динамической типизацией. Тип переменной определяется автоматически.</p>
<pre><code>name = "Анна"        # str
age = 30              # int
height = 1.75         # float
is_student = False    # bool
hobbies = None        # NoneType

# Множественное присваивание
a, b, c = 1, 2, 3

# Одно значение — нескольким переменным
x = y = z = 0</code></pre>

<h3>Базовые типы данных</h3>
<table>
  <tr><th>Тип</th><th>Название</th><th>Пример</th><th>Изменяемый</th></tr>
  <tr><td><code>int</code></td><td>Целое число</td><td><code>42, -7, 0</code></td><td>Нет</td></tr>
  <tr><td><code>float</code></td><td>Число с плавающей точкой</td><td><code>3.14, -2.5, 1e10</code></td><td>Нет</td></tr>
  <tr><td><code>complex</code></td><td>Комплексное число</td><td><code>1+2j</code></td><td>Нет</td></tr>
  <tr><td><code>str</code></td><td>Строка</td><td><code>"hello", 'привет'</code></td><td>Нет</td></tr>
  <tr><td><code>bool</code></td><td>Логический</td><td><code>True, False</code></td><td>Нет</td></tr>
  <tr><td><code>list</code></td><td>Список</td><td><code>[1, 2, 3]</code></td><td>Да</td></tr>
  <tr><td><code>tuple</code></td><td>Кортеж</td><td><code>(1, 2, 3)</code></td><td>Нет</td></tr>
  <tr><td><code>dict</code></td><td>Словарь</td><td><code>{"key": "value"}</code></td><td>Да</td></tr>
  <tr><td><code>set</code></td><td>Множество</td><td><code>{1, 2, 3}</code></td><td>Да</td></tr>
  <tr><td><code>bytes</code></td><td>Байты</td><td><code>b"hello"</code></td><td>Нет</td></tr>
</table>

<h3>Проверка и приведение типов</h3>
<pre><code># Проверка типа
type(42)           # <class 'int'>
isinstance(42, int)  # True

# Приведение (кастинг)
int("123")         # 123
str(42)            # "42"
float("3.14")      # 3.14
bool(1)            # True
bool(0)            # False
bool("")           # False
bool([])           # False

# Что считается False:
# 0, 0.0, "", [], (), {}, set(), None, False</code></pre>

<h3>Ничего (None)</h3>
<pre><code>result = None
if result is None:
    print("Результата нет")</code></pre>

<div class="warn">Python различает <code>is</code> (проверка тождества) и <code>==</code> (проверка равенства). Для сравнения с None всегда используйте <code>is None</code>.</div>
'''
    },
    {
        'slug': 'numbers',
        'title': 'Числа и математика',
        'desc': 'Целые, дробные, комплексные числа, математические функции',
        'html': '''
<h3>Целые числа (int)</h3>
<p>Python поддерживает целые числа произвольной точности — не ограничены 32 или 64 битами.</p>
<pre><code>a = 42
b = -7
big = 10**100  # гугол — работает!

# Системы счисления
0b1010    # двоичная → 10
0o12      # восьмеричная → 10
0xFF      # шестнадцатеричная → 255

# Разделитель разрядов
million = 1_000_000  # удобно читать</code></pre>

<h3>Числа с плавающей точкой (float)</h3>
<pre><code>pi = 3.14159
small = 1.5e-10  # научная нотация
inf = float('inf')
nan = float('nan')

# Осторожно: погрешность вычислений
0.1 + 0.2  # 0.30000000000000004 (не 0.3!)</code></pre>

<div class="warn">Из-за двоичного представления float не могут точно хранить десятичные дроби. Для денег используйте <code>Decimal</code>.</div>

<h3>Математические операции</h3>
<pre><code>10 + 3   # 13
10 - 3   # 7
10 * 3   # 30
10 / 3   # 3.3333333333333335
10 // 3  # 3 (целочисленное деление)
10 % 3   # 1 (остаток)
10 ** 3  # 1000 (степень)

# Функции с округлением
round(3.14159, 2)   # 3.14
round(3.5)         # 4 (банковское округление!)
round(4.5)         # 4 (к чётному!)
int(3.9)           # 3 (отбрасывание дробной части)</code></pre>

<h3>Модуль math</h3>
<pre><code>import math

math.sqrt(16)       # 4.0
math.pow(2, 3)      # 8.0
math.pi             # 3.141592653589793
math.e              # 2.718281828459045
math.sin(math.pi/2) # 1.0
math.cos(0)         # 1.0
math.log(100, 10)   # 2.0
math.log(math.e)    # 1.0
math.ceil(3.2)      # 4
math.floor(3.8)     # 3
math.trunc(3.8)     # 3
math.factorial(5)   # 120
math.gcd(12, 8)     # 4
math.isfinite(x)    # проверка на бесконечность
math.isnan(x)       # проверка на NaN</code></pre>

<h3>Модуль random</h3>
<pre><code>import random

random.random()         # 0.0–1.0
random.randint(1, 6)    # 1–6 (кубик)
random.choice(['a','b','c'])  # случайный элемент
random.choices(pop, k=3)  # выборка с возвращением
random.sample(pop, k=3)   # выборка без возвращения
random.shuffle(lst)       # перемешать список
random.seed(42)           # фиксация случайности</code></pre>

<h3>Decimal — точные десятичные числа</h3>
<pre><code>from decimal import Decimal

Decimal('0.1') + Decimal('0.2')  # Decimal('0.3')
Decimal('10.00').quantize(Decimal('0.1'))  # округление</code></pre>

<h3>Fraction — дроби</h3>
<pre><code>from fractions import Fraction

Fraction(1, 3) + Fraction(1, 6)  # Fraction(1, 2)</code></pre>
'''
    },
    {
        'slug': 'strings',
        'title': 'Строки',
        'desc': 'Создание, методы, форматирование, f-строки',
        'html': '''
<h3>Создание строк</h3>
<pre><code>s1 = 'одинарные кавычки'
s2 = "двойные кавычки"
s3 = '\'\'\'многострочный\nтекст с одинарными\'\'\''
s4 = '"""многострочный\nтекст с двойными"""'</code></pre>

<h3>Экранирование и raw-строки</h3>
<pre><code># Экранирование
s = "Он сказал: \\"Привет!\\""
path = "C:\\\\Users\\\\name"

# Raw-строки (не обрабатывают \\)
path = r"C:\\Users\\name"
regex = r"\\d+\\.\\d+"</code></pre>

<h3>Индексы и срезы</h3>
<pre><code>s = "Python"
s[0]    # 'P'
s[-1]   # 'n'
s[0:3]  # 'Pyt' (0, 1, 2)
s[3:]   # 'hon'
s[:3]   # 'Pyt'
s[::2]  # 'Pto' (шаг 2)
s[::-1] # 'nohtyP' (разворот)

# Строки неизменяемы — нельзя s[0] = 'J'</code></pre>

<h3>Основные методы строк</h3>
<pre><code>s = "  Hello, World!  "

s.lower()         # '  hello, world!  '
s.upper()         # '  HELLO, WORLD!  '
s.strip()         # 'Hello, World!' (удалить пробелы)
s.lstrip()        # 'Hello, World!  '
s.rstrip()        # '  Hello, World!'
s.replace("World", "Python")  # '  Hello, Python!  '
s.split(", ")     # ['  Hello', ' World!  ']
s.split()         # ['Hello,', 'World!'] (по пробелам)
", ".join(["a","b","c"])  # 'a, b, c'
s.startswith("  He")   # True
s.endswith("!")        # True
s.find("World")        # 8 (индекс или -1)
s.count("l")           # 3
"42".zfill(5)          # '00042'
"hello".capitalize()   # 'Hello'
"hello world".title()  # 'Hello World'
"ABC".isupper()        # True
"abc".islower()        # True
"123".isdigit()        # True
"abc123".isalnum()     # True</code></pre>

<h3>Форматирование строк</h3>
<h4>f-строки (Python 3.6+)</h4>
<pre><code>name = "Анна"
age = 30
print(f"Меня зовут {name}, мне {age} лет")

# Выражения внутри
print(f"Через 5 лет мне будет {age + 5}")

# Форматирование чисел
pi = 3.14159265
print(f"π = {pi:.2f}")        # π = 3.14
print(f"π = {pi:.4f}")        # π = 3.1416
print(f"{1000000:,}")         # 1,000,000
print(f"{0.25:.1%}")          # 25.0%
print(f"{42:05d}")            # 00042
print(f"{255:#x}")            # 0xff
print(f"{255:b}")             # 11111111

# Выравнивание
print(f"|{'left':<10}|")      # |left      |
print(f"|{'right':>10}|")     # |     right|
print(f"|{'center':^10}|")    # |  center  |</code></pre>

<h4>Метод format</h4>
<pre><code>"{} — {}".format("Ключ", "Значение")
"{0} — {1}".format("Ключ", "Значение")
"{name}: {age}".format(name="Анна", age=30)</code></pre>

<h3>Полезные функции</h3>
<pre><code>len("Python")      # 6
ord('A')           # 65 (Unicode)
chr(65)            # 'A'
str([1, 2, 3])     # "[1, 2, 3]"
repr("hello")      # "'hello'" (для отладки)
ascii("привет")    # "'\\u043f\\u0440\\u0438\\u0432\\u0435\\u0442'"</code></pre>
'''
    },
    {
        'slug': 'lists',
        'title': 'Списки',
        'desc': 'Создание, методы, списковые включения, сортировка',
        'html': '''
<h3>Создание списков</h3>
<pre><code>empty = []
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4]]

# Из строки
list("abc")        # ['a', 'b', 'c']

# range — создание последовательности
list(range(5))     # [0, 1, 2, 3, 4]
list(range(2, 7))  # [2, 3, 4, 5, 6]
list(range(0, 10, 2))  # [0, 2, 4, 6, 8]</code></pre>

<h3>Доступ и срезы</h3>
<pre><code>nums = [10, 20, 30, 40, 50]
nums[0]     # 10
nums[-1]    # 50
nums[1:3]   # [20, 30]
nums[:3]    # [10, 20, 30]
nums[::2]   # [10, 30, 50]
nums[::-1]  # [50, 40, 30, 20, 10]

# Изменение по индексу
nums[0] = 100</code></pre>

<h3>Методы списков</h3>
<pre><code>lst = [1, 2, 3]

lst.append(4)         # [1, 2, 3, 4]
lst.insert(0, 0)      # [0, 1, 2, 3, 4]
lst.extend([5, 6])    # [0, 1, 2, 3, 4, 5, 6]
lst.remove(3)         # удалить первое вхождение 3
lst.pop()             # 6, lst → [0, 1, 2, 4, 5]
lst.pop(0)            # 0, lst → [1, 2, 4, 5]
lst.index(4)          # 2 (индекс элемента)
lst.count(2)          # 1 (количество вхождений)
lst.sort()            # сортировка (in-place)
lst.sort(reverse=True)# по убыванию
sorted(lst)           # новая сортированная копия
lst.reverse()         # разворот (in-place)
len(lst)              # длина
sum(lst)              # сумма (для чисел)
min(lst), max(lst)    # минимум/максимум
del lst[0]            # удалить по индексу
lst.clear()           # очистить список

# Копирование
copy = lst.copy()     # поверхностная копия
copy = lst[:]         # то же самое
deep = copy.deepcopy(lst)  # глубокая копия</code></pre>

<h3>Списковые включения (List Comprehension)</h3>
<pre><code># Квадраты чисел от 0 до 9
squares = [x**2 for x in range(10)]

# Чётные числа
evens = [x for x in range(20) if x % 2 == 0]

# Вложенный цикл
pairs = [(x, y) for x in [1,2] for y in [3,4]]
# [(1,3), (1,4), (2,3), (2,4)]

# С условием if-else
labels = ["чёт" if x % 2 == 0 else "нечёт" for x in range(5)]

# Трансформация строк
words = ["hello", "world"]
uppers = [w.upper() for w in words]  # ['HELLO', 'WORLD']

# Фильтрация с None
values = [1, None, 3, None, 5]
clean = [v for v in values if v is not None]  # [1, 3, 5]</code></pre>

<h3>Функции для работы со списками</h3>
<pre><code># all / any — все / хотя бы один
all([True, True, True])   # True
any([False, True, False]) # True
all([x > 0 for x in nums])  # все положительные?

# enumerate — индексы с элементами
for i, val in enumerate(["a", "b", "c"]):
    print(i, val)  # 0 a, 1 b, 2 c

# zip — параллельная итерация
names = ["Анна", "Борис"]
ages  = [30, 25]
for name, age in zip(names, ages):
    print(f"{name}: {age}")</code></pre>
'''
    },
    {
        'slug': 'tuples',
        'title': 'Кортежи',
        'desc': 'Неизменяемые последовательности, распаковка, именованные кортежи',
        'html': '''
<h3>Создание кортежей</h3>
<pre><code>empty = ()
single = (42,)     # запятая обязательна!
nums = (1, 2, 3)
without_parens = 1, 2, 3  # тоже кортеж

# Из списка
tuple([1, 2, 3])  # (1, 2, 3)</code></pre>

<h3>Особенности кортежей</h3>
<pre><code># Неизменяемость
t = (1, 2, 3)
# t[0] = 0  # TypeError!

# Но если внутри изменяемый объект — его можно изменить
t = (1, [2, 3])
t[1].append(4)  # (1, [2, 3, 4]) — работает!

# Индексы и срезы — как у списков
t[0], t[-1], t[1:3]

# Методы
t.count(2)  # количество вхождений
t.index(3)  # индекс первого вхождения</code></pre>

<h3>Распаковка кортежей</h3>
<pre><code># Базовая распаковка
point = (10, 20)
x, y = point  # x=10, y=20

# Замена значений
a, b = b, a  # swap!

# Звёздочка — остаток
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2,3,4]
first, *mid, last = (1,2,3,4)  # first=1, mid=[2,3], last=4

# Возврат нескольких значений из функции
def min_max(lst):
    return min(lst), max(lst)

low, high = min_max([3, 1, 4, 1, 5])</code></pre>

<h3>Именованные кортежи (namedtuple)</h3>
<pre><code>from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
p.x      # 10 (по имени)
p[0]     # 10 (по индексу)
x, y = p # распаковка

# С полями по умолчанию
Person = namedtuple('Person', ['name', 'age', 'city'])
p = Person('Анна', 30, 'Москва')

# _asdict — в словарь
p._asdict()  # {'name': 'Анна', 'age': 30, 'city': 'Москва'}

# _replace — новый экземпляр с изменением
p2 = p._replace(age=31)</code></pre>

<h3>Когда использовать кортежи</h3>
<ul>
  <li>Неизменяемые данные — безопасность от случайных изменений</li>
  <li>Ключи словаря (списки нельзя)</li>
  <li>Группировка связанных значений</li>
  <li>Более эффективны по памяти, чем списки</li>
</ul>
'''
    },
    {
        'slug': 'dicts',
        'title': 'Словари',
        'desc': 'Ключи-значения, методы, dict comprehension, defaultdict',
        'html': '''
<h3>Создание словарей</h3>
<pre><code>empty = {}
user = {"name": "Анна", "age": 30}
user = dict(name="Анна", age=30)  # ключи без кавычек
pairs = dict([("a", 1), ("b", 2)])

# Динамическое создание
keys = ["name", "age"]
values = ["Анна", 30]
user = dict(zip(keys, values))</code></pre>

<h3>Доступ к элементам</h3>
<pre><code>user = {"name": "Анна", "age": 30}

# Прямой доступ
user["name"]       # 'Анна'
user["city"]       # KeyError!

# Безопасный доступ с умолчанием
user.get("city")          # None
user.get("city", "Москва") # 'Москва'
user.get("name")          # 'Анна'

# setdefault — получить или создать
user.setdefault("city", "Москва")  # 'Москва' (добавлено в словарь)

# Проверка наличия
"name" in user    # True
"city" in user    # теперь True (setdefault)</code></pre>

<h3>Методы словарей</h3>
<pre><code>user = {"name": "Анна", "age": 30}

# Изменение
user["age"] = 31
user["city"] = "Москва"  # добавление нового ключа

# Обновление из другого словаря
user.update({"age": 32, "job": "QA"})

# Удаление
del user["city"]
user.pop("age")        # 30 (возвращает значение)
user.pop("city", None) # None (без ошибки)
user.clear()           # {}

# Ключи, значения, пары
user.keys()     # dict_keys(['name', 'age'])
user.values()   # dict_values(['Анна', 30])
user.items()    # dict_items([('name', 'Анна'), ('age', 30)])

# Итерация
for key, value in user.items():
    print(f"{key}: {value}")</code></pre>

<h3>Dict Comprehension</h3>
<pre><code># Квадраты чисел
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Фильтрация
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}

# Инверсия
original = {"a": 1, "b": 2}
inverted = {v: k for k, v in original.items()}

# Трансформация
users = {"alice": 30, "bob": 25}
adults = {name.title(): age for name, age in users.items() if age >= 18}</code></pre>

<h3>Слияние словарей (3.9+)</h3>
<pre><code>d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

merged = d1 | d2       # {'a': 1, 'b': 3, 'c': 4}
d1 |= d2               # обновление in-place</code></pre>

<h3>OrderedDict и defaultdict</h3>
<pre><code>from collections import OrderedDict, defaultdict

# OrderedDict — запоминает порядок вставки (с 3.7 dict тоже)
od = OrderedDict()
od["a"] = 1; od["b"] = 2

# defaultdict — значение по умолчанию для отсутствующих ключей
dd = defaultdict(int)
dd["a"] += 1  # {'a': 1} — автоматически создаётся 0

dd = defaultdict(list)
dd["items"].append(1)  # {'items': [1]}

# Counter — подсчёт элементов
from collections import Counter
cnt = Counter("abracadabra")
cnt  # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})</code></pre>
'''
    },
    {
        'slug': 'sets',
        'title': 'Множества',
        'desc': 'Создание, операции, frozenset, set comprehension',
        'html': '''
<h3>Создание множеств</h3>
<pre><code>empty = set()       # {}, но {} это словарь!
nums = {1, 2, 3, 2}  # {1, 2, 3} (дубликаты удалены)
from_list = set([1, 2, 2, 3])  # {1, 2, 3}
from_str = set("hello")  # {'h', 'e', 'l', 'o'}

# Генератор множества
squares = {x**2 for x in range(5)}  # {0, 1, 4, 9, 16}</code></pre>

<h3>Операции с множествами</h3>
<pre><code>a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Объединение
a | b           # {1, 2, 3, 4, 5, 6}
a.union(b)

# Пересечение
a & b           # {3, 4}
a.intersection(b)

# Разность
a - b           # {1, 2} (что в a, но не в b)
a.difference(b)
b - a           # {5, 6}

# Симметрическая разность
a ^ b           # {1, 2, 5, 6}
a.symmetric_difference(b)

# Подмножество / надмножество
{1, 2}.issubset(a)     # True
a.issuperset({1, 2})   # True
{1, 2}.isdisjoint({3}) # True (нет общих)</code></pre>

<h3>Методы множеств</h3>
<pre><code>s = {1, 2, 3}

s.add(4)              # {1, 2, 3, 4}
s.remove(4)           # KeyError если нет
s.discard(4)          # нет ошибки
s.pop()               # удалить случайный элемент
s.clear()             # {}

# Неизменяемое множество
fs = frozenset([1, 2, 3])  # можно как ключ словаря</code></pre>

<h3>Применение множеств</h3>
<pre><code># Удаление дубликатов
list(set([1, 2, 2, 3, 3, 3]))  # [1, 2, 3]

# Поиск общих элементов
common = set(list1) & set(list2)

# Поиск уникальных
unique = set(list1) - set(list2)

# Проверка уникальности
def has_duplicates(lst):
    return len(lst) != len(set(lst))</code></pre>
'''
    },
    {
        'slug': 'conditionals',
        'title': 'Условные операторы',
        'desc': 'if/elif/else, match/case, тернарный оператор',
        'html': '''
<h3>if / elif / else</h3>
<pre><code>age = 18

if age >= 18:
    print("Совершеннолетний")
elif age >= 14:
    print("Подросток")
else:
    print("Ребёнок")</code></pre>

<h3>Логические операторы</h3>
<pre><code># and — оба истинны
if age >= 18 and has_document:
    print("Доступ разрешён")

# or — хотя бы один истинен
if is_admin or is_owner:
    print("Есть права")

# not — отрицание
if not is_banned:
    print("Пользователь активен")

# Сравнения можно цепочкой
if 0 <= score <= 100:
    print("Корректный балл")

# Проверка на None / пустоту
if value is None: ...
if not value: ...  # 0, "", [], None, False → True</code></pre>

<h3>Тернарный оператор</h3>
<pre><code>age = 20
status = "совершеннолетний" if age >= 18 else "несовершеннолетний"

# Вложенный тернарник (не злоупотребляйте)
category = "ребёнок" if age < 14 else "подросток" if age < 18 else "взрослый"</code></pre>

<h3>match / case (Python 3.10+)</h3>
<pre><code>def http_status(code):
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"

# Связывание переменных
def process(point):
    match point:
        case (0, 0):
            print("Начало координат")
        case (x, 0):
            print(f"На оси X: {x}")
        case (0, y):
            print(f"На оси Y: {y}")
        case (x, y):
            print(f"Точка: ({x}, {y})")

# С условиями (guard)
def classify(value):
    match value:
        case x if x < 0:
            return "Отрицательное"
        case x if x == 0:
            return "Ноль"
        case x if x > 0:
            return "Положительное"</code></pre>

<h3>Короткое замыкание (short-circuit)</h3>
<pre><code># Python вычисляет and/or слева направо
# and: если первое False — второе не вычисляется
# or:  если первое True — второе не вычисляется

# Часто используется для значений по умолчанию
name = input_name or "Гость"  # если input_name пусто → "Гость"
</code></pre>
'''
    },
    {
        'slug': 'loops',
        'title': 'Циклы',
        'desc': 'for, while, break/continue, enumerate, генераторы',
        'html': '''
<h3>Цикл for</h3>
<pre><code># По списку
for item in [1, 2, 3]:
    print(item)

# По строке
for char in "Python":
    print(char)

# По range
for i in range(5):
    print(i)

# По словарю
for key in user: ...
for val in user.values(): ...
for key, val in user.items(): ...

# По нескольким последовательностям
for name, age in zip(names, ages):
    print(f"{name}: {age}")

# С индексом
for i, val in enumerate(["a", "b", "c"]):
    print(i, val)</code></pre>

<h3>Цикл while</h3>
<pre><code>i = 0
while i < 5:
    print(i)
    i += 1

# Бесконечный цикл с break
while True:
    cmd = input("> ")
    if cmd == "exit":
        break
    if cmd == "help":
        continue  # к следующей итерации
    print(f"Вы ввели: {cmd}")</code></pre>

<h3>break / continue / else</h3>
<pre><code># break — выход из цикла
for i in range(10):
    if i == 5:
        break
    print(i)  # 0 1 2 3 4

# continue — переход к следующей итерации
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0 1 3 4

# else в цикле — выполняется, если break не сработал
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            break
    else:
        print(n, "простое число")</code></pre>

<h3>Генераторы списков (повторение)</h3>
<pre><code># Базовая форма
[expr for item in iterable]

# С условием
[expr for item in iterable if condition]

# С if-else
[expr_if_true if condition else expr_if_false for item in iterable]

# Примеры
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
labels = ["чёт" if x % 2 == 0 else "нечёт" for x in range(5)]</code></pre>

<h3>Функция range</h3>
<pre><code>range(stop)       # 0, 1, ..., stop-1
range(start, stop)  # start, ..., stop-1
range(start, stop, step)  # с шагом

list(range(5))          # [0, 1, 2, 3, 4]
list(range(2, 7))       # [2, 3, 4, 5, 6]
list(range(0, 10, 2))   # [0, 2, 4, 6, 8]
list(range(5, 0, -1))   # [5, 4, 3, 2, 1]</code></pre>

<h3>Итерация по нескольким коллекциям</h3>
<pre><code># zip — параллельная
for a, b in zip(list1, list2):
    print(a, b)

# enumerate — с индексом
for idx, val in enumerate(collection):
    print(idx, val)

# reversed — обратный порядок
for item in reversed(lst):
    print(item)

# sorted — сортированный
for item in sorted(lst):
    print(item)</code></pre>
'''
    },
    {
        'slug': 'functions',
        'title': 'Функции',
        'desc': 'Определение, параметры, return, lambda, декораторы',
        'html': '''
<h3>Определение функций</h3>
<pre><code>def greet(name):
    """Документация функции."""
    return f"Привет, {name}!"

# Вызов
result = greet("Анна")

# Функция без return возвращает None
def log(msg):
    print(f"[LOG] {msg}")</code></pre>

<h3>Параметры функций</h3>
<pre><code># Позиционные
def add(a, b):
    return a + b
add(2, 3)

# Именованные
add(b=3, a=2)

# Значения по умолчанию
def greet(name, greeting="Привет"):
    return f"{greeting}, {name}!"

# *args — произвольное число позиционных
def sum_all(*args):
    return sum(args)
sum_all(1, 2, 3)  # 6

# **kwargs — произвольное число именованных
def print_kwargs(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")
print_kwargs(name="Анна", age=30)

# Все вместе: def func(a, b, *args, c=1, **kwargs)</code></pre>

<h3>Параметры только по имени (keyword-only)</h3>
<pre><code># После * — только именованные
def configure(*, host, port):
    print(f"{host}:{port}")
configure(host="localhost", port=8080)
# configure("localhost", 8080)  # TypeError!

# С после *args
def func(a, b, *args, verbose=False): ...</code></pre>

<h3>Аннотации типов (type hints)</h3>
<pre><code>def add(a: int, b: int) -> int:
    return a + b

def get_user(name: str) -> dict | None:
    ...

from typing import List, Optional
def process(items: List[int]) -> Optional[str]: ...</code></pre>

<h3>Лямбда-функции</h3>
<pre><code># Анонимные функции
square = lambda x: x**2
square(5)  # 25

# Сортировка с ключом
pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
pairs.sort(key=lambda x: x[1])  # по строке

# filter / map / sorted
nums = [1, 2, 3, 4, 5]
list(filter(lambda x: x > 3, nums))  # [4, 5]
list(map(lambda x: x*2, nums))       # [2, 4, 6, 8, 10]</code></pre>

<h3>Декораторы</h3>
<pre><code>def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-start:.3f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)

slow_function()  # slow_function: 1.002s

# Декоратор с параметрами
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")</code></pre>

<h3>Замыкания (closures)</h3>
<pre><code>def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
c()  # 1
c()  # 2
c()  # 3</code></pre>

<h3>functools — полезные декораторы</h3>
<pre><code>from functools import lru_cache, partial

# Кэширование
@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# Частичное применение
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
square(5)  # 25</code></pre>
'''
    },
    {
        'slug': 'modules',
        'title': 'Модули и пакеты',
        'desc': 'Импорт, создание модулей, __name__, пакеты',
        'html': '''
<h3>Импорт модулей</h3>
<pre><code># Полный импорт
import math
math.sqrt(16)

# Импорт с псевдонимом
import numpy as np
np.array([1, 2, 3])

# Импорт конкретных функций
from math import sqrt, pi
sqrt(16)  # без префикса

# Импорт всех (не рекомендуется)
from math import *</code></pre>

<h3>Создание модуля</h3>
<p>Любой <code>.py</code> файл — это модуль.</p>
<pre><code># utils.py
def greet(name):
    return f"Привет, {name}"

PI = 3.14159

# main.py
import utils
print(utils.greet("Анна"))
print(utils.PI)</code></pre>

<h3>__name__ и __main__</h3>
<pre><code># utils.py
def greet(name):
    return f"Привет, {name}"

if __name__ == "__main__":
    # Этот код выполнится только при запуске файла
    print(greet("Мир"))</code></pre>

<h3>Пакеты</h3>
<p>Пакет — это директория с файлом <code>__init__.py</code>.</p>
<pre><code>my_package/
├── __init__.py
├── module_a.py
└── module_b.py

# __init__.py
from .module_a import func_a
from .module_b import func_b

# Использование
import my_package
my_package.func_a()

from my_package import func_b</code></pre>

<h3>Стандартные модули (часто используемые)</h3>
<table>
  <tr><th>Модуль</th><th>Назначение</th></tr>
  <tr><td>os</td><td>Работа с ОС, пути, переменные окружения</td></tr>
  <tr><td>sys</td><td>Системные параметры, аргументы командной строки</td></tr>
  <tr><td>json</td><td>Работа с JSON</td></tr>
  <tr><td>re</td><td>Регулярные выражения</td></tr>
  <tr><td>datetime</td><td>Дата и время</td></tr>
  <tr><td>math</td><td>Математические функции</td></tr>
  <tr><td>random</td><td>Случайные числа</td></tr>
  <tr><td>pathlib</td><td>Работа с путями (объектно)</td></tr>
  <tr><td>collections</td><td>Специализированные коллекции</td></tr>
  <tr><td>itertools</td><td>Инструменты для итераторов</td></tr>
  <tr><td>functools</td><td>Функциональное программирование</td></tr>
  <tr><td>logging</td><td>Логирование</td></tr>
  <tr><td>argparse</td><td>Парсинг аргументов командной строки</td></tr>
</table>
'''
    },
    {
        'slug': 'exceptions',
        'title': 'Обработка исключений',
        'desc': 'try/except, finally, raise, пользовательские исключения',
        'html': '''
<h3>Базовый try/except</h3>
<pre><code>try:
    result = 10 / 0
except ZeroDivisionError:
    print("Деление на ноль!")

try:
    num = int(input("Введите число: "))
except ValueError:
    print("Это не число!")</code></pre>

<h3>Несколько except</h3>
<pre><code>try:
    value = risky_operation()
except ValueError:
    print("Неверное значение")
except (TypeError, KeyError):
    print("Ошибка типа или ключа")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
else:
    print(f"Всё ок: {value}")
finally:
    print("Выполняется всегда")</code></pre>

<h3>raise — выброс исключения</h3>
<pre><code>def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль")
    return a / b

# Переброс
try:
    divide(10, 0)
except ValueError:
    print("Ошибка")
    raise  # перебросить дальше</code></pre>

<h3>Пользовательские исключения</h3>
<pre><code>class CustomError(Exception):
    """Базовое исключение приложения."""
    pass

class ValidationError(CustomError):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

raise ValidationError("email", "Неверный формат")</code></pre>

<h3>Иерархия исключений</h3>
<pre><code>BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ValueError
    ├── TypeError
    ├── OSError
    │   └── FileNotFoundError
    ├── AttributeError
    └── ...</code></pre>

<h3>Exception Groups (Python 3.11+)</h3>
<pre><code>def validate(data):
    errors = []
    if not data.get("name"):
        errors.append(ValueError("name required"))
    if not data.get("age"):
        errors.append(ValueError("age required"))
    if errors:
        raise ExceptionGroup("Validation failed", errors)

try:
    validate({"name": ""})
except* ValueError as eg:
    for e in eg.exceptions:
        print(e)</code></pre>

<h3>Контекстный менеджер try/except/finally</h3>
<pre><code># try — опасный код
# except — обработка ошибки
# else — если ошибки не было
# finally — в любом случае

try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError:
    print("Файл не найден")
else:
    print(f"Прочитано {len(data)} символов")
finally:
    file.close()</code></pre>
'''
    },
    {
        'slug': 'files',
        'title': 'Работа с файлами',
        'desc': 'open, чтение/запись, with, pathlib, форматы',
        'html': '''
<h3>Открытие файлов</h3>
<pre><code># Режимы: r (чтение), w (запись), a (добавление)
# r+ (чтение+запись), w+ (чтение+запись с очисткой)

# Явное закрытие (старый стиль)
file = open("data.txt", "r", encoding="utf-8")
data = file.read()
file.close()

# Контекстный менеджер (рекомендуется)
with open("data.txt", "r", encoding="utf-8") as f:
    data = f.read()  # файл закроется автоматически</code></pre>

<h3>Чтение файлов</h3>
<pre><code>with open("data.txt", encoding="utf-8") as f:
    content = f.read()          # весь файл в строку
    lines = f.readlines()       # список строк
    line = f.readline()         # одна строка

# Итерация по строкам (эффективно для больших файлов)
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())</code></pre>

<h3>Запись файлов</h3>
<pre><code>with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Строка 1\\n")
    f.write("Строка 2\\n")

# Дозапись
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Строка 3\\n")

# Список строк
lines = ["a", "b", "c"]
with open("output.txt", "w") as f:
    f.writelines(line + "\\n" for line in lines)</code></pre>

<h3>pathlib — современный подход</h3>
<pre><code>from pathlib import Path

path = Path("data") / "subdir" / "file.txt"

# Создание/проверка
path.exists()         # True/False
path.is_file()        # True/False
path.is_dir()         # True/False
path.mkdir(parents=True, exist_ok=True)  # создать директорию

# Чтение/запись
content = path.read_text(encoding="utf-8")
path.write_text("Новый текст", encoding="utf-8")
data = path.read_bytes()  # бинарные

# Работа с путями
path.name              # 'file.txt'
path.stem              # 'file'
path.suffix            # '.txt'
path.parent            # Path('data/subdir')
path.absolute()        # полный путь

# Список файлов
for f in Path(".").iterdir():
    print(f.name)

for py in Path(".").glob("*.py"):
    print(py)

for all_py in Path(".").rglob("*.py"):
    print(all_py)</code></pre>

<h3>CSV</h3>
<pre><code>import csv

# Чтение
with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Чтение в словари
with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])

# Запись
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Анна", 30])

# Запись словарей
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Анна", "age": 30})</code></pre>

<h3>JSON</h3>
<pre><code>import json

data = {"name": "Анна", "age": 30, "hobbies": ["чтение", "бег"]}

# Запись
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Чтение
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)

# В строку
json_str = json.dumps(data, ensure_ascii=False, indent=2)
data_again = json.loads(json_str)</code></pre>
'''
    },
    {
        'slug': 'oop',
        'title': 'ООП (Объектно-ориентированное программирование)',
        'desc': 'Классы, наследование, магические методы, dataclasses',
        'html': '''
<h3>Классы и объекты</h3>
<pre><code>class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Привет, я {self.name}"

user = User("Анна", 30)
print(user.greet())  # Привет, я Анна</code></pre>

<h3>Методы класса</h3>
<pre><code>class Counter:
    count = 0  # атрибут класса

    @classmethod
    def increment(cls):
        cls.count += 1

    @staticmethod
    def info():
        return "Счётчик"

    def instance_method(self):
        return self.count

Counter.increment()
Counter.info()</code></pre>

<h3>Свойства (property)</h3>
<pre><code>class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name.upper()

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @name.deleter
    def name(self):
        print("Удаление имени")
        del self._name

p = Person("Анна")
print(p.name)   # АННА (геттер)
p.name = "Ольга"  # сеттер</code></pre>

<h3>Наследование</h3>
<pre><code>class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return f"{self.name}: Гав!"

class Cat(Animal):
    def speak(self):
        return f"{self.name}: Мяу!"

# super() — вызов родительского метода
class Developer:
    def __init__(self, name, lang):
        self.name = name
        self.lang = lang

class SeniorDeveloper(Developer):
    def __init__(self, name, lang, years):
        super().__init__(name, lang)
        self.years = years</code></pre>

<h3>Магические методы (dunder)</h3>
<pre><code>class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):     # repr()
        return f"Vector({self.x}, {self.y})"

    def __str__(self):      # str(), print()
        return f"({self.x}, {self.y})"

    def __add__(self, other):  # +
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):   # ==
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):   # < (для сортировки)
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

    def __len__(self):         # len()
        return int((self.x**2 + self.y**2) ** 0.5)

    def __getitem__(self, i):  # индексация
        return (self.x, self.y)[i]

v1 = Vector(2, 3)
v2 = Vector(1, 4)
print(v1 + v2)  # (3, 7)
print(v1 == Vector(2, 3))  # True</code></pre>

<h3>dataclasses (Python 3.7+)</h3>
<pre><code>from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int = 0
    emails: list = field(default_factory=list)
    is_active: bool = True

user = User("Анна", 30)
print(user)            # User(name='Анна', age=30, emails=[], is_active=True)
print(user == User("Анна", 30))  # True

# Frozen (неизменяемый)
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int</code></pre>

<h3>Абстрактные классы</h3>
<pre><code>from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2</code></pre>
'''
    },
    {
        'slug': 'decorators',
        'title': 'Декораторы и замыкания',
        'desc': 'Декораторы функций, functools.wraps, декораторы классов',
        'html': '''
<h3>Декораторы функций</h3>
<pre><code>import functools
import time

def timer(func):
    @functools.wraps(func)  # сохраняет имя и документацию
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} заняла {elapsed:.3f}s")
        return result
    return wrapper

@timer
def slow_add(a, b):
    """Складывает два числа."""
    time.sleep(0.5)
    return a + b

slow_add(1, 2)  # slow_add заняла 0.501s
print(slow_add.__name__)  # slow_add (без wraps было бы 'wrapper')</code></pre>

<h3>Декораторы с параметрами</h3>
<pre><code>def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(message):
    print(message)

say("Привет!")  # Привет! × 3</code></pre>

<h3>Декораторы классов</h3>
<pre><code>def add_repr(cls):
    def __repr__(self):
        items = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({items})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Анна", 30)
print(user)  # User(name=Анна, age=30)</code></pre>

<h3>Декоратор для методов класса</h3>
<pre><code>def log_call(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        print(f"Вызов {method.__name__}")
        return method(self, *args, **kwargs)
    return wrapper

class Service:
    @log_call
    def process(self, data):
        return f"Обработка: {data}"</code></pre>

<h3>Замыкания (closures)</h3>
<pre><code>def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15</code></pre>

<h3>functools.partial — частичное применение</h3>
<pre><code>from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)

print(square(5))  # 25
print(cube(5))    # 125</code></pre>
'''
    },
    {
        'slug': 'generators',
        'title': 'Генераторы и итераторы',
        'desc': 'yield, генераторные выражения, itertools',
        'html': '''
<h3>Генераторные функции</h3>
<pre><code>def count_up_to(n):
    i = 0
    while i < n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)  # 0, 1, 2, 3, 4

# Генераторы — ленивые: значения создаются на лету</code></pre>

<h3>Генераторные выражения</h3>
<pre><code># Круглые скобки — генератор (ленивый)
squares = (x**2 for x in range(10))
print(squares)  # <generator object ...>
print(list(squares))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Квадратные — список (все сразу в памяти)
list_squares = [x**2 for x in range(10)]

# Эффективно для больших данных
sum(x**2 for x in range(1000000))  # без создания списка</code></pre>

<h3>Stateful-генераторы</h3>
<pre><code>def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
[next(fib) for _ in range(10)]  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]</code></pre>

<h3>yield from — делегирование</h3>
<pre><code>def chain(*iterables):
    for it in iterables:
        yield from it

list(chain([1,2], [3,4]))  # [1, 2, 3, 4]</code></pre>

<h3>Итераторы вручную</h3>
<pre><code>class Squares:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        result = self.i ** 2
        self.i += 1
        return result

list(Squares(5))  # [0, 1, 4, 9, 16]</code></pre>

<h3>itertools — инструменты для итераторов</h3>
<pre><code>import itertools

# Бесконечные
itertools.count(10, 2)    # 10, 12, 14, ...
itertools.cycle("ABC")    # A, B, C, A, B, C, ...
itertools.repeat(42, 3)   # 42, 42, 42

# Комбинаторика
itertools.permutations("ABC", 2)  # AB, AC, BA, BC, CA, CB
itertools.combinations("ABC", 2)  # AB, AC, BC
itertools.product("AB", "12")     # A1, A2, B1, B2

# Полезные
itertools.chain([1,2], [3,4])     # 1, 2, 3, 4
itertools.zip_longest([1,2], [3,4,5])  # (1,3), (2,4), (None,5)
itertools.islice(range(100), 10)  # первые 10
itertools.groupby(data, key_func) # группировка</code></pre>

<h3>Генераторы vs списки: память</h3>
<pre><code>import sys

list_comp = [x for x in range(1000000)]
gen_expr = (x for x in range(1000000))

sys.getsizeof(list_comp)  # ~8 MB (все элементы в памяти)
sys.getsizeof(gen_expr)   # ~200 bytes (ленивый)</code></pre>
'''
    },
    {
        'slug': 'stdlib',
        'title': 'Стандартная библиотека',
        'desc': 'os, sys, collections, itertools, logging, argparse',
        'html': '''
<h3>os — операционная система</h3>
<pre><code>import os

os.getcwd()          # текущая директория
os.chdir("..")       # сменить директорию
os.listdir(".")      # список файлов
os.mkdir("new_dir")  # создать директорию
os.remove("file")    # удалить файл
os.rename("old", "new")  # переименовать
os.environ.get("PATH")   # переменная окружения
os.path.join("dir", "file")  # правильный путь
os.path.exists("path")   # проверка существования
os.path.isfile("path")   # файл?
os.path.isdir("path")    # директория?
os.path.splitext("file.txt")  # ('file', '.txt')</code></pre>

<h3>sys — системные параметры</h3>
<pre><code>import sys

sys.version          # версия Python
sys.platform         # платформа ('win32', 'linux', 'darwin')
sys.argv             # аргументы командной строки
sys.path             # пути поиска модулей
sys.exit(0)          # выход с кодом
sys.modules          # загруженные модули
sys.getsizeof(obj)   # размер объекта в байтах</code></pre>

<h3>collections — дополнительные коллекции</h3>
<pre><code>from collections import defaultdict, Counter, deque, OrderedDict

# defaultdict — значение по умолчанию
dd = defaultdict(list)
dd["key"].append(1)

# Counter — подсчёт
cnt = Counter("abracadabra")
cnt.most_common(2)  # [('a', 5), ('b', 2)]

# deque — двусторонняя очередь
dq = deque([1, 2, 3])
dq.append(4); dq.appendleft(0)
dq.pop(); dq.popleft()

# namedtuple — кортеж с именами
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])</code></pre>

<h3>itertools — работа с итераторами</h3>
<pre><code>import itertools

# Бесконечные
itertools.count(10, 2)    # 10, 12, 14, ...
itertools.cycle("ABC")    # A, B, C, A, ...

# Комбинаторика
itertools.product("AB", "12")     # все пары
itertools.permutations("ABC", 2)  # все перестановки
itertools.combinations("ABC", 2)  # все сочетания

# Группировка
itertools.groupby(sorted(data), key=func)</code></pre>

<h3>logging — логирование</h3>
<pre><code>import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.debug("Отладка")
logging.info("Информация")
logging.warning("Предупреждение")
logging.error("Ошибка")
logging.critical("Критическая ошибка")

# Логирование в файл
file_handler = logging.FileHandler("app.log")
logger = logging.getLogger("my_app")
logger.addHandler(file_handler)</code></pre>

<h3>argparse — аргументы командной строки</h3>
<pre><code>import argparse

parser = argparse.ArgumentParser(description="Описание")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-o", "--output", default="out.txt")
parser.add_argument("files", nargs="+")

args = parser.parse_args()
print(args.verbose, args.output, args.files)

# Запуск: python script.py -v -o result.txt file1.txt file2.txt</code></pre>

<h3>copy — копирование объектов</h3>
<pre><code>import copy

original = [1, [2, 3], 4]
shallow = copy.copy(original)     # поверхностная
deep = copy.deepcopy(original)    # глубокая

# Поверхностная: вложенные объекты разделяются
# Глубокая: полная независимая копия</code></pre>

<h3>hashlib — хеширование</h3>
<pre><code>import hashlib

hashlib.md5(b"data").hexdigest()
hashlib.sha256(b"data").hexdigest()
hashlib.sha256("пароль".encode()).hexdigest()</code></pre>
'''
    },
    {
        'slug': 'datetime',
        'title': 'Дата и время',
        'desc': 'datetime, date, time, timedelta, strftime/strptime',
        'html': '''
<h3>datetime — основные типы</h3>
<pre><code>from datetime import datetime, date, time, timedelta

# Текущие дата/время
now = datetime.now()          # 2026-06-17 14:30:00.123456
today = date.today()          # 2026-06-17
current_time = datetime.now().time()  # 14:30:00.123456

# Создание вручную
dt = datetime(2026, 6, 17, 14, 30, 0)
d = date(2026, 6, 17)
t = time(14, 30, 0)</code></pre>

<h3>Форматирование и парсинг</h3>
<pre><code># datetime → строка (strftime)
now = datetime.now()
now.strftime("%Y-%m-%d")              # 2026-06-17
now.strftime("%d.%m.%Y %H:%M")        # 17.06.2026 14:30
now.strftime("%A, %d %B %Y")          # Wednesday, 17 June 2026
now.strftime("%Y-%m-%dT%H:%M:%S")     # 2026-06-17T14:30:00 (ISO)

# Строка → datetime (strptime)
dt = datetime.strptime("2026-06-17", "%Y-%m-%d")
dt = datetime.fromisoformat("2026-06-17T14:30:00")  # 3.7+</code></pre>

<h3>Коды форматирования</h3>
<table>
  <tr><th>Код</th><th>Значение</th><th>Пример</th></tr>
  <tr><td>%Y</td><td>Год (4 цифры)</td><td>2026</td></tr>
  <tr><td>%m</td><td>Месяц (01–12)</td><td>06</td></tr>
  <tr><td>%d</td><td>День (01–31)</td><td>17</td></tr>
  <tr><td>%H</td><td>Часы (00–23)</td><td>14</td></tr>
  <tr><td>%M</td><td>Минуты (00–59)</td><td>30</td></tr>
  <tr><td>%S</td><td>Секунды (00–59)</td><td>00</td></tr>
  <tr><td>%A</td><td>День недели (полный)</td><td>Wednesday</td></tr>
  <tr><td>%B</td><td>Месяц (полный)</td><td>June</td></tr>
</table>

<h3>timedelta — разница во времени</h3>
<pre><code>from datetime import timedelta

delta = timedelta(days=7, hours=3)
print(delta)  # 7 days, 3:00:00

# Арифметика
now = datetime.now()
next_week = now + timedelta(weeks=1)
yesterday = now - timedelta(days=1)
deadline = now + timedelta(hours=24)

# Между датами
start = datetime(2026, 1, 1)
end = datetime(2026, 12, 31)
diff = end - start  # timedelta(days=363)

diff.days            # 363
diff.total_seconds() # 31363200.0</code></pre>

<h3>timezone — часовые пояса</h3>
<pre><code>from datetime import timezone, timedelta

# UTC
utc_now = datetime.now(timezone.utc)

# Смещение
msk = timezone(timedelta(hours=3))
moscow_now = datetime.now(msk)

# pip install pytz — для полной поддержки поясов
import pytz
tz = pytz.timezone("Europe/Moscow")
moscow = datetime.now(tz)</code></pre>

<h3>time — низкоуровневое время</h3>
<pre><code>import time

# Таймер
start = time.time()
# ... код ...
elapsed = time.time() - start
print(f"{elapsed:.3f}s")

# Ожидание
time.sleep(2)   # 2 секунды

# Структурированное время
time.localtime()  # time.struct_time
time.strftime("%Y-%m-%d", time.localtime())</code></pre>
'''
    },
    {
        'slug': 'regex',
        'title': 'Регулярные выражения',
        'desc': 'Поиск, замена, группы, флаги, re.compile',
        'html': '''
<h3>Модуль re</h3>
<pre><code>import re

text = "Мой email: user@example.com"

# Поиск первого совпадения
match = re.search(r"\\w+@\\w+\\.\\w+", text)
if match:
    print(match.group())  # user@example.com

# Все совпадения
emails = re.findall(r"\\w+@\\w+\\.\\w+", text)

# Замена
result = re.sub(r"\\d+", "NUMBER", "Цена: 100 рублей")
# 'Цена: NUMBER рублей'</code></pre>

<h3>Специальные символы</h3>
<table>
  <tr><th>Символ</th><th>Значение</th></tr>
  <tr><td><code>.</code></td><td>Любой символ, кроме новой строки</td></tr>
  <tr><td><code>\\d</code></td><td>Цифра (0–9)</td></tr>
  <tr><td><code>\\w</code></td><td>Буква, цифра, подчёркивание</td></tr>
  <tr><td><code>\\s</code></td><td>Пробельный символ</td></tr>
  <tr><td><code>\\D</code></td><td>Не цифра</td></tr>
  <tr><td><code>\\W</code></td><td>Не буква/цифра</td></tr>
  <tr><td><code>\\S</code></td><td>Не пробельный</td></tr>
  <tr><td><code>^</code></td><td>Начало строки</td></tr>
  <tr><td><code>$</code></td><td>Конец строки</td></tr>
  <tr><td><code>\\b</code></td><td>Граница слова</td></tr>
</table>

<h3>Квантификаторы</h3>
<table>
  <tr><th>Символ</th><th>Значение</th></tr>
  <tr><td><code>*</code></td><td>0 и более</td></tr>
  <tr><td><code>+</code></td><td>1 и более</td></tr>
  <tr><td><code>?</code></td><td>0 или 1</td></tr>
  <tr><td><code>{3}</code></td><td>Ровно 3</td></tr>
  <tr><td><code>{2,5}</code></td><td>От 2 до 5</td></tr>
  <tr><td><code>{2,}</code></td><td>2 и более</td></tr>
</table>

<h3>Группы</h3>
<pre><code>text = "Иван: 30 лет"
match = re.search(r"(\\w+): (\\d+)", text)
if match:
    print(match.group(0))   # 'Иван: 30' (всё совпадение)
    print(match.group(1))   # 'Иван' (первая группа)
    print(match.group(2))   # '30' (вторая группа)
    print(match.groups())   # ('Иван', '30')

# Именованные группы
match = re.search(r"(?P<name>\\w+): (?P<age>\\d+)", text)
print(match.group("name"))  # 'Иван'</code></pre>

<h3>Флаги</h3>
<pre><code>re.IGNORECASE / re.I  — регистронезависимый
re.MULTILINE  / re.M — ^ и $ работают по строкам
re.DOTALL     / re.S — точка включает \\n
re.VERBOSE    / re.X — комментарии в паттерне

re.search(r"python", text, re.IGNORECASE)

# VERBOSE — паттерн с комментариями
pattern = re.compile(r"""
    \\b        # граница слова
    \\d{3}     # код
    -\\d{2}-  # первая часть
    \\d{2}    # вторая часть
    \\b
""", re.VERBOSE)</code></pre>

<h3>Компиляция регулярных выражений</h3>
<pre><code># Без компиляции (каждый раз компилируется заново)
for text in texts:
    re.search(r"сложный\\s+паттерн", text)

# С компиляцией (быстрее в цикле)
pattern = re.compile(r"сложный\\s+паттерн")
for text in texts:
    pattern.search(text)</code></pre>

<h3>Примеры</h3>
<pre><code># Email
r"[\\w.+-]+@[\\w-]+\\.[\\w.]+"

# URL
r"https?://[\\w./-]+"

# Телефон (Россия)
r"\\+7\\d{10}|8\\d{10}"

# IP-адрес
r"\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}"

# Дата ДД.ММ.ГГГГ
r"\\d{2}\\.\\d{2}\\.\\d{4}"

# HTML-тег
r"<[^>]+>"

# Все цифры в строке
re.findall(r"\\d+", text)

# Разделить строку по нескольким разделителям
re.split(r"[,\\;\\s]+", text)</code></pre>
'''
    },
    {
        'slug': 'json',
        'title': 'JSON и сериализация',
        'desc': 'json.load/dump, pickle, работа с форматами данных',
        'html': '''
<h3>JSON — основы</h3>
<pre><code>import json

data = {
    "name": "Анна",
    "age": 30,
    "is_student": False,
    "hobbies": ["чтение", "бег"],
    "address": None
}

# Парсинг строки
json_str = '{"name": "Анна", "age": 30}'
parsed = json.loads(json_str)

# В строку
json_str = json.dumps(data, ensure_ascii=False, indent=2)

# Чтение из файла
with open("data.json", encoding="utf-8") as f:
    data = json.load(f)

# Запись в файл
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)</code></pre>

<h3>Маппинг типов JSON ↔ Python</h3>
<table>
  <tr><th>JSON</th><th>Python</th></tr>
  <tr><td>object</td><td>dict</td></tr>
  <tr><td>array</td><td>list</td></tr>
  <tr><td>string</td><td>str</td></tr>
  <tr><td>number (int)</td><td>int</td></tr>
  <tr><td>number (real)</td><td>float</td></tr>
  <tr><td>true/false</td><td>True/False</td></tr>
  <tr><td>null</td><td>None</td></tr>
</table>

<h3>Сериализация объектов</h3>
<pre><code>from dataclasses import dataclass, asdict
import json

@dataclass
class User:
    name: str
    age: int

user = User("Анна", 30)
json.dumps(asdict(user), ensure_ascii=False)

# Кастомный сериализатор
class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

json.dumps(user, cls=UserEncoder, ensure_ascii=False)</code></pre>

<h3>pickle — бинарная сериализация</h3>
<pre><code>import pickle

data = {"key": [1, 2, 3], "nested": {"a": 1}}

# Сохранение в файл
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Загрузка из файла
with open("data.pkl", "rb") as f:
    loaded = pickle.load(f)

# Внимание: pickle небезопасен! Не загружайте данные из ненадёжных источников.</code></pre>

<h3>Другие форматы</h3>
<pre><code># YAML — нужен PyYAML
import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# TOML — нужен tomllib (3.11+) или tomli
import tomllib
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# CSV
import csv
with open("data.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)</code></pre>

<h3>Полезные приёмы</h3>
<pre><code># Сортировка ключей
json.dumps(data, sort_keys=True)

# Компактный вывод
json.dumps(data, separators=(",", ":"))

# Пропуск None
json.dumps(data, ignore_nan=True)  # или default

# Красивый вывод для отладки
import pprint
pprint.pprint(data)
pprint.pp(data)  # Python 3.8+</code></pre>
'''
    },
    {
        'slug': 'networking',
        'title': 'Работа с сетью',
        'desc': 'requests, urllib, сокеты, HTTP-клиенты',
        'html': '''
<h3>Модуль requests</h3>
<p>Стандартный HTTP-клиент. Установка: <code>pip install requests</code></p>
<pre><code>import requests

# GET-запрос
response = requests.get("https://api.github.com")
print(response.status_code)  # 200
print(response.json())       # JSON-ответ
print(response.text)         # текст ответа
print(response.headers)      # заголовки

# Параметры
params = {"q": "python", "page": 1}
response = requests.get("https://api.github.com/search", params=params)

# POST с JSON
response = requests.post(
    "https://api.example.com/users",
    json={"name": "Анна", "age": 30},
    headers={"Authorization": "Bearer token"}
)

# POST с формой
response = requests.post("https://httpbin.org/post", data={"key": "value"})</code></pre>

<h3>Обработка ответов</h3>
<pre><code>import requests

response = requests.get("https://httpbin.org/status/404")

if response.ok:            # True для 2xx
    data = response.json()
elif response.status_code == 404:
    print("Не найдено")
elif response.status_code >= 500:
    print("Ошибка сервера")

# Исключения
try:
    response = requests.get("https://example.com", timeout=5)
    response.raise_for_status()  # выбросит HTTPError для 4xx/5xx
except requests.Timeout:
    print("Таймаут")
except requests.ConnectionError:
    print("Ошибка соединения")
except requests.HTTPError:
    print(f"HTTP {response.status_code}")</code></pre>

<h3>Сессии</h3>
<pre><code>session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})

# Куки сохраняются между запросами
session.get("https://httpbin.org/cookies/set/test/true")
response = session.get("https://httpbin.org/cookies")

# Закрытие сессии
session.close()

# Контекстный менеджер
with requests.Session() as session:
    session.get("https://example.com")</code></pre>

<h3>urllib — стандартная библиотека</h3>
<pre><code>from urllib.request import urlopen
from urllib.parse import urlencode, quote

# Простой GET
with urlopen("https://api.github.com") as f:
    data = f.read().decode()
    print(f.status)  # 200

# Параметры
params = urlencode({"q": "python", "page": 1})
url = f"https://api.github.com/search?{params}"

# Кодирование URL
quote("привет мир")  # %D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82%20%D0%BC%D0%B8%D1%80</code></pre>

<h3>Сокеты (низкий уровень)</h3>
<pre><code>import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("example.com", 80))
sock.send(b"GET / HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n")
response = sock.recv(4096)
sock.close()

# TCP-сервер
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8080))
server.listen(1)

conn, addr = server.accept()
data = conn.recv(1024)
conn.send(b"OK")
conn.close()</code></pre>
'''
    },
    {
        'slug': 'databases',
        'title': 'Базы данных',
        'desc': 'SQLite, подключение, запросы, ORM',
        'html': '''
<h3>SQLite (встроенная БД)</h3>
<pre><code>import sqlite3

# Подключение (создаст файл, если нет)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE
    )
""")

# Вставка
cursor.execute(
    "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
    ("Анна", 30, "anna@example.com")
)
conn.commit()

# Чтение
cursor.execute("SELECT * FROM users WHERE age > ?", (18,))
rows = cursor.fetchall()  # список строк
for row in rows:
    print(row)

# Одна строка
row = cursor.fetchone()

# Закрытие
conn.close()</code></pre>

<h3>Контекстный менеджер</h3>
<pre><code>with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    # conn.commit() — авто commit при выходе из with

# row_factory — доступ по имени колонки
conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
row = cursor.fetchone()
print(row["name"])  # доступ по имени</code></pre>

<h3>Транзакции</h3>
<pre><code>try:
    cursor.execute("BEGIN")
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    conn.commit()
except Exception:
    conn.rollback()
    print("Транзакция откачена")</code></pre>

<h3>Сырой SQL vs ORM</h3>
<p>Для работы с БД в Python часто используют ORM:</p>
<ul>
  <li><strong>SQLAlchemy</strong> — мощный ORM с полным контролем</li>
  <li><strong>Django ORM</strong> — встроен в Django, удобен для веб-приложений</li>
  <li><strong>Peewee</strong> — лёгкий ORM для небольших проектов</li>
</ul>

<pre><code># SQLAlchemy (пример)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)

with Session(engine) as session:
    user = User(name="Анна", age=30)
    session.add(user)
    session.commit()</code></pre>
'''
    },
    {
        'slug': 'typing',
        'title': 'Типизация (type hints)',
        'desc': 'Аннотации типов, Generic, Union, Optional, Protocol',
        'html': '''
<h3>Аннотации функций</h3>
<pre><code>def greet(name: str) -> str:
    return f"Привет, {name}"

def add(a: int, b: int) -> int:
    return a + b

def process(data: list[int]) -> dict[str, int]:
    return {str(x): x for x in data}</code></pre>

<h3>Аннотации переменных</h3>
<pre><code>name: str = "Анна"
age: int = 30
items: list[int] = [1, 2, 3]
user: dict[str, str | int] = {"name": "Анна", "age": 30}</code></pre>

<h3>Базовые типы из typing</h3>
<pre><code>from typing import (
    List, Dict, Tuple, Set, Optional, Union, Any,
    Callable, Iterable, Iterator, Sequence, Mapping,
    TypeVar, Generic, Protocol
)

# До 3.9: List[int], Dict[str, int]
# С 3.9: list[int], dict[str, int]

# Optional — может быть None
def find_user(id: int) -> Optional[dict]:
    ...

# Union — один из типов
def format(value: Union[str, int, float]) -> str:
    ...

# Union с |
def format(value: str | int | float) -> str:  # 3.10+
    ...

# Any — любой тип
def log(value: Any) -> None: ...</code></pre>

<h3>Generic — обобщённые типы</h3>
<pre><code>T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Generic класс
class Stack(T):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Использование
stack = Stack[int]()
stack.push(1)
value = stack.pop()  # type: int</code></pre>

<h3>Protocol — структурная типизация (3.8+)</h3>
<pre><code>from typing import Protocol

class Flyable(Protocol):
    def fly(self) -> str: ...

class Bird:
    def fly(self) -> str:
        return "Птица летит"

class Plane:
    def fly(self) -> str:
        return "Самолёт летит"

def travel(obj: Flyable) -> None:
    print(obj.fly())

travel(Bird())   # OK
travel(Plane())  # OK (duck typing)</code></pre>

<h3>Callable — тип функции</h3>
<pre><code>from typing import Callable

# Функция с int → str
def apply(func: Callable[[int], str], value: int) -> str:
    return func(value)

# Функция без параметров
def run(callback: Callable[[], None]) -> None:
    callback()</code></pre>

<h3>Literal — конкретные значения</h3>
<pre><code>from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    ...

set_mode("read")   # OK
set_mode("delete") # Ошибка проверки типов</code></pre>

<h3>TypedDict — типизированный словарь</h3>
<pre><code>from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str | None

user: User = {"name": "Анна", "age": 30, "email": None}</code></pre>

<h3>Мой любимый инструмент: mypy</h3>
<pre><code># Установка
pip install mypy

# Запуск
mypy script.py

# mypy находит ошибки типов без запуска кода
</code></pre>
'''
    },
    {
        'slug': 'async',
        'title': 'Асинхронное программирование',
        'desc': 'async/await, asyncio, корутины, параллелизм',
        'html': '''
<h3>Основы async/await</h3>
<pre><code>import asyncio

# Асинхронная функция (корутина)
async def greet(name: str) -> str:
    await asyncio.sleep(1)  # имитация долгой операции
    return f"Привет, {name}!"

# Запуск корутины
result = asyncio.run(greet("Мир"))
print(result)</code></pre>

<h3>Параллельный запуск</h3>
<pre><code>async def fetch_data(url: str) -> str:
    print(f"Загрузка {url}")
    await asyncio.sleep(2)
    return f"Данные {url}"

async def main():
    # Последовательно
    r1 = await fetch_data("url1")
    r2 = await fetch_data("url2")

    # Параллельно
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    print(results)

asyncio.run(main())</code></pre>

<h3>asyncio.create_task — фоновые задачи</h3>
<pre><code>async def background_work():
    while True:
        print("Работаю...")
        await asyncio.sleep(5)

async def main():
    # Запуск в фоне
    task = asyncio.create_task(background_work())
    await asyncio.sleep(12)
    task.cancel()  # остановка

asyncio.run(main())</code></pre>

<h3>Тайм-ауты</h3>
<pre><code>async def slow_operation():
    await asyncio.sleep(10)
    return "Готово"

async def main():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5)
    except asyncio.TimeoutError:
        print("Таймаут! Операция отменена")

asyncio.run(main())</code></pre>

<h3>Асинхронные генераторы</h3>
<pre><code>async def async_counter(n: int):
    for i in range(n):
        await asyncio.sleep(0.5)
        yield i

async def main():
    async for value in async_counter(5):
        print(value)  # 0, 1, 2, 3, 4 с интервалом 0.5с

asyncio.run(main())</code></pre>

<h3>Работа с сетью (aiohttp)</h3>
<pre><code>import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    urls = ["https://api.github.com"] * 5
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

asyncio.run(main())</code></pre>

<h3>Синхронное vs асинхронное</h3>
<table>
  <tr><th>Синхронно</th><th>Асинхронно</th></tr>
  <tr><td><code>def func()</code></td><td><code>async def func()</code></td></tr>
  <tr><td><code>func()</code></td><td><code>await func()</code></td></tr>
  <tr><td><code>result</code></td><td><code>await result</code></td></tr>
  <tr><td><code>for</code></td><td><code>async for</code></td></tr>
  <tr><td><code>with</code></td><td><code>async with</code></td></tr>
  <tr><td><code>time.sleep()</code></td><td><code>await asyncio.sleep()</code></td></tr>
</table>

<h3>asyncio vs threading vs multiprocessing</h3>
<pre><code># asyncio — для I/O-bound задач (сеть, файлы, БД)
# threading — для I/O-bound, но с GIL
# multiprocessing — для CPU-bound задач (реальные потоки ОС)

import asyncio
import threading
import multiprocessing

# asyncio — одна корутина за раз, переключение по await
# threading — переключение по прерыванию ОС
# multiprocessing — параллельное выполнение на всех ядрах</code></pre>

<h3>Синхронизация в asyncio</h3>
<pre><code>import asyncio

async def worker(name, lock):
    async with lock:
        print(f"{name} работает")
        await asyncio.sleep(1)

async def main():
    lock = asyncio.Lock()
    tasks = [worker(f"W{i}", lock) for i in range(3)]
    await asyncio.gather(*tasks)

asyncio.run(main())</code></pre>
'''
    },
    {
        'slug': 'testing',
        'title': 'Тестирование',
        'desc': 'unittest, pytest, фикстуры, моки, coverage',
        'html': '''
<h3>pytest — современный тестовый фреймворк</h3>
<p>Установка: <code>pip install pytest</code></p>

<pre><code># test_calc.py
def add(a, b):
    return a + b

# Имя теста начинается с test_
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0</code></pre>

<pre><code># Запуск
pytest                       # все тесты
pytest test_calc.py          # конкретный файл
pytest test_calc.py::test_add  # конкретный тест
pytest -v                    # подробный вывод
pytest -k "add"              # фильтр по имени
pytest -x                    # остановка при первой ошибке
pytest --tb=short            # короткий traceback</code></pre>

<h3>Фикстуры (fixtures)</h3>
<pre><code>import pytest

@pytest.fixture
def user_data():
    return {"name": "Анна", "age": 30}

@pytest.fixture
def database():
    # Setup
    db = create_test_database()
    yield db
    # Teardown
    db.drop()

def test_user_name(user_data):
    assert user_data["name"] == "Анна"

def test_user_age(user_data):
    assert user_data["age"] == 30</code></pre>

<h3>Параметризация</h3>
<pre><code>import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert a + b == expected

# Несколько параметров
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [3, 4])
def test_product(a, b):
    pass  # 4 комбинации</code></pre>

<h3>Моки (unittest.mock)</h3>
<pre><code>from unittest.mock import Mock, patch
import requests

# Mock объект
mock_response = Mock()
mock_response.json.return_value = {"id": 1, "name": "Анна"}
mock_response.status_code = 200

# patch — замена в контексте
@patch("requests.get")
def test_fetch(mock_get):
    mock_get.return_value = mock_response
    result = fetch_user(1)
    assert result["name"] == "Анна"

# Проверка вызова
mock_get.assert_called_once_with("https://api.example.com/users/1")</code></pre>

<h3>unittest — встроенный модуль</h3>
<pre><code>import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        """Выполняется перед каждым тестом"""
        self.data = [1, 2, 3]

    def test_sum(self):
        self.assertEqual(sum(self.data), 6)

    def test_max(self):
        self.assertEqual(max(self.data), 3)

    def test_in(self):
        self.assertIn(2, self.data)

if __name__ == "__main__":
    unittest.main()</code></pre>

<h3>Проверки (assertions)</h3>
<pre><code>assert result == expected
assert result != wrong
assert result is None
assert result is not None
assert value in collection
assert len(items) > 0
assert "error" not in response.text
assert response.status_code == 200

# pytest предоставляет
pytest.approx(3.14159, 0.001)  # сравнение float
pytest.raises(ValueError)      # ожидание исключения
pytest.warns(UserWarning)      # ожидание предупреждения</code></pre>

<h3>Проверка исключений</h3>
<pre><code>import pytest

def test_raises():
    with pytest.raises(ValueError, match="деление на ноль"):
        divide(10, 0)

def test_raises_no_match():
    with pytest.raises(ZeroDivisionError):
        1 / 0</code></pre>

<h3>Покрытие кода (coverage)</h3>
<pre><code># Установка
pip install pytest-cov

# Запуск с покрытием
pytest --cov=my_module --cov-report=html
pytest --cov=my_module --cov-report=term-missing

# Минимальный порог
pytest --cov=my_module --cov-fail-under=80</code></pre>
'''
    },
    {
        'slug': 'best-practices',
        'title': 'Советы и лучшие практики',
        'desc': 'PEP 8, идиомы, частые ошибки, производительность',
        'html': '''
<h3>PEP 8 — стиль кода</h3>
<ul>
  <li>Отступы: 4 пробела (не табуляция)</li>
  <li>Максимум 79 символов в строке</li>
  <li>Пустые строки между функциями (2) и внутри класса (1)</li>
  <li>Пробелы вокруг операторов: <code>a = b + c</code>, не <code>a=b+c</code></li>
  <li>Импорты: стандартные → сторонние → локальные</li>
</ul>

<h3>Pythonic-идиомы</h3>
<pre><code># Swap
a, b = b, a

# Проверка на None
if value is None: ...

# Пустая коллекция → False
if not items: ...

# Тернарник
status = "чёт" if n % 2 == 0 else "нечёт"

# Распаковка
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2,3,4]

# enumerate с индексом
for i, val in enumerate(lst): ...

# zip для параллельной итерации
for name, age in zip(names, ages): ...

# any / all
if any(x > 0 for x in lst): ...

# Вхождение в диапазон
if 0 <= score <= 100: ...

# Словарь с get
value = d.get("key", default)

# Множественные сравнения
if a == b == c: ...</code></pre>

<h3>Частые ошибки</h3>
<pre><code># 1. Изменяемый аргумент по умолчанию
def add(item, lst=[]):      # ПЛОХО!
    lst.append(item)
    return lst

def add(item, lst=None):    # ХОРОШО
    if lst is None:
        lst = []
    lst.append(item)
    return lst

# 2. Использование is с числами/строками
# is — для None и True/False. == — для всего остального

# 3. Выход за границы списка
items = [1, 2, 3]
try:
    items[10]
except IndexError:
    ...

# 4. Изменение списка во время итерации
# ПЛОХО: for item in lst: lst.remove(item)
# ХОРОШО: [x for x in lst if condition]

# 5. Исключение в except без указания типа
# ПЛОХО: except:
# ХОРОШО: except ValueError:

# 6. global — обычно не нужно
# ПЛОХО: def f(): global x; x += 1

# 7. range(len(lst)) — используйте enumerate</code></pre>

<h3>Производительность</h3>
<pre><code># Генераторы быстрее списков, если не нужен весь результат
sum(x**2 for x in range(1000000))  # быстрее
sum([x**2 for x in range(1000000)])  # медленнее

# local variables быстрее global
def func():
    local_math = math.sqrt  # привязка к локальной
    for i in range(1000):
        local_math(i)

# join быстрее + для строк
# ПЛОХО: s = ""; for p in parts: s += p
# ХОРОШО: s = "".join(parts)

# set быстрее list для in
# in set: O(1), in list: O(n)
lookup = set(items)
if value in lookup: ...

# collections.deque быстрее list для pop(0) / insert(0, x)
from collections import deque
dq = deque([1, 2, 3])
dq.popleft()  # O(1)</code></pre>

<h3>Полезные однострочники</h3>
<pre><code># Уникальные элементы
unique = list(set(items))

# Разворот строки/списка
reversed_s = s[::-1]

# Палиндром
is_palindrome = s == s[::-1]

# Плоский список из вложенного
flat = [x for sub in nested for x in sub]

# Транспонирование матрицы
transposed = list(zip(*matrix))

# Самое частое значение
from statistics import mode
most_common = mode(data)

# Чтение файла в список строк
lines = open("file.txt").read().splitlines()</code></pre>

<h3>Инструменты</h3>
<ul>
  <li><strong>black</strong> — автоформатирование кода</li>
  <li><strong>ruff</strong> — быстрый линтер (замена flake8, isort)</li>
  <li><strong>mypy</strong> — проверка типов</li>
  <li><strong>pre-commit</strong> — хуки перед коммитом</li>
  <li><strong>pytest</strong> — тестирование</li>
  <li><strong>poetry</strong> / <strong>uv</strong> — управление зависимостями</li>
  <li><strong>ipdb</strong> — отладка (import ipdb; ipdb.set_trace())</li>
</ul>

<h3>Ресурсы</h3>
<ul>
  <li><a href="https://docs.python.org">docs.python.org</a> — официальная документация</li>
  <li><a href="https://pypi.org">PyPI</a> — репозиторий пакетов</li>
  <li><a href="https://realpython.com">Real Python</a> — учебные материалы</li>
  <li><a href="https://peps.python.org/pep-0008">PEP 8</a> — руководство по стилю</li>
</ul>
'''
    },
]

# ── Генерация HTML ──
def make_nav(current_slug=None):
    items = []
    for s in SECTIONS:
        active = ' class="active"' if s['slug'] == current_slug else ''
        items.append(f'      <li><a href="{s["slug"]}.html"{active}>{s["title"]}</a></li>')
    return '\n'.join(items)

def make_content(content_str):
    return content_str.strip()

# Создание статичных страниц
for sec in SECTIONS:
    slug = sec['slug']
    nav = make_nav(slug)
    content = make_content(sec['html'])
    html = PAGE_TPL.format(
        title=sec['title'],
        nav_items=nav,
        content=content
    )
    path = os.path.join(OUT, f'{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  {slug}.html — {sec["title"]}')

# Index page
nav = make_nav(None)
cards = []
for sec in SECTIONS:
    cards.append(f'''      <a href="{sec["slug"]}.html" class="card">
        <h3>{sec["title"]}</h3>
        <p>{sec["desc"]}</p>
      </a>''')

index_html = INDEX_TPL.format(
    nav_items=nav,
    cards='\n'.join(cards)
)

with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

# CSS
with open(os.path.join(OUT, 'pytestru-style.css'), 'w', encoding='utf-8') as f:
    f.write(CSS)

print(f'\nГотово: {len(SECTIONS)} страниц + index.html + CSS')

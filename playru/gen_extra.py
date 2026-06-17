#!/usr/bin/env python3
"""Дополнительные разделы справочника Python."""

import os, html as html_mod

OUT = r'C:\Users\win11\Documents\GIT\qasdet.github.io\pytestru'

# ── Шаблоны ──
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

# ── Новые разделы ──
NEW_SECTIONS = []

# ── 1. Перечисления (Enum) ──
NEW_SECTIONS.append({
    'slug': 'enums',
    'title': 'Перечисления (Enum)',
    'desc': 'Enum, IntEnum, auto, методы и возможности перечислений',
    'html': '''
<h3>Базовый Enum</h3>
<pre><code>from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Доступ
Color.RED              # Color.RED
Color.RED.name         # 'RED'
Color.RED.value        # 1
type(Color.RED)        # <enum 'Color'>
isinstance(Color.RED, Color)  # True

# Итерация
for c in Color:
    print(c.name, c.value)

# Доступ по значению
Color(1)               # Color.RED
Color['RED']           # Color.RED</code></pre>

<h3>StrEnum и IntEnum</h3>
<pre><code>from enum import IntEnum, StrEnum

class StatusCode(IntEnum):
    OK = 200
    NOT_FOUND = 404
    ERROR = 500

# IntEnum можно сравнивать с int
StatusCode.OK == 200  # True
StatusCode.OK > 300   # False

class Protocol(StrEnum):
    HTTP = "http"
    HTTPS = "https"
    FTP = "ftp"

Protocol.HTTP == "http"  # True</code></pre>

<h3>auto — автоматические значения</h3>
<pre><code>from enum import Enum, auto

class Priority(Enum):
    LOW = auto()      # 1
    MEDIUM = auto()   # 2
    HIGH = auto()     # 3
    CRITICAL = auto() # 4

# Кастомный auto
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

class Status(AutoName):
    PENDING = auto()
    ACTIVE = auto()
    BLOCKED = auto()

Status.ACTIVE.value  # 'ACTIVE'</code></pre>

<h3>Flag — флаги (комбинации)</h3>
<pre><code>from enum import Flag, auto

class Permission(Flag):
    READ = auto()     # 1
    WRITE = auto()    # 2
    EXECUTE = auto()  # 4
    ALL = READ | WRITE | EXECUTE  # 7

# Комбинации
perm = Permission.READ | Permission.WRITE
perm & Permission.READ   # Permission.READ (есть)
perm & Permission.EXECUTE  # 0 (нет)
Permission.ALL in perm   # False
Permission.READ in perm  # True</code></pre>

<h3>Методы и декораторы</h3>
<pre><code>from enum import Enum, unique

@unique  # гарантирует уникальность значений
class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2
    # ACTIVE_DUP = 1  # ValueError!

# Методы в Enum
class Planet(Enum):
    EARTH = (1, 5.972e24)
    MARS = (2, 6.39e23)

    def __init__(self, order, mass):
        self.order = order
        self.mass = mass

    @property
    def name_ru(self):
        names = {1: "Земля", 2: "Марс"}
        return names.get(self.order)

Planet.EARTH.mass      # 5.972e+24
Planet.MARS.name_ru    # "Марс"</code></pre>

<h3>Best practices</h3>
<ul>
  <li>Используйте <code>Enum</code> вместо строк/магических чисел</li>
  <li><code>@unique</code> — предотвращает дубликаты значений</li>
  <li><code>IntEnum</code> — когда нужно сравнивать с int (например, HTTP-статусы)</li>
  <li><code>Flag</code> — для комбинаций флагов (права доступа, настройки)</li>
  <li>Избегайте наследования Enum от других классов кроме <code>int</code>/<code>str</code></li>
  <li>Храните дополнительную логику прямо в Enum через <code>__init__</code></li>
</ul>
'''
})

# ── 2. Менеджеры контекста ──
NEW_SECTIONS.append({
    'slug': 'context-managers',
    'title': 'Менеджеры контекста',
    'desc': 'with, contextlib, contextmanager, создание своих контекстов',
    'html': '''
<h3>Зачем нужны менеджеры контекста</h3>
<p>Гарантируют выполнение кода при входе и выходе из блока, даже при исключениях.</p>

<pre><code># Без менеджера контекста
f = open("file.txt")
try:
    data = f.read()
finally:
    f.close()  # надо не забыть!

# С менеджером контекста
with open("file.txt") as f:
    data = f.read()  # close() автоматически</code></pre>

<h3>Несколько контекстов</h3>
<pre><code># Несколько файлов
with open("a.txt") as a, open("b.txt") as b:
    # ...

# Parentheses для длинных (3.10+)
with (
    open("a.txt") as a,
    open("b.txt") as b,
    open("c.txt") as c,
):
    pass</code></pre>

<h3>Создание своего контекста через класс</h3>
<pre><code>class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start
        print(f"Время: {elapsed:.3f}s")
        # return True — подавить исключение
        return False

with Timer() as t:
    sum(range(1000000))
# Время: 0.025s</code></pre>

<h3>contextmanager — декоратор</h3>
<pre><code>from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"Время: {elapsed:.3f}s")

with timer():
    sum(range(1000000))

# Передача значения
@contextmanager
def managed_resource(name):
    print(f"Вход: {name}")
    yield name.upper()
    print(f"Выход: {name}")

with managed_resource("data") as r:
    print(r)  # DATA</code></pre>

<h3>contextlib — полезные утилиты</h3>
<pre><code>from contextlib import suppress, redirect_stdout, nullcontext
import os

# suppress — игнорировать исключение
with suppress(FileNotFoundError):
    os.remove("nonexistent.txt")
# Не выбросит FileNotFoundError

# redirect_stdout — перенаправление вывода
with open("log.txt", "w") as f:
    with redirect_stdout(f):
        print("Это пойдёт в файл")

# nullcontext — контекст-заглушка (3.7+)
from contextlib import nullcontext
def process_file(path):
    ctx = open(path) if path else nullcontext()
    with ctx as f:
        read(f)

# ExitStack — динамическое управление
from contextlib import ExitStack

files = ["a.txt", "b.txt"]
with ExitStack() as stack:
    file_objects = [stack.enter_context(open(f)) for f in files]
    # все файлы закроются при выходе</code></pre>

<h3>contextmanager с обработкой ошибок</h3>
<pre><code>@contextmanager
def database_transaction(conn):
    print("BEGIN")
    try:
        yield conn
    except Exception:
        conn.rollback()
        print("ROLLBACK")
        raise
    else:
        conn.commit()
        print("COMMIT")

with database_transaction(connection) as conn:
    conn.execute("INSERT ...")</code></pre>

<h3>Best practices</h3>
<ul>
  <li>Всегда используйте <code>with</code> для файлов, сокетов, БД, блокировок</li>
  <li><code>@contextmanager</code> — проще, чем писать класс с <code>__enter__</code>/<code>__exit__</code></li>
  <li><code>suppress</code> вместо пустых <code>try/except</code></li>
  <li><code>ExitStack</code> — когда количество контекстов известно только в runtime</li>
  <li>Возвращайте <code>True</code> из <code>__exit__</code> только если уверены, что подавление исключения безопасно</li>
</ul>
'''
})

# ── 3. Отладка и профилирование ──
NEW_SECTIONS.append({
    'slug': 'debugging',
    'title': 'Отладка и профилирование',
    'desc': 'pdb, breakpoint, логирование, профилирование, timeit',
    'html': '''
<h3>pdb — встроенный отладчик</h3>
<pre><code>import pdb

def buggy_func(x):
    result = []
    for i in range(x):
        pdb.set_trace()  # остановка здесь
        result.append(i ** 2)
    return result

# Команды pdb:
# n (next) — шаг
# s (step) — войти в функцию
# c (continue) — продолжить
# p var — напечатать переменную
# ll — показать исходный код
# q (quit) — выход</code></pre>

<h3>breakpoint() — встроенная точка остановки (3.7+)</h3>
<pre><code>def calculate(a, b):
    result = a + b
    breakpoint()  # автоматический вызов pdb.set_trace()
    return result * 2

# Переменная окружения PYTHONBREAKPOINT
# PYTHONBREAKPOINT=0 — отключить все breakpoint
# PYTHONBREAKPOINT=pudb.set_trace — использовать pudb</code></pre>

<h3>post-mortem отладка</h3>
<pre><code>import pdb

try:
    1 / 0
except ZeroDivisionError:
    pdb.post_mortem()  # отладчик в контексте ошибки

# Автоматическая post-mortem
python -m pdb script.py  # запуск с отладчиком</code></pre>

<h3>__debug__ и assert</h3>
<pre><code># assert — проверка условия, выброс AssertionError
def divide(a, b):
    assert b != 0, "Деление на ноль"
    return a / b

# Отключаются флагом -O (python -O script.py)
# assert исчезают при оптимизации!

# __debug__ — True если без -O
if __debug__:
    print("Режим отладки")</code></pre>

<h3>logging — правильное логирование</h3>
<pre><code>import logging

# Настройка
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    filename="app.log",  # в файл
)

logger = logging.getLogger("my_app")

logger.debug("Детальная отладка")
logger.info("Информационное сообщение")
logger.warning("Предупреждение: %s", value)
logger.error("Ошибка: %s", exc_info=True)
logger.critical("Критическая ошибка")

# Лучше, чем print()
# Есть уровни, фильтры, форматы, вывод в несколько мест</code></pre>

<h3>Профилирование</h3>
<pre><code># time — простое измерение
import time
start = time.perf_counter()
result = sum(range(1000000))
elapsed = time.perf_counter() - start
print(f"{elapsed:.4f}s")

# timeit — точное измерение (отключает GC)
import timeit
time = timeit.timeit('sum(range(1000))', number=10000)
print(f"Среднее: {time/10000:.6f}s")

# cProfile — профилирование функций
import cProfile, pstats

def main():
    total = sum(range(1000000))
    print(total)

cProfile.run('main()', 'profile_stats')
p = pstats.Stats('profile_stats')
p.sort_stats('cumtime').print_stats(10)  # топ-10 по времени</code></pre>

<h3>trace — трассировка выполнения</h3>
<pre><code>import trace

# Создание трассировщика
tracer = trace.Trace(
    count=True,      # подсчёт строк
    trace=True,      # вывод строк по мере выполнения
    timing=True      # время выполнения
)

tracer.run('sum(range(100))')
tracer.results().write_results(coverdir='cover')</code></pre>

<h3>Интерактивная отладка</h3>
<pre><code># ipdb — улучшенный pdb (pip install ipdb)
import ipdb; ipdb.set_trace()

# IPython.embed — полное интерактивное окружение
from IPython import embed; embed()

# rich.inspect — красивая инспекция объекта (pip install rich)
from rich import inspect
inspect(open("file.txt"))</code></pre>

<h3>Best practices</h3>
<ul>
  <li>Замените <code>print()</code> на <code>logging</code> — гибкость уровней и форматов</li>
  <li>Используйте <code>breakpoint()</code> вместо <code>pdb.set_trace()</code></li>
  <li>Не оставляйте точки остановки в production-коде</li>
  <li><code>assert</code> — для тестов и отладки, НЕ для валидации данных</li>
  <li><code>timeit</code> — для точных замеров, <code>time.perf_counter()</code> — для быстрых</li>
  <li>cProfile — первым делом при оптимизации: измерьте, прежде чем менять</li>
</ul>
'''
})

# ── 4. Командная строка и подпроцессы ──
NEW_SECTIONS.append({
    'slug': 'subprocess',
    'title': 'Командная строка и подпроцессы',
    'desc': 'subprocess, os.system, shutil, argparse, click',
    'html': '''
<h3>subprocess — запуск внешних команд</h3>
<pre><code>import subprocess

# Простой запуск (ждать завершения)
subprocess.run(["ls", "-la"])
subprocess.run(["dir", "/w"], shell=True)  # Windows

# Захват вывода
result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout)   # Python 3.11.9
print(result.returncode)  # 0
# check=True → CalledProcessError при ненулевом коде

# stderr
result = subprocess.run(
    ["python", "-c", "print('ok')"],
    capture_output=True,
    text=True,
)
print(result.stderr)  # пусто</code></pre>

<h3>subprocess — продвинутое использование</h3>
<pre><code>import subprocess

# PIPE — передача данных
p1 = subprocess.Popen(["echo", "hello"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "h"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
output = p2.communicate()[0]
print(output.decode())  # hello

# timeout
try:
    subprocess.run(["sleep", "10"], timeout=5)
except subprocess.TimeoutExpired:
    print("Таймаут")

# Работа с shell-командами (осторожно!)
subprocess.run("ls -la | grep py", shell=True)

# env — переменные окружения
import os
env = os.environ.copy()
env["MY_VAR"] = "value"
subprocess.run(["python", "script.py"], env=env)</code></pre>

<h3>os и shutil — работа с файловой системой</h3>
<pre><code>import os, shutil

# os — базовые операции
os.getcwd()           # текущая директория
os.chdir("..")        # сменить
os.listdir(".")       # список файлов
os.mkdir("new_dir")   # создать папку
os.makedirs("a/b/c", exist_ok=True)  # вложенные
os.remove("file.txt")  # удалить файл
os.rename("old", "new")  # переименовать
os.rmdir("dir")       # удалить пустую папку

# shutil — высокоуровневые операции
shutil.copy("src.txt", "dst.txt")       # копировать файл
shutil.copytree("src", "dst")           # копировать дерево
shutil.move("src", "dst")               # переместить
shutil.rmtree("dir")                    # удалить дерево
shutil.make_archive("backup", "zip", "dir")  # архив
shutil.which("python")                  # путь к исполняемому файлу
shutil.disk_usage("/")                  # статистика диска

# glob — поиск файлов по шаблону
import glob
glob.glob("*.py")        # все .py в текущей
glob.glob("**/*.py", recursive=True)  # рекурсивно</code></pre>

<h3>argparse — аргументы командной строки</h3>
<pre><code>import argparse

parser = argparse.ArgumentParser(
    description="Обработка файлов",
    epilog="Пример: python script.py -o out.txt input.csv",
)

parser.add_argument("input", help="Входной файл")
parser.add_argument("-o", "--output", default="out.txt", help="Выходной файл")
parser.add_argument("-v", "--verbose", action="store_true", help="Подробный вывод")
parser.add_argument("-n", "--number", type=int, default=1, help="Количество")
parser.add_argument("--format", choices=["json", "csv"], default="csv")

args = parser.parse_args()
print(args.input, args.output, args.verbose)

# Запуск: python script.py -v -o result.txt data.csv --format json</code></pre>

<h3>os.environ — переменные окружения</h3>
<pre><code>import os

# Чтение
home = os.environ.get("HOME")  # None если нет
path = os.environ.get("PATH", "/usr/bin")

# Установка
os.environ["MY_VAR"] = "value"

# Проверка
if "DEBUG" in os.environ:
    print("Режим отладки")

# python-dotenv — .env файлы (pip install python-dotenv)
from dotenv import load_dotenv
load_dotenv()  # загрузить .env в os.environ
db_url = os.getenv("DATABASE_URL")</code></pre>

<h3>tempfile — временные файлы</h3>
<pre><code>import tempfile, os

# Временный файл
with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
    f.write("временные данные")
    tmppath = f.name

os.unlink(tmppath)  # удалить

# Временная директория
with tempfile.TemporaryDirectory() as tmpdir:
    path = os.path.join(tmpdir, "test.txt")
    with open(path, "w") as f:
        f.write("test")
# директория удалится автоматически</code></pre>

<h3>Best practices</h3>
<ul>
  <li>Используйте <code>subprocess.run()</code> вместо <code>os.system()</code> — больше контроля</li>
  <li>Всегда указывайте <code>capture_output=True</code> и <code>text=True</code> для читаемости</li>
  <li><code>shell=True</code> — опасно (shell injection). Избегайте, если возможно</li>
  <li>Для сложных CLI — используйте <code>argparse</code> или <code>click</code></li>
  <li><code>shutil</code> — вместо нескольких <code>os</code>-вызовов для копирования/удаления деревьев</li>
  <li><code>tempfile</code> — для тестов и временных данных</li>
  <li><code>pathlib</code> — вместо <code>os.path</code> для работы с путями</li>
</ul>
'''
})

# ── 5. Начинающим и шпаргалка ──
NEW_SECTIONS.append({
    'slug': 'cheatsheet',
    'title': 'Шпаргалка',
    'desc': 'Сводка всех ключевых конструкций языка в одной таблице',
    'html': '''
<h3>Типы данных</h3>
<table>
  <tr><th>Тип</th><th>Мутабельный</th><th>Создание</th><th>Особенность</th></tr>
  <tr><td><code>int</code></td><td>Нет</td><td><code>x = 42</code></td><td>Произвольная точность</td></tr>
  <tr><td><code>float</code></td><td>Нет</td><td><code>x = 3.14</code></td><td>Погрешность 0.1+0.2</td></tr>
  <tr><td><code>str</code></td><td>Нет</td><td><code>s = "hello"</code></td><td>Срезы, f-строки</td></tr>
  <tr><td><code>list</code></td><td>Да</td><td><code>lst = [1,2,3]</code></td><td>Упорядочен, изменяем</td></tr>
  <tr><td><code>tuple</code></td><td>Нет</td><td><code>t = (1,2,3)</code></td><td>Неизменяем, хешируем</td></tr>
  <tr><td><code>dict</code></td><td>Да</td><td><code>d = {"k":"v"}</code></td><td>Ключи хешируемые</td></tr>
  <tr><td><code>set</code></td><td>Да</td><td><code>s = {1,2,3}</code></td><td>Уникальные, неупорядочены</td></tr>
  <tr><td><code>frozenset</code></td><td>Нет</td><td><code>fs = frozenset([1])</code></td><td>Хешируемый</td></tr>
  <tr><td><code>bool</code></td><td>Нет</td><td><code>b = True</code></td><td>True/False</td></tr>
  <tr><td><code>NoneType</code></td><td>Нет</td><td><code>x = None</code></td><td>Отсутствие значения</td></tr>
</table>

<h3>Срезы (slicing)</h3>
<pre><code>s[start:stop:step]
s[::-1]    # разворот
s[::2]     # каждый второй
s[:-1]     # все кроме последнего
s[1:]      # все кроме первого
s[-3:]     # последние 3
s[1:-1]    # без первого и последнего</code></pre>

<h3>Списковые включения</h3>
<pre><code>[expr for x in iterable]           # базовая форма
[expr for x in iterable if cond]   # с фильтром
[expr if cond else alt for x in iterable]  # с if-else
[(x,y) for x in a for y in b]      # вложенные</code></pre>

<h3>Лямбда и сортировка</h3>
<pre><code>lambda x: x**2                          # анонимная функция
sorted(lst, key=lambda x: x[1])         # сортировка по ключу
sorted(lst, key=lambda x: len(x))       # по длине
sorted(lst, key=lambda x: x, reverse=True)  # по убыванию
max(lst, key=lambda x: x.score)         # максимум по ключу</code></pre>

<h3>Распаковка</h3>
<pre><code>a, b = (1, 2)              # кортеж
a, *rest = [1,2,3,4]       # a=1, rest=[2,3,4]
first, *mid, last = range(5)  # first=0, mid=[1,2,3], last=4
{**d1, **d2}               # слияние словарей (3.5+)
d1 | d2                    # слияние (3.9+)
*a, = range(5)             # распаковать в список</code></pre>

<h3>f-строки — форматирование</h3>
<pre><code>f"{value}"                 # значение
f"{value:.2f}"             # 2 знака после запятой
f"{value:>10}"             # выравнивание вправо
f"{value:<10}"             # выравнивание влево
f"{value:^10}"             # по центру
f"{value:010d}"            # заполнение нулями
f"{value:,}"               # разделитель разрядов
f"{value:.1%}"             # проценты
f"{value:#x}"              # шестнадцатеричное
f"{value:b}"               # двоичное
f"{name!r}"                # repr()
f"{func()}"                # вызов функции</code></pre>

<h3>Полезные функции одной строкой</h3>
<table>
  <tr><th>Задача</th><th>Код</th></tr>
  <tr><td>Уникальные элементы</td><td><code>list(set(lst))</code></td></tr>
  <tr><td>Палиндром</td><td><code>s == s[::-1]</code></td></tr>
  <tr><td>Плоский список</td><td><code>[x for sub in nested for x in sub]</code></td></tr>
  <tr><td>Разворот словаря</td><td><code>{v:k for k,v in d.items()}</code></td></tr>
  <tr><td>Транспонирование</td><td><code>list(zip(*matrix))</code></td></tr>
  <tr><td>Счётчик элементов</td><td><code>Counter(lst).most_common(n)</code></td></tr>
  <tr><td>Группировка</td><td><code>groupby(sorted(data), key=func)</code></td></tr>
  <tr><td>Значение по умолчанию</td><td><code>d.get(key, default)</code></td></tr>
  <tr><td>Тернарник</td><td><code>val if cond else alt</code></td></tr>
  <tr><td>Swap</td><td><code>a, b = b, a</code></td></tr>
  <tr><td>Разворот строки</td><td><code>s[::-1]</code></td></tr>
  <tr><td>Чтение файла в список</td><td><code>open(f).read().splitlines()</code></td></tr>
</table>

<h3>Модули на каждый день</h3>
<table>
  <tr><th>Модуль</th><th>Задача</th></tr>
  <tr><td><code>json</code></td><td>JSON</td></tr>
  <tr><td><code>csv</code></td><td>CSV-файлы</td></tr>
  <tr><td><code>re</code></td><td>Регулярные выражения</td></tr>
  <tr><td><code>pathlib</code></td><td>Пути к файлам</td></tr>
  <tr><td><code>datetime</code></td><td>Дата и время</td></tr>
  <tr><td><code>collections</code></td><td>Counter, defaultdict, deque</td></tr>
  <tr><td><code>itertools</code></td><td>Комбинаторика, цепочки</td></tr>
  <tr><td><code>functools</code></td><td>lru_cache, partial</td></tr>
  <tr><td><code>logging</code></td><td>Логирование</td></tr>
  <tr><td><code>argparse</code></td><td>CLI-аргументы</td></tr>
  <tr><td><code>subprocess</code></td><td>Внешние команды</td></tr>
  <tr><td><code>hashlib</code></td><td>Хеши</td></tr>
  <tr><td><code>uuid</code></td><td>UUID</td></tr>
  <tr><td><code>statistics</code></td><td>mean, median, mode</td></tr>
</table>

<h3>False-значения</h3>
<pre><code># Все эти значения приводятся к False:
False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0)
# Всё остальное — True</code></pre>

<h3>Проверка типа</h3>
<pre><code>isinstance(x, int)        # одного типа
isinstance(x, (int, float))  # нескольких типов
type(x) is int            # строгая проверка (без наследования)
callable(func)            # можно ли вызвать
hasattr(obj, "attr")      # есть ли атрибут
getattr(obj, "attr", default)  # безопасно получить атрибут</code></pre>

<h3>Итерация — полезные паттерны</h3>
<pre><code>for i, v in enumerate(lst):     # с индексом
for a, b in zip(lst1, lst2):    # параллельно
    for a, b in zip_longest(lst1, lst2):  # разной длины
for item in reversed(lst):      # в обратном порядке
for item in sorted(lst):        # сортированно
for k, v in d.items():          # словарь
for item in set(lst):           # без дубликатов
any(pred(x) for x in lst)       # есть ли хотя бы один
all(pred(x) for x in lst)       # все ли подходят</code></pre>
'''
})

# ── 6. Продвинутые темы ──
NEW_SECTIONS.append({
    'slug': 'advanced',
    'title': 'Продвинутые темы',
    'desc': 'Дескрипторы, метаклассы, слоты, __dict__, weakref',
    'html': '''
<h3>__slots__ — оптимизация памяти</h3>
<pre><code># Обычный класс — каждый объект имеет __dict__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Со __slots__ — без __dict__, меньше памяти
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

# Преимущества: экономия памяти (~40-60%)
# Недостатки: нельзя добавлять новые атрибуты
# p.z = 3  # AttributeError</code></pre>

<h3>Дескрипторы — управление доступом</h3>
<pre><code>class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name, 0)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Число должно быть положительным")
        setattr(obj, self.name, value)

class Order:
    price = PositiveNumber()
    quantity = PositiveNumber()

order = Order()
order.price = 100    # OK
order.price = -50    # ValueError!
# order.price = 100  # OK
print(order.price)   # 100</code></pre>

<h3>property через дескриптор</h3>
<pre><code>class Property:
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("read-only property")
        self.fset(obj, value)

class Person:
    def __init__(self, name):
        self._name = name

    @Property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value</code></pre>

<h3>Метаклассы — классы, создающие классы</h3>
<pre><code># type() — стандартный метакласс
# Создание класса динамически
MyClass = type('MyClass', (Base,), {'attr': 42})

# Свой метакласс
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def log(self, msg):
        print(msg)

# Все экземпляры Logger — один и тот же объект
a = Logger()
b = Logger()
a is b  # True</code></pre>

<h3>__init_subclass__ — действие при наследовании</h3>
<pre><code>class BasePlugin:
    plugins = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins[cls.__name__] = cls

class JsonPlugin(BasePlugin):
    def process(self, data):
        return json.loads(data)

class YamlPlugin(BasePlugin):
    def process(self, data):
        return yaml.safe_load(data)

BasePlugin.plugins
# {'JsonPlugin': JsonPlugin, 'YamlPlugin': YamlPlugin}</code></pre>

<h3>weakref — слабые ссылки</h3>
<pre><code>import weakref

class BigData:
    def __init__(self, size):
        self.data = [0] * size

data = BigData(1000000)

# Слабая ссылка — не увеличивает счётчик ссылок
ref = weakref.ref(data)
print(ref())  # <__main__.BigData object at ...>

del data       # объект удалён
print(ref())  # None (сборщик мусора удалил)

# WeakValueDictionary — словарь с автоматическим удалением
cache = weakref.WeakValueDictionary()

class ExpensiveObject:
    pass

obj = ExpensiveObject()
cache["key"] = obj
print(cache.get("key"))  # <...>
del obj
print(cache.get("key"))  # None</code></pre>

<h3>dataclasses — продвинутое использование</h3>
<pre><code>from dataclasses import dataclass, field, InitVar

@dataclass
class User:
    name: str
    age: int = 0
    emails: list = field(default_factory=list)
    id: int = field(init=False)  # не передаётся в __init__

    # InitVar — параметр, который не становится полем
    db: InitVar[str] = None

    def __post_init__(self, db):
        # Вызывается после __init__
        self.id = hash(self.name)
        if db:
            self.load_from_db(db)

    def load_from_db(self, db):
        ...</code></pre>

<h3>Best practices для продвинутых тем</h3>
<ul>
  <li><code>__slots__</code> — только когда нужна экономия памяти (миллионы объектов)</li>
  <li>Метаклассы — мощный инструмент, но не злоупотребляйте. Часто есть более простые решения</li>
  <li>Дескрипторы — основа property, classmethod, staticmethod. Полезны для валидации</li>
  <li><code>weakref</code> — для кэшей, чтобы не блокировать сборку мусора</li>
  <li><code>__init_subclass__</code> — элегантная альтернатива метаклассам для регистрации подклассов</li>
</ul>
'''
})

# ── Читаем существующие разделы из index.html ──
def read_existing_nav():
    """Читает существующие разделы из index.html."""
    index_path = os.path.join(OUT, 'index.html')
    existing = []
    try:
        with open(index_path, encoding='utf-8') as f:
            content = f.read()
        # Находим все ссылки в sidebar
        import re
        links = re.findall(r'<a href="([^"]+\.html)">([^<]+)</a>', content)
        for href, title in links:
            if href != 'index.html':
                slug = href.replace('.html', '')
                existing.append((slug, title))
    except FileNotFoundError:
        pass
    return existing

# ── Генерация ──
existing = read_existing_nav()
existing_slugs = {s for s, _ in existing}

# Собираем все разделы (существующие + новые) для навигации
all_nav = list(existing)
for sec in NEW_SECTIONS:
    if sec['slug'] not in existing_slugs:
        all_nav.append((sec['slug'], sec['title']))

def make_nav(current_slug=None):
    items = []
    for slug, title in all_nav:
        active = ' class="active"' if slug == current_slug else ''
        items.append(f'      <li><a href="{slug}.html"{active}>{title}</a></li>')
    return '\n'.join(items)

# Генерация новых страниц
for sec in NEW_SECTIONS:
    slug = sec['slug']
    html = PAGE_TPL.format(
        title=sec['title'],
        nav_items=make_nav(slug),
        content=sec['html'].strip()
    )
    path = os.path.join(OUT, f'{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  {slug}.html — {sec["title"]}')

# ── Обновление index.html ──
index_path = os.path.join(OUT, 'index.html')
with open(index_path, encoding='utf-8') as f:
    index_content = f.read()

# Обновляем навигацию
import re
nav_section_pattern = r'(<nav class="sidebar">.*?<ul>).*?(</ul>)'
def replace_nav(m):
    return m.group(1) + '\n' + make_nav(None) + '\n      ' + m.group(2)
# Эта операция сложная, проще пересобрать index
# Сделаем проще — читаем существующие card-элементы и добавляем новые

cards_block = ''
for slug, title in all_nav:
    if slug == 'index.html':
        continue
    # Находим описание для новых разделов
    desc = title
    for sec in NEW_SECTIONS:
        if sec['slug'] == slug:
            desc = sec['desc']
            break
    # Для существующих пытаемся прочитать desc из карточек
    if desc == title:
        # Поищем в старом index
        m = re.search(
            rf'<a href="{slug}\.html" class="card">\s*<h3>[^<]*</h3>\s*<p>([^<]*)</p>',
            index_content
        )
        if m:
            desc = m.group(1)

    cards_block += f'''      <a href="{slug}.html" class="card">
        <h3>{title}</h3>
        <p>{desc}</p>
      </a>\n'''

# Регенерируем index.html
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

index_html = INDEX_TPL.format(
    nav_items=make_nav(None),
    cards=cards_block
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_html)

# ── Обновление всех существующих страниц (навигация) ──
for slug, title in existing:
    path = os.path.join(OUT, f'{slug}.html')
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Замена навигации
    content = re.sub(
        r'(<nav class="sidebar">.*?<ul>).*?(</ul>)',
        lambda m: m.group(1) + '\n' + make_nav(slug) + '\n      ' + m.group(2),
        content,
        flags=re.DOTALL
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f'\nГотово. Всего разделов: {len(all_nav)}')
print(f'Новых страниц: {len(NEW_SECTIONS)}')

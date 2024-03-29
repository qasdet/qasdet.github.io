---
title: Оператор выбора в Python (if else)
layout: post
date: '2021-11-07 21:33:18'
categories:
- Python
---

![](https://pythonchik.ru/pic/lb1/cover_04600fd5-2ec8-4a15-9a33-ace71e5e89b5_big.jpeg)

**Зачем нужны условные инструкции**

Фундаментальная важность условий для любого из языков программирования заключается в их возможности описывать большую часть логики работы программы.

> `Говоря простыми словами, конструкция if else в Python указывает интерпретатору, следует ли выполнять определенный участок кода или нет`.

Как и все прочие составные инструкции языка, оператор выбора также поддерживает свойство вложенности. Это означает, что использование `if else` позволяет создавать внутри программного модуля так называемое логическое ветвление.

**Как работает if else**

Синтаксис

Оператор `if else` в языке Python — это типичная условная конструкция, которую можно встретить и в большинстве других языков программирования.

самый простой пример, где есть всего одно условие
{% highlight python %}
a = 1
if a == 1:
    print("It is true")
 
#=> It is true
{% endhighlight %}

Синтаксически конструкция выглядит следующим образом:

1. сначала записывается часть `if` с условным выражением, которое возвращает истину или ложь;
2. затем может следовать одна или несколько необязательных частей `elif `(в других языках вы могли встречать `else if`);
3. Завершается же запись этого составного оператора также необязательной частью else.

![](https://pythonchik.ru/pic/lb1/intext_45b0e9fc-ff4e-4c43-981e-b0fd60273af0_original.svg)


**Принцип работы оператора выбора в Python**

{% highlight python %}
count = 1
#условное выражение может быть 
#сколь угодно сложным, 
#и может быть сколь угодно elif-частей
if True and count == 1 and count == 2:
    print("if")
elif count == 'count':
    print("First elif")
elif count == 14.2:
    print("Second elif")
elif count == 1:
    print("Nth elif")
else:
    print("Else")

> Nth elif
{% endhighlight %}

Для каждой из частей существует ассоциированный 
с ней блок инструкций, которые выполняются в случае 
истинности соответствующего им условного выражения.

{% highlight python %}
b = 10
if b == 10:
    #любое количество инструкций
    print(b)
    b = b * 15
    b = b - 43
    b = b ** 0.5
    print(b)
elif b == 20:
    print("You will not see me")
else:
    print("And me")

> 10
> 10.344080432788601
{% endhighlight %}


То есть интерпретатор начинает последовательное выполнение программы, доходит до`if` и вычисляет значение сопутствующего условного выражения. Если условие истинно, то выполняется связанный с if набор инструкций. После этого управление передается следующему участку кода, а все последующие части elif и часть `else` (если они присутствуют) опускаются.
Отступы

Отступы — важная и показательная часть языка Python. Их смысл интуитивно понятен, а определить их можно, как размер или ширину пустого пространства слева от начала программного кода.

{% highlight python %}
#начало кода
#код
#код
#код
    # начало первого отступа
    # первый отступ
    # первый отступ
        # начало второго отступа
        # второй отступ
        # второй отступ
        # конец второго отступа
   #конец первого отступа
	{% endhighlight %}
	
Благодаря отступам, python-интерпретатор определяет границы блоков. Все последовательно записанные инструкции, чье смещение вправо одинаково, принадлежат к одному и тому же блоку кода. Конец блока совпадает либо с концом всего файла, либо соответствует такой инструкции, которая предшествует следующей строке кода с меньшим отступом.

{% highlight python %}
var_a = 5
var_b = 10
var_c = 20
if var_c**2 > var_a * var_b:
    # блок №1
    if var_c < 100:
        # блок №2
        if var_c > 10:
            # блок №3
            var_a = var_a * var_b * var_c
        # блок №2
        var_b = var_a + var_c
    # блок №1
    var_c = var_a - var_b
print(var_a)
print(var_b)
print(var_c)

> 1000
> 1020
> -20
{% endhighlight %}

Таким образом, с помощью отступов появляется возможность создавать блоки на различной глубине вложенности, следуя простому принципу: чем глубже блок, тем шире отступ.

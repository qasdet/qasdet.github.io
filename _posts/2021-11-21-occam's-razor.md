---
title: 'Бритва Оккама: как QA принимать быстрые и правильные решения?'
layout: page
date: '2021-11-21 18:03:14'
categories:
- Python
- QA
---

«Эра цифровой революции требует быстрых решений от лидов и их сотрудников. Тестировщики часто рассматриваются как «узкое место» в процессах Agile и DevOps, несмотря на все последние достижения в индустрии автоматизации тестов. Скорость принятия решений сейчас требуется от каждого в команде, и при этом важно, чтобы эта скорость не оказывала негативного влияния на качество решений. Как профессионал-тестировщик, ты делаешь сотни решений каждый день и можешь этого не замечать. Твои решения влияют на твой личный успех, и на успех всей команды. Некоторые твои решения могут влиять на всю компанию», говорит глава QA-отдела в компании MoEngage, доставляющей около миллиарда рекламных сообщений в месяц.

«Жизнь кажется сложной, если приходится долго размышлять над каждым решением. Кто бы что не говорил, наш мозг способен обрабатывать лишь часть информации с должным вниманием. Существуют ограничения, и это хорошо что наш мозг приспособлен избегать перегрузки избыточной информацией. Он автоматически выбирает пути решений, предполагающие минимум усилий. Осознанно или нет, мы “срезаем путь”, это экономит время и, иногда, приносит хороший результат.

Ниже обсудим, как тестировщики могут делать быстрые эффективные решения, вспомнив о таком философском феномене, как “Бритва Оккама”.

**Что это?**
“Бритва Оккама”, или “философская бритва” — это умственный “шорткат”, одно из главных правил, позволяющих устранить ненужные объяснения в каком-то философском вопросе. Это отличная вещь для развития критического мышления. Такие “ментальные модели” помогают отсечь логические выводы, имеющие низкую вероятность оказаться правильными, чтобы освободить свои умственные ресурсы для рассмотрения проблемы в целом.

Бритва Оккама — это философская модель, помогающая получить:

1. удовлетворительное решение 
2. быстро
3.  и с минимальным умственным трудом.

Ниже рассмотрим применение Бритвы Оккама в тестировании софта, его автоматизации, и смежных областях разработки.

**Итак, режем**
В XIV столетии английский философ Уильям Оккам сформулировал принцип: 

**“Не стоит без нужды умножать сущности.”**

Другими словами, 

**“Простейшее объяснение часто является самым правильным.”**

Имея дело с множеством конкурирующих гипотез какой-то проблемы, выбирай то, в котором меньше всего допущений. Это правило применимо в многих ситуациях, когда нужно принимать быстрые решения при минимуме информации. **Бритва Оккама дает приоритет простоте над сложностью,** если не доказано что сложность необходима. Детективы, доктора, и ученые применяют этот принцип в своей работе, когда ищут решения, «отрезая» сложные предположения.

Представим, что ты тестируешь приложение, которое создает рекламные кампании по email. Находишь баг. Разбираешься. Оказывается, какая-то сторонняя библиотека внезапно перестала работать. Твоя команда не выдавала релиз уже две недели. Ты в первую очередь инженер, поэтому ты действуешь проактивно: расследуешь почему это случилось, перед тем как завести баг. Размышляешь: а какая самая вероятная причина бага?

1. **Предположение 1.** Кто-то хакнул приложение и специально вставил баг.
2. **Предположение 2.** Проблема возникла из-за неожиданного скачка трафика. Надо провести тест производительности и пробовать воспроизвести баг.
3. **Предположение 3.** Библиотека-редактор выпустила релиз прошлой ночью (как следует из их release notes), в этом-то и проблема.

> "Сколько раз я говорил вам, отбросьте все невозможное,  то  что
> останется, и будет ответом,  каким  бы  невероятным  он  ни  казался."
> Артур Конан Дойл

Бритва Оккама легко отсекает первое и второе предположения, и «запускает расследование» по третьему — поскольку оно самое простое, в нем меньше всего неправдоподобных допущений, и оно основано на здравом смысле, очевидности.

Предположения 1 и 2 также возможны — сугубо теоретически — но имеет смысл начинать дебаг, пользуясь лишь Предположением 3. Всегда начинай с простейшего предположения, и продолжай отсекать лишнее, продвигаясь к корню проблемы. Это сохраняет время и усилия. Многие из тестировщиков, сугубо из накопленного опыта, умеют отследить корень проблемы пользуясь этим принципом, даже никогда его не встретив в сформулированной форме. А осознанное применение этого принципа делает тестировщика более зрелым в профессиональном плане.

**Примечание.**  Если предположение простое, оно не обязательно во всех 100% правильное. Простейшее предположение должно основываться на всех доступных данных.

В ИТ-индустрии существует более практическое и приближенное к ИТ изложение этого принципа — называется KISS (“Keep It Simple, Stupid” = “`Делай проще, тупица`”). 

* Делай свои автотесты простыми, насколько это возможно. Убедись, что их код прост и хорошо структурирован. Избегай сложности и того что называется “over-engineering”. Жизнь будет проще, и для тебя, и для команды. Помни, что удерживать простоту не так легко, она требует хорошего планирования, и постоянного улучшения.

* При выборе фреймворка автоматизации и дополнительных инструментов руководствуйся принципом: чем проще, тем лучше. Простые инструменты позволяют создавать и обслуживать наборы тестов с удобной кривой обучаемости.

* Рост сложности означает рост стоимости обслуживания, и, неизбежно, рост количества багов. К примеру, если проект очень простой, и есть возможность использовать простые вещи, например платформу типа TestProject поддерживаемую сообществом тестировщиков, то, может быть, не стОит использовать серьезные вещи (например Selenium или Appium). 

Бритва Оккама применима также в следующих сферах:

**Управление проектами.** Не стоит усложнять вещи, поддерживай минимум процессов. Поощряй команду выбирать только релевантные процессы, действительно необходимые. Лишние процессы затруднят деятельность команды. Регулярно проверяй процессы, устраняй лишние, не повышающие стоимость продукта. Методики Agile и Lean созданы для простоты и инноваций, и они работают «по бритве Оккама».
**Управление продуктами.** Минимизируй функции. Добавляй “фичи” лишь если они действительно ценны для клиентов. Не делай продукт сложным — это отталкивает клиента.

![](https://testengineer.ru/wp-content/uploads/2021/11/ms-word.jpg)

**Дизайн интерфейсов.** Выше — пример. Сосредоточься на простых пользовательских интерфейсах. Твоя цель — простота. Надо понимать, что простой интерфейс привлекает клиентов. Попробуй экспериментировать с А/B-тестированием, мультивариантным тестированием, чтобы понять, что реально нравится клиентам.

**Документация API (и документация в целом).** Вместо бомбардировки пользователей избыточной информацией, пиши простые и ясные доки по API. Разработчики любят работать с API только если документация на высшем уровне, и API легко освоить.

**Коммуникация.** Будь прост в общении. Критически важно доносить правильные вещи правильным людям. Например, имея дело с представителями заказчика, рассказывай о проекте с точки зрения бизнеса и функциональности. Старайся не вдаваться в технические детали. Понимай свою аудиторию, говори с людьми на их языке.

**Итак:**
Поддерживать простоту — еще та задача. Но она приводит к успеху. Всегда выбирай решение простейшее из возможных. Выбирай архитектуру, дизайн, рабочий процесс, технологию, фреймворк, инструмент, исходя из их простоты. Помни о Бритве Оккама, разрабатывая автотесты и когда ищешь причину критикал-бага. Это важный инструмент, которым тестировщик должен “резать” несущественные предположения. Так достигается быстрота, и обеспечивается качество.»
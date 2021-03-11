---
title: Настройка LACP на Distributed Switch в VMware vSphere
layout: post
date: '2021-03-11 20:58:19 +0300'
categories:
- VMWare
- Switch
- LACP
---

Настройка LACP на Distributed Switch в VMware vSphere
Выполняем настройку групп агрегации каналов (Link Aggregation Groups) с использованием LACP на распределённом коммутаторе vSphere (vSphere Distributed Switch)

В данной статье мы рассмотрим пример настройки агрегации для VMware vSAN.

Агрегация каналов позволяет объединять несколько сетевых подключений параллельно для увеличения пропускной способности и обеспечения избыточности. Когда группирование сетевых адаптеров настроено с помощью LACP, происходит распределение нагрузки сети vSAN по нескольким аплинкам. Однако это происходит на сетевом уровне, а не через vSAN.

Ознакомиться с общей информацией об агрегировании каналов можно в одной из моих статей про Агрегирование каналов Cisco

В то время как объединение каналов является очень свободным термином, для целей этой статьи основное внимание будет уделяться протоколу управления объединением каналов или LACP. В то время как IEEE имеет свой собственный стандарт LACP 802.3ad, некоторые производители разработали проприетарные типы LACP. Например, PAgP (протокол агрегации портов) похож на LAG, но является собственностью Cisco. Таким образом, руководство поставщика имеет решающее значение, и следует всегда придерживаться лучших практик поставщиков.

Основным выводом при реализации LACP является то, что он использует отраслевой стандарт и реализован с использованием port-channel. Там может быть много алгоритмов хеширования. Политика группы портов vSwitch и конфигурация канала порта (хэш) должны совпадать и соответствовать.

Добавляем LAG
Переходим в наш распределённый коммутатор и создаём новую группу агрегации. Указываем имя, количество портов агрегации, режим работы, а так же режим балансировки.

![](https://bogachev.biz/2020/04/05/nastroyka-lacp-na-distributed-switch-v-vmware-vsphere/001.png)

Активный режим (Active) - устройства немедленно отправляют сообщения LACP, когда порт подходит. Конечные устройства с включенным LACP отправляют/получают кадры, называемые сообщениями LACP, друг другу для согласования создания LAG.

Пассивный режим (Passive) - переводит порт в состояние пассивного согласования, в котором порт отвечает только на полученные сообщения LACP, но не инициирует согласование.

Обратите внимание, что если хост и коммутатор находятся в пассивном режиме, LAG не будет инициализирован, так как нет активной части, которая инициировала бы соединение.

Назначаем LAG для PortGroup
Назначаем созданную группу агрегации необходимой порт группе и переводим LAG в режим ожидания (Standby).

![](https://bogachev.biz/2020/04/05/nastroyka-lacp-na-distributed-switch-v-vmware-vsphere/002.png)

При подтверждение изменений появится предупреждающее окно, о том, что использование комбинации активных аплинков и LAG в режиме ожидания поддерживается только для переноса физических адаптеров между LAG и автономными аплинками. Нажимаем ОК.

Проверяем, что LAG добавился.

![](https://bogachev.biz/2020/04/05/nastroyka-lacp-na-distributed-switch-v-vmware-vsphere/003.png)

Настраиваем адаптеры на хостах
Переходим в меню “Добавление и редактирование хостов” нашего распределённого коммутатора, выбираем пункт “Редактирование хостов”, добавляем хосты, которые подключены к данному distributed switch.

Назначаем LAG-порты к соответствующим vmnic. По аналогии назначаем порты для других хостов.

![](https://bogachev.biz/2020/04/05/nastroyka-lacp-na-distributed-switch-v-vmware-vsphere/004.png)

Создаём PortChannel на Cisco
Тема конфигурации PortChannel затронута в одной из моих статей по настройке объединения портов (bonding) Cisco IOS и CentOS LACP

Рассмотрим пример нашего тестового стенда:

```
4900m(config)# interface range TenGigabitEthernet1/1-2
4900m(config-if-rang)# shutdown
4900m(config-if-rang)# channel-group 2 mode active
Creating a port-channel interface Port-channel 2
4900m(config-if-range)# no sh

interface Port-channel2
 description slv-esxi01[vSAN-LAG]
 switchport
 switchport access vlan 2
 switchport mode access
 spanning-tree portfast trunk
 spanning-tree bpdufilter enable

interface TenGigabitEthernet1/1
 description slv-esxi01[vSAN-LAG]_Uplink1
 switchport access vlan 2
 switchport mode access
 channel-group 2 mode active
 spanning-tree portfast trunk
 spanning-tree bpdufilter enable

interface TenGigabitEthernet1/2
 description slv-esxi01[vSAN-LAG]_Uplink2
 switchport access vlan 2
 switchport mode access
 channel-group 2 mode active
 spanning-tree portfast trunk
 spanning-tree bpdufilter enable
```

Проверьте какой алгоритм балансировки используется на физическом коммутаторе.

```
4900m#sh run all | i load-balance
port-channel load-balance src-dst-ip
```

Проверяем состояние PortChannel.

```
C4900m#show etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        R - Layer3      S - Layer2
        U - in use      f - failed to allocate aggregator

        M - not in use, minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port


Number of channel-groups in use: 4
Number of aggregators:           4

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
2      Po2(SU)         LACP      Te1/1(P)    Te1/2(P)    
3      Po3(SU)         LACP      Te1/3(P)    Te1/4(P)    
4      Po4(SU)         LACP      Te1/5(P)    Te1/6(P)    
5      Po5(SU)         LACP      Te1/7(P)    Te1/8(P)
```

Переводим LAG в активный режим
Возвращаемся к настройкам нашего распределённого коммутатора, переходим в настройки порт группы и переводим LAG в режим Active, а автономные аплинки - в раздел неиспользуемых.

![](https://bogachev.biz/2020/04/05/nastroyka-lacp-na-distributed-switch-v-vmware-vsphere/005.png)


Обратите внимание, что когда LAG выбран, как основной аплинк, режим балансировки порт группы наследуется от режима балансировки, указанного в LAG, о чём нас дополнительно информируют.

Ещё раз проверяем топологию сети.

![](https://bogachev.biz/2020/04/05/nastroyka-lacp-na-distributed-switch-v-vmware-vsphere/007.png)


 [Источник](https://docs.vmware.com/en/VMware-vSphere/6.0/com.vmware.vsphere.networking.doc/GUID-0D1EF5B4-7581-480B-B99D-5714B42CD7A9.html)

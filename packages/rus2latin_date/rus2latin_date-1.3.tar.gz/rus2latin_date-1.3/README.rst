====================================================================
 Пакет для конвертирования русской даты в дату по римскому календарю
====================================================================

Пакет умеет конвертировать русскую дату в дату по римскому календарю. Например, 24 марта => ante diem IX Kalendas Apriles.

Установка
============

Как обычно, с pip

::

    pip install rus2latin_date


Использование
==============

::

    >>> from rus2latin_date import Converter
    >>> c = Converter()
    >>> c.conv("28 февраля 2012")
    'ante diem III Kalendas Martias'
    >>> c.conv("24 марта")
    'ante diem VIIII Kalendas Apriles'
    >>> c.conv("15-11-1983")
    'ante diem XVII Kalendas Decembres'
    >>> c.conv("26.5.1900")
    'ante diem VII Kalendas Iunias'

Источники
==============

* `Латинский календарь <https://telegra.ph/Latinskij-kalendar-09-03-2>`_
* `Index dierum calendarii Romani <https://la.wikipedia.org/wiki/Index_dierum_calendarii_Romani>`_

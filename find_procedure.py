#!/usr/bin/env python
# -*- coding: utf-8 -*-

# заготовка для домашней работы
# прочитайте про glob.glob
# https://docs.python.org/3/library/glob.html

# Задание
# мне нужно отыскать файл среди десятков других
# я знаю некоторые части этого файла (на память или из другого источника)
# я ищу только среди .sql файлов
# 1. программа ожидает строку, которую будет искать (input())
# после того, как строка введена, программа ищет её во всех файлах
# выводит список найденных файлов построчно
# выводит количество найденных файлов
# 2. снова ожидает ввод
# поиск происходит только среди найденных на этапе 1
# 3. снова ожидает ввод
# ...
# Выход из программы программировать не нужно.
# Достаточно принудительно остановить, для этого можете нажать Ctrl + C

# Пример на настоящих данных

# python3 find_procedure.py
# Введите строку: INSERT
# ... большой список файлов ...
# Всего: 301
# Введите строку: APPLICATION_SETUP
# ... большой список файлов ...
# Всего: 26
# Введите строку: A400M
# ... большой список файлов ...
# Всего: 17
# Введите строку: 0.0
# Migrations/000_PSE_Application_setup.sql
# Migrations/100_1-32_PSE_Application_setup.sql
# Всего: 2
# Введите строку: 2.0
# Migrations/000_PSE_Application_setup.sql
# Всего: 1

# не забываем организовывать собственный код в функции
# на зачёт с отличием, использовать папку 'Advanced Migrations'
import Profiler
import glob
import os
from ClassSearcher import MySearcher
import ClassSearcher
import time

migrations = 'Migrations'
migrations = 'Advanced Migrations'

files = glob.glob(os.path.join(migrations, "*.sql"))

searcher = MySearcher()  # осеществляет поиск (движек)

# Программа по умолчанию
while True:
    pattern_text = input("Введите исковую строку: ")
    if pattern_text == "":
        print("Строка не должна быть пустой!")
        break
        continue
    begin_time = time.time()
    files = [file for file in files if searcher.is_containts(file, pattern_text)]
    end_time = time.time()
    for file in files:
        print(file)
    print("Всего файлов: %d" % len(files))
    print("Время поиска %f сек" % (end_time - begin_time))


# Тут многопоточная программа реализующая многопоточность (на случай если файлов очень много, и в системе несколько логических ядер)
import multiprocessing

count_cores = multiprocessing.cpu_count()

searcher = ClassSearcher.MySearcher(threads_count=count_cores)

if searcher == 1:
    print("Многопоточная программа не будет запущена!")
    exit()

while True:
    pattern_text = input("Введите исковую строку: ")
    if pattern_text == "":
        print("Строка не должна быть пустой!")
        continue
    begin_time = time.time()
    files = searcher.fast_search(files, pattern_text)
    end_time = time.time()
    for file in files:
        print(file)
    print("Всего файлов: %d" % len(files))
    print("Время поиска %f сек" % (end_time - begin_time))


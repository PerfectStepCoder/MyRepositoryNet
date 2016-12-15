#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


def execution_time(fun, data):
    """
    Запуск функции и подсчет времени ее отработки над данными
    :param fun:
    :param data:
    :return:
    """
    begin_time = time.time()
    result = fun(data)
    end_time = time.time()
    return result, end_time - begin_time

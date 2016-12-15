#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from queue import Queue
import multiprocessing


class MySearcher(object):
    """
    Ищет в текстовых файлах информацию
    """
    def __init__(self, threads_count=1):
        self.pool = None
        if threads_count > 1:
            self.pool = ThreadPool(threads_count)  # пул потоков

    def is_containts(self, path_to_file, pattern_text):
        """
        Содержиться ли тектовый паттерн в файле
        :param path_to_file:
        :param pattern_text:
        :return:
        """
        file = open(path_to_file, 'r')
        text = file.read()
        if str.upper(pattern_text) in str.upper(text):  # регистронезависимый поиск
            return True
        else:
            return False

    def fast_search(self, lits_path_files, pattern_text):
        result = []
        for file in lits_path_files:
            self.pool.add_task(self.is_containts, file, pattern_text, result)
        self.pool.wait_completion()
        return result


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, path_to_file, pattern_text, result):
        """ Add a task to the queue """
        self.tasks.put((func, path_to_file, pattern_text, result))

    # def map(self, func, args_list):
    #     """ Add a list of tasks to the queue """
    #     for args in args_list:
    #         self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks  # ссылка на очередь с дадачами
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, path_to_file, pattern_text, result = self.tasks.get()  # смотрим есть ли в очереди задачи
            try:
                if func(path_to_file, pattern_text):
                    result.append(path_to_file)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


if __name__ == "__main__":
    from random import randrange
    from time import sleep

    # Function to be executed in a thread
    def wait_delay(d):
        print("sleeping for (%d)sec" % d)
        sleep(d)

    # Generate random delays
    delays = [randrange(3, 7) for i in range(50)]

    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(5)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map(wait_delay, delays)
    pool.wait_completion()
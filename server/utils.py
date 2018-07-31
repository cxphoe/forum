import time


def log(*args, **kwargs):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


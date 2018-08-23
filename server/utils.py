import time


def log(*args, **kwargs):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        # log 到文件，在服务器运行时可以用来查看
        print(formatted, *args, file=f, **kwargs)


def copy_attrs(attrs, src):
    d = {}
    for a in attrs:
        d[a] = getattr(src, a)
    return d

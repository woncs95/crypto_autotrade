import sys

def raise_error():
    raise TypeError

def error_handle():
    try:
        raise_error()
    except TypeError as t:
        print(t.args)

error_handle()
import time

def waitseconds(seconds):
    starttime = time.clock()

    while True:
        yield None

        if time.clock() - starttime >= seconds:
            return
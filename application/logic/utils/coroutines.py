import time

def waitseconds(seconds):
    starttime = time.time()

    print("I need to wait "+str(seconds))
    while True:
        yield None

        diff = time.time() - starttime

        if  diff >= seconds:
            return
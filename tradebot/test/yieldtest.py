i=0
def some():
    while True:
        if i%2==0:
            result = i+1000
            yield result
        print(result+3)
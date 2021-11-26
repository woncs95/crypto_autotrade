from concurrent.futures import ThreadPoolExecutor


def f(a, b):
    return a+b


with ThreadPoolExecutor() as executor:
    for el1 in range(1,10):
        el2=1
        submitted = executor.submit(f, el1, el2)
        el2 +=1
    print(submitted.result())
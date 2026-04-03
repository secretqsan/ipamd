configure = {
    "type": "function",
    "schema": ['test'],
    "resource": []
}
def func(*args, **kwargs):
    print(kwargs, args)
from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.Neo.Storage import Get, Put, GetContext

def Main(op, args):
    context = GetContext()
    key = 'key'

    if op == 'get':
        value = Get(context, key)
        Notify(["read from storage", value])
        return value

    if op == 'put':
        if len(args) == 0:
            Notify("i have no value to put")
            return False
        Put(context, key, args[0])
        return True


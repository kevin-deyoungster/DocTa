def addOne(item):
    return item + 1


def addTwo(item):
    return item + 2


def removeOne(item):
    return item - 1


def multiplyTwo(item):
    return item * 2


def start():
    functions = [addOne, addTwo, removeOne, multiplyTwo]
    temp = 1
    for function in functions:
        temp = function(temp)
    print(temp)


start()

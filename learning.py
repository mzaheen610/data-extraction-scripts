import pandas as pd
import cProfile

dict = {
    "name": "John",
    "age": 23,
    "place": "New York",
    "height": 189
}

series =  pd.Series(dict)

print(series)

def my_function():
    result = 0
    for i in range(1000000):
        result += i
    return result

cProfile.run('my_function()')

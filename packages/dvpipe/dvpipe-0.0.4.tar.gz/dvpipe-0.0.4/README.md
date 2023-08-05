# dvpipe

> A small Python utility for piping data from function to function in sequential order.

dvpipe allows you to pass data from function to function sequentially as you would in
tradional method chaining. You can use dvpipe to transform any type of data not
just DataFrames as with [DataFrame.pipe()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html)

![Version](https://img.shields.io/pypi/v/dvpipe)
![License](https://img.shields.io/github/license/chrisdiana/dvpipe.svg)

### Installation
```
$ pip install dvpipe
```

### Usage
```python
processed_data = pipe(data, func_a, func_b, func_c, ...)
```

### Example
```python
from dvpipe import pipe

data = (pipe(data,
             clean,
             transform,
             aggregate))
```

### Why?
dvpipe attempts to help solve this classic problem seen in many data tranformation applications to allow for cleaner, more understandable code.

```python
data = clean(data)
data = transform(data)
data = aggregate(data)
```

### Functions with Arguments
Use Python tuples for functions with parameters.
```python
df = pipe(df, (replace_foo, 'bar'))
```

### Full Example
```python
from dvpipe import pipe

raw_data = {'foo': 1, 'bar': 2}

def subtract_foo(data):
    data['foo'] = data['foo'] - 1
    return data

def add_bar(data):
    data['bar'] = data['bar'] + 1
    return data

def add_entry(data, entry):
    data.update(entry)
    return data

data = (pipe(raw_data,
             subtract_foo,
             add_bar,
             (add_entry, {'foobar': 5})))
```



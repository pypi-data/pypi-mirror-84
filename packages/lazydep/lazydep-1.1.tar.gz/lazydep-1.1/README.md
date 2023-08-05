# lazydep

Evaluates some set of functions, according to tome dependency graph structure


There's pretty much 1 function that is worth noting:

```python
lazydep.resolve(graph, state, functions, request=None)
```


### Arguments
* graph: dictionary, mapping function names to the names of parameters required for their execution
* state: dictionary, initial input to functions. the remainder of intermediary parameters will be bootstrapped
* functions: list of functions in any order, or dictionary mapping function names to functions
* request: name of desired function evaluation. If request is specified, only the desired function call will be returned. If left empty, all functions specified will be returned, in the same form as state object.

### Returns
dictionary, or result of 'request' function



## Example
```python


# Each key here corresponds to a function name
# Once evaluated, a function's return value is stored as a key as its name
depGraph = {

	# Once we specify seed, all else will be inferred
    'f1': 'seed',
    'f2': 'f1',
    'f3': ['f1','f2'],

	# Function unused. If we only request 'f3', these will never be evaluated
    'f4': 'f3',
    'f5': 'f6',
    'f6': 'seed'
}



# Functions will receive parameters according to the dependency graph
# Keyword args only, positional args not supported
def f1(seed):
    return seed % 10

def f2(f1):
    return [f1]*f1

def f3(f1, f2):
    return (f1,sum(f2))




# The initial information, some set of named parameters.
istate = {'seed': 42}


res = lazydep.resolve(

	# How are inputs and outputs reordered?
	graph = depGraph,

	# What information are we working with?
	state = istate,

	# What functions are allowed?
	functions = [f1,f2,f3],

	# Which function output are we requesting?
	# If request == None, we will return the aggregate state, after running all functions
	request = 'f3',
)

assert( res == (2,4) )


```




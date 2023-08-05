
__all__ = ='resolve'




def pruneGraph (graph, root=None):
	'''Returns a cut graph, with request as parent
	Note- mutates graph, so it might be smart to pass in a copy
	'''
	cutTree = {}
	
	if root is None or root not in graph.keys():
		return {}
	
	children = graph.get(root)
	if root is not None:
		cutTree[root] = children
	
	del graph[root]
	
	if not isinstance(children,list):
		children = [children]
	
	for child in children:
		cutTree.update(pruneGraph(graph,child))
		
	return cutTree
	
	
	
	
	

def whichResolve (graph, state, request=None):
	'''Decides which function to evaluate next, given what's available
	Returns: string, name of function
	'''
	preComputed = set(list(state.keys()))	
	
	# Only make essential function calls
	graph = pruneGraph(graph.copy(), request)
	
	for k, v in graph.items():
		if not isinstance(v, list):
			v = [v]
		if set(v) <= preComputed:
			return k
	raise RuntimeError('Not enough information to evaluate any function')
	
	
	
		
	

def resolve(graph, state, functions, request=None):
	'''Evaluates some set of functions, according to tome dependency graph structure
	
	Arguments:
		graph: dictionary, mapping function names to the names of parameters required for their execution
		state: dictionary, initial input to functions. the remainder of intermediary parameters will be bootstrapped
		functions: list of functions in any order, or dictionary mapping function names to functions
		request: name of desired function evaluation. If request is specified, only the desired function call will be returned. If left empty, all functions specified will be returned, in the same form as state object.
		
	Returns:
		dictionary, or result of 'request' function
	'''
	myGraph = graph.copy()
	
	if isinstance(functions,list):
		functions = { f.__name__:f for f in functions }
	
	if request is None:
		cond = lambda x: x != {}
	else:
		cond = lambda x: request in x.keys()
	
	while cond(myGraph):
		f = whichResolve(myGraph, state, request)

		argsNeeded = myGraph[f]
		if not isinstance(argsNeeded, list):
			argsNeeded = [argsNeeded]

		argsHave = { x:state[x] for x in argsNeeded }

		state[f] = functions[f](**argsHave)

		del myGraph[f]
		
	if request is None:
		return state
	else:
		return state[request]
	

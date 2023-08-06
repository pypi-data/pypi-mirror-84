'''
nothing in this file is used. it's a place for development of other ideas.
'''


'''
in thinking about a way to quickly or easily make facts out of functions,
I thought maybe we'd make a decorator, but probably not, it runs everytime
the function is run. we really want a way to compile them on import, so
it'll be more custom per project I think.
from factum import DataFact, Fact
# this is a decorator. use like this
# @as_fact(facts_list_object, ...)
# def test_something(): ...
def as_fact(
    facts: object,
    name: str = None,
    inputs: '([], {})' = None,
    kind: str = 'Fact'
):
    def for_resolution(func):
        def inside(*args, **kwargs):
            if kind == 'Fact':
                facts.add(Fact(transformation=func, inputs=inputs, name=name))
            elif kind == 'DataFact':
                facts.add(Fact(transformation=func, params=(args, kwargs), name=name))
            fact = Fact
            results = func()
            print(results)
            func()
        return inside
    return for_resolution
'''

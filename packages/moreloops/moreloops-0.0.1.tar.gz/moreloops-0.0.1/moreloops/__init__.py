### IMPORTS                 ###
    ## Dependencies             ##
import decorate_all_methods
import docifyPLUS
    ## Dependencies             ##
import abc
import collections.abc
import typing
### IMPORTS                 ###
### CONSTANTS               ###
Nothing = lambda: None
LOOPS   = (
    "while", "until",   # infinite loops
    "for", "foreach", "repeat", "transfer"  # finite loops
)
### CONSTANTS               ###
### CLASSES                 ###
    ## Base Loops               ## 
class Loop(object):
    """
    Base class for all loop types
    """
        # abstract class methods    #
    @classmethod
    def oneline(cls): pass
        # abstract class methods    #
@decorate_all_methods.decorate_all_methods(abc.abstractmethod, [])
class _InfiniteLoop(Loop, abc.ABC):
        # abstract methods          #
    def __init__(
        self,
        condition: str,
        code: collections.abc.Callable,
        do: collections.abc.Callable,
        else_: collections.abc.Callable
        ): pass
    def __enter__(self): pass
    def __exit__(self, *args, **kwargs): pass
        # abstract methods          #
@decorate_all_methods.decorate_all_methods(abc.abstractmethod, ['oneline'])
class _FiniteLoop(Loop, abc.ABC):
        # abstract methods          #
    def __init__(
        self,
        condition: str,
        code: collections.abc.Callable,
        do: collections.abc.Callable,
        else_: collections.abc.Callable
        ): pass
    def __enter__(self): pass
    def __exit__(self, *args, **kwargs): pass
        # abstract methods          #
    ## Base Loops               ##
class _Loops(object):
    ## Infinite Loops           ##
    class While(_InfiniteLoop):

        __variables = {}       # dictionary 
        __exections = []       # all expressions and statements to exec
        __code_body = []       # the code block inside the with statement

        @classmethod
        def execute(cls, expr): cls.__add_code(expr)
        @classmethod
        def declare(cls, name, expr): cls.__add_variable((name, expr))

        def __init__(self, condition, do, else_, vars_={}):
            self.__cond = condition
            self.__do   = do
            self.__else = else_
            self.__vars = vars_

        def __enter__(self): self.__do(); return self   # call do and return instance
        def __exit__(self, *args, **kwargs):
            while eval(self.__cond, {}, self.__vars): exec(
                "\n".join(self.__code_body),
                {},
                self.__vars
            )
            self.__else()   # call else

        # for adding stuffs to collections
        @classmethod
        def __add_code(cls, expr): cls.__code_body.append(expr)
        @classmethod
        def __add_variable(cls, kv_pair): cls.__variables[kv_pair[0]] = kv_pair[1]
    class Until(_InfiniteLoop):

        __variables = {}       # dictionary 
        __exections = []       # all expressions and statements to exec
        __code_body = []       # the code block inside the with statement

        @classmethod
        def execute(cls, expr): cls.__add_code(expr)
        @classmethod
        def declare(cls, name, expr): cls.__add_variable((name, expr))

        def __init__(self, condition, do, else_, vars_={}):
            self.__cond = condition
            self.__do   = do
            self.__else = else_
            self.__vars = vars_

        def __enter__(self): self.__do(); return self   # call do and return instance
        def __exit__(self, *args, **kwargs):
            while not eval(self.__cond, {}, self.__vars): exec(
                "\n".join(self.__code_body),
                {},
                self.__vars
            )
            self.__else()   # call else

        # for adding stuffs to collections
        @classmethod
        def __add_code(cls, expr): cls.__code_body.append(expr)
        @classmethod
        def __add_variable(cls, kv_pair): cls.__variables[kv_pair[0]] = kv_pair[1]
    ## Infinite Loops           ##
    ## Finite Loops             ##
    class For(_FiniteLoop): pass
    class ForEach(_FiniteLoop): pass
    class Repeat(_FiniteLoop): pass
    class Transfer(_FiniteLoop): pass
    ## Finite Loops             ##
### CLASSES                 ###
### FUNCS                   ###
    ## Infinite Loops           ##
def while_(
    bool_expr: str,     # a bool expression which will be evaluated using eval every loop
    do: collections.abc.Callable=Nothing,   # code called at the start of loop
    else_: collections.abc.Callable=Nothing,     # code called at the end of the loop
    oneline: bool=False,    # bool determining returning with-statement or value
    vars_=[]
    ):
    # if the user wants a line loop, return the res else return a c-manager
    return _Loops.While.oneline() if oneline else _Loops.While(
        bool_expr,
        do, else_,
        vars_
    )
def until(
    bool_expr: str,     # a bool expression which will be evaluated using eval every loop
    do: collections.abc.Callable=Nothing,   # code called at the start of loop
    else_: collections.abc.Callable=Nothing,     # code called at the end of the loop
    oneline: bool=False,    # bool determining returning with-statement or value
    vars_=[]
    ):
    # if the user wants a line loop, return the res else return a c-manager
    return _Loops.Until.oneline() if oneline else _Loops.Until(
        bool_expr,
        do, else_,
        vars_
    )
    ## Infinite Loops           ##

def loop(
    loop_type: str,
    do: collections.abc.Callable=Nothing,
    else_: collections.abc.Callable=Nothing,
    oneline: bool=False,
    **kw
    ) -> Loop:
    """
    Input any loop_type in the loop_type parameter as a string as well as any additional
    paramters (**kw, do, else_, oneline) and the function will return a call to the
    loop_type given

    If the loop_type is invalid, an Exception will be raised
    """
    loop_type = loop_type.lower()   # normalize
    # kw gets:
    vars_ = {} if kw.get('vars_') == None else kw.get('vars_')
    inf_args = (kw['bool_expr'], do, else_, oneline, vars_)

    for l in LOOPS:
        if l == 'while': return while_(*inf_args)
        elif l == 'until': return until(*inf_args)
    else: pass      # raise exception LoopTypeInvalid
### FUNCS                   ###
### DOCUMENTATION           ###
docifyPLUS.document(
    while_,
    """
    Alternate syntax for a while loop.
    
    Basic principles and functionality still apply
    except for while/else syntax which is now a parameter/expression
    rather than a statement.
    """
)
docifyPLUS.document(
    until,
    """
    A backwards while loop.

    Breaks when a condition becomes True
    """
)
docifyPLUS.document(
    loop,
    """
    Handler function allowing one to switch between loop types using a the loop_type
    parameter
    """
)
### DOCUMENTATION           ###
### TESTS                   ###
#ct = 0
# with until("ct == 5", vars_={"ct": ct}) as u:
#    u.execute('print("LLJW"); ct += 1')
# with while_("ct < 5", vars_={"ct": ct}) as w:
#    w.execute("""print("LLJW"); ct += 1""")
# with loop('while', bool_expr="ct < 5", vars_={"ct": ct}) as w:
#    w.execute('print("LLJW"); ct += 1')
### TESTS                   ###
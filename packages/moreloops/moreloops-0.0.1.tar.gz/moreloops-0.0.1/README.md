# MoreLoops
##### *MoreLoops is a library the brings loops from other languages (and some that don't yet exist) into Python*

---

## ***Instilation***
    python -m pip install moreloops

## ***Dependencies***
###### *All dependencies for MoreLoops are auto-installed*

- _decorate_all_methods_ - For decorating all the methods inside a class
- _docifyPLUS_ - For documenting documentables

---

## ***Features***

### __Functions__
#
### *while_*

- Parameters:
- * bool_expr: str
- * do: Callable
- * - Default: Nothing
- * else\_: Callable
- * - Default: Nothing
- * oneline: bool
- * - Default: False
- * vars_: list
- * - Default: [ ]
- Output:
- * If oneline is True
- * - Returns: \_Loops.While.oneline( )
- * If oneline is False
- * - Returns: \_Loops.While(bool\_expr, do, else\_, vars\_)


### *until*

- Parameters:
- * bool_expr: str
- * do: Callable
- * - Default: Nothing
- * else\_: Callable
- * - Default: Nothing
- * oneline: bool
- * - Default: False
- * vars_: list
- * - Default: [ ]
- Output:
- * If oneline is True
- * - Returns: \_Loops.Until.oneline( )
- * If oneline is False
- * - Returns: \_Loops.Until(bool\_expr, do, else\_, vars\_)
- * - * Note: _Loops.Until is a *context manager* and is designed to be used as such
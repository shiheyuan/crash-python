# Stubs for gdb.xmethod (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

basestring = str
long = int

class XMethod:
    name: Any = ...
    enabled: bool = ...
    def __init__(self, name: Any) -> None: ...

class XMethodMatcher:
    name: Any = ...
    enabled: bool = ...
    methods: Any = ...
    def __init__(self, name: Any) -> None: ...
    def match(self, class_type: Any, method_name: Any) -> None: ...

class XMethodWorker:
    def get_arg_types(self) -> None: ...
    def get_result_type(self, *args: Any) -> None: ...
    def __call__(self, *args: Any) -> None: ...

class SimpleXMethodMatcher(XMethodMatcher):
    class SimpleXMethodWorker(XMethodWorker):
        _arg_types: Any = ...
        _method_function: Any = ...
        def __init__(self, method_function: Any, arg_types: Any) -> None: ...
        def get_arg_types(self): ...
        def __call__(self, *args: Any): ...
    _method_function: Any = ...
    _class_matcher: Any = ...
    _method_matcher: Any = ...
    _arg_types: Any = ...
    def __init__(self, name: Any, class_matcher: Any, method_matcher: Any, method_function: Any, *arg_types: Any) -> None: ...
    def match(self, class_type: Any, method_name: Any): ...

def _validate_xmethod_matcher(matcher: Any): ...
def _lookup_xmethod_matcher(locus: Any, name: Any): ...
def register_xmethod_matcher(locus: Any, matcher: Any, replace: bool = ...) -> None: ...

# Stubs for gdb.types (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, List, Dict, Optional, Union

import gdb

def get_basic_type(type_: gdb.Type) -> gdb.Type: ...
def has_field(type_: gdb.Type, field: str) -> bool: ...
def make_enum_dict(enum_type: gdb.Type) -> Dict[str, int]: ...
def deep_items(type_: gdb.Type) -> None: ...

class TypePrinter:
    name: str = ...
    enabled: bool = ...
    def __init__(self, name: str) -> None: ...
    def instantiate(self) -> None: ...

def _get_some_type_recognizers(result: Any, plist: List[Any]) -> None: ...
def get_type_recognizers() -> Any: ...
def apply_type_recognizers(recognizers: Any,
			   type_obj: gdb.Type) -> Optional[Any]: ...
def register_type_printer(locus: Optional[Union[gdb.Objfile, gdb.Progspace]],
			  printer: Any) -> None: ...

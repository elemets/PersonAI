from typing import Optional, Iterable, Iterator, Union, Any
from pathlib import Path

def get_string_id(key: Union[str, int]) -> int: ...

class StringStore:
    def __init__(
        self, strings: Optional[Iterable[str]] = ..., freeze: bool = ...
    ) -> None: ...
    def __getitem__(self, string_or_id: Union[bytes, str, int]) -> Union[str, int]: ...
    def as_int(self, key: Union[bytes, str, int]) -> int: ...
    def as_string(self, key: Union[bytes, str, int]) -> str: ...
    def add(self, string: str) -> int: ...
    def __len__(self) -> int: ...
    def __contains__(self, string: str) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __reduce__(self) -> Any: ...
    def to_disk(self, path: Union[str, Path]) -> None: ...
    def from_disk(self, path: Union[str, Path]) -> StringStore: ...
    def to_bytes(self, **kwargs: Any) -> bytes: ...
    def from_bytes(self, bytes_data: bytes, **kwargs: Any) -> StringStore: ...
    def _reset_and_load(self, strings: Iterable[str]) -> None: ...

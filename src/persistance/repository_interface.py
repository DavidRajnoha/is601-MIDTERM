from typing import Generic, TypeVar, List, Optional, Callable

T = TypeVar('T')


class RepositoryInterface(Generic[T]):
    def add(self, item: T) -> None: pass

    def get_all(self) -> List[T]: pass

    def get_by_id(self, id: str) -> Optional[T]: pass

    def get_last(self) -> Optional[T]: pass

    def filter(self, predicate: Callable[[T], bool]) -> List[T]: pass

    def clear(self) -> None: pass
    
    def delete(self, id: str) -> bool: pass

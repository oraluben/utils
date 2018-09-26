import traceback
import typing
from sys import version_info

assert version_info >= (3, 6, 0)

FuncType = typing.Callable[..., typing.Any]
F = typing.TypeVar('F', bound=FuncType)
T = typing.TypeVar('T')
ResourceT = typing.TypeVar('ResourceT', bound='Resource')
DateResourceT = typing.TypeVar('DateResourceT', bound='DateResource')


def error_safe(f: F) -> F:
    def inner(*args, **kwargs):
        try:
            return f(args, **kwargs)
        except:
            traceback.print_exc()

    return typing.cast(F, inner)


class Resource:
    pass


class DateResource(Resource, typing.Generic[T]):
    def raw_data(self) -> T:
        pass

    @classmethod
    def wrap(cls: typing.Type['DateResourceT'],
             generator: typing.Callable[['Task'], T]) -> 'DateResourceT':
        pass


class Str(DateResource[str]):
    pass


class File(Str):
    """use Str to represent file name"""

    @classmethod
    def as_file(cls, text: str) -> 'File':
        pass

    def save_as(self, file_name) -> 'File':
        pass


class IterableResource(DateResource[typing.Iterator[T]],
                       typing.Iterable[DateResource[T]],
                       typing.Generic[T]):

    @classmethod
    def wrap_iter(cls: typing.Type[DateResourceT],
                  typ: typing.Type[DateResource[T]]) -> typing.Callable[
        [typing.Callable[['Task'], typing.Iterator[T]]],
        DateResourceT
    ]:
        def inner(generator: typing.Callable[['Task'], typing.Iterator[T]]) -> DateResourceT:
            pass

        return inner

    def __iter__(self) -> typing.Iterator[ResourceT]:
        return self.foreach()

    def foreach(self) -> typing.Iterator[ResourceT]:
        pass


class Task:
    args: typing.List[typing.Union[str, Resource]] = []

    def __init__(self,
                 args: typing.List[typing.Union[str, Resource]]) -> None:
        self.args = args

    def check(self) -> bool:
        raise NotImplementedError()

    def start(self):
        assert self.check()
        raise NotImplementedError()

    @property
    def stdout(self) -> str:
        return ''

    @property
    def stderr(self) -> str:
        return ''

    @property
    def return_code(self) -> int:
        return 0


class DockerTask(Task):
    docker_image: str
    docker_args: typing.Sequence[str]

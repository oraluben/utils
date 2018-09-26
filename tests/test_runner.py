import unittest

from runner import *


class RunnerTest(unittest.TestCase):
    class InitTask(Task):
        def __init__(self):
            super().__init__(['echo', '/etc/dev'])

        @File.wrap
        def out_file(self):
            return self.stdout

    class EndTask(Task):
        def __init__(self, file: File) -> None:
            super().__init__(['cat', file])

        @Str.wrap
        def out_code(self):
            return '{}'.format(self.return_code)

    def test_base(self):
        t1 = self.InitTask()
        f = t1.out_file
        t2 = self.EndTask(f)

        t1.start()

        print(t2.out_code)

    class Mapper1(Task):
        def __init__(self) -> None:
            super().__init__(['echo', '-e', """
for i in range(10):
    print(i)""".replace('\n', '\\n'), '-', 'python'])

        @IterableResource.wrap_iter(Str)
        def num1(self) -> typing.Iterator[str]:
            pass

    def test_main(self):
        self.assertTrue(True)

from typing import Union, Generator, Sequence
import numpy as np

from ayda_tools.interfaces import AnnotatedData


def test_generator():
    class MyClass(AnnotatedData):
        def __init__(self):
            super().__init__(".", num_workers=3, batch_size=4)

        def _validation(self) -> Union[Generator, Sequence]:
            class ValidationSequence:
                def __getitem__(self, item):
                    return np.array([item]), np.array([item])

                def __len__(self):
                    return 2000

            return ValidationSequence()

        def get_data_shape(self) -> tuple:
            pass

        def _training(self) -> Union[Generator, Sequence]:
            while True:
                yield 1

    data = MyClass()

    val_gen = data.validation(300)

    for e in range(2000):
        print(e)
        for v in range(300):
            d = next(val_gen)
            result = d[0][1]
            assert v*4 +1 == result
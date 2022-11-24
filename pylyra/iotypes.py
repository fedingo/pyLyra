from ctypes import *
import numpy as np

def Generic_C_Array(c_type, np_type):
    class Array(Structure):
        _fields_ = [
            ("array", POINTER(c_type)),
            ("length", c_int)
        ]

        def __init__(self, array: np.array):
            super().__init__()

            assert array.dtype == np_type, f"Expected type {np_type}, got instead {array.dtype}"
            self.array = (c_type * len(array))(*array.tolist())
            self.length = len(array)

        @classmethod
        def to_numpy(cls, pointer) -> np.array:
            obj = cls.from_address(pointer)
            return np.array([obj.array[i] for i in range(obj.length)], dtype=np_type)

    return Array

Int16Array = Generic_C_Array(c_int16, np.int16)
UInt8Array = Generic_C_Array(c_uint8, np.uint8)

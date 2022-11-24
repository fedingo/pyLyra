from ctypes import *
import numpy as np
from scipy.io.wavfile import read
from typing import Callable, List
from iotypes import *

__all__ = ["encode_wav"]


# ! Setup for the C library bindings
__MODEL_PATH = "c_lib/model_coeffs"
__LIB_PATH = "c_lib/libencoder.so"

# ? Load SO Library
lib = cdll.LoadLibrary(__LIB_PATH)

# # ? Extract methods and annotate them with the correct C typings
EncodeWav: Callable = lib.EncodeWav
EncodeWav.argtypes = [POINTER(Int16Array), c_int, c_int, c_int, c_bool, c_char_p]
EncodeWav.restype = c_void_p

Free: Callable = lib.Free
Free.argtypes = [c_void_p]

def encode_wav(
    wav_data: np.array,
    sample_rate: int,
    num_channels: int = 1,
    bitrate: int = 3200,
    enable_dtx: bool = False,
) -> np.array:

    assert wav_data.dtype == np.int16, "wav_data should be passed as an array of np.int16"

    pointer = Int16Array(wav_data)

    output = EncodeWav(
        pointer, # Struct
        num_channels, 
        sample_rate, 
        bitrate, 
        enable_dtx,
        __MODEL_PATH.encode("ascii")
    )

    out_array = UInt8Array.to_numpy(output)
    Free(output)

    return out_array


if __name__ == "__main__":

    test_paths = [
        # "/home/gateway/projects/lyra/testdata/sample1_8kHz.wav",
        "/home/gateway/projects/lyra/testdata/sample1_16kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample1_32kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample1_48kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample2_8kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample2_16kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample2_32kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample2_48kHz.wav",
    ]

    for path in test_paths:

        # Test encode_wav
        sample_rate, audio = read(path)
        encoded_wav = encode_wav(audio, sample_rate)

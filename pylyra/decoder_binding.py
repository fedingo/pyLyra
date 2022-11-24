from ctypes import *
import numpy as np
from scipy.io.wavfile import read
from typing import Callable
from iotypes import *

__all__ = ["decode_wav"]


# ! Setup for the C library bindings
__MODEL_PATH = "c_lib/model_coeffs"
__LIB_PATH = "c_lib/libdecoder.so"

# ? Load SO Library
lib = cdll.LoadLibrary(__LIB_PATH)

# # ? Extract methods and annotate them with the correct C typings
DecodeWav: Callable = lib.DecodeWav
DecodeWav.argtypes = [POINTER(UInt8Array), c_int, c_int, c_int, c_bool, c_char_p]
DecodeWav.restype = c_void_p

Free: Callable = lib.Free
Free.argtypes = [c_void_p]


def decode_wav(
    lyra_data: np.array,
    sample_rate: int,
    num_channels: int = 1,
    bitrate: int = 3200,
    enable_dtx: bool = False,
) -> np.array:

    assert lyra_data.dtype == np.uint8, f"wav_data should be passed as an array of np.int16 and not {lyra_data.dtype}"

    output = DecodeWav(
        UInt8Array(lyra_data),
        num_channels, 
        sample_rate, 
        bitrate, 
        enable_dtx,
        __MODEL_PATH.encode("ascii")
    )

    out_array = Int16Array.to_numpy(output)
    Free(output)

    return out_array

if __name__ == "__main__":

    from encoder_binding import encode_wav

    test_paths = [
        "/home/gateway/projects/lyra/testdata/sample1_8kHz.wav",
        # "/home/gateway/projects/lyra/testdata/sample1_16kHz.wav",
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
        encoded = encode_wav(audio, sample_rate)
        decoded = decode_wav(encoded, sample_rate)

        print(len(audio), len(decoded))
#! /Users/tannerwilliams/.conda/envs/untitled/bin/python
import scipy.io.wavfile as wav
import scipy.fft as fft
import numpy as np


class DigitalSignal:

    def __init__(self, source_data, sampling_frequency):
        self.sampling_frequency = sampling_frequency
        self.source_data = source_data
        self.filtered_data = source_data.copy()
        self.freq_low = 0
        self.nyquist = max(source_data)
        self.freq_high = self.nyquist

        self.freq_array = None
        self.fft_array = None

    def bandpass(self, low=None, high=None):
        """
        :param low: optional argument for bandpass lowe cutoff
        :param high: optional argument for bandpass upper cutoff
        :return:
        """
        if low is None:
            low = 0
        if high is None:
            high = self.nyquist

        self.fft_array = fft.rfft(self.source_data)
        self.freq_array = fft.rfftfreq(len(self.source_data), 1./self.sampling_frequency)

        for i, value in self.fft_array:
            if value < low:
                freq_array[i] = 0
            if value > high:
                freq_array = 0

        return self.fft_array

    @classmethod
    def from_wav(cls, filename):
        f_s, raw_data = wav.read(filename)
        return f_s,  raw_data


if __name__ == '__main__':
    print('-----Problem 1-----')
    my_signal = DigitalSignal.from_wav('starwars.wav')
    print(my_signal)

    print('-----Problem 2-----')
    my_test = DigitalSignal(my_signal[1], my_signal[0])
    print(my_test.bandpass())


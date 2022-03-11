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

        fft_array = fft.rfft(self.source_data)
        freq_array = fft.rfftfreq(len(self.source_data), 1./self.sampling_frequency)
        # Find indexes where bandpass cutoffs are exceeded
        low_cutoff_indexes = np.where(freq_array < low)
        high_cutoff_indexes = np.where(freq_array > high)
        # Replace values that exceed bandpass with zero (this is the filter)
        np.put(fft_array, low_cutoff_indexes, 0)
        np.put(fft_array, high_cutoff_indexes, 0)
        # Store results and cutoff frequencies
        self.filtered_data = fft.irfft(fft_array).astype(np.int16)
        self.freq_low = low
        self.freq_high = high
        return self.filtered_data

    def subset_signal(self, start=None, end=None):
        if start is None:
            start = 0.0
        if end is None:
            # Length in seconds is number of samples/sample frequency
            end = (len(self.source_data) - 1)/self.sampling_frequency
        return np.arange(start, end, 1/self.sampling_frequency)

    def save_wav(self, filename, start=None, end=None):

        if start is None:
            start = 0.0
        if end is None:
            # Length in seconds is number of samples/sample frequency
            end = len(self.source_data)/self.sampling_frequency

        time = np.arange(0, (len(self.source_data) - 1)/self.sampling_frequency, 1/self.sampling_frequency)
        return wav.write(filename, self.sampling_frequency, time)


    @classmethod
    def from_wav(cls, filename):
        f_s, raw_data = wav.read(filename)
        return f_s,  raw_data


# if __name__ == '__main__':
#     print('-----Problem 1-----')
#     my_signal = DigitalSignal.from_wav('starwars.wav')
#     print(my_signal)
#
#     print('-----Problem 2-----')
#     my_test = DigitalSignal(my_signal[1], my_signal[0])
#     print(my_test.bandpass(low=10, high=10500))
#
#     print('-----Problem 3-----')
#     print(my_test.save_wav('test.wav', 2.5, 4))
#     wav.read('test.wav')

    # time_lower = np.where(time < start)
    # print(time_lower)
    # time_upper = np.where(time > end)
    # timeframe = np.delete(time, time_lower[0])
    # timeframe = np.delete(timeframe, time_upper[0])

    # return wav.write(filename, self.sampling_frequency, output)
    # return timeframe


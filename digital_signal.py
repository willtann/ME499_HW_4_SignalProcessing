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
        self.nyquist_freq = sampling_frequency/2
        self.freq_high = self.nyquist_freq

    def bandpass(self, low=0, high=None):
        """
        :param low: optional argument for bandpass lowe cutoff
        :param high: optional argument for bandpass upper cutoff
        :return: signal data only within specified frequency range
        """
        if high is None:
            high = self.nyquist_freq

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

    def subset_signal(self, start=0, end=None):
        """
        :param start: Timestamp in original audio to be saved as new start time
        :param end: Timestamp in original audio to be saved as new start time
        :return: audio signal in specified timeframe from original audio signal
        """
        if end is None:
            # Length in seconds is number of samples/sample frequency
            end = len(self.filtered_data)/self.sampling_frequency
        include_indexes = np.arange(start*self.sampling_frequency + 1, end*self.sampling_frequency, 1).astype(int)
        return self.filtered_data[include_indexes]

    def save_wav(self, filename, start=0, end=None):
        """
        :param filename: required filename for method to save as .wav
        :param start: Timestamp in original audio to be saved as new start time
        :param end: Timestamp in original audio to be saved as new start time
        :return: .wav file with specified timeframe of audio from original audio signal
        """
        if end is None:
            # Length in seconds is number of samples/sample frequency
            end = len(self.filtered_data)/self.sampling_frequency
        wav_data = self.subset_signal(start, end)
        return wav.write(filename, self.sampling_frequency, wav_data)

    @classmethod
    def from_wav(cls, filename):
        """
        :param filename: existing file from which signal data will be extracted
        :return: sample frequency and data from file
        """
        f_s, raw_data = wav.read(filename)
        return cls(raw_data, f_s)


# if __name__ == '__main__':
#     print('Testing bandpass...')
#     my_test = DigitalSignal.from_wav('sinewave1000hz.wav')
#     my_test.bandpass(900, 1200)
#     print('Saved file', my_test.save_wav('testing1000.wav'))

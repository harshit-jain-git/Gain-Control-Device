from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    print(low, high)
    b, a = butter(order, [low, high], btype='band')
    print(b, a)
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data, axis=0)
    return y

fs_rate, signal = wavfile.read("sample.wav")
print ("Frequency sampling", fs_rate)
l_audio = len(signal.shape)
print ("Channels: ", l_audio)
if l_audio == 2:
    signal = signal.sum(axis=1) / 2
N = signal.shape[0]

print ("Complete Samplings N", N)
secs = N / float(fs_rate)

print ("secs", secs)
Ts = 1.0/fs_rate     # sampling interval in time

print ("Timestep between samples Ts", Ts)
t = scipy.arange(0, secs, Ts)     # time vector as scipy arange field / numpy.ndarray
FFT_a = abs(scipy.fft(signal))
FFT_side_a = FFT_a[range(N//2)]     # one side FFT range
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)]     # one side frequency range
fft_freqs_side = np.array(freqs_side)

plt.subplot(411)
p1 = plt.plot(t, signal, "g")   # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.subplot(412)
p3 = plt.plot(freqs_side/4000, abs(FFT_side_a), "b")     # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')

y = butter_bandpass_filter(signal, 300, 3200, fs_rate, order=5)
print(y, len(y))

FFT_b = abs(scipy.fft(y))
FFT_side_b = FFT_b[range(N//2)]

plt.subplot(413)
p4 = plt.plot(freqs_side/4000, abs(FFT_side_b), "b")     # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('After filter')


plt.show()

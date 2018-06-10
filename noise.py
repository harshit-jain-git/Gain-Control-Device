from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import butter, sosfilt, sosfreqz, lfilter, buttord

# def butter_bandpass(lowcut, highcut, fs, order=5):
#         nyq = 0.5 * fs
#         low = lowcut / nyq
#         high = highcut / nyq
#         print(low, high);
#         sos = butter(order, [low, high], analog=False, btype='band', output='sos')
#         return sos

# def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
#         sos = butter_bandpass(lowcut, highcut, fs, order=order)
#         y = sosfilt(sos, data)
#         return y

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    print(low, high);
    b, a = butter(order, [low, high], btype='band')
    print(b, a);
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
Ts = 1.0/fs_rate # sampling interval in time
print ("Timestep between samples Ts", Ts)
t = scipy.arange(0, secs, Ts) # time vector as scipy arange field / numpy.ndarray
FFT = abs(scipy.fft(signal))
FFT_side = FFT[range(N//2)] # one side FFT range
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)] # one side frequency range
fft_freqs_side = np.array(freqs_side)
plt.subplot(411)
p1 = plt.plot(t, signal, "g") # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.subplot(412)
p2 = plt.plot(freqs/4000, FFT, "r") # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')
plt.subplot(413)
p3 = plt.plot(freqs_side/4000, abs(FFT_side), "b") # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')
# y = butter_bandpass_filter(freqs_side/4000, 300, 3200, fs_rate, order=5)
n,wn = scipy.signal.buttord(ws=[300/4000,3200/4000], wp=[200/4000,3300/4000],
   gpass=0.0, gstop=5.0)
print(y, len(y));
plt.subplot(414)
p4 = plt.plot(freqs_side/4000, abs(y), "b") # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('After filter')

plt.show()

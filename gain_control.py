import scipy.io.wavfile
import numpy as np
from agc import tf_agc
from matplotlib import pyplot as plt
import scipy.fftpack

# read audiofile
sr, d = scipy.io.wavfile.read('./noise_reduction/00_samples/sample_2.wav')
if (len(d.shape) == 2):
    d = d[:, 0]

print ("Frequency sampling", sr)
l_audio = len(d.shape)
print ("Channels: ", l_audio)
if l_audio == 2:
    d = d.sum(axis=1) / 2
N = d.shape[0]

print ("Complete Samplings N", N)
secs = N / float(sr)

print ("secs", secs)
Ts = 1.0/sr     # sampling interval in time

print ("Timestep between samples Ts", Ts)
t = scipy.arange(0, secs, Ts)     # time vector as scipy arange field / numpy.ndarray
FFT = abs(scipy.fft(d))
FFT_side = FFT[range(N//2)]     # one side FFT range
freqs = scipy.fftpack.fftfreq(d.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)]     # one side frequency range
fft_freqs_side = np.array(freqs_side)

plt.subplot(311)
p1 = plt.plot(t, d, "g")   # plotting the d
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.subplot(312)
p2 = plt.plot(freqs_side/4000, abs(FFT_side), "b")     # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')

# convert from int16 to float (-1,1) range
convert_16_bit = float(2 ** 15)
d = d / (convert_16_bit + 1.0)

# apply AGC
(y, D, E) = tf_agc(d, sr)

# convert back to int16 to save
y = np.int16(y / np.max(np.abs(y)) * convert_16_bit)

FFT_b = abs(scipy.fft(y))
FFT_side_b = FFT_b[range(N//2)]

plt.subplot(414)
p3 = plt.plot(freqs_side/4000, abs(FFT_side_b), "b")     # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('After filter')
plt.show()

scipy.io.wavfile.write('./noise_reduction/00_samples/sample_agc.wav', sr, y)
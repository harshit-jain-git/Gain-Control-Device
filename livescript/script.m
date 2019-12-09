global N Fs gain_range_0_500 gain_range_500_1000 gain_range_1000_1500 gain_range_1500_2000 gain_range_2000_2500 gain_range_2500_3000 gain_range_3000_3500 gain_range_3500_4000
gain_range_0_500 = 1.4;
gain_range_500_1000 = 1.2;
gain_range_1000_1500 = 1.5;
gain_range_1500_2000 = 1;
gain_range_2000_2500 = 2;
gain_range_2500_3000 = 1.1;
gain_range_3000_3500 = 2;
gain_range_3500_4000 = 2;

[f, Fs] = audioread('../noise_reduction/00_samples/sample.wav');
f = f(:,1);
T = 1/Fs;
L = length(f);
t = (0:L-1)*T;
N = size(f, 1);

figure; stem(t,f);
title('Original: Time domain')
xlabel('time(seconds)')

y1 = fft(f) / N; % For normalizing
y2 = fftshift(y1);

figure;     subplot(2, 1, 1);
plot(Fs * (0:(L/2))/L, abs(y2(N/2:N)))
title('Original: Single-Sided Amplitude Spectrum')
xlabel('Frequency(Hz)')

n = 3;
beginFreq = 300 /(Fs/2);
endFreq = 3200 / (Fs/2);
[b,a] = butter(n, [beginFreq endFreq], 'bandpass');
fOut = filter(b, a, f);

subplot(2, 1, 2);
plot(Fs * (0:(L/2))/L, abs(fOut(N/2:N)))
title('Original: Single-Sided Amplitude Spectrum')
xlabel('Frequency(Hz)')

y3 = fft(fOut) / N;
y4 = fftshift(y3);

y4 = gain_filter(y4);
plot(Fs * (0:(L/2))/L, abs(y4(N/2:N)))
title('After processing: Amplitude Spectrum');
xlabel('Frequency(Hz)');

output = ifft(ifftshift(y4) * N);
audiowrite('../noise_reduction/00_samples/processed_sample.wav', output, Fs);

function out = gain_filter(y)
global gain_range_0_500 gain_range_500_1000 gain_range_1000_1500 gain_range_1500_2000 gain_range_2000_2500 gain_range_2500_3000 gain_range_3000_3500 gain_range_3500_4000 
y = gain_correction(y, 1, 500, gain_range_0_500);
y = gain_correction(y, 500, 1000, gain_range_500_1000);
y = gain_correction(y, 1000, 1500, gain_range_1000_1500);
y = gain_correction(y, 1500, 2000, gain_range_1500_2000);
y = gain_correction(y, 2000, 2500, gain_range_2000_2500);
y = gain_correction(y, 2500, 3000, gain_range_2500_3000);
y = gain_correction(y, 3000, 3500, gain_range_3000_3500);
out = gain_correction(y, 3500, 3999, gain_range_3500_4000);
end

function out = gain_correction(y, a, b, gain)
global N Fs
out = y;
out(int32(-(N*b)/Fs + N/2) : int32(-(N*a)/Fs + N/2)) = gain * y(int32(-(N*b)/Fs + N/2) : int32(-(N*a)/Fs + N/2));
out(int32((N*a)/Fs + N/2) : int32((N*b)/Fs + N/2)) = gain * y(int32((N*a)/Fs + N/2) : int32((N*b)/Fs + N/2));
end
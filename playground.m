clear;
[f, Fs] = audioread('sample_2.wav');
T = 1/Fs;
L = length(f);
t = (0:L-1)*T;

N = size(f, 1);
figure; stem(t,f);
title('Original: Time domain')
xlabel('time(seconds)')

df = Fs/N;
w = (-(N/2):(N/2)-1) * df;
y = fft(f) / N; % For normalizing
y2 = fftshift(y);
figure;  plot(w, abs(y2))
title('Original: Amplitude Spectrum')
xlabel('Frequency(Hz)')

figure;
plot(Fs * (0:(L/2))/L, abs(y2(N/2:N)))
title('Original: Single-Sided Amplitude Spectrum')
xlabel('Frequency(Hz)')

norm = Fs / 2;
[b, a] = butter(6,[50 3000]/norm, 'bandpass');

% [b, a] = butter(n, [beginFreq, endFreq], 'stop');
fOut = filter(b, a, f);
figure;  stem(t, fOut);
title('After processing: Time-domain');
xlabel('time(seconds)');

y3 = fftshift(fft(fOut)/N);
% y3 = abs(y3) * 2 + abs(y2);
figure; plot(Fs * (0:(L/2))/L, abs(y3(N/2:N)), 'r');
title('After processing: Amplitude Spectrum');
xlabel('Frequency(Hz)');
fOut2 = ifft(ifftshift(y3) * N);
% close all;
pOrig = audioplayer(f,Fs); 
% pOrig.play;
p = audioplayer(fOut, Fs);  
% p.play;
audiowrite('handel_J_processed.wav', fOut2, Fs);
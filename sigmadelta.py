import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

fs = 1000000
f = 1000
OSR = 500
t = np.arange(0, 0.1, 1/fs)
Vin = 0.7 * np.sin(2 * np.pi * f * t)

integrator = 0
dac_out = 0
bitstream = []
integrator_history = []

for x in Vin:
    error = x - dac_out
    integrator += error
    if integrator >= 0:
        bit = 1
    else:
        bit = 0
    if bit == 1:
        dac_out = 1
    else:
        dac_out = -1
    bitstream.append(bit)
    integrator_history.append(integrator)

bits = 2 * np.array(bitstream) - 1
N = len(bits)
Y = fft(bits)
freq = fftfreq(N, d=1/fs)
pos_freq = freq[:N//2]
Ymag = np.abs(Y[:N//2])

f_band = fs / (2 * OSR)
signal_bin = np.argmax(Ymag)

band_mask = pos_freq <= f_band
exclude = np.zeros(N//2, dtype=bool)
exclude[max(0, signal_bin-50): signal_bin+51] = True  # changed from ±5

noise_mask = band_mask & ~exclude
signal_power = np.sum(Ymag[band_mask & exclude]**2)
noise_power  = np.sum(Ymag[noise_mask]**2)

snr  = 10 * np.log10(signal_power / noise_power)
enob = (snr - 1.76) / 6.02

plt.figure(figsize=(10, 5))
plt.plot(pos_freq, 20*np.log10(Ymag + 1e-10))
plt.axvline(x=f_band, color='r', linestyle='--', label=f'Band edge {f_band:.0f} Hz')
plt.title("FFT of Bitstream (dB scale)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.legend()
plt.grid()
plt.show()

print(f"Peak Frequency = {freq[signal_bin]:.2f} Hz")
print(f"Signal band= {f_band:.0f} Hz")
print(f"SNR = {snr:.2f} dB")
print(f"ENOB = {enob:.2f} bits")
print(f"OSR = {OSR}")

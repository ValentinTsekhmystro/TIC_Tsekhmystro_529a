import matplotlib.pyplot as plt
import numpy.random
import scipy

a = 0
b = 10
n = 500
random = numpy.random.normal(a, b, n)

Fs = 1000
x = numpy.arange(n)/Fs

F_max = 31
w = F_max/(Fs/2)
parameters_filter = scipy.signal.butter(3, w, "low", output="sos")
y = scipy.signal.sosfiltfilt(parameters_filter, random)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(x, y, linewidth=1)
ax.set_xlabel("Час(секунди)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 31", fontsize=14)
fig.savefig("./figures/" + "Сигнал з максимальною частотою F_max = 31" + ".png", dpi=600)

spectrum = scipy.fft.fft(y)
s_spectrum = numpy.abs(scipy.fft.fftshift(spectrum))
frequency_readings =scipy.fft.fftfreq(n, 1/n)
readings = scipy.fft.fftshift(frequency_readings)

fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(readings, s_spectrum, linewidth=1)
ax.set_xlabel("Частота (Гц)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 31", fontsize=14)
fig.savefig("./figures/" + "Спектр сигналу з максимальною частотою F_max = 31" + ".png", dpi=600)

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

F_filter = 38

discrete_signals = []
discrete_spectrums = []
filter_signals = []
dispersion_dif = []
signal_noise = []

for Dt in [2, 4, 8, 16]:
        discrete_signal = numpy.zeros(n)
        for i in range(0, round(n/Dt)):
            discrete_signal[i*Dt] = y[i*Dt]
        discrete_signals += [list(discrete_signal)]

        spectrum = scipy.fft.fft(discrete_signal)
        t_spectrum = numpy.abs(scipy.fft.fftshift(spectrum))
        discrete_spectrums += [list(t_spectrum)]

        w = F_filter/(Fs/2)
        parameters_filter = scipy.signal.butter(3, w, 'low', output='sos')
        filter_signal = scipy.signal.sosfiltfilt(parameters_filter, discrete_signal)
        filter_signals += [list(filter_signal)]

        E1 = filter_signal - y
        dispersion_1 = numpy.var(y)
        dispersion_2 = numpy.var(E1)
        dispersion_dif += [dispersion_2]
        signal_noise += [dispersion_1 / numpy.var(E1)]

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(x, discrete_signals[s], linewidth=1)
        s += 1
fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/" + "Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)" + ".png", dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(readings, discrete_spectrums[s], linewidth=1)
        s += 1
fig.supxlabel("Частота (Гц)", fontsize=14)
fig.supylabel("Амплітуда спектру", fontsize=14)
fig.suptitle("Спектри сигналів з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/" + "Спектри сигналів з кроком дискретизації Dt = (2, 4, 8, 16)" + ".png", dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(x, filter_signals[s], linewidth=1)
        s += 1
fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/" + "Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)" + ".png", dpi=600)

fig,ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot([2, 4, 8, 16], dispersion_dif, linewidth=1)
fig.supxlabel('Крок дискретизації', fontsize=14)
fig.supylabel('Дисперсія', fontsize=14)
fig.suptitle('Залежність дисперсії від кроку дискретизації', fontsize=14)
fig.savefig('./figures/' + 'Залежність дисперсії від кроку дискретизації' + '.png', dpi=600)

fig,ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot([2, 4, 8, 16], signal_noise, linewidth=1)
fig.supxlabel('Крок дискретизації', fontsize=14)
fig.supylabel('ССШ', fontsize=14)
fig.suptitle('Залежність співвідношення сигнал-шум від кроку дискретизації', fontsize=14)
fig.savefig('./figures/' + 'Залежність співвідношення сигнал-шум від кроку дискретизації' + '.png', dpi=600)

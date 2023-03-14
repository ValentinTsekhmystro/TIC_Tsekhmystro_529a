import matplotlib.pyplot as plt
import numpy as np
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
frequency_readings = scipy.fft.fftfreq(n, 1/n)
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

dispersion_dif.clear()
signal_noise.clear()
quantize_signals = []
for M in [4, 16, 64, 256]:
    bits = []
    delta = (numpy.max(y)-numpy.min(y))/(M-1)
    quantize_signal = delta*np.round(y/delta)
    quantize_signals += [quantize_signal]
    quantize_levels = numpy.arange(numpy.min(quantize_signal), numpy.max(quantize_signal) + 1, delta)
    quantize_bit = numpy.arange(0, M)
    quantize_bit = [format(bits, '0' + str(int(numpy.log(M)/numpy.log(2)))+'b') for bits in quantize_bit]
    quantize_table = numpy.c_[quantize_levels[:M], quantize_bit[:M]]
    fix, ax = plt.subplots(figsize=(14/2.54, M/2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fix.savefig('./figures/' + 'Таблиця квантування для ' + str(M) + ' рівнів' + '.png', dpi=600)

    for signal_value in quantize_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if numpy.round(numpy.abs(signal_value - value), 0) ==0:
                bits.append(quantize_bit[index])
                break
    bits = [int(item) for item in list(''.join(bits))]

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(numpy.arange(0, len(bits)), bits, linewidth=0.1)
    ax.set_xlabel("Біти", fontsize=14)
    ax.set_ylabel("Амплітуда сигналу", fontsize=14)
    plt.title("Кодова послідовність сигналу при кількості рівнів квантування " + str(M), fontsize=14)
    fig.savefig("./figures/" + "Кодова послідовність сигналу при кількості рівнів квантування " + str(M) + ".png", dpi=600)

    E = quantize_signal - y
    dispersion_1 = numpy.var(y)
    dispersion_2 = numpy.var(E)
    dispersion_dif += [dispersion_2]
    signal_noise += [dispersion_1 / numpy.var(E)]

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(x, quantize_signals[s], linewidth=1)
        s += 1

fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Цифрові сигнали з рівнями квантування (4, 16, 64, 256)", fontsize=14)
fig.savefig("./figures/" + "Цифрові сигнали з рівнями квантування (4, 16, 64, 256)" + ".png", dpi=600)

M = [4, 16, 64, 256]
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(M, dispersion_dif, linewidth=1)
ax.set_xlabel("Кількість рівнів квантування", fontsize=14)
ax.set_ylabel("Дисперсія", fontsize=14)
plt.title("Залежність дисперсії від кількості рівнів квантування", fontsize=14)
fig.savefig("./figures/" + "Залежність дисперсії від кількості рівнів квантування" + ".png", dpi=600)

fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(M, signal_noise, linewidth=1)
ax.set_xlabel("Кількість рівнів квантування", fontsize=14)
ax.set_ylabel("ССШ", fontsize=14)
plt.title("Залежність співвідношення сигнал-шум від кількості рівнів квантування", fontsize=14)
fig.savefig("./figures/" + "Залежність співвідношення сигнал-шум від кількості рівнів квантування" + ".png", dpi=600)

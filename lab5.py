import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def process_wave_file(file: Path):
    data = []
    with file.open('r') as f:
        lines = f.readlines()
    for line in lines[1:]:
        data.append([float(x) for x in line.split(';')[7:]])

    averaged_data = np.average(data, axis=0)
    print(len(averaged_data))

    return averaged_data


def process_spectral_file(file: Path):
    with file.open('r') as f:
        lines = f.readlines()
    spectrum = [int(x.split(' ')[1]) for x in lines[3:]]
    return np.array(spectrum)

def calibrate_cs_spectrum(spectrum: np.ndarray) -> np.ndarray:
    peaks, _ = find_peaks(spectrum, height=70)
    cs_662 = peaks[-1]
    print(f"CS-662 peak: {cs_662}")
    # return np.array([i for i in range(len(spectrum))])
    return np.array([i*662/cs_662 for i in range(len(spectrum))])


def main():
    # plot spectral data
    spectral_files = sorted(list((Path.cwd() / "lab5").glob("*.txt3")))
    spectral_data = [process_spectral_file(file) for file in spectral_files]
    spectral_names = [file.name.split('_')[4] for file in spectral_files]
    plt.clf()
    for i, spectral_name in enumerate(spectral_names):
        plt.plot(calibrate_cs_spectrum(spectral_data[i]), spectral_data[i], label=spectral_name)
    plt.legend()
    plt.xlim(0, 800)
    plt.xlabel("Energy (keV)")
    plt.ylabel("Counts")
    plt.savefig("spectral.png")
    plt.close()

    # plot wave data
    wave_files = sorted(list((Path.cwd() / "lab5").glob("*.CSV")))
    wave_data = [process_wave_file(file) for file in wave_files]
    wave_names = [file.name.split('_')[4] for file in wave_files]
    plt.clf()
    for i, wave_name in enumerate(wave_names):
        plt.plot(wave_data[i], label=wave_name)
    plt.legend()
    plt.savefig("waves.png")
    plt.close()


if __name__ == "__main__":
    main()

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import becquerel as bq
from bs4 import BeautifulSoup
import numpy as np


calibration_coefficients = [
    [-52.366, 0.45616, 0.0],  # Ch 0
    [-50.891, 0.55576, 0.0],  # Ch 1
    [-35.717, 0.56898, 0.0],  # Ch 2
    [-45.479, 0.57868, 0.0],  # Ch 3
    [-48.463, 0.57439, 0.0],  # Ch 4
    [-44.758, 0.56232, 0.0],  # Ch 5
    [-49.019, 0.57326, 0.0],  # Ch 6
    [-57.965, 0.55279, 0.0],  # Ch 7
]

def get_n42_paths(folder_name: str) -> list[Path]:
    return sorted(list((Path.cwd() / "samples" / folder_name).glob("*.n42*")))

def read_n42(file: Path) -> bq.Spectrum:
    sword_num = int(file.name.split("@")[0].split('H')[-1]) # since each file starts with CH3@...
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'xml')
    spectrum = soup.find_all('ChannelData')[0].text
    spectrum = [int(x) for x in spectrum.split()]

    coefficients = calibration_coefficients[sword_num]
    # print(f'{file}: {coefficients}')

    def energy_calculator(channel: int) -> float:
        return coefficients[0] + coefficients[1] * channel + coefficients[2] * channel**2

    energies = [energy_calculator(channel) for channel in range(len(spectrum))]

    spectrum = [spectrum[i] if energy > 60 else 0 for i, energy in enumerate(energies)]

    return np.array([energies, spectrum])

def main():
    print("Hello from 586projectdata!")
    # get n42 files
    background_n42_files = get_n42_paths("background")
    calibration_n42_files = get_n42_paths("energy_calibration")
    open_pit_mine_n42_files = get_n42_paths("soil_openpit")

    # read n42 files
    background_spectra = [read_n42(file) for file in background_n42_files]
    calibration_spectra = [read_n42(file) for file in calibration_n42_files]
    open_pit_mine_spectra = [read_n42(file) for file in open_pit_mine_n42_files]


    graphing_folder = Path.cwd() / "graphs"
    graphing_folder.mkdir(exist_ok=True)




    # for index in range(8):
    #     # print(background_spectra[index])
    #     plt.plot(background_spectra[index][0], background_spectra[index][1])
    #     plt.savefig(graphing_folder / f"background{index}.png")
    #     plt.close()

    #     # plot calibration spectra
    #     plt.plot(calibration_spectra[index][0], calibration_spectra[index][1])
    #     plt.savefig(graphing_folder / f"calibration{index}.png")
    #     plt.close()

    #     # plot open pit mine spectra
    #     plt.plot(open_pit_mine_spectra[index][0], open_pit_mine_spectra[index][1])
    #     plt.savefig(graphing_folder / f"open_pit_mine{index}.png")
    #     plt.close()

    

    

    
    



if __name__ == "__main__":
    main()

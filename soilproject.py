from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import becquerel as bq
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, timedelta
import utils



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

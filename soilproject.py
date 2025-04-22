from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import becquerel as bq
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, timedelta
import utils
from scipy import interpolate



def main():
    print("Start geometric efficiency calibration...")
    calibration_names = ["2275411", "2275412",
                         "2339312", "2339314",
                         "2339311"]
    manifest = utils.read_manifest()  # dict of bottle info
    efficiencies = utils.read_efficiencies()  # dict of efficiencies

    bottle_efficiencies = {}
    # read in calibration bottles
    for name in calibration_names:
        # note that this uses 20_000 bins from 0 to 2_000 keV
        spectrum = utils.get_corrected_spectrum(f'serial_{name}')

        # get cps under specific peaks: 662, 1173, 1333
        bottle_efficiencies[name] = {}
        peaks = [662, 1173, 1333]
        gamma_info = manifest[name]['gamma_info']
        for peak in peaks:
            cps, _ = utils.get_cps_peak(spectrum, peak)
            overall_efficiency = cps / gamma_info[gamma_info['energy'] == peak]['activity_cps'].values[0]
            # intrinsic_efficiency = efficiencies[peak]
            geometry_efficiency = overall_efficiency  # / intrinsic_efficiency
            bottle_efficiencies[name][peak] = geometry_efficiency
    print(bottle_efficiencies)

    # energy_splines = {}
    # # setup spline interpolation with volumes and densities resulting in efficiencies per energy
    # volumes = [manifest[name]['volume'] for name in calibration_names]
    # densities = [manifest[name]['density'] for name in calibration_names]
    # efficiencies = [bottle_efficiencies[name][662] for name in calibration_names]
    # energy_splines[662] = interpolate.bisplrep(volumes, densities, efficiencies)

    # volumes = [manifest[name]['volume'] for name in calibration_names]
    # densities = [manifest[name]['density'] for name in calibration_names]
    # efficiencies = [bottle_efficiencies[name][1173] for name in calibration_names]
    # energy_splines[1173] = interpolate.bisplrep(volumes, densities, efficiencies)

    # volumes = [manifest[name]['volume'] for name in calibration_names]
    # densities = [manifest[name]['density'] for name in calibration_names]
    # efficiencies = [bottle_efficiencies[name][1333] for name in calibration_names]
    # energy_splines[1333] = interpolate.bisplrep(volumes, densities, efficiencies)

    # # read in soil samples
    # print("Start reading soil samples...")
    # soil_low = utils.get_corrected_spectrum("soil_tailing11")
    # soil_medium = utils.get_corrected_spectrum("soil_tailing3")
    # soil_high = utils.get_corrected_spectrum("soil_openpit")



    graphing_folder = Path.cwd() / "graphs"
    graphing_folder.mkdir(exist_ok=True)


 

    

    
    



if __name__ == "__main__":
    main()

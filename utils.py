from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import becquerel as bq
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, timedelta


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

def get_sword_num(file: Path) -> int:
    sword_num = int(file.name.split("@")[0].split('H')[-1]) # since each file starts with CH3@...
    return sword_num

def convert_to_timedelta(time: str) -> timedelta:
    time = time.split('S')[0] + '000S'
    time = datetime.strptime(time, "PT%HH%MM%S.%fS").time()
    time_delta = timedelta(hours=time.hour,
                           minutes=time.minute,
                           seconds=time.second,
                           microseconds=time.microsecond)
    return time_delta

def read_n42(file: Path) -> bq.Spectrum:
    sword_num = get_sword_num(file)
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'xml')

    live_time = soup.find_all('LiveTimeDuration')[0].text
    live_time = convert_to_timedelta(live_time)
    real_time = soup.find_all('RealTimeDuration')[0].text
    real_time = convert_to_timedelta(real_time)
    start_time = soup.find_all('StartDateTime')[0].text
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S-04:00")
    spectrum_kwargs = {
        'start_time': start_time,
        'livetime': live_time.total_seconds(),
        'realtime': real_time.total_seconds(),
    }

    coefficients = calibration_coefficients[sword_num]
    # print(f'{file}: {coefficients}')
    cal = bq.Calibration("p[0] + p[1] * x", coefficients[:2])

    spectrum = soup.find_all('ChannelData')[0].text
    spectrum = [int(x) for x in spectrum.split()]
    # adc_like = []
    # for i in range(len(spectrum)):
    #     adc_like.extend([i]*spectrum[i])

    spectrum = bq.Spectrum(spectrum, **spectrum_kwargs)
    spectrum.apply_calibration(cal)
    common_bins = np.arange(0, 2000, .1)
    spectrum = spectrum.rebin(common_bins)

    return spectrum


def read_manifest() -> pd.DataFrame:
    manifest = pd.read_csv("calibration_bottles/bottle_manifest.csv")
    bottle_manifest = {}    
    for row in range(len(manifest)):
        bottle_info = {}
        bottle_info['volume'] = manifest.iloc[row]['Volume (mL)']
        bottle_info['density'] = manifest.iloc[row]['Density (g/cc)']
        source_name = str(int(manifest.iloc[row]['Source Number']))

        gamma_info = pd.read_csv(f"calibration_bottles/{source_name}.csv")
# Gamma-Ray Energy (KeV),Nuclide,Isotope,HalfLife,Half Life Uncertainty,Branching Ratio (%),Activity (?Ci),Gammas per second,Total Uncertainty
        gamma_info = gamma_info[['Gamma-Ray Energy (KeV)', 'Nuclide',
                                 'Isotope', 'HalfLife', 'Half Life Uncertainty',
                                 'Gammas per second']]
        gamma_info.rename(columns={'Gamma-Ray Energy (KeV)': 'energy',
                                 'Nuclide': 'protons',
                                 'Isotope': 'atomic_number',
                                 'HalfLife': 'half_life',
                                 'Half Life Uncertainty': 'half_life_uncertainty',
                                 'Gammas per second': 'activity_cps'},
                         inplace=True)
        decay_time = (datetime(2025, 4, 15) - datetime(2024, 6, 23)).total_seconds() / (3600 * 24 * 365.25)

        decay_constants = np.log(2) / gamma_info['half_life']
        gamma_info['activity_cps'] = np.exp(-decay_constants * decay_time) * gamma_info['activity_cps']

        bottle_info['gamma_info'] = gamma_info
        bottle_manifest[source_name] = bottle_info

    return bottle_manifest



if __name__ == "__main__":
    # test manifest
    print(read_manifest())
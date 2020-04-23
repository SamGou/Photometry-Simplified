import pandas as pd
import csv
from PyAstronomy import pyasl
import numpy as np
import os


def aperture_file(data):
    dir = os.getcwd() + "\\GAIA Data\\experimental"
    df = pd.read_csv(data)

    ra = np.array(df["ra"])
    dec = np.array(df["dec"])
    pmra = np.array(df["pmra"])
    pmdec = np.array(df["pmdec"])

    nan = np.where(np.isnan(pmra))
    ra = np.delete(ra, nan)
    dec = np.delete(dec, nan)
    pmra = np.delete(pmra, nan)
    pmdec = np.delete(pmdec, nan)

    radecpairs = zip(ra, dec)
    string_list = []
    for radec in radecpairs:
        ra = radec[0]
        dec = radec[1]
        sexa = pyasl.coordsDegToSexa(ra, dec)
        ra, dec = sexa.split("  ")
        ra = ra.split()
        ra = ":".join(ra)
        dec = dec.split()
        dec = ":".join(dec)
        string = "{}, {}, 0, 0, 99.999".format(ra, dec)
        string_list.append(string)

    subdir = dir + "\\RADECforAIJ"

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    with open(subdir + "\\RADEC_Py.radec", "a+") as file:
        for line in string_list:
            line = line + "\n"
            file.write(line)

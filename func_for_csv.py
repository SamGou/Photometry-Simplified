import xlrd
import pandas as pd
import numpy as np
import os
import csv


def index(arr):
    for i in arr:
        if ('Source_AMag_C' in i) == True:
            ind = arr.index(i) + 1
            return ind
        else:
            continue


def trns_tableTocsv(f2table, f1table, BPRP, filter, res, excess, distance): #original f1 was V f2 was B
    workbookf1 = xlrd.open_workbook(f1table, on_demand=True)
    worksheetf1 = workbookf1.sheet_by_index(0)

    arrayofnamesf1 = worksheetf1.col_values(1)
    arrayofvaluesf1 = worksheetf1.col_values(2)
    f1_array = np.array(arrayofvaluesf1[index(arrayofnamesf1):])

    NaN_index = list(np.where(f1_array == "NaN")[0])
    NaN_index = list(np.where(f1_array == "Infinity")[0]) + NaN_index
    #############################################################
    workbookf2 = xlrd.open_workbook(f2table, on_demand=True)
    worksheetf2 = workbookf2.sheet_by_index(0)

    arrayofnamesf2 = worksheetf2.col_values(1)
    arrayofvaluesf2 = worksheetf2.col_values(2)
    f2_array = np.array(arrayofvaluesf2[index(arrayofnamesf2):])

    NaN_index = list(np.where(f2_array == "NaN")[0]) + NaN_index
    NaN_index = list(set(list(np.where(f2_array == "Infinity")[0]) + NaN_index))
    #############################################################
    f2_array = np.delete(f2_array, NaN_index)
    f2_array = np.array(list(map(float, f2_array)))
    f2_extremal = list(np.where(f2_array >= res)[0])

    f1_array = np.delete(f1_array, NaN_index)
    f1_array = np.array(list(map(float, f1_array)))
    f1_extremal = list(np.where(f1_array >= res)[0])

    all_extremal = list(set(f2_extremal + f1_extremal))
    f2_array = np.delete(f2_array, all_extremal)
    f1_array = np.delete(f1_array, all_extremal)

    df = pd.read_csv(BPRP) # open the topcat VO document


    ##############################################################
    def AbsoluteMag(mag_array,distance):
        modulus = 5 - 5*(np.log10(distance))
        return np.add(mag_array,modulus)

    f2_array = AbsoluteMag(f2_array,distance)
    f1_array = AbsoluteMag(f1_array,distance)
    df2f1_array = f2_array - f1_array #filter 1 and 2 difference
    bp = AbsoluteMag(np.array(df["phot_bp_mean_mag"]),distance)
    rp = AbsoluteMag(np.array(df["phot_rp_mean_mag"]),distance)
    g = AbsoluteMag(np.array(df["phot_g_mean_mag"]),distance)
    dbprp = bp-rp # get Gbp - Grp

    if filter == "BV": # f2 is "B" | f1 is "V"
        def df2f1TodGf1(df1f2):
            dgv = []
            for i in df1f2:
                dgv.append(-0.02907 - 0.02385 * (i) - 0.2297 *
                           pow(i, 2) - 0.001768 * pow(i, 3))
            return dgv

        def dBPRpTodGf1(dbprp):
            dgv = []
            c1 = -0.0176
            c2 = -0.00686
            c3 = -0.1732
            for i in dbprp:
                dgv.append(c1 + c2 * i + c3 * pow(i, 2))
            return dgv

        def Extinction_correction_diff(AbsMag,excess):
            return np.subtract(AbsMag,excess)

        def Extinction_correction_mag(AbsMag,excess):
            Rv = 3.1
            Av = Rv*excess
            return np.subtract(AbsMag,Av)

        df2f1_array =  Extinction_correction_diff(df2f1_array,excess)
        f1_array = Extinction_correction_mag(f1_array,excess)

        dGV_f2f1 = df2f1TodGf1(df2f1_array)
        dGV_BPRP = dBPRpTodGf1(dbprp)

        topcat_df = pd.read_csv(BPRP)
        topcat_df["Mg-Mv"] = dGV_BPRP
        topcat_df["Mg"] = g
        topcat_df.to_csv(BPRP)

    elif filter == "BR": # f2 is "B" | f1 is "R"
        def df2f1TodGf1(df1f2):
            dgv = []
            for i in df1f2:
                dgv.append(-0.0128 + 0.3064 * (i) - 0.0520 *
                           pow(i, 2) - 0.0139 * pow(i, 3))
            return dgv

        def dBPRpTodGf1(dbprp):
            dgv = []
            c1 = -0.003226
            c2 = 0.3833
            c3 = -0.1345
            for i in dbprp:
                dgv.append(c1 + c2 * i + c3 * pow(i, 2))
            return dgv

        def Extinction_correction_diff(AbsMag,excess):
            excess = 1.78*excess
            return np.subtract(AbsMag,excess)

        def Extinction_correction_mag(AbsMag,excess):
            Ar = 2.32*excess
            return np.subtract(AbsMag,Ar)

        df2f1_array = Extinction_correction_diff(df2f1_array,excess)
        f1_array = Extinction_correction_mag(f1_array,excess)

        dGV_f2f1 = df2f1TodGf1(df2f1_array)
        dGV_BPRP = dBPRpTodGf1(dbprp)

        topcat_df = pd.read_csv(BPRP)
        topcat_df["Mg-Mr"] = dGV_BPRP
        topcat_df["Mg"] = g
        topcat_df.to_csv(BPRP)

    ##############################################################
    f2_array = list(f2_array)
    f1_array = list(f1_array)
    df2f1_array = list(df2f1_array)
    data = list(zip(f2_array, f1_array, df2f1_array, dGV_f2f1))
    ##############################################################
    n = 0
    dir = os.getcwd()
    with open(dir + "\\GAIA Data\\PhotometryTable_minmag{}_excess{}_distance{}_filter{}.csv".format(res,excess,distance,filter), "w") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            if n == 0:
                if filter == "BV":
                    labels = ["Mb", "Mv", "Mb-Mv", "Mg-Mv"]
                elif filter == "BR":
                    labels = ["Mb", "Mr", "Mb-Mr", "Mg-Mr"]
                filewriter.writerow(labels)
                n += 1
                continue
            else:
                filewriter.writerow(row)

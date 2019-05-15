import netCDF4
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import glob

def get_L1(file_pathL1):
    #todo: get wavelenth once
    L1 = netCDF4.Dataset(file_pathL1)
    L1_id = L1["SoundingGeometry/sounding_id"][...]#.compressed()#.flatten()

    #sza = L1["SoundingGeometry/sounding_solar_zenith"][...]#.compressed()#.flatten()
    flag = L1["SoundingGeometry/sounding_qual_flag"][...]#.compressed()#.flatten()#should be 0


    sco2 = L1["SoundingMeasurements/radiance_strong_co2"][...]#.compressed()#.flatten()
    wco2 = L1["SoundingMeasurements/radiance_weak_co2"][...]#.compressed()#.flatten()
    o2 = L1["SoundingMeasurements/radiance_o2"][...]#.compressed()#.flatten()

    #snr_o2_l1b = L1["SoundingMeasurements/snr_o2_l1b"][...]
    #snr_strong_co2_l1b = L1["SoundingMeasurements/snr_strong_co2_l1b"][...]
    #snr_weak_o2_l1b = L1["SoundingMeasurements/snr_weak_o2_l1b"][...]

    first_sound = L1["Metadata/FirstSoundingId"][...]#.compressed()#.flatten()
    last_sound = L1["Metadata/LastSoundingId"][...]#.compressed()#.flatten()
    print(f"sounding range L1: ({first_sound[0]},{last_sound[0]}) with {L1_id.size} elements")# or ({L1_id[0][0]},{L1_id[-1][-1]})
    
    elems = [L1_id,sco2,wco2,o2]#sza
    #[print(elem.shape) for elem in elems]
    #print("flag",flag.shape)
    elems = [np.ma.filled(elem,np.nan) for elem in elems]
    #print("Hi")
    ###print(f"spectrum consists of {len(elems)} elements with shapes:")
    for i,elem in enumerate(elems):
        #print(i, type(elem))
        ##print(i, np.shape(elem))
        new_elem = elem.reshape(-1, *elem.shape[2:])
        #print(np.shape(new_elem))
        elems[i] = new_elem

        #only for masked arrays
        #print(elem.count())
        #print(elem.compressed())
        #elem_mask = elem.mask()
        #try:
        #    print("sum of mask",np.sum(np.ma.getmaskarray(elem)))
        #except:
        #    print(f"{i} is not a masked array")

    L1_id = elems[0]
    #sza = elem
    ###flag = elems[2] == 0#np.array(elems[2], dtype=bool)
    #print(flag.shape)
    flag = flag.reshape(-1, *flag.shape[2:])
    #print(flag.shape)
    flag = np.ma.filled(flag,np.nan)
    #print(flag)
    ##print(type(L1_id))
    #print(np.sum(L1_id))
    ##print(L1_id)
    ##print(flag)
    ##print("s id",np.shape(L1_id))
    ##print("s flag",np.shape(flag))
    #print(flag.size)
    #print(L1_id.size)
    #print(flag.max())
    #print(flag.min())
    flag =np.logical_not(np.asarray(flag,dtype=bool)) # 0 is true, all other codes are false
    #print(np.sum(flag))
    print("flagged L1 shape",np.shape(L1_id[flag]))
    #print(f"sounding after flag {L1_id[flag].size} elements")
    elems = [np.ma.filled(elem[flag],np.nan) for elem in elems]

    #wavelenth = np.ma.filled(L1[f"InstrumentHeader/dispersion_coef_samp"][...],np.nan)
    #wave_path = Path(__file__).parent.joinpath("tmp/wavelenth.npy")
    #np.save(wave_path, wavelenth)

    return elems#L1_id,sza,flag,sco2,wco2,o2

def get_L2(file_pathL2):
    L2 = netCDF4.Dataset(file_pathL2)
    L2_id = L2['sounding_id'][...]
    #retrived
    xco2 = L2.variables['xco2'][...]
    albedo_o2 = L2['Retrieval/albedo_o2a'][...]
    albedo_sco2 = L2['Retrieval/albedo_sco2'][...]
    albedo_wco2 = L2['Retrieval/albedo_wco2'][...]
    tcwv = L2['Retrieval/tcwv'][...]

    #aerosols
    aod_bc = L2['Retrieval/aod_bc'][...]
    aod_dust = L2['Retrieval/aod_dust'][...]
    aod_ice = L2['Retrieval/aod_ice'][...]
    aod_oc = L2['Retrieval/aod_oc'][...]
    aod_seasalt = L2['Retrieval/aod_seasalt'][...]
    aod_sulfate = L2['Retrieval/aod_sulfate'][...]
    aod_total = L2['Retrieval/aod_total'][...]
    aod_water = L2['Retrieval/aod_water'][...]

    #externally given
    t700 = L2['Retrieval/t700'][...]
    psurf = L2['Retrieval/psurf'][...]
    windspeed = L2['Retrieval/windspeed'][...]
    tcwv_apriori = L2['Retrieval/tcwv_apriori'][...]

    #date = L2['date'][...]
    #sounding
    snr_wco2 = L2['Sounding/snr_wco2'][...]
    snr_sco2 = L2['Sounding/snr_sco2'][...]
    snr_o2a = L2['Sounding/snr_o2a'][...]
    glint_angle = L2['Sounding/glint_angle'][...]
    altitude = L2['Sounding/altitude'][...]

    #given
    sza = L2.variables[f"solar_zenith_angle"][...]
    sensor_zenith_angle = L2.variables[f"sensor_zenith_angle"][...]
    latitude = L2.variables[f"latitude"][...]
    longitude = L2.variables[f"longitude"][...]
    #pressure = L2["pressure_levels"]
    time = L2["time"][...]
    date = L2["date"][...]#of satelite time. y,m,d,h,min,sec,msec

    #for analysis
    xco2_apriori = L2["xco2_apriori"][...]
    xco2_raw = L2['Retrieval/xco2_raw'][...]
    xco2_uncertainty = L2.variables['xco2_uncertainty'][...]
    xco2_averaging_kernel = L2.variables['xco2_averaging_kernel'][...]
    tcwv_uncertainty = L2['Retrieval/tcwv_uncertainty'][...]


    print ("date ",np.shape(date))

    land = L2[f"Sounding"].variables['land_fraction'][...]#should be >99
    flag = L2.variables[f"xco2_quality_flag"][...]#should be 0

    #todo: Temperature should be positive flag!
    masks = np.logical_not(flag)
    lands = np.greater_equal(land,90)
    temp_flag = np.greater_equal(t700,0)
    wind_flag = np.greater_equal(windspeed,0) 
    land_mask = np.logical_and(masks,lands)
    land_mask = np.logical_and(land_mask,temp_flag)
    #land_mask = np.logical_and(land_mask,wind_flag) #wind flag is called to ofter. ignore wind

    print(f"sounding range L2: ({L2_id[0]},{L2_id[-1]}) with {L2_id.size} elements ")

    source_files = L2[f"source_files"][...]

    elems = [L2_id,xco2,albedo_o2,albedo_sco2,albedo_wco2,tcwv,aod_bc,aod_dust,aod_ice,aod_oc,aod_seasalt,aod_sulfate,aod_total,aod_water,t700,psurf,windspeed,sza,latitude,longitude, date[:,0],date[:,1],date[:,2]]
    elems2 = [sensor_zenith_angle,snr_wco2,snr_sco2,snr_o2a,glint_angle,altitude,tcwv_apriori,tcwv_uncertainty,xco2_apriori,xco2_uncertainty,xco2_raw,xco2_averaging_kernel]


    elems = [np.ma.filled(elem[land_mask],np.nan) for elem in elems]
    elems2 = [np.ma.filled(elem[land_mask],np.nan) for elem in elems2]

    return elems+elems2, source_files


#Writes filelists

#get files with wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -i <url.txt>
#filePath_L1 = Path(f"data/generate/download/L1/subset_OCO2_L1_Science_V8r_20190226_145859.txt")
#filePath_L2 = Path(f"data/generate/download/L2_9000/subset_OCO2_L2_Lite_FP_V9r_20190226_173114.txt")
#filePath_L1 = Path(__file__).parent.joinpath(f"process/L1/subset_OCO2_L1_Science_V8r_20190307_103950.txt")
#filePath_L2 = Path(__file__).parent.joinpath(f"L2_8100/OCO2LtCO2v8-155195260053.txt")
filePath_L2 = Path(__file__).parent.joinpath(f"L2_9000/subset_OCO2_L2_Lite_FP_V9r_20190308_141525.txt")


def getLoadingList(files_list_path):
    """Takes path list and returns the names of the files
    
    Arguments:
        files_list {[type]} -- f.e. 'L2_9000/subset_OCO2_L2_Lite_FP_V9r_20190308_141525.txt'
    
    Returns:
        files[string] -- f.e. ['oco2_LtCO2_181130_B9003r_190220194056s.nc4']
        filelist[string] -- f.e. ['https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_L2_Lite_FP.9r/2018/oco2_LtCO2_181130_B9003r_190220194056s.nc4']

    """

    files = []

    with files_list_path.open("r") as myfile:
        filelist=myfile.readlines()
    for i, filename in enumerate(filelist):
        #if i>2:
        if "oco2_L1bScND" in filename or "oco2_LtCO2" in filename:
            name = filename.split('/')[-1:][0].strip()
            #print(name)
            files.append(name)
    
    filelist = [flist.strip() for flist in filelist]
    
    return files, filelist



#print(np.shape(files_L1))
#print(np.shape(files_L2))

#print("\n L1 and L2 file lists")
#print(fileList_L1[:10])
#print(fileList_L2[:10])




def read_L2(fileList_L2):
    """Reads all L2 files in list. Calls getL2 for each entry
    
    Arguments:
        fileList_L2 {[type]} -- List of L2 filename
    
    Returns:
        L2_array_list -- all relevant information from L2
        source_list -- L1 files, used to generate this L2 file
    """

    L2_array_list = []
    source_list = []
    t = time.perf_counter()
    #print(f"t0: {time.perf_counter() - t:.2f}s")
    for i,L2 in enumerate(fileList_L2):
        print(i,"L2 ",L2)
        L2Path = Path(__file__).parent.joinpath(f"L2_9000/{L2}")
        #download(L2,writePath)
        #if i>0:
        L2s, sources = get_L2(L2Path)

        L2_array_list.append(L2s)
        for source in sources:
            source_list.append(source)

    print(f"Time to read {i} L2 files: {time.perf_counter() - t:.2f}s")
    return L2_array_list,source_list



def getL2_ids(L2_array_list):
    #Get L2 id
    L2_ids = list(zip(*L2_array_list))[0] #returns masked arrays
    print(np.shape(L2_ids))
    L2_ids = [(L2.data) for L2 in L2_ids]#removes the mask and flattens
    print(np.shape(L2_ids))
    L2_ids = np.concatenate(L2_ids)#.flatten()#turn the list into a single np array
    print(L2_ids)
    #np.save((Path(__file__).parent.joinpath(f"tmp/L2_id.npy")),L2_ids)
    return L2_ids


def matchL1L2(L1_ids,L2_ids):
    L1_ids = L1_ids.flatten()
    mutal_ids = np.intersect1d(L1_ids,L2_ids) #for filtering all matches
    print("mutal: ",np.shape(mutal_ids),"single: L1 ",np.shape(L1_ids), ", L2 ", np.shape(L2_ids))
    pos = np.where(L1_ids == L2_ids[0])
    #print (pos)
    #np.set_printoptions(suppress=True)
    #print(L1_ids[pos[0][0]:][:100])
    #print(mutal_ids.astype(int)[:100])
    #print(L2_ids[:100])

    mask_equal_L1 = np.isin(L1_ids,L2_ids)
    mask_equal_L2 = np.isin(L2_ids,L1_ids)
    #print(L1_ids[mask_equal_L1][:100])
    #print(np.shape(mask_equal_L1),np.shape(mask_equal_L2),np.shape(L1_ids),np.shape(L2_ids))
    #print(np.sum(np.abs(L1_ids[mask_equal_L1]-L2_ids)))
    print("0 check: ",np.sum(np.abs(L1_ids[mask_equal_L1]-L2_ids[mask_equal_L2])))
    print("unused L2 values: ",np.sum(mask_equal_L2 == False))
    assert np.sum(np.abs(L1_ids[mask_equal_L1]-L2_ids[mask_equal_L2]))<0.1
    if np.abs(np.sum(mask_equal_L2 == False))>0.1:
        print("\n\n WARNING! Not all L2 values were matched")
    return mask_equal_L1, mask_equal_L2

def saveElems(array_list,mask_equal, name = "L1"):
    #sort out L1 elems and get big array
    elems = np.array([])
    elem_list = list(zip(*array_list))
    for i in range(len(array_list[0])):
        elem = elem_list[i]
        #for e in L1_elem:
        #        print(i,np.shape(e))
        elem = np.concatenate(elem,axis=0)
        #print("1 elem ",np.shape(L1_elem))
        elem=elem[mask_equal]
        #print("1 elem masked",np.shape(L1_elem))
        #print("all elems ",np.shape(L1_elems))
        #print("elem1",np.shape(elem))
        if elem.ndim < 2:
                elem = elem [:,None]
        #print("elem2",np.shape(elem))
        elems= np.concatenate([elems, elem],axis=1) if elems.size else elem #np.vstack
        #L1_elems.append()

    elemsPath = f"npy/{name}_elems.npy"
    print(f"{name}_elems shape {np.shape(elems)},saved to {elemsPath}")
    np.save(Path(__file__).parent.joinpath(elemsPath),elems)
    return elems

def read_L1(files_L1,source_list, month = "1409"):
    load_spectra = []
    #print(files_L1)
    #get list of L1 files to download
    for filename in source_list:
        name = filename.split('/')[-1:][0].strip()
        name_split = name.split('_')
        ##print(name_split)
        if name_split[1] == "L2StdND":
            #load_spectra.append(f"oco2_L1bScND_{name_split[3]}_{name_split[4]}_{name_split[5]}_")#'oco2_L1bScND_22586a_180930_B8100r'
            L1_name = f"oco2_L1bScND_{name_split[2]}_{name_split[3]}_" #{name_split[4]}_ B8100r (L2) and B8000r (L1b)
            #print(L1_name)
            #print(files_L1[:2])
            complete_L1 = [s.strip() for s in files_L1 if L1_name in s]
            if len(complete_L1)>1:
                print("found to many")
                print(complete_L1)
            if len(complete_L1)>0:
                print("Found and will append L1 path",complete_L1[0])
                load_spectra.append(complete_L1[0])
            else:
                print(f"{filename} not found")
                print(f"Was looking for {L1_name}")
            #assert complete_L1

    
    if len(load_spectra)>0:
        #Loads L1 files previously selected
        t = time.perf_counter()

        #L1_ids = np.load((Path(f"tmp/L1_id.npy")))#(__file__).parent.joinpath
        L1_array_list = []
        print(f"\nwill read {len(load_spectra)} files")
        for i,L1 in enumerate(load_spectra):
            readPath = Path(__file__).parent.joinpath(f"L1/{month}/{L1}")
            print(i," L1 ",readPath)#(__file__).parent.joinpath
            if i<100:
                L1s = get_L1(readPath)#(__file__).parent.joinpath
                L1_array_list.append(L1s)
        print(f"Time to read L1: {time.perf_counter() - t:.2f}s")
        return L1_array_list

    else:
        print("\n\ncould not find spectra\n\n")
        return []

def load_and_match(file_L2,month,filenumber):
    """Matches all L1 files belonging to a L2 file. Results are saved and named after 
    
    Arguments:
        file_L2 {[string]} -- [L2 file path]
        month {[int]} -- [month]
        filenumber {[int]} -- [day of month]
    """

    #loads content from L2 file
    L2_array_list,source_list = read_L2([file_L2])
    L2_ids = getL2_ids(L2_array_list)
    print("L2_ids",L2_ids)
    #uses source list of L2 to find correct L1 files
    L1_array_list = read_L1(files_L1,source_list, month)
    if len(L1_array_list)>0:
        L1_ids = list(zip(*L1_array_list))[0] 
        L1_ids = [(L1.data) for L1 in L1_ids]

        L1_ids = np.concatenate(L1_ids,axis=0)
        print("L1 id shape",np.shape(L1_ids))

        mask_equal_L1, mask_equal_L2 = matchL1L2(L1_ids,L2_ids)

        print("\n")
        #Saves results for each day and month
        saveElems(L1_array_list,mask_equal_L1, name = f"L1_{month}{filenumber:02d}")
        saveElems(L2_array_list,mask_equal_L2, name = f"L2_{month}{filenumber:02d}")
    else:
        print(f"\n\n\n No Spectrum for day {month}{filenumber:02d}")

#select files to load
month_L2 = [1409,1607]
month_L2 = [1409,1410,1411,1412]
month_L2 = [1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512]
month_L2 = [1601,1602,1603,1604,1605,1606,1607,1608,1609,1610,1611,1612]
month_L2 = [1701,1702,1703,1704]
month_L2 = [1705,1706,1707]
month_L2 = [1709,1710,1711,1712]
month_L2 = [1801,1802,1803,1804]
month_L2 = [1805,1806,1807,1808]
month_L2 = [1809,1810,1811,1812]
files_L2, _ = getLoadingList(filePath_L2)
for month in month_L2:
    print("\n Starts month ",month)
    t_month = time.perf_counter()
    #gets all lists in month file and uses first one
    filePath_glob_L1 = Path(__file__).parent.joinpath(f"L1/{month}/").glob("subset_OCO2_L1B_Science_*")#1409/subset_OCO2_L1B_Science_V8r_20190307_131740.txt"
    #globlist = list(filePath_glob_L1)
    filePath_L1 = list(filePath_glob_L1)[0]
    print("Reads L1 files from file",filePath_L1)
    files_L1, fileList_L1 = getLoadingList(filePath_L1)
    
    print(f"\n Found {np.shape(files_L1)} L1 and {np.shape(files_L2)} L2 files")

    #Will likely select one L2 Lite file for each day of the month
    monthList =[m for m in files_L2 if f"oco2_LtCO2_{month}" in m ]
    print("L2 files relevant for month",monthList)
    print(f"Will read {len(monthList)} days")
    #Matches the L1 files for each day of the month. Results are saved in files named after month and day
    for i in range(len(monthList)):#len(monthList)-1,
        t_day = time.perf_counter()
        load_and_match(monthList[i],month,i)
        print(f"Time process day: {time.perf_counter() - t_day:.2f}s")
    print(f"Time process month: {time.perf_counter() - t_month:.2f}s")

def dict_list(L1_elems,L2_elems):
    all_elems = np.concatenate([L2_elems, L1_elems],axis=1)
    print(np.shape(all_elems))
    spec_length= 1016
    namedict = {
        "L2_id":0,
        "xco2":1,
        "albedo_o2":2,
        "albedo_sco2":3,
        "albedo_wco2":4,
        "tcwv":5,
        "aod_bc":6,
        "aod_dust":7,
        "aod_ice":8,
        "aod_oc":9,
        "aod_seasalt":10,
        "aod_sulfate":11,
        "aod_total":12,
        "aod_water":13,
        "t700":14,
        "psurf":15,
        "windspeed":16,
        "sza":17,
        "latitude":18,
        "longitude":19,
        "year":20,
        "month":21,
        "day":22,
        "L1_id":23,
        "sza":24,
        "flag":25,
        "sco2":list(range(26,26+spec_length)),
        "wco2":list(range(26+spec_length,26+spec_length*2)),
        "o2":list(range(26+spec_length*2,26+spec_length*3)),
    }

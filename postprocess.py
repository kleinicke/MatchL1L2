import numpy as np
import glob
import re

from pathlib import Path
import time
import timeit
import math

"""Get required files from 
https://1drv.ms/f/s!AvXm21cCRGJ86hYwZC2TJvxV40Pk
and put them in co2_data/files.
Required by functions load_spects load_params
Returns:
    [type] -- [description]
"""

#todo get date... at least month test and compare with and without sin
#todo: use date parameter, load numpy passively 
spec_length= 1016

kernel_length = 20
spec_start = 34+1+kernel_length
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
    "sensor_zenith_angle":23,
    "snr_wco2":24,
    "snr_sco2":25,
    "snr_o2a":26,
    "glint_angle":27,
    "altitude":28,
    "tcwv_apriori":29,
    "tcwv_uncertainty":30,
    "xco2_apriori":31,
    "xco2_uncertainty":32,
    "xco2_raw":33,
    "xco2_averaging_kernel":list(range(34,34+kernel_length)),
    "L1_id":34+kernel_length,
    "sco2":list(range(spec_start,spec_start+spec_length)),
    "wco2":list(range(spec_start+spec_length,spec_start+spec_length*2)),
    "o2":list(range(spec_start+spec_length*2,spec_start+spec_length*3)),
}
#test = np.array([1,2,3,4])
#print(test)
#slicer = np.ones(test.size,dtype=bool)
#print(slicer)
#print(test[slicer])
#print(spec_start+spec_length*3)
#assert 0
spectra_names = ["sco2","wco2","o2","snr_wco2","snr_sco2","snr_o2a","sza","day","month","month","month","year","xco2_apriori","tcwv_apriori","sensor_zenith_angle","glint_angle","altitude","psurf","t700","longitude","latitude"] 
#spectra_names = ["sco2","wco2","o2","snr_wco2","snr_sco2","snr_o2a","sza","day","month","year","sensor_zenith_angle","glint_angle","altitude","psurf","t700","longitude","latitude"] 
#spectra_names = ["sco2","wco2","o2","sza","longitude","latitude","psurf","t700"] 
params_names = np.array(["xco2","xco2","albedo_o2","albedo_sco2","albedo_wco2","tcwv","tcwv","aod_bc","aod_dust","aod_ice","aod_oc","aod_seasalt","aod_sulfate","aod_total","aod_water"])
#params_names = np.array(["xco2","xco2","albedo_o2","albedo_sco2","albedo_wco2","tcwv","aod_bc","aod_dust","aod_ice","aod_oc","aod_seasalt","aod_sulfate","aod_total","aod_water"])
#ana_names = ["xco2","tcwv_apriori","tcwv_uncertainty","xco2_apriori","xco2_uncertainty","xco2_raw","xco2_averaging_kernel","longitude","latitude"]

ana_names = ["xco2","tcwv","tcwv_apriori","tcwv_uncertainty","xco2_apriori","xco2_uncertainty","xco2_raw","xco2_averaging_kernel","longitude","latitude"]

#params_mask = np.array([1,1,1,1,1,0,1,1,0,0,1,1,1],dtype=bool)
#params_mask = np.array([1,1,1,1,1,0,1,0,0,0,0,1,0],dtype=bool)
#params_mask = np.array([0,1,1,1,1,0,1,0,0,0,0,0,0,1,0],dtype=bool)#9#10
#params_mask = np.array([1,0,1,1,1,1,0,0,0,0,0,0,0,1,0],dtype=bool)#8#11
#params_mask = np.array([1,1,1,1,1,1,0,0,0,0,0,0,0,1,0],dtype=bool)#13
#params_names = params_names[params_mask]
#params_mask = np.ones(params_names.size,dtype=bool)
#params_mask = np.array([1,1,1,1,1,0,1,0,0,0,0,1,0],dtype=bool)
#params_mask = np.array([1,1,1,1,1,0,0,0,0,0,0,1,0],dtype=bool)
#print(params_names)

#spec_mask = np.ones(len(spectra_names),dtype=bool)
#a_index = spectra_names.index("xco2_apriori")
#tis number will be deleted. Make it positive to delete nothing.
#spec_delete = np.array([-(len(spectra_names)-a_index)])#10
#spec_delete = np.array([5])
####spec_mask[a_co2_offset] = False

#print(spectra_names,spec_mask)
#print(np.asarray(spectra_names)[spec_mask])
#print(np.delete(np.asarray(spectra_names),len(spectra_names)+spec_delete))
print(np.asarray(spectra_names))

#assert 0

#def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
spectra_pos = []
for spec in spectra_names:
    spec = namedict[spec]
    spectra_pos+= spec if type(spec) is list else [spec]
#spectra_pos = [namedict[spec] for spec in spectra_name_list]
params_pos = [namedict[params] for params in params_names]

ana_pos = []
for ana in ana_names:
    ana = namedict[ana]
    ana_pos+= ana if type(ana) is list else [ana]
#world_positions = np.array([1,2],dtype=int)
#print(spectra_names[-2:])
#assert 0
#print("params: ",len(params_pos),params_pos)
#print("spects: ",len(spectra_pos),spectra_pos)



additional_trainingdata_sets = []
number_of_additional_trainingdata_sets = len(additional_trainingdata_sets)
kill_spectra = False
load_orig_data = True
external_config = 0
use_additional_parameter = []
number_external_params = len(spectra_names)-3#5


#training_config_text = "loads"
#if load_orig_data:
#    training_config_text += f" orig data and"
#training_config_text += f"{number_of_additional_trainingdata_sets} additional sets. The sets are {additional_trainingdata_sets}"
#print(training_config_text)
mu_x,w_x,mu_y,w_y,mu_py,w_py=[0,0,0,0,0,0]
epsilon=1e-10


plotting=False

if plotting:
    import plot_data

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

filtered_L1L2_path = Path(__file__).parent.joinpath("../files/0_filtered_L1L2")
spectraparams_path = Path(__file__).parent.joinpath("../files/1_spectraparams/")
samples_path = Path(__file__).parent.joinpath("../files/1_sp_samples/")
normed_path = Path(__file__).parent.joinpath("../files/2_normed")
xy_unsorted_path = Path(__file__).parent.joinpath("../files/3_unsorted_xy/")
xy_train_path = Path(__file__).parent.joinpath("../files/4_train_xy/")
xy_test_path = Path(__file__).parent.joinpath("../files/4_test_xy/")
short_test_path = Path(__file__).parent.joinpath("../files/4_short_test_xy/")
files_folder_path = Path(__file__).parent.joinpath("../files/")



def sort_elems():
    """
    Matches L1 and L2 files into long file, creates elem and spec files and sorts for bad spectra.

    Returns:
        [type] -- [description]
    """
    #data_month = [1409]#,14100,14101,14102,1411,1412,1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1607]
    #data_month = [14101,14102,1411,1412,1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1607]

    sample_params = np.array([])
    sample_spectra = np.array([])

    """
    samples_p = sorted(files_month_path.glob(f"sample_params*.npy"))
    samples_s = sorted(files_month_path.glob(f"sample_spectra*.npy"))
    print(samples_p,samples_s)
    if len(samples_p) > 0 and True:
        print("loads samples")
        sample_params = np.load(samples_p[-1])
        sample_spectra = np.load(samples_s[-1])
    """
    t_total = time.perf_counter()
    print("Start with samplesize of ",len(sample_params))
    L2s = sorted(filtered_L1L2_path.glob(f"L2_*.npy"))
    L1s = sorted(filtered_L1L2_path.glob(f"L1_*.npy"))
    for i in range(math.ceil(len(L2s)/5)):
        L2_names = L2s[i*5:(i+1)*5]
        L1_names = L1s[i*5:(i+1)*5]
        week = str(L2_names[0]).split('/')[-1:][0].strip()[3:9]
        print(f"\n\n\n Starting week {week}\n")
        t_month = time.perf_counter()
        L1_elems = np.array([])
        L2_elems = np.array([])

        for path in L2_names:#sorted(filtered_L1L2_path.glob(f"L2_{week}*.npy")):
            L2 = np.load(str(path),mmap_mode = 'c')
            L2_elems = np.concatenate([L2_elems, L2],axis=0) if len(L2_elems) > 0 else L2
            print(f"L2 filelenth: {len(L2_elems)}")

        for path in L1_names:#sorted(filtered_L1L2_path.glob(f"L1_{week}*.npy")):
            L1 = np.load(str(path),mmap_mode = 'c')
            L1_elems = np.concatenate([L1_elems, L1],axis=0) if len(L1_elems) > 0 else L1
            print(f"L1 filelenth: {len(L1_elems)}")

        print(np.shape(L1_elems),np.shape(L2_elems))

        #filtered_L1L2_path = Path(__file__).parent.joinpath("files/")
        #L1_elems = np.load(filtered_L1L2_path.joinpath("L1_elems.npy"))
        #L2_elems = np.load(filtered_L1L2_path.joinpath("L2_elems.npy"))
        all_elems = np.concatenate([L2_elems, L1_elems],axis=1) 
        len(all_elems)
        length_mask = np.full(len(all_elems), False)
        length_mask[:int(len(all_elems)/4)] = True
        np.random.shuffle(length_mask)
        all_elems=all_elems[length_mask]
        #for i in range(spec_start+2):
        #    if i < 35:
        #        print("elems",i,list(namedict)[i],np.min(all_elems[:,i]),np.max(all_elems[:,i])) #todo add name of elem
        #    else:
        #        print("elems",i,np.min(all_elems[:,i]),np.max(all_elems[:,i])) #todo add name of elem
        #for i in range(10):
        #    print("elems",-i,np.min(all_elems[:,-i]),np.max(all_elems[:,-i])) #todo add name of elem
        for i in range(len(list(namedict))):
            #print(namedict[list(namedict)[i]])
            print("elems",i,list(namedict)[i],np.min(all_elems[:,namedict[list(namedict)[i]]]),np.max(all_elems[:,namedict[list(namedict)[i]]])) #todo add name of elem
 
        params = all_elems[:,params_pos]
        spectra = all_elems[:,spectra_pos]
        #print(spectra[:,world_positions])
        #for i in range(len(params[0])):
        #    print(params_names[i],i,np.min(params[:,i]),np.max(params[:,i])) 
        #    spectra_names
        #for i in range(len(spectra_names[:])-3):
        #    print(spectra_names[-i],-i-1,np.min(spectra[:,-i]),np.max(spectra[:,-i])) #

        print(f"found NaN values in params: {np.sum(np.isnan(params))} and spectra: {np.sum(np.isnan(spectra))}")
        #print(f"faulti spectra1: {np.sum(np.array(np.sum(np.isnan(spectra),axis=1),dtype=bool))}")
        #print(f"faulti spectra0: {np.sum(np.array(np.sum(np.isnan(spectra),axis=0),dtype=bool))}")
        print(f"faulti spectra: {np.sum(np.isnan(spectra).any(axis=1))}")
        print(f"faulti channel: {np.sum(np.isnan(spectra).any(axis=0))}")
        print(np.isnan(spectra).any(axis=0))
        print(np.shape(np.isnan(spectra).any(axis=0)))
        #assert 0
        print("small t:",np.sum(spectra[:,-1]<-10000))
        print("small 668:",np.sum(spectra[:,668]<1e10))
        print("small spectra:",np.sum((spectra[:,:3*spec_length]<1e5).any(axis=1)))
        print("small both:",np.sum(np.logical_or(spectra[:,668]<1e10,spectra[:,-1]<-10000)))
        #unusual_mask = np.logical_not(np.logical_or(spectra[:,668]<1e10,spectra[:,-1]<-10000))
        unusual_mask = np.logical_and(np.logical_not(np.isnan(spectra).any(axis=1)),np.logical_not((spectra[:,:3*spec_length+3]<1e0).any(axis=1)))#np.logical_and(unusual_mask,)
        print("deletes",len(spectra)-np.sum(unusual_mask),"spectra")
        print("len params, spectra before",len(params),len(spectra))
        params = params[unusual_mask]
        spectra = spectra[unusual_mask]

        #print("len params, spectra before",len(params),len(spectra))
        all_elems = all_elems[unusual_mask]
        print("applied masks")
        for i in range(3):
            print(spectra_names[i],i,np.min(spectra[:,i*spec_length:(i+1)*spec_length]),np.max(spectra[:,i*spec_length:(i+1)*spec_length])) 
        ana_elems = all_elems[:,ana_pos]
        i_apriori = ana_names.index("xco2_apriori")
        params[:,0] -= ana_elems[:,i_apriori]
        i_tcwv_apriori = ana_names.index("tcwv_apriori")
        i_tcwv = np.where(params_names=="tcwv")[0][0]
        i_month = spectra_names.index("month")
        i_rel_month = i_month - len(spectra_names)
        #print(spectra[0,i_rel_month:i_rel_month+3])
        spectra[:,i_rel_month+1]=np.sin(spectra[:,i_rel_month]/12*2*np.pi)
        spectra[:,i_rel_month+2]=np.cos(spectra[:,i_rel_month]/12*2*np.pi)
        #print(spectra[0,i_rel_month-1:i_rel_month+5])
        #assert 0
        #print(i_tcwv)
        #print(np.where(params_names=="tcwv"))
        #print(params[0,i_tcwv],ana_elems[0,i_tcwv_apriori])

        params[:,i_tcwv] -=ana_elems[:,i_tcwv_apriori]
        #print(params[0,0],ana_elems[0,0],ana_elems[0,i_apriori])
        #print(params[0,i_tcwv],ana_elems[0,i_tcwv_apriori])
        #assert 0
        ##np.save(spectraparams_path.joinpath(f"all_elems{week}.npy"),all_elems)
        np.save(spectraparams_path.joinpath(f"spectra{week}.npy"),spectra)
        np.save(spectraparams_path.joinpath(f"params{week}.npy"),params)
        np.save(spectraparams_path.joinpath(f"ana_elems{week}.npy"),ana_elems)

        #Sample some spec and elems to apply whightening on the data
        all_elems = None
        ana_elems = None
        print(params[0:2,:10])
        #for i in range(3):
        #    print(spectra_names[i],i,np.min(spectra[:,i*spec_length:(i+1)*spec_length]),np.max(spectra[:,i*spec_length:(i+1)*spec_length])) 
        #    print(spectra_names[i],i,np.min(np.log(spectra[:,i*spec_length:(i+1)*spec_length])),np.max(np.log(spectra[:,i*spec_length:(i+1)*spec_length]))) 

        print("len params, spectra after",len(params),len(spectra))
        print("all spectra",np.min(spectra[:,:]),np.max(spectra[:,:]))

        #logspectra = np.concatenate([np.log(spectra[:,:3*spec_length]),spectra[:,3*spec_length:]],axis = 1)
        np.log(spectra[:,:3*spec_length],out = spectra[:,:3*spec_length])
        logspectra = spectra
        #print(np.sum(logspectra-spectra))
        #assert 0
        spectra = None
        print("all logspectra",np.min(logspectra[:,:]),np.max(logspectra[:,:]),np.shape(logspectra))        #assert not np.isnan(logspectra).any

        print("found nans in logspectrum:",np.isnan(logspectra).any())
        choosen_spectra = logspectra[np.random.choice((logspectra.shape[0]),size = 1000, replace = False)]
        sample_spectra = np.concatenate([sample_spectra, choosen_spectra],axis=0) if len(sample_spectra) > 0 else choosen_spectra
        choosen_params = params[np.random.choice((params.shape[0]),size = 1000, replace = False)]
        sample_params = np.concatenate([sample_params, choosen_params],axis=0) if len(sample_params) > 0 else choosen_params
        print("samples:", np.shape(sample_params),np.shape(sample_spectra))
        #print("len params, spectra after",len(params),len(spectra))

        #print(spectra[:,668].tolist())
        #for i in range(len(logspectra[0])):
        #    print("spectra",i,np.min(spectra[:,i]),np.max(spectra[:,i]))
        #    print("logspectra",i,np.min(logspectra[:,i]),np.max(logspectra[:,i]))
            #del spectra 668

        """
        load = False
        if load:
            mu_x = np.load(filtered_L1L2_path.joinpath("mu_x.npy"))
            w_x = np.load(filtered_L1L2_path.joinpath("w_x.npy"))
            mu_y = np.load(filtered_L1L2_path.joinpath("mu_y.npy"))
            w_y = np.load(filtered_L1L2_path.joinpath("w_y.npy"))
            x = params_to_x(params,mu_x, w_x)
            y = obs_to_y(logspectra,mu_y, w_y)
        else:
            print("params:")
            mu_x,w_x = (np.mean(params, 0),whitening_matrix(params))
            print("spectra:")
            sample_spectra = logspectra[np.random.choice(logspectra.shape[0],10000,replace=False)]
            mu_y,w_y = (np.mean(sample_spectra, 0),whitening_matrix(sample_spectra))
            #mu_py,w_py = (np.mean(logspectra, 0),whitening_matrix(logspectra))
            x = params_to_x(params,mu_x, w_x)
            y = obs_to_y(logspectra,mu_y, w_y)
        """
        assert not np.isnan(np.sum(params))
        assert not np.isnan(np.sum(logspectra))
        #np.save(files_path.joinpath("mu_x.npy"),mu_x)
        #np.save(files_path.joinpath("w_x.npy"),w_x)
        #np.save(files_path.joinpath("mu_y.npy"),mu_y)
        #np.save(files_path.joinpath("w_y.npy"),w_y)
        #np.save(files_month_path.joinpath(f"logspectra{week}.npy"),logspectra)
        np.save(samples_path.joinpath(f"sample_spectra{week}.npy"),sample_spectra)
        np.save(samples_path.joinpath(f"sample_params{week}.npy"),sample_params)
        #np.save(files_path.joinpath("x.npy"),x)
        #np.save(files_path.joinpath("y.npy"),y)


        #print("Show last spectra: ",spectra[0:10,-10:])
        print(f"Time process month: {time.perf_counter() - t_month:.2f}s")
        #print(f"And in exact: {timeit.default_timer() - t_ex_month:.2f}s")
    print(f"Time process all month: {time.perf_counter() - t_total:.2f}s")

    #all_elems, params, spectra, mu_y, w_y, mu_x, w_x, x, y



def sort_arrays(month="2015", filesize = 10000):
    """Rearranges arrays, to be equally sized, so loading is easiert for the dataloader
    """

    params_list = sorted(spectraparams_path.glob(f"params{month[-2:]}*.npy"))#[0-5]
    spectra_list = sorted(spectraparams_path.glob(f"spectra{month[-2:]}*.npy"))
    ana_list = sorted(spectraparams_path.glob(f"ana_elems{month[-2:]}*.npy"))
     
    print(params_list)
    print(spectra_list)
    print(ana_list)
    params_values = np.array([])
    spectra_values = np.array([])
    ana_values = np.array([])
    index = 0
    for i in range((len(params_list))):
        number = str(params_list[i]).split('/')[-1:][0].strip()[6:12]
        number2 = str(spectra_list[i]).split('/')[-1:][0].strip()[7:13]
        print(i, number,number2)
        assert number == number2, print(number,number2)
        params_val = np.load(params_list[i])
        spectra_val = np.load(spectra_list[i])       
        ana_val = np.load(ana_list[i])
        #print(ana_val.shape,x_val.shape,ana_list[i],ana_list[i])       
        params_values = np.concatenate([params_values, params_val],axis=0) if len(params_values) > 0 else params_val
        spectra_values = np.concatenate([spectra_values, spectra_val],axis=0) if len(spectra_values) > 0 else spectra_val
        ana_values = np.concatenate([ana_values, ana_val],axis=0) if len(ana_values) > 0 else ana_val
        print(len(params_values))
        assert len(params_values)==len(spectra_values),f"{len(x_values),len(y_values)}"
        assert len(ana_values)==len(params_values),f"length{len(ana_values),len(x_values)}"
        while len(params_values)>filesize:
            np.save(files_folder_path.joinpath(f"4_spectraparams_{month}/params_{index:03d}"),params_values[:filesize])
            np.save(files_folder_path.joinpath(f"4_spectraparams_{month}/spectra_{index:03d}"),spectra_values[:filesize])
            np.save(files_folder_path.joinpath(f"4_spectraparams_{month}/ana_{index:03d}"),ana_values[:filesize])
            
            index+=1
            params_values = np.delete(params_values, np.s_[0:filesize], axis = 0)
            spectra_values = np.delete(spectra_values, np.s_[0:filesize], axis = 0)
            ana_values = np.delete(ana_values, np.s_[0:filesize], axis = 0)
            print(np.shape(params_values))

def shorten_test(filesize = 10000):
    x_list = sorted(xy_test_path.glob(f"x*.npy"))
    y_list = sorted(xy_test_path.glob(f"y*.npy"))
    ana_list = sorted(xy_test_path.glob(f"ana*.npy"))
    x_values = np.array([])
    y_values = np.array([])
    ana_values = np.array([])
    for i in range(len(x_list)):
        x = np.load(x_list[i])
        y = np.load(y_list[i])       
        ana = np.load(ana_list[i])
        mask = np.full(len(x), False)
        mask[:int(len(x)/20)] = True
        np.random.shuffle(mask)
        x=x[mask]
        y=y[mask]
        ana = ana[mask]
        x_values = np.concatenate([x_values, x],axis=0) if len(x_values) > 0 else x
        y_values = np.concatenate([y_values, y],axis=0) if len(y_values) > 0 else y
        ana_values = np.concatenate([ana_values, ana],axis=0) if len(ana_values) > 0 else ana
        while len(x_values)>filesize:
            np.save(xy_test_path.joinpath(f"x_{index:03d}"),x_values[:filesize])
            np.save(xy_test_path.joinpath(f"y_{index:03d}"),y_values[:filesize])
            np.save(xy_test_path.joinpath(f"ana_{index:03d}"),ana_values[:filesize])
            index+=1
            x_values = np.delete(x_values, np.s_[0:filesize], axis = 0)
            y_values = np.delete(y_values, np.s_[0:filesize], axis = 0)
            ana_values = np.delete(ana_values, np.s_[0:filesize], axis = 0)
            print(np.shape(x_values))
        
#sort_elems()
sort_arrays(month="2014")
sort_arrays(month="2015")
sort_arrays(month="2016")
sort_arrays(month="2017")
sort_arrays(month="2018")

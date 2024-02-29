import h5py 
import numpy as np
from netCDF4 import Dataset as DS
import os
import argparse


DEFAULT_NCHANNELS = 20
CHANNELS = (
    ('u10',0,'surface'), # 0 surface
    ('v10',0,'surface'), # 1 surface
    ('t2m',0,'surface'), # 2 surface
    ('sp',0,'surface'), # 3 surface
    ('msl',0,'surface'), # 4 surface
    ('t',2,'pl'), #5 850hpa
    ('u',3,'pl'), #6 1000hpa
    ('v',3,'pl'), #7 1000hpa
    ('z',3,'pl'), #8 1000hpa 
    ('u',2,'pl'), #9  850hpa
    ('v',2,'pl'), #10 850hpa,
    ('z',2,'pl'), #11 850hpa,
    ('u',1,'pl'), #12 500hpa,
    ('v',1,'pl'), #13 500hpa
    ('z',1,'pl'), #14 500hpa
    ('t',1,'pl'), #15 500hpa,
    ('z',0,'pl'), #16 50hpa
    ('r',1,'pl'), #17 500hpa
    ('r',2,'pl'), #18 500hpa
    ('tcwv','0','surface') #19 Integrated
)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg # return an open file handle

def add_feature(src,dest,channel_idx,variable_name,src_idx=0,frmt='nc'):
    if frmt == 'nc':
        fsrc = DS(src,'r',format="NETCDF4").variables[variable_name]
    elif frmt == 'h5':
        fsrc = h5py.File(src,'r')[varslist[0]]
    with h5py.File(dest,'a') as fdest:
        if len(fsrc.shape) == 4:
            ims = fsrc[:,src_idx]
        else:
            ims = fsrc
        print(ims.shape)
        fdest['fields'][:,channel_idx,:,:] = ims
    fsrc.close()
                
def make_h5_file(surf,pl,out):
    fsurf = DS(surf,'r')
    fpl = DS(pl,'r')
    if fsurf.dimensions['time'].size != fpl.dimensions['time'].size:
        raise ValueError("Surface and Pressure level files are of different lengths!")
    fpl.close()
    time = fsurf.dimensions['time'].size
    width = fsurf.dimensions['longitude'].size
    height = fsurf.dimensions['latitude'].size
    with h5py.File(out,'w') as fdest:
        fdest.create_dataset('fields',(time,DEFAULT_NCHANNELS,height,width))
    fsurf.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create FourCastNet H5 file from ERA5 inputs")
    parser.add_argument('surface',type=lambda x: is_valid_file(parser,x),help='ERA5 Surface Variable file (netCDF)')
    parser.add_argument('pl',type=lambda x: is_valid_file(parser,x),help='ERA5 Output Variable file (netCDF)')
    parser.add_argument('output',type=str,help='Output location of h5 file')

    args = parser.parse_args()
    make_h5_file(args.surface,args.pl,args.output)

    for i,(var,src_idx,file) in enumerate(CHANNELS):
        print(var,src_idx,file)
        add_feature(args.surface if file == 'surface' else args.pl,args.output,i,var,src_idx)
        print('Written channel #'+str(i))
    print("DONE!")
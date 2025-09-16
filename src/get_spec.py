
# SPARCL imports
from sparcl.client import SparclClient

import pandas as pd
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.coordinates import SkyCoord

# Data Lab imports
from dl import queryClient as qc
from dl import authClient as ac
from getpass import getpass

import utils

def get_spec(cons):
    client = SparclClient()
    
    out = ['sparcl_id', 'ra', 'dec', 'redshift', 'spectype', 'objtype', 'data_release', 'desiname', 'zcat_nspec', 'targetid']
    found_I = client.find(outfields=out, constraints=cons, limit=None)
    
    # Define the fields to include in the retrieve function
    inc = ['sparcl_id', 'specid', 'targetid', 'data_release', 'redshift', 'flux',
           'wavelength', 'model', 'ivar', 'mask', 'wave_sigma', 'spectype', 'ra', 'dec']
    
    ids_I = found_I.ids
    results_I = client.retrieve(uuid_list=ids_I, include=inc, limit=None, dataset_list = ['DESI-DR1'])
    
    results_desi_dr1 = pd.json_normalize(results_I.records)

    return results_desi_dr1

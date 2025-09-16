
import os
import utils
import spectrum_io
import pandas as pd


def main(saving_dir): 

    """
    Retrieves DESI spectra for a given object name and RA, DEC and Redshift ranges.

    Parameters
    ----------
    name : str
        The name of the object to retrieve the spectra for.

    Returns
    -------
    results_DESI_DR1 : pandas.DataFrame
        A DataFrame containing the retrieved spectra.

    Notes
    -----
    This function filters the DESI spectra by the given RA, DEC and Redshift ranges, and then 
    saves the results to a new parquet file if the file does not already exist.
    """

    name = 'DESI_DR1_spec.parquet'

    if name not in os.listdir(saving_dir):

        # -------->  Here you need to define the RA, DEC and Redshift ranges of the objects that you want to retrieve from DESI.  < -----------------------------------

        ra_min, ra_max = utils.get_range("Type the right ascension range (X.XXX, Y.YYY): ", "RA")
        dec_min, dec_max = utils.get_range("Type the declination range (X.XXX, Y.YYY): ", "Dec")
        
        do_redshift = input('Do you want to search by redshift too? (y/n): ').lower()
        if do_redshift in ["y", "yes"]:
            z_min, z_max = utils.get_range("Type the redshift range (X.XXX, Y.YYY): ", "z")
            print(f"Filtering by RA: [{ra_min},{ra_max}] and DEC: [{dec_min},{dec_max}] and Redshift: [{z_min},{z_max}]\n")
            cons = {'spectype': ['GALAXY'],
                    'ra': [ra_min,ra_max],
                    'dec': [dec_min,dec_max],
                    'redshift':[z_min,z_max],
                    'data_release': ['DESI-DR1']}        
        else:
            print(f"Filtering by RA: [{ra_min},{ra_max}] and DEC: [{dec_min},{dec_max}]\n")
            cons = {'spectype': ['GALAXY'],
                    'ra': [ra_min,ra_max],
                    'dec': [{dec_min,dec_max}],
                    'data_release': ['DESI-DR1']} 
            

        results_DESI_DR1 = utils.get_spec(cons) # returns a Pandas DataFrame with the results
        count = results_DESI_DR1['spectype'].count()
        if do_redshift in ["y", "yes"]:
            print(f"Retrieved {count} galaxies for RA: [{ra_min},{ra_max}] and DEC: [{dec_min},{dec_max}] and Redshift: [{z_min},{z_max}]\n")
        else: 
            print(f"Retrieved {count} galaxies for RA: [{ra_min},{ra_max}] and DEC: [{dec_min},{dec_max}]\n")

        # Saving the objects to a new parquet file 
        results_DESI_DR1.to_parquet(f'{saving_dir}{name}', index=False, engine='pyarrow', compression='snappy')
        print(f'Saved retrieved data to {saving_dir} named as {name}.')

        return results_DESI_DR1

    else:
        print(f'Already found parquet file for {name}. \n')
        results_DESI_DR1 = pd.read_parquet(f'{saving_dir}{name}', engine='pyarrow')
        return results_DESI_DR1


if __name__ == "__main__":
    
    if not os.path.exists('./data/'):
        os.makedirs('./data/')

    saving_dir = './data/'
    data = main(saving_dir)

    do_save_txt = input('Do you want to create a .txt file with wavelength, flux and flux error for Starlight input? (y/n): ').lower() 
    if do_save_txt == 'y':
        spectrum_io.to_txt(data, saving_dir)

    do_save_fits = input('Do you want to create a fits file? (y/n): ').lower()
    if do_save_fits == 'y':
        spectrum_io.to_fits(data, saving_dir)
    
    print('Finished!')

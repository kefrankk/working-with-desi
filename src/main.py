
import os
import utils
import spectrum_io
import pandas as pd


def main(): 

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

    if not os.path.exists('./data/'):
        os.makedirs('./data/')

    if name not in os.listdir('./data/'):

        # -------->  Here you need to define the RA, DEC and Redshift ranges of the objects that you want to retrieve from DESI.  < -----------------------------------
        ra_range = [0, 10] 
        dec_range = [-10, 10]
        redshift_range = [0, 0.1]

        if redshift_range:
            print(f"Filtering by RA: {ra_range} and DEC: {dec_range} and Redshift: {redshift_range}\n")
        else: 
            print(f"Filtering by RA: {ra_range} and DEC: {dec_range}\n")

        cons = {'spectype': ['GALAXY'],
                'redshift':redshift_range,
                'ra': ra_range,
                'dec': dec_range,
                'data_release': ['DESI-DR1']}

        results_DESI_DR1 = utils.get_spec(cons) # returns a Pandas DataFrame with the results
        if redshift_range:
            print(f"Retrieved data for RA: {ra_range} and DEC: {dec_range} and Redshift: {redshift_range}\n")
        else: 
            print(f"Retrieved data for RA: {ra_range} and DEC: {dec_range}\n")

        # Saving the objects to a new parquet file 
        results_DESI_DR1.to_parquet(f'./data/{name}', index=False, engine='pyarrow', compression='snappy')

        return results_DESI_DR1

    else:
        print(f'Already found parquet file for {name}. \n')
        results_DESI_DR1 = pd.read_parquet(f'./data/{name}', engine='pyarrow')
        return results_DESI_DR1


def save_to_txt(data, saving_dir):
    """
    Saves the given data to a .txt file with wavelength, flux and flux error for Starlight input.

    Parameters
    ----------
    data : pandas.DataFrame
        The data to be saved to a .txt file. It should have columns named 'wavelength', 'flux' and 'eflux'.
    saving_dir : str
        The directory where the .txt file will be saved.

    Returns
    -------
    None
    """
    spectrum_io.to_txt(data, saving_dir)


if __name__ == "__main__":
    
    data = main()

    do_save_txt = input('Do you want to create a .txt file with wavelength, flux and flux error for Starlight input? (y/n) ')

    if do_save_txt.lower() == 'y':
        saving_dir = './data/'
        save_to_txt(data)
        print('Finished!')

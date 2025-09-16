
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.io import fits

def interpolate_spec(wave, flux, eflux):
    """
    Interpolates a spectrum using linear interpolation.

    Parameters
    ----------
    wave : array
        The wavelengths of the spectrum.
    flux : array
        The fluxes of the spectrum.
    eflux : array
        The errors of the fluxes of the spectrum.

    Returns
    -------
    df : pandas.DataFrame
        A DataFrame containing the interpolated spectrum.

    Notes
    -----
    The errors are also interpolated and filled with the minimum error
    value in case of non-finite values.
    """

    #Cria novo eixo de comprimento de onda com passo de 1 Å
    wavelength_linear = np.arange(np.ceil(wave.min()), np.floor(wave.max()) + 1, 1)

    # Interpola o fluxo
    interp_flux = interp1d(wave, flux, kind='linear', bounds_error=False, fill_value="extrapolate")
    interp_error = interp1d(wave, eflux, kind='linear', bounds_error=False, fill_value="extrapolate")

    flux_linear = interp_flux(wavelength_linear)
    error_linear = interp_error(wavelength_linear)

    error_linear = np.where(~np.isfinite(error_linear), min(eflux), error_linear)

    df = pd.DataFrame({'wavelength': wavelength_linear, 'flux': flux_linear, 'flux_error': error_linear}) #, 'flux_error': flux_error})

    return df


def to_txt(data: pd.DataFrame, saving_dir: str):
    """
    Writes a DataFrame to a text file.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame to be written to a text file.
    saving_dir : str
        The directory where the text file will be saved.

    Notes
    -----
    The text file will be written to a directory specified by the user.
    The filename will be the SPARCL ID of the object.
    The file will contain the restframe wavelength, flux and flux error.
    The file will be written in the format: wavelength flux flux_error.
    """
    for obj, row in data.iterrows():
        flux        = row['flux']
        ivar        = row['ivar']
        wavelength  = row['wavelength']
        redshift    = row['redshift']

        sparclid    = row['sparcl_id']

        eflux       = 1 / np.sqrt(ivar)
        rest_wave = wavelength / (1 + redshift)

        df = interpolate_spec(wave=rest_wave, flux=flux, eflux=eflux)

        df.to_csv(f'{saving_dir}{sparclid}.txt', sep=' ', header=False, index=False)


def to_fits(data, saving_dir):

    for obj, row in data.iterrows():
        wavelength  = row['wavelength']
        flux        = row['flux']
        ivar        = row['ivar']

        sparclid    = row['sparcl_id']

        cdelt = np.median(np.diff(wavelength))
        crpix = 1
        crval = wavelength[0]

        wcs = WCS(naxis=1)
        wcs.wcs.crpix  = [crpix]
        wcs.wcs.cdelt  = [cdelt]
        wcs.wcs.crval  = [crval]
        wcs.wcs.ctype  = ['WAVE']

        header = wcs.to_header()

        # Creates the MEF file
        h = fits.HDUList()
        hdu = fits.PrimaryHDU(header=header)
        hdu.name = 'PRIMARY'
        h.append(hdu)

        # Creates the observed spectrum extension
        hdu = fits.ImageHDU(data=flux, header=header)
        hdu.name = 'FLUX'
        h.append(hdu)

        # Creates the ivar extension.
        hdu = fits.ImageHDU(data=ivar, header=header)
        hdu.name = 'IVAR'
        h.append(hdu)

        h.writeto(f'{saving_dir}{sparclid}.fits', overwrite=True)


        

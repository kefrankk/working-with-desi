
import pandas as pd
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy.convolution import convolve, Gaussian1DKernel


def plot_spec(result):

    """
    Plot the spectrum of a single DESI target.

    Parameters
    ----------
    result : object
        A single record from a SPARCL query, containing the spectrum,
        model, and metadata for the target.

    Returns
    -------
    None

    Notes
    -----
    This function will overwrite any existing plot.  If you want to
    create multiple plots, you should use subplots or create a new figure
    before calling this function.

    """

    sparcl_id       = result.sparcl_id
    data_release    = result.data_release
    flux            = result.flux
    wavelength      = result.wavelength
    model           = result.model
    spectype        = result.spectype
    redshift        = result.redshift
    ra              = result.ra
    dec             = result.dec

    plt.title(f"Data Set = {data_release}\n"
              f"Type = {spectype}\n"
              f"ID = {sparcl_id}\n"
              f"Redshift = {redshift}\n"
              f"RA = {ra}\n"
              f"Dec = {dec}", loc='left')
    plt.xlabel('wavelength $[\AA]$')
    plt.ylabel('$f_{\lambda}$ $(10^{-17}$ $erg$ $s^{-1}$ $cm^{-2}$ $\AA^{-1})$')
    
    # Plot unsmoothed spectrum in grey
    plt.plot(wavelength, flux, color='k', alpha=0.2, label='Unsmoothed spectrum')
    
    # Overplot spectrum smoothed using a 1-D Gaussian Kernel in black
    plt.plot(wavelength, convolve(flux, Gaussian1DKernel(5)), color='k', label='Smoothed spectrum')
    
    # Overplot the model spectrum in red
    plt.plot(wavelength, model, color='r', label='Model spectrum')
    

def match_galaxies(splus, survey):
    # print(splus, survey)
    """
    Matches galaxies between the SPLUS dataset and another survey.
    
    Parameters
    ----------
    splus : pandas.DataFrame
        DataFrame containing galaxies from the SPLUS survey.
    survey : pandas.DataFrame
        DataFrame containing galaxies from the comparison survey.
    
    Returns
    -------
    df_common_filtered : pandas.DataFrame
        DataFrame containing galaxies found in both SPLUS and the comparison survey.
    """

    # Convert the RA and DEC columns to astropy SkyCoord objects
    coords_splus    = SkyCoord(ra=splus["ra"].values * u.degree, dec=splus["dec"].values * u.degree)

    coords     = SkyCoord(ra=survey["ra"].values * u.degree, dec=survey["dec"].values * u.degree)
    
    # Tolerance for the match
    tolerance = 0.5 * u.arcsec

    # Match the galaxies between the two datasets
    idx, d2d, _ = coords.match_to_catalog_sky(coords_splus)

    # Create a mask for the matches
    mask = d2d < tolerance

    # Get the matched DataFrame
    df_matched = splus.iloc[idx].reset_index(drop=True)

    # Concatenate the two DataFrames
    df_common = pd.concat([survey.reset_index(drop=True), df_matched], axis=1)

    # Filter the DataFrame with the mask
    df_common_filtered = df_common[mask]

    return df_common_filtered
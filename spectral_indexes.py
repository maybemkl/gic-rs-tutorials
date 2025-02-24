import xarray as xr

def return_ndvi(data:xr.Dataset) -> xr.DataArray:
    """
    Calculate and return NDVI.
    """

    # Turn red band into floats
    red = data["red"].astype("float") 

    # Turn near infrared band into floats
    nir = data["nir"].astype("float")

    # Calculate NDVI
    ndvi = (nir - red) / (nir + red) 
    return ndvi

def return_ndbi(data: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return NDBI.
    """
    swir = data["swir22"].astype("float")  # e.g., band 11 for Sentinel-2
    nir = data["nir"].astype("float")    # e.g., band 8 for Sentinel-2

    ndbi = (swir - nir) / (swir + nir)
    return ndbi

def return_ndwi(data: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return NDWI (modified version).
    """
    green = data["green"].astype("float")  # e.g., band 3 for Sentinel-2
    swir = data["swir22"].astype("float")    # e.g., band 11 for Sentinel-2

    ndwi = (green - swir) / (green + swir)
    return ndwi

def return_nbai(data: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return NBAI (one common definition).
    """
    swir = data["swir22"].astype("float")   # e.g., band 11 for Sentinel-2
    green = data["green"].astype("float") # e.g., band 3 for Sentinel-2

    nbai = (swir - green) / (swir + green)
    return nbai

def return_nbr(data: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return NBR (Normalized Burn Ratio).
    """
    nir = data["nir"].astype("float")   # e.g., band 8 for Sentinel-2
    swir = data["swir22"].astype("float") # e.g., band 12 or band 11 (depending on your workflow)

    nbr = (nir - swir) / (nir + swir)
    return nbr

def return_dnbr(data_pre: xr.Dataset, data_post: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return dNBR given two datasets (pre-fire and post-fire).
    """
    # Calculate NBR for pre-fire
    nir_pre = data_pre["nir"].astype("float")
    swir_pre = data_pre["swir22"].astype("float")
    nbr_pre = (nir_pre - swir_pre) / (nir_pre + swir_pre)

    # Calculate NBR for post-fire
    nir_post = data_post["nir"].astype("float")
    swir_post = data_post["swir22"].astype("float")
    nbr_post = (nir_post - swir_post) / (nir_post + swir_post)

    # Differenced NBR
    dnbr = nbr_pre - nbr_post
    return dnbr
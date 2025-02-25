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

def return_nbr(data: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return NBR (Normalized Burn Ratio).
    """
    nir = data["nir"].astype("float")   # e.g., band 8 for Sentinel-2
    swir = data["swir22"].astype("float") # e.g., band 12 or band 11 (depending on your workflow)

    nbr = (nir - swir) / (nir + swir)
    return nbr

def return_ibi(data: xr.Dataset) -> xr.DataArray:
    """
    Calculate and return the Index-based Built-up Index (IBI).
    """
    ndvi = (data["nir"] - data["red"]) / (data["nir"] + data["red"])
    ndwi = (data["green"] - data["swir22"]) / (data["green"] + data["swir22"])
    ndbi = (data["swir16"] - data["nir"]) / (data["swir16"] + data["nir"])

    ibi = (ndbi - (ndvi + ndwi)) / (ndbi + (ndvi + ndwi))
    return ibi



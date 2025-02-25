import matplotlib.pyplot as plt
import numpy as np
import shapely
import xarray as xr

from matplotlib.image import AxesImage
from odc.stac import load
from pystac.item import Item
from pystac_client.item_search import ItemSearch
from shapely import Polygon
from shapely.geometry import box
from tqdm import tqdm
from typing import Callable, List

def print_item_search_attributes(items:ItemSearch):
    """
    Print selectd attributes from PyStac ItemCollection.
    """
    print(f"{items.matched()} items found:\n")
    for item in items.items():
        area = np.round(
            Polygon(*item.geometry['coordinates']).area,
            2)
        print("ID:", item.id, "\n",
              "Cloud cover (%):", item.properties['eo:cloud_cover'], "\n",
              "Missing pixels (%):", item.properties['s2:nodata_pixel_percentage'], "\n",
              "Missing band data (%):", item.properties['s2:degraded_msi_data_percentage'],"\n",
              "Image area (km^2):", area,"\n")

def plot_single_image_spectral_idx(index:np.ndarray, x_dim:int, y_dim:int, name:str, cmap:str="Greens"):
    """
    Plot a single np.ndarray with spectral index values.
    """
    fig, ax = plt.subplots(figsize=(x_dim, y_dim))
    cax = ax.imshow(index, cmap=cmap)
    ax.set_title(f"{name} on one image", size=40)
    ax.tick_params(axis='both', which='major', labelsize=20)
    cbar = fig.colorbar(cax, pad=0.01)
    cbar.ax.tick_params(labelsize=18) 
        
# Code from https://gis.stackexchange.com/questions/480666/how-to-convert-sentinel-2-rgb-bands-to-0-255
def sentinel2_l2a_to_rgb(image:np.ndarray) -> np.ndarray:
    """
    Convert Sentinel-2 RGB bands to the 0, 255 range.
    """
    
    min_val = 0.0
    max_val = 0.3
    rgb_image = (image / 10000 - min_val) / (max_val - min_val)
    rgb_image[rgb_image < 0] = 0
    rgb_image[rgb_image > 1] = 1
    return rgb_image

def normalize_to_rgb(data:xr.Dataset) -> np.ndarray:
    """
    Turn xr.DataSet with Sentinel-2 data to 0,255 range RGB Numpy array.
    """
    
    rgb = data[["red", "green", "blue"]].to_array().to_numpy()
    normalized_rgb = sentinel2_l2a_to_rgb(rgb)
    normalized_rgb = np.transpose(normalized_rgb, (1, 2, 0))
    return normalized_rgb

def find_intersection_poly(item:Item, bbox_poly:Polygon) -> Polygon:
    """
    Find the intersection between an item and the bbox over the total area of interest.
    """

    # Turn item coordinates into polygon
    item_poly = Polygon(*item.geometry['coordinates']) 

    # Find intersection polygon
    intersection_poly = shapely.intersection( 
        bbox_poly,
        item_poly)
    return intersection_poly

def print_assets(item:Item):
    """
    Prints assets for a PyStac Item.
    """
    assets = item.assets.items()
    for key,title in assets:
        print(key,'|',title.title)

def get_item_with_min_attribute(items:ItemSearch.items, attr:str='eo:cloud_cover') -> Item:
    """
    Select a key attribute and get the item with the minimum value of that attribute among items in 
    a PyStac ItemSearch.
    """
    min_item = min(items,
                   key=lambda item: 
                   item.properties[attr])
    return min_item

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

def load_data_from_item(item:Item, bands:List[str], bbox_poly:List[float]) -> xr.Dataset:
    """ 
    Load data from PyStac Item to xr.Dataset.
    """
    # Get the bounds for the part of the item that are within the bbox of interest.
    item_bbox = find_intersection_poly(item, bbox_poly) 
    
    # Load data
    data = load([item], 
            bands=bands, 
            bbox=item_bbox.bounds,
            progress=tqdm).isel(time=0)
    
    return data

def calculate_spectral_index_over_items(
    items: List[Item],
    bands: List[str],
    bbox: List[float],
    spectral_index_func: Callable[[xr.Dataset], xr.DataArray]
) -> List[xr.DataArray]:
    """
    Iterate over items in a PySTAC ItemSearch and calculate a spectral index
    for each, using a user-provided function.

    Parameters:
    -----------
    items : List[Item]
        List of PySTAC items to process.
    bands : List[str]
        The list of bands to load from each item.
    bbox : List[float]
        Bounding box [minX, minY, maxX, maxY].
    spectral_index_func : Callable[[xr.Dataset], xr.DataArray]
        A function that takes an xr.Dataset (with loaded bands) and returns
        an xr.DataArray representing the computed spectral index.

    Returns:
    --------
    List[xr.DataArray]
        A list of spectral index arrays, one for each item.
    """
    n_items = len(items)
    bbox_poly = box(*bbox)
    index_results = []

    for idx, item in enumerate(items):
        print(f"Processing item {idx+1} out of {n_items}")
        data = load_data_from_item(item, bands, bbox_poly)
        spectral_index = spectral_index_func(data)
        index_results.append(spectral_index)

    return index_results


def calculate_median_index(spectral_index_values:List[xr.DataArray]) -> xr.DataArray:
    """
    Find median Spectral Index Values from list of xr.DataArray objects.
    """
    
    print("Concatenating Spectral Index images.")
    spectral_index_values_xr = xr.concat(spectral_index_values, dim="image").load()
    
    print("Calculating the means, this will take a while.")
    spectral_index_values_xr_median = spectral_index_values_xr.median(dim="image")
    return spectral_index_values_xr_median

def xr_spectral_index_data_to_np(xr_data:xr.DataArray) -> np.ndarray:
    """
    Turn xr.DataArray to np.ndarray and flip the results to make map face south to north.
    """
    
    return np.flipud(xr_data.to_numpy())

def plot_territory(data:np.ndarray, x_dim:int, y_dim:int, cmap:str, title:str):
    """
    Plot the data over the section of the Wet'suwet'en territory under investigation in this tutorial.
    Matplotlib parameters have been set to produce legible and well-formed plots for the tutorial data.
    """

    data = np.flipud(data)
    fig, ax = plt.subplots(figsize=(40, 10))
    cax = ax.imshow(data, cmap=cmap)
    ax.set_title(title,size=40)
    ax.tick_params(axis='both', which='major', labelsize=20)
    cbar = fig.colorbar(cax,fraction=0.015, pad=0.01)
    cbar.ax.tick_params(labelsize=18) 

def plot_overlay(
    ax: plt.Axes,
    data: np.ndarray,
    cmap: str = "viridis",
    alpha: float = 0.5
) -> AxesImage:
    """
    Overlay 'data' on an existing axes (ax) with a chosen colormap and alpha.
    """
    # Optionally flip if you want a certain origin orientation
    data_to_plot = np.flipud(data)

    # Overlay on the existing axes
    overlay = ax.imshow(data_to_plot, cmap=cmap, alpha=alpha)
    return overlay
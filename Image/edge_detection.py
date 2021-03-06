'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/edge_detection.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/edge_detection.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Image/edge_detection.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/edge_detection.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The magic command `%%capture` can be used to hide output from a specific cell.
'''


# %%
# %%capture
# !pip install earthengine-api
# !pip install geehydro

# %%
'''
Import libraries
'''


# %%
import ee
import folium
import geehydro

# %%
'''
Authenticate and initialize Earth Engine API. You only need to authenticate the Earth Engine API once. Uncomment the line `ee.Authenticate()` 
if you are running this notebook for this first time or if you are getting an authentication error.  
'''


# %%
# ee.Authenticate()
ee.Initialize()

# %%
'''
## Create an interactive map 
This step creates an interactive map using [folium](https://github.com/python-visualization/folium). The default basemap is the OpenStreetMap. Additional basemaps can be added using the `Map.setOptions()` function. 
The optional basemaps can be `ROADMAP`, `SATELLITE`, `HYBRID`, `TERRAIN`, or `ESRI`.
'''

# %%
Map = folium.Map(location=[40, -100], zoom_start=4)
Map.setOptions('HYBRID')

# %%
'''
## Add Earth Engine Python script 

'''

# %%
# Load a Landsat 8 image, select the panchromatic band.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')

# Perform Canny edge detection and display the result.
canny = ee.Algorithms.CannyEdgeDetector(**{
  'image': image, 'threshold': 10, 'sigma': 1
})
Map.setCenter(-122.054, 37.7295, 10)
Map.addLayer(canny, {}, 'canny')

# Perform Hough transform of the Canny result and display.
hough = ee.Algorithms.HoughTransform(canny, 256, 600, 100)
Map.addLayer(hough, {}, 'hough')

# Load a Landsat 8 image, select the panchromatic band.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')
Map.addLayer(image, {'max': 12000})

# Define a "fat" Gaussian kernel.
fat = ee.Kernel.gaussian(**{
  'radius': 3,
  'sigma': 3,
  'units': 'pixels',
  'normalize': True,
  'magnitude': -1
})

# Define a "skinny" Gaussian kernel.
skinny = ee.Kernel.gaussian(**{
  'radius': 3,
  'sigma': 1,
  'units': 'pixels',
  'normalize': True,
})

# Compute a difference-of-Gaussians (DOG) kernel.
dog = fat.add(skinny)

# Compute the zero crossings of the second derivative, display.
zeroXings = image.convolve(dog).zeroCrossing()
Map.setCenter(-122.054, 37.7295, 10)
Map.addLayer(zeroXings.updateMask(zeroXings), {'palette': 'FF0000'}, 'zero crossings')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map
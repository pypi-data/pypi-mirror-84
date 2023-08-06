# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpdd_dataset',
 'cpdd_dataset.config',
 'cpdd_dataset.data',
 'cpdd_dataset.intrinsics']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.10.0,<3.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 's3fs>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'cpdd-dataset',
    'version': '0.1.3',
    'description': 'Accessors for CARLA Panoramic Depth Detection Dataset, the dataset created as part of my thesis',
    'long_description': '\n# CPDD-Dataset\n\nThis is the data access package for the CARLA panoramaic depth detection dataset,\ncreated and published as part of my thesis *Dataset and Evaluation of Self-Supervised Learning for Panoramic Depth Estimation*\n\nThe code used to generate the dataset is available at https://github.com/rnett/CARLASim.\n\n## Example\n\nSet the environment variable `CARLA_DOWNLOAD_LOCATION` to wherever you want to keep the data.\n\nThen, loading the data is as simple as:\n\n```python\nimport cpdd_dataset\n\ntrain_configs = cpdd_dataset.config.load_csv("train_data.csv")\ntrain_data = []\n\nfor config in train_configs:\n    with config.cylindrical_data.download() as data:\n        train_data.append({"color": data.color, "depth": data.depth})\n```\n\nYou can make a csv file structured like:\n```csv\ncity,rain,time,num_cars,num_peds,index\nTown01,Clear,Noon,*,*,2\n```\nand load it in a single line: `carla_dataset.data.load_csv("train.csv")`.\n\nIf you need camera intrinsics, `CylindricalIntrinsics`, `SphericalIntrinsics`, `PinholeIntrinsics`, and `Pinhole90Intrinsics` (see Utilities) classes are available in `data`, and provide the intrinsics values and matrix.\n\n```python\nK = CylindricalIntrinsics().K\n```\n\n\n## Structure\n\n### Data Location\nTo set the dataset download/loading location, you can use `data.set_download_location`, and `get_download_location` to get it.\nHowever, this is not advised.\nInstead, set the environment variable `CARLA_DOWNLOAD_LOCATION`.\nThe above methods are simply wrappers around it.\nIt is loaded using `pathlib.Path`, so use whatever path format your machine does.\n\n### Config\n\nEach simulation run is represented by a `config.Config` object, which contains the simulation parameters \n(city, rain, number of pedestrians, etc) necessary to get the location of the data files.\nIt provides utility methods and properties based on this, including getting data files for pinhole, cylindrical, \nspherical, and pose data, getting the local and remote locations, and downloading all of the data files.\n\n#### Loading\n\nA `Config` can be constructed manually or from the folder name (using `Config.from_folder_name`), \nbut will probably be loaded from `config.expand_wildcards`.\n`expand_wildcards` fills `None` parameters will all valid values.\nYou probably don\'t need to use it directly, as loader methods `load_df`, `load_csv`, and `load_text` methods are provided, as well as `all`.\n\n### Data Files\n\nData files can be gotten from `Config` objects, and represent a data file.\nThey have `download` methods that accept a `force` parameter, an `is_downloaded()` method, and a `data` property.\nNon-pose data files also have an `intrinsics` property to get the associated intrinsics (described later).\nThe `data` property opens and loads the file, returning a `DataFile`.\n`DataFile`s also work with Python\'s `with` blocks, and can be used like `with file as data:`.\nThis has the advantage of automatically closing the file. \nThe pinhole data file also exposes side methods `top`, `bottom`, etc. to get individual sides\'\ngroups within the pinhole data file, and a `__getitem__` operator that takes a `data.Side` to do the same.\n\n### Data\n\nThe data objects gotten from data files expose the ndarray data for the training run.\nPinhole data (gotten from pinhole data files) has properties to get the data for each side.\nPinhole side data (gotten from side data files), cylindrical data, and spherical data have `rgb` and `depth` properties\nthat return their respective data as `numpy` `ndarray`s.\nBoth are of shape `[batch, height, width, channels]`, where color images have 3 channels (RGB) and depth images have 1.\nDepth images are `uint16` and have the depth in decimeters, while color images are the standard `uint8`.\nPinhole images are 768x768, while cylindrical and spherical images are 2048x1024 (width x height).\n\n\nPose data objects have fields `absolute_pose`, `relative_pose`, and `start_relative_pose`.\nRelative pose is relative to the last pose value, while start relative pose is relative to the inital post of that simulation.\nPose data is shape `[batch, 6]`, where the 6 values are `[X, Y, Z, x, y, z]` where `[X, Y, Z]` is the position in meters, and `[x, y, z]` is the unit heading vector of the car.\n\n### Intrinsics\n`CylindricalIntrinsics`, `SphericalIntrinsics`, `PinholeIntrinsics`, and `Pinhole90Intrinsics` (see Utilities) are available in `data`, and provide the intrinsics values and matrix.\nEach object has `K`, `normalized_K`, `height`, `width`, `f_x`, `f_y`, `c_x`, `c_y`, and `fov` (degrees) fields.\n\n### Utilities\n\nA method `data.crop_pinhole_to_90` is provided to crop the 100 degree FOV pinhole images into 90 degree FOV images of the same size.\nIt uses `cv2.getRectSubPix` internally.\nThe intrinsics for these images are provided by `Pinhole90Intrinsics` using the same format as other intrinsics.\n',
    'author': 'Ryan Nett',
    'author_email': 'rnett@calpoly.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rnett/cpdd-dataset',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

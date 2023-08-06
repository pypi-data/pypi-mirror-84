[![PyPI](https://img.shields.io/pypi/v/btrack)](https://pypi.org/project/btrack)  [![Downloads](https://pepy.tech/badge/btrack)](https://pepy.tech/project/btrack)

# Bayesian Tracker (btrack) :microscope::computer:

BayesianTracker (`btrack`) is a Python library for multi object tracking,
used to reconstruct trajectories in crowded fields. Here, we use a
probabilistic network of information to perform the trajectory linking. This
method uses spatial information as well as appearance information for track linking.

The tracking algorithm assembles reliable sections of track that do not
contain splitting events (tracklets). Each new tracklet initiates a
probabilistic model, and utilises this to predict future states (and error in
states) of each of the objects in the field of view.  We assign new observations
to the growing tracklets (linking) by evaluating the posterior probability of
each potential linkage from a Bayesian belief matrix for all possible linkages.

The tracklets are then assembled into tracks by using multiple hypothesis
testing and integer programming to identify a globally optimal solution. The
likelihood of each hypothesis is calculated for some or all of the tracklets
based on heuristics. The global solution identifies a sequence of
high-likelihood hypotheses that accounts for all observations.

### Cell tracking in time-lapse imaging data

We developed `btrack` for cell tracking in time-lapse microscopy data.

<!-- [![LineageTree](http://lowe.cs.ucl.ac.uk/images/bayesian_tracker_lineage_tree.png)](http://lowe.cs.ucl.ac.uk)   -->
<!-- [![LineageTree](https://raw.githubusercontent.com/quantumjot/BayesianTracker/master/examples/render.png)](http://lowe.cs.ucl.ac.uk/cellx.html)  
*Automated cell tracking and lineage tree reconstruction*. Cell divisions are highlighted in red. -->
[![LineageTree](https://raw.githubusercontent.com/quantumjot/arboretum/master/examples/napari.png)](http://lowe.cs.ucl.ac.uk/cellx.html)  
*Automated cell tracking and lineage tree reconstruction*. Visualization is provided by our plugin to Napari, [arboretum](#Usage-with-Napari).


[![CellTracking](http://lowe.cs.ucl.ac.uk/images/youtube.png)](https://youtu.be/EjqluvrJGCg)  
*Video of tracking, showing automatic lineage determination*

Read about the science:  
http://lowe.cs.ucl.ac.uk/cellx.html

You can also --> :star: :wink:

---

### Installation

BayesianTracker has been tested with Python 3.7+ on OS X, Linux and Win10.
The tracker and hypothesis engine are mostly written in C++ with a Python
wrapper.

 #### Installing the latest stable version
 ```sh
 $ pip install btrack
 ```

 #### (Advanced) Installing the latest development version

If you would rather install the latest development version, and/or compile
directly from source, you can clone and install from this repo:

```sh
$ git clone https://github.com/quantumjot/BayesianTracker.git
$ conda env create -f ./BayesianTracker/environment.yml
$ conda activate btrack
$ cd BayesianTracker
$ pip install -e .
```

Addtionally, the `build.sh` script will download Eigen source, run the makefile
and pip install.

---
### Usage in Colab notebooks

If you do not want to install a local copy, you can run the tracker in a Colab notebook. Please note that these examples are work in progress and may change:

| Status        | Level | Notebook                                     | Link |
| ------------- | ----- | -------------------------------------------- | ---- |
| Complete      | Basic | Data import options                          | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1V2TtJ5FGqSILTuThSRg5j9crsBsorUmy)|
| Complete      | Basic | Object tracking with btrack                  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1A1PRM0a3Z0ufszdnVxntcaEDzU_Vh4u9)|
| *In progress* | Advanced | Configuration options                     | -
| Complete      | Advanced | How to compile btrack from source         | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/19t5HBV76_Js8M3LX63CwiXzemax7Tvsk)|


---

### Usage with Napari

You can run btrack with a GUI and visualize the output using our plugin (called `arboretum`) for the open source image viewer [`Napari`](https://github.com/napari/napari).

| Status        | Notebook                                     | Link |
| ------------- | -------------------------------------------- | ---- |
| *In progress* | Visualizing btrack output using arboretum    | [GitHub](https://github.com/quantumjot/arboretum)

---

### Usage from Python

BayesianTracker can be used simply as follows:

```python
import btrack
from btrack.dataio import import_CSV

# NOTE(arl): This should be from your image segmentation code
objects = import_CSV('/path/to/your/objects.csv')

# initialise a tracker session using a context manager
with btrack.BayesianTracker() as tracker:

  # configure the tracker using a config file
  tracker.configure_from_file('/path/to/your/models/cell_config.json')

  # append the objects to be tracked
  tracker.append(objects)

  # set the volume (Z axis volume is set very large for 2D data)
  tracker.volume=((0,1200),(0,1600),(-1e5,1e5))

  # track them (in interactive mode)
  tracker.track_interactive(step_size=100)

  # generate hypotheses and run the global optimizer
  tracker.optimize()

  # get the tracks as a python list
  tracks = tracker.tracks
```

Tracks themselves are python objects with properties:

```python
# get the first track
track_zero = tracks[0]

# print the length of the track
print(len(track_zero))

# print all of the xyzt positions in the track
print(track_zero.x)
print(track_zero.y)
print(track_zero.z)
print(track_zero.t)

# print the fate of the track
print(track_zero.fate)

# print the track ID, root node, parent node, children and generational depth
print(track_zero.ID)
print(track_zero.root)
print(track_zero.parent)
print(track_zero.children)
print(track_zero.generation)

```

There are many additional options, including the ability to define object models.

### Importing data
Observations can be provided in several basic formats:
+ a simple CSV or JSON file
+ HDF5 for larger/more complex datasets, or
+ using your own code from numpy arrays or pandas data arrays.

For example, CSV data of the format:
```
t x   y   z
0 300 300 0
1 301 299 1
2 302 288 2
...
```

can be imported:

```python
from btrack.dataio import import_CSV
objects = import_CSV('/path/to/your/objects.csv')
```

More detail the colab notebooks above.

### Exporting data

Tracks can also be exported in CSV and/or the LBEP format:
```python
from btrack.dataio import export_CSV
from btrack.dataio import export_LBEP

# export tracks in CSV format
export_CSV('/path/to/your/tracks.csv', tracks)

# export the LBEP table of lineage information
export_LBEP('/path/to/your/lbep_tracks.txt', tracks)
```


### Dealing with very large datasets
btrack supports three different methods:

+ `EXACT` - (DEFAULT) exact calculation of Bayesian belief matrix, but can be slow on large datasets
+ `APPROXIMATE` - approximate calculation, faster, for use with large datasets. This has an additional `max_search_radius` parameter, which sets the local spatial search radius (isotropic, pixels) of the algorithm.
+ `CUDA` - GPU implementation of the EXACT method (*in progress*)

For most cell datasets (<1000 cells per time point) we recommend `EXACT`. If you have larger datasets, we recommend `APPROXIMATE`.

If the tracking does not complete, and is stuck on the optimization step, this
means that your configuration is poorly suited to your data. Try turning off
optimization, followed by modifying the parameters of the config file.

```python

import btrack
from btrack.constants import BayesianUpdates

with btrack.BayesianTracker() as tracker:

    # configure the tracker and change the update method
    tracker.configure_from_file('/path/to/your/models/cell_config.json')
    tracker.update_method = BayesianUpdates.APPROXIMATE
    tracker.max_search_radius = 100
    ...
```


---
### Citation

More details of how this type of tracking approach can be applied to tracking
cells in time-lapse microscopy data can be found in the following publications:

**Automated deep lineage tree analysis using a Bayesian single cell tracking approach**  
Ulicna K, Vallardi G, Charras G and Lowe AR.  
*bioRxiv* (2020)  
<https://www.biorxiv.org/content/early/2020/09/10/2020.09.10.276980>


**Local cellular neighbourhood controls proliferation in cell competition**  
Bove A, Gradeci D, Fujita Y, Banerjee S, Charras G and Lowe AR.  
*Mol. Biol. Cell* (2017)  
<https://doi.org/10.1091/mbc.E17-06-0368>

```
@article {Ulicna2020.09.10.276980,
  author = {Ulicna, Kristina and Vallardi, Giulia and Charras, Guillaume and Lowe, Alan R.},
  title = {Automated deep lineage tree analysis using a Bayesian single cell tracking approach},
  elocation-id = {2020.09.10.276980},
  year = {2020},
  doi = {10.1101/2020.09.10.276980},
  publisher = {Cold Spring Harbor Laboratory},
  URL = {https://www.biorxiv.org/content/early/2020/09/10/2020.09.10.276980},
  eprint = {https://www.biorxiv.org/content/early/2020/09/10/2020.09.10.276980.full.pdf},
  journal = {bioRxiv}
}
```
```
@article{Bove07112017,
  author = {Bove, Anna and Gradeci, Daniel and Fujita, Yasuyuki and Banerjee,
    Shiladitya and Charras, Guillaume and Lowe, Alan R.},
  title = {Local cellular neighborhood controls proliferation in cell competition},
  volume = {28},
  number = {23},
  pages = {3215-3228},
  year = {2017},
  doi = {10.1091/mbc.E17-06-0368},
  URL = {http://www.molbiolcell.org/content/28/23/3215.abstract},
  eprint = {http://www.molbiolcell.org/content/28/23/3215.full.pdf+html},
  journal = {Molecular Biology of the Cell}
}
```

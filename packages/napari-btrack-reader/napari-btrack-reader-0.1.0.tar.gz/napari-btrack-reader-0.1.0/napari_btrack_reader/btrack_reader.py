"""
This module is a reader plugin btrack files for napari.

It implements the ``napari_get_reader`` hook specification, (to create
a reader plugin) but your plugin may choose to implement any of the hook
specifications offered by napari.
see: https://napari.org/docs/plugins/hook_specifications.html

Replace code below accordingly.  For complete documentation see:
https://napari.org/docs/plugins/for_plugin_developers.html
"""

from btrack.utils import tracks_to_napari
from btrack.dataio import HDF5FileHandler
from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_get_reader(path):
    """A basic implementation of the napari_get_reader hook specification.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    extensions = ".hdf", ".hdf5", ".h5"
    if not path.endswith(extensions):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will default
        to layer_type=="image" if not provided
    """
    # handle both a string and a list of strings
    paths = [path] if isinstance(path, str) else path

    # store the layers to be generated
    layers = []

    for _path in paths:
        with HDF5FileHandler(_path, 'r') as hdf:

            # get the segmentation if there is one
            if "segmentation" in hdf._hdf:
                segmentation = hdf.segmentation
                layers.append((segmentation, {}, "labels"))

            # iterate over object types and create a layer for each
            for obj_type in hdf.object_types:

                # set the object type, and retrieve the tracks
                hdf.object_type = obj_type

                if f"tracks/{obj_type}" not in hdf._hdf:
                    continue

                tracklets = hdf.tracks
                tracks, properties, graph = tracks_to_napari(tracklets, ndim=2)

                # optional kwargs for the corresponding viewer.add_* method
                # https://napari.org/docs/api/napari.components.html#module-napari.components.add_layers_mixin
                add_kwargs = {
                    'properties': properties,
                    'graph': graph,
                    'name': obj_type,
                    'blending': 'translucent'
                }

                layer = (tracks, add_kwargs, "tracks")
                layers.append(layer)
    return layers

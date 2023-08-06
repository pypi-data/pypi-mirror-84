import os
import logging
import webcolors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mypalette import LoadPalette

logger = logging.getLogger(__name__)

def visualize_palette(json_path = None, save_plot = True, save_type = 'png'):
    """
    This function load a palette file create by create_new_palette() and visualize the colors palette.
    Such plot can be saved in the same folder of json_path.

    Parameters
    ----------
    json_path : string, default=None
        Path to the JSON file containing the palette in the correct format.
    save_plot : bool, default=True
        Save figure in same folder of 
    save_type : string, default='png' json_path

    Examples
    --------   
    >>> from mypalette import visualize_palette
    >>> visualize_palette(json_path = 'palette.json')
    """
    p = LoadPalette()
    all_colours = p.load_palette(json_path=json_path, code='All')

    colours = all_colours['HEXs']
    y_pos = np.arange(len(colours))
    performance = [1] * len(colours)

    # rgb = [tuple(webcolors.hex_to_rgb(x)) for x in colours]
    rgb = [clr.to_rgb(x) for x in colours]

    very_color = [x+"\n"+y.upper()+"\n"+str(z) for x, y, z in zip(
        all_colours['Names'], 
        all_colours['HEXs'], 
        rgb)]

    fig, axes = plt.subplots(figsize=(10, 4.5), dpi=100)

    axes.bar(y_pos, performance, width=1.0, color=colours)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['left'].set_visible(False)

    axes.set_xticks(y_pos)
    axes.set_xticklabels(very_color)
    axes.set_yticks([])
    axes.set_title('From file {}'.format(os.path.splitext(os.path.basename(json_path))[0]))

    if bool(save_plot) == True:
        fig.savefig('{}.{}'.format(
            os.path.splitext(json_path)[0],
            save_type))
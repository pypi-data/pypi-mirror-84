import os
import math
import logging
import colorsys
import webcolors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mypalette import LoadPalette

logger = logging.getLogger(__name__)

def __luminosity(r, g, b):
    """
    From https://www.alanzucconi.com/2015/09/30/colour-sorting/
    Two visually different shades of blue are closer, compared two two different colours with the similar intensity. An attempt to compensate for this is by sorting directly for the perceived luminosity of a colour.
    """
    return math.sqrt(.241 * r + .691 * g + .068 * b)


def __step(r, g, b, repetitions=8):
    """
    From https://www.alanzucconi.com/2015/09/30/colour-sorting/
    """
    lum = math.sqrt( .241 * r + .691 * g + .068 * b)
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
    h2   = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2   = int(v * repetitions)
    return(h2, lum, v2)


def __sort_colors(hexs, sort_by):
    if sort_by == None:
        return(hexs)
    else:
        colors = [list(webcolors.hex_to_rgb(x)) for x in hexs]
        if sort_by == 'luminosity':
            colors.sort(key=lambda colors: __luminosity(*colors))
        elif sort_by == 'step':
            colors.sort(key=lambda x: __step(x[0], x[1], x[2]))
        else:
            print('No sorting method has be selected.')
        return([webcolors.rgb_to_hex(x) for x in colors])


def __plot_text(hexs, all_colors):    
    return [x+"\n\n"+y.upper()+"\n\n"+str(z) for x, y, z in zip(
            [all_colors['Names'][all_colors['HEXs'].index(x)] for x in hexs], 
            hexs, 
            [list(webcolors.hex_to_rgb(x))for x in hexs])]

def __text_colors(colors):
    return [('white' if x[0]* x[1]* x[2] < 0.05 else 'black') for x in [clr.to_rgb(x) for x in colors]]


def visualize_palette(json_path = None, 
                      sort_by = None,
                      save_plot = True, 
                      save_type = 'png',
                      fig_size  = None,
                     ):
    """
    This function load a palette file create by create_new_palette() and visualize the colors palette.
    Such plot can be saved in the same folder of json_path.

    Parameters
    ----------
    json_path : string, default=None
        Path to the JSON file containing the palette in the correct format.
    sort_by: string, default=None
        Options: luminosity, step.
    save_plot : bool, default=True
        Save figure in same folder of json_path
    save_type : string, default='png'.
    fig_size: tuple, default=None. Figure size in inches.
    
    Returns
    ----------
    all_colors : The results from LoadPalette().load_palette()

    Examples
    --------   
    >>> from mypalette import visualize_palette
    >>> visualize_palette(json_path = 'palette.json')
    """
    ## Loading
    p = LoadPalette()
    all_colors = p.load_palette(json_path=json_path, code='All')

    ## Sorting colors
    colors = __sort_colors(all_colors['HEXs'], sort_by=sort_by)
    
    ## Creat text for plot
    plot_texts = __plot_text(colors, all_colors)
     
    ## Colors for text
    text_color = __text_colors(colors)
    
    ## Plotting
    y_pos = np.arange(len(colors))
    performance = [1] * len(colors)

    if fig_size==None:
        fig_size = (len(colors)*5, 5)

    fig, axes = plt.subplots(figsize=fig_size, dpi=100)
    axes.bar(y_pos, performance, width=1.0, color=colors)

    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_visible(False)

    for x,(y,z) in enumerate(zip(colors, text_color)):
        axes.text(x, 0.5, plot_texts[x], color=z, ha='center', va='center',
        fontsize=fig_size[1]**2, fontweight='black')
        
    axes.set_yticks([])
    axes.set_xticks([])

    ## Saving the plot 
    if bool(save_plot) == True:
        fig.savefig('{}.{}'.format(
            os.path.splitext(json_path)[0], 
            save_type))
            
    return(all_colors)
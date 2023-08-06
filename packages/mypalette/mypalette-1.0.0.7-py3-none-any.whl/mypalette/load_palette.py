import os
import ast
import json
import webcolors
import logging
import matplotlib.colors as clr

logger = logging.getLogger(__name__)

class LoadPalette():
    """ 
    Core class of mypalette library. After initializing this class, you can create new palette or load pre existing ones.
    You can download the color palette from coolors.co or submite a list of hexadecimal code colors.

    Parameters
    ----------

    Attributes
    ----------
    primary : list of strings.
        List of the primary web colors.
    secondary : list of strings.
        List of the secondary web colors.
    tertiary : list of strings.
        List of the tertiary web colors.
    black_white : list of strings.
        List of the black and white color.

    Notes
    -----

    References
    -----
    .. [1] coolors.co: Website of reference from which to download the color palette compatible with this package
    <https://coolors.co/>`_
    .. [2] List of web colors: usability.gov
    <https://www.usability.gov/how-to-and-tools/methods/color-basics.html>`_

    Examples
    --------
    >>> from mypalette import LoadPalette

    >>> palette = LoadPalette()
    >>> p = palette.create_new_palette(input_txt=/palette_1.txt', output_json='palette_1.json')
    >>> print(p)
    {'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}

    >>> p = palette.load_palette(json_path='palette_1.json')
    >>> print(p)
    ['#000000', '#FFFFFF']

    >>> p = palette.create_palette_from_hex_list(
        hexadecimal = ['#000000', '#FFFFFF'],
        output_json = 'black_and_white.json')
    >>> print(p)
    {'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
    """
    primary = ['#FF0000', '#00FF00', '#0000FF']
    secondary = ['#00FFFF', '#FF00FF', '#FFFF00']
    tertiary = ['#FF7000',  "#7FFF00", '#00FF7F', '#007FFF', '#7F00FF', '#FF007F']
    black_white = ['#000000', '#FFFFFF']
    matplotlib_colors = clr.BASE_COLORS
    
    def __init__(self):
        pass


    def __str__(self):
        return "This class load and create stored color palette."


    def __load_txt_from_coolors(self, input_txt):
        """ 
        Parameters
        ----------
        input_txt : string
            Path to the TXT file containing the palette as downloaded by coolors.co.

        Returns
        -------
        palette : dictionary
            Python dictionary containg colors codes and values.
        """
        with open(input_txt , 'r') as reader:
            extended_array = False
            for pos, line in enumerate(reader):
                if extended_array:
                    return ast.literal_eval(line)
                if "extended array" in line.lower():
                    extended_array = True


    def __save_palette(self, palette, output_json):
        """ 
        Parameters
        ----------
        palette : dictionary
            Python dictionary containg colors codes and values.
        output_json : string
            Path for the JSON file where to save the palette in the correct format.
        """
        logger.info('Saving new {} file in {}.\n'.format(
                os.path.basename(output_json), 
                os.path.dirname(output_json)))
        with open(output_json, 'w') as f:
            json.dump(palette , f)


    def __palette_code(self, json_path, palette, code):
        """ 
        Parameters
        ----------
        json_path : string, default=None 
            Path to the JSON file containing the palette in the correct format.
        palette : dictionary
            Python dictionary containg colors codes and values.
        code : {'HEXs', 'All', 'RGBs', 'Names'}
            Specifies the type of color code required from palette.
            It can be 'HEXs' hexadecimal, 'RGBs' stands for red, green, and blue, 'Names' list of the name of all color (Some colors have no name), 'All' all previous info in a dictionary.
        Returns
        -------
        palette : dictionary
            Python dictionary containg colors codes and values in matplotlib compatible format.
        """
        if code == 'All':
            logger.info('Returning all codes from {}'.format( 
                os.path.basename(json_path)))
            palette['RGBs'] = [tuple(x) for x in palette['RGBs']]
            return palette
        elif code == 'RGBs':
            logger.info('Returning {} {} code from {}'.format(len(palette), code, os.path.basename(json_path)))
            return [tuple(x) for x in palette[code]]
        else:
            logger.info('Returning {} {} code from {}'.format(len(palette), code, os.path.basename(json_path)))
            return palette[code]


    def __get_compatible_codes(self, palette):
        """ 
        Parameters
        ----------
        palette : dictionary
            Python dictionary containg colors codes and values.
        Returns
        -------
        palette : dictionary
            Python dictionary containg colors codes and values.
        """
        rgb = [x['rgb'] for x in palette]
        rgb = [tuple([y/255 for y in x]) for x in rgb]
        return {
            'HEXs':['#'+x['hex'] for x in palette], 
            'RGBs':rgb,  
            'Names':[x['name'] for x in palette]}


    def load_palette(self, json_path, code = 'HEXs'):
        """ 
        Parameters
        ----------
        json_path : string, default=None 
            Path to the JSON file containing the palette in the correct format.
        code : {'HEXs', 'RGBs', 'Names', 'All'}, default='HEXs'
            Specifies the type of color code required from palette.
            It can be 'HEXs' hexadecimal, 'RGBs' stands for red, green, and blue, 'Names' list of the name of all color (Some colors have no name), 'All' all previous info in a dictionary.
        Returns
        -------
        palette : list of strings or dictionary
            It contains the ccolors codes and values compatible with matplotlib.
        Examples
        -------
        >>> from mypalette import LoadPalette
        >>> palette = LoadPalette()
        >>> p = palette.load_palette(json_path='black_and_white.json')
        >>> print(p)
        ['#000000', '#FFFFFF']
        """
        with open(json_path , "r") as read_file:
            palette = json.load(read_file)
        palette = self.__palette_code(
            json_path = json_path,
            palette = palette,
            code = code)
        return palette


    def create_new_palette(self, input_txt, output_json):
        """ 
        Parameters
        ----------
        input_txt : string
            Path to the TXT file containing the palette as downloaded by coolors.co.
        output_json : string
            Path for the JSON file where to save the palette in the correct format.

        Returns
        -------
        palette : dictionary
            Python dictionary containg colors codes and values.
        
        Examples
        -------
        >>> from mypalette import LoadPalette
        >>> palette = LoadPalette()
        >>> p = palette.create_new_palette(input_txt='palette_1.txt', output_json='palette_1.json')
        >>> print(p)
        {'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
        """
        palette = self.__load_txt_from_coolors(input_txt = input_txt)
        palette = self.__get_compatible_codes(palette=palette)
        self.__save_palette(palette = palette, output_json=output_json)
        return palette


    def create_palette_from_hex_list(self, hexadecimal, output_json):
        """
        Given a list of hexadecimal code colors, it creates a new palette saved in output_json containg the hexadecimal and RGB codes, and color names (if existing).

        Parameters
        ----------
        hexadecimal: list of strings
            List of hexadecimal values in format: ['#XXXXXX', ...]
        output_json : string
            Path for the JSON file where to save the palette in the correct format.
            
        Returns
        -------
        palette : dictionary
            Python dictionary containg colors codes and values.

        Examples
        -------
        >>> from mypalette import LoadPalette
        >>> palette = LoadPalette()
        >>> p = palette.create_palette_from_hex_list(
            hexadecimal = ['#000000', '#FFFFFF'],
            output_json = 'black_and_white.json')
        >>> print(p)
        {'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
        """
        hexadecimal = [x if x.startswith("#") else '#'+x for x in hexadecimal]
        Names = []
        for x in hexadecimal:
            try:
                Names.append(webcolors.hex_to_name(x))
            except ValueError:
                Names.append(x)

        rgb = [clr.to_rgb(x) for x in hexadecimal]

        palette = {
            'HEXs': hexadecimal,
            'RGBs': rgb,
            'Names': Names,
        }
        self.__save_palette(palette = palette, output_json = output_json)
        return palette
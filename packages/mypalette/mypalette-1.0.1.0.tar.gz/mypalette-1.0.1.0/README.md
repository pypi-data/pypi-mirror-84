![Banner](https://github.com/MattiaCinelli/mycolorpalette/blob/master/commons/banner.png?raw=true)

![License](https://img.shields.io/github/license/mattiacinelli/mycolorpalette)
![GitHub last commit](https://img.shields.io/github/last-commit/mattiacinelli/mycolorpalette)
[![Website](https://img.shields.io/badge/Website-MattiaCinelli-blue?style=flat-square)](https://mattiacinelli.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-MattiaCinelli-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/mattia-cinelli-b8a06879/)
[![Medium](https://img.shields.io/badge/Medium-MattiaCinelli-green?style=flat-square&logo=medium)](https://medium.com/@mattia.cinelli)

# My Palette
This package handles user created color palettes scheme to be used in Python plotting libraries (matplotlib, seaborn, etch).

Users can use specific colors in accordance with their taste or company guidelines that are different from the defaults in matplotlib. Therefore, mypalette helps to create, store, and use color palettes.

It can use a text file from https://coolors.co or a list of hexadecimal codes and saves a JSON format, comprising of colors: name, hexadecimal and RGB codes.

# Table of contents
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
    - [From coolors.co](#from-coolors)
    - [From hexadecimal](#from-hexadecimal)
- [Development and Contribute](#development-and-contribute)
- [License](#license)

# Installation
```bash
pip install mypalette
```

# Usage
Currently, you can choose two ways to input your palette in mypalette: 
From coolors.co or as a list of hexadecimal codes

## From coolors
Coolors.co is a website designed to generate new palettes, pick palettes from photos, create gradients, etch. 

Do download needed, proceed to https://coolors.co, and click "Start the generator" or use this set of [colors](https://coolors.co/5fad56-f5e663-410b9b-ef271b-f9c80e). 

On the top right corner, click on Export -> Code -> Download

This will save a text file named 'palette' on your computer. 

Now we can use this file in mypalette:

```python
from mypalette import LoadPalette

palette = LoadPalette()
p = palette.create_new_palette(input_txt='palette.txt', output_json='palette.json')
print(p)

{'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
```

Load a compatible JSON file:
```python
p = palette.load_palette(json_path='palette.json')

print(p)
['#000000', '#FFFFFF']
```

## From hexadecimal
Alternatively, you can choose to use a list of hexadecimal codes as your input. 

Note, such list can be obtained from the coolors.co/generate url.

```python
p = palette.create_palette_from_hex_list(
    hexadecimal = ['#000000', '#FFFFFF'],
    output_json = 'black_and_white.json')

print(p)
{'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
```

# Development and Contribute
I welcome contributors (of all experience levels) to improve this package and expand its scope and reach.

If you have never worked on open source project before or you want to brush up your memory here, check out these links:
- [How to Contribute to Open Source Projects](https://github.com/firstcontributions/first-contributions)
- [First contributions](https://github.com/firstcontributions/first-contributions)

Please do not hesitate to contact me to report issues or new ideas.

# License
Copyright (c) 2020 Mattia Cinelli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

![Footer](https://github.com/MattiaCinelli/mycolorpalette/blob/master/commons/footer.png?raw=true)
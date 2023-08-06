![Banner](https://github.com/MattiaCinelli/mycolorpalette/blob/master/commons/banner.png)

![License](https://img.shields.io/github/license/mattiacinelli/mycolorpalette)
![GitHub last commit](https://img.shields.io/github/last-commit/mattiacinelli/mycolorpalette)
[![Website](https://img.shields.io/badge/Website-MattiaCinelli-blue?style=flat-square)](https://mattiacinelli.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-MattiaCinelli-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/mattia-cinelli-b8a06879/)
[![Medium](https://img.shields.io/badge/Medium-MattiaCinelli-green?style=flat-square&logo=medium)](https://medium.com/@mattia.cinelli)

# My Palette
This package has been create to fast-load color palettes for Python matplotlib library, and to convert txt files  downloaded from https://coolors.co to generate and save new color palettes. 

<!-- ![Banner](https://lonelyboy1977.files.wordpress.com/2017/08/work-in-progress.png) -->

# Table of contents
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
    - [Examples](#examples)
- [Development and Contribute](#development-and-contribute)
- [License](#license)

# Installation
```bash
pip install --extra-index-url https://test.pypi.org/simple/ mypalette
```
<!-- pip install git+https://https://github.com/MattiaCinelli/mycolorpalette.git#egg=mypalette -->
<!-- pip install mypalette -->

# Usage
Go to https://coolors.co and click "Start the generator"
or use this set of [colors](https://coolors.co/5fad56-f5e663-410b9b-ef271b-f9c80e) on the top right corner press click on Export, Code, Download

This will save a file 'palette.txt' on you computer. 

## Examples
Create a new palette from existing txt file:
```python
from mypalette import LoadPalette

palette = LoadPalette()
p = palette.create_new_palette(input_txt='palette_1.txt', output_json='palette_1.json')
print(p)

{'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
```

Load a compatible JSON file:
```python
p = palette.load_palette(json_path='palette_1.json')

print(p)
['#000000', '#FFFFFF']
```

Create a compatible JSON file from list of hexadecimal codes:
```python
p = palette.create_palette_from_hex_list(
    hexadecimal = ['#000000', '#FFFFFF'],
    output_json = 'black_and_white.json')

print(p)
{'HEXs': ['#000000', '#FFFFFF'], 'RGBs': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 'Names': ['black', 'white']}
```

# Development and Contribute
I really welcome contributors (of all experience levels) to improve this package and expand its scope and reach.

If you have never worked on open source project before or you want to brush up your memory here, check out these links:
- [How to Contribute to Open Source Projects](https://github.com/firstcontributions/first-contributions)
- [First contributions](https://github.com/firstcontributions/first-contributions)


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

![Footer](https://github.com/MattiaCinelli/mycolorpalette/blob/master/commons/banner2.png)
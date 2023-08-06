# Setup

```
pip3 install colorifix
```

# Requirements
* Python 3.6+

# Import
```python
from colorifix import paint, random, sample
from colorifix import Color, Background, Style
```

# Usage
There are 2 main functions, one to color a string and one to randomize color, background and style of a string.
```python
from colorifix import paint, Color, Background, Style

paint('String to color',color=Color.RED)
paint('String to color',background=Background.GREEN,style=(Style.BOLD,Style.UNDERLINE))
paint('String to color',color=34,background=27)

random('YOLO',color=True,background=True)
random('YOLO',color=True,style=True)
random('YOLO',background=True)
```

# Colors
You can choose from the default colors for main color and backgrounds  
`RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE`, `GRAY` and `BLACK`.  

For style you can choose from  
`BOLD`, `UNDERLINE`, `DIM`, `BLINK`, `REVERSE` and `HIDDEN`.  

> If you want a custom colors you can choose between a number from 0 to 256.

### Sample
To disaply all different color you can use the function `sample`
```python
from colorifix import sample

sample('colors')            # default colors
sample('background')
sample('style')
sample('colors',True)       # all colors
sample('background',True)
```
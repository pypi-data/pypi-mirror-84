# py-msyh
python utils to use font msyh.ttf in a minute.

# install
`pip install py-msyh`

# usage
```python
import pymsyh
# get font path of msyh.ttf
font_path=pymsyh.get_font_path()
# load font (using ImageFont.truetype from PIL)
font= pymsyh.load_font(size=24)
```
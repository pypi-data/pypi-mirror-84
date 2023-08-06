
import os
_root=os.path.dirname(__file__)
def get_font_path():
    return os.path.join(_root,'data/msyh.ttf')

def load_font(size=10):
    from PIL import ImageFont
    font_path=get_font_path()
    font=ImageFont.truetype(font_path,size)
    return font
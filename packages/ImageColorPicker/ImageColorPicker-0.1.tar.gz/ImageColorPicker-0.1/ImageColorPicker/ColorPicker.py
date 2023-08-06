from PIL import Image
import requests
from io import BytesIO

class ColorPicker(object):
    """
    Simple class for finding dominant colors from image 
    """

    def __init__(self, **kwargs):
        """
        Constructor requires ImageUri or ImagePath
        """
        for key, value in kwargs.items():
            if key == 'ImageUri':
                response = requests.get(value)
                self.imageFile = BytesIO(response.content)
            if key == 'ImagePath':
                self.imageFile = value


    def getColors(self, numcolors=10, resize=150) -> list :
        """
        Get rgb colors from image
        """
        # Resize image to speed up processing
        img = Image.open(self.imageFile)
        img = img.copy()
        img.thumbnail((resize, resize))

        # Reduce to palette
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

        # Find dominant colors
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        colors = list()
        for i in range(numcolors):
            palette_index = color_counts[i][1]
            dominant_color = palette[palette_index*3:palette_index*3+3]
            colors.append(tuple(dominant_color))

        return colors

    def toHex(self, colors: list) -> list: 
        """
        Convert rgb tuples to hexs
        """

        hexArr = []
        for color in colors:
            hexArr.append('#%02x%02x%02x' % color)

        return hexArr

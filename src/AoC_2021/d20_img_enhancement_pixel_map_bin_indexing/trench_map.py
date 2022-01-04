"""
Author: Darren
Date: 20/12/2021

Solving https://adventofcode.com/2021/day/20

Mapping the ocean trench floor.  Input data made up of:
- A single line 512-char image enhancement algorithm, e.g. ..#.#..#####.#.#.#.###.##.....###. etc.
- A 2D grid of light pixels (#) and dark pixels (.)
  E.g.  #..#.
        #....
        ##..#
        ..#..
        ..###

The image enhancement algorithm takes each pixel in the grid, 
looks at the 3x3 grid of pixels centred on that pixel, and coverts the grid to a 9-bit value 
(where .=0 and #=1). The resulting number is a lookup index value for the algorithm line.
Note that 0b111111111 = 511, so a 3x3 grid of all # would result in a lookup index of 511,
i.e. the last char of the algorithm line. 
The algorithm should be applied to each source pixel SIMULTANEOUSLY. 

Consider the original image to be on an infinite canvas of dark pixels.
Each pass of enhancement will change the original pixels, but will also grow the image at the border.

Part 1:
    How many pixels are lit after two iterations?
    
    Store lit pixels in a set, usings coords from input str.
    Determine the bounds of the set.
    ImageArray class creates a set of deltas in order to generate a 3x3 grid of any given point.
    The hard work is done in the enhance() method.
    For each cycle, we use the 3x3 grid about each px to generate a integer value lookup.
    This lookup is used agains the enhancement map, to determine the new value of the px in the new 
    ImageArray.  The infinite canvas is typically made up of '.'  
    But with certain enhancement maps, the infinite canvas alternates between lit and dark.
    So, our ImageArray determines which char should be used in the next cycle,
    and passes it to the initiaser for the new ImageArray.

Part 2:
    Same, but 50 cycles instead of 2.  Runs pretty quick, so no need to do anything clever.
"""
from __future__ import annotations
import logging
from pathlib import Path
import time
from typing import NamedTuple
from PIL import Image

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

RENDER = True
OUTPUT_DIR = Path(SCRIPT_DIR, "output/")
OUTPUT_FILE = Path(OUTPUT_DIR, "trench_anim.gif")

class Point(NamedTuple):
    """ Point class, which knows how to return a 3x3 grid of all Points centred on itself. """    
    
    DELTAS = [(dx,dy) for dy in range(-1, 2) for dx in range(-1, 2)] 
   
    x: int
    y: int
    
    def neighbours(self) -> list[Point]:
        """ Return 3x3 grid of all points centered on itself """
        return [Point(self.x+dx, self.y+dy) for dx,dy in Point.DELTAS] 

class ImageArray():
    """ Stores array of pixels (points) in a set. 
    Knows how many pixels are lit.  Is able to create a new ImageArray based on rules. """
    LIGHT = "#" # 1
    DARK = "."  # 0
    BIN_MAP = { DARK: '0', LIGHT: '1'}
    
    def __init__(self, image_data: str|set, img_enhancement_map: str, canvas_char='.') -> None:
        """ Create a new ImageArray, containing a set of lit pixels.

        Args:
            image_data (str|set): Str representation or set.
            img_enhancement_map (str): Map used for enhancing the image.
            canvas_char (str, optional): Typically DARK, but can be lit depending on enhancement map.
        """
        self._img_enhancement_map = img_enhancement_map
        
        if isinstance(image_data, str):
            self._pixels = self._process_img_str(image_data)    # convert to set
        else:
            assert isinstance(image_data, set)
            self._pixels = image_data
        
        # bounds of set, based on min and max coords in the set
        self._min_x = min(pixel.x for pixel in self._pixels)
        self._max_x = max(pixel.x for pixel in self._pixels)
        self._min_y = min(pixel.y for pixel in self._pixels)
        self._max_y = max(pixel.y for pixel in self._pixels)
        
        # The background canvas char can be changed, depending on first and last chars of the enhancement map
        self._canvas_char = canvas_char 
        
    def _process_img_str(self, image_data: str) -> set[Point]:
        """ Take a str of image data and convert to a set.
        Only stores points that are lit. """
        pixels = set()
        
        for y, line in enumerate(image_data.splitlines()):
            for x, char in enumerate(line):
                if char == ImageArray.LIGHT:    # only store lit pixels
                    pixels.add(Point(x, y))
        
        return pixels
    
    def render(self) -> str:
        """ Generate str representation """
        lines = []    
        for y in range(self._min_y, self._max_y+1):
            line = ""
            for x in range(self._min_x, self._max_x+1):                 
                char = ImageArray.LIGHT if Point(x,y) in self._pixels else ImageArray.DARK
                line += char

            lines.append(line)
            
        return "\n".join(lines)
    
    def render_image(self) -> Image.Image:
        '''Render this infinity bitmap as an image.'''
        width = self._max_x - self._min_x + 1
        height = self._max_y - self._min_y + 1

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (127, 127, 127)

        image = Image.new('RGB', (width, height), WHITE)
        image_data = []
        
        for x in range(width):
            for y in range(height):
                x_val = x + self._min_x
                y_val = y + self._min_y
                point = Point(x_val, y_val)

                if point in self._pixels:
                    image_data.append(WHITE)
                else:
                    image_data.append(BLACK)

        image.putdata(image_data)
        return image   
                            
    @property
    def lit_count(self) -> int:
        """ Return count of lit pixels """
        return len(self._pixels)

    def enhance(self) -> ImageArray:
        """ Process all squares simultaneously, i.e. based on current state of all pixels.
        Returns: New ImageArray, which will 1px bigger in all directions. """
        new_pixels = set()
        # Process using rules, with a 1px border around existing bounds
        for y in range(self._min_y-1, self._max_y+2):
            for x in range(self._min_x-1, self._max_x+2): 
                pnt = Point(x,y)       
                enhancement_i = self._image_enhancement_index(pnt) # get enhancement index for this point
                char = self._img_enhancement_map[enhancement_i] # determine type of pixel
                if char == ImageArray.LIGHT:
                    new_pixels.add(pnt)
        
        # Update the char that should be used for the infinite canvas next time.          
        next_canvas_char = self._img_enhancement_map[ImageArray._surrounded_by_index(self._canvas_char)]   
        return ImageArray(new_pixels, self._img_enhancement_map, canvas_char=next_canvas_char)
    
    def _outside_bounds(self, point: Point) -> bool:
        """ Determine if the specified point is within the existing bounds of the image. """
        return (point.x < self._min_x or point.x > self._max_x or
                point.y < self._min_y or point.y > self._max_y)
    
    @classmethod
    def _surrounded_by_index(cls, char: str) -> int:
        """ Get the mapping index for any char surrounded by . or # 
        I.e. where the 3x3 grid is all '.' (so int=0) or all '#' (so int=511). """
        assert char in (ImageArray.DARK, ImageArray.LIGHT), "Can only be surrounded by . or #"
        return ImageArray.convert_to_dec(9*ImageArray.BIN_MAP[char])
    
    def _image_enhancement_index(self, point: Point) -> int:
        """ Determine the decimal value of the 9-bit representation of this point.
        The 9-bit representation of the point is based on the 3x3 grid of pixels with this point at the centre. 
        Pixel lit (#) = 1, else 0.
        E.g. if only BR it lit, then the binary repr is 000000001.  If TL is lit, then 100000000.
        If the infinite canvas should be lit, then treat any pixels outside of 
        the current boundary as a lit pixel. """
        
        nine_box_bin = ""
        for nine_box_point in point.neighbours():   # process pixel by pixel
            if nine_box_point in self._pixels:  # If this is lit
                nine_box_bin += ImageArray.BIN_MAP[ImageArray.LIGHT]
            elif (self._outside_bounds(nine_box_point)): # in the infinite canvas area
                if self._canvas_char == ImageArray.LIGHT:
                    nine_box_bin += ImageArray.BIN_MAP[ImageArray.LIGHT]
                else:
                    nine_box_bin += ImageArray.BIN_MAP[ImageArray.DARK]
            else:   # dark pixel, and within bounds
                nine_box_bin += ImageArray.BIN_MAP[ImageArray.DARK]
        
        return int(nine_box_bin, 2)
    
    @staticmethod
    def convert_to_dec(input_str: str) -> int:
        """ Convert bin str (e.g. '111110101') to int value """
        assert len(input_str) == 9, "Valid input should be a nine-box str representation"
        return int(input_str, 2)
        
    def __repr__(self) -> str:
        return self.render()

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().split("\n\n")
        
    image_enhance_map, input_img = data
    image = ImageArray(input_img, image_enhance_map)
    
    base_image = image.render_image().resize((400, 400), Image.NEAREST)
    frames = []

    # Part 1 - Stop at 2 cycles
    for i in range(2):
        logger.debug("Image iteration %d", i)
        image = image.enhance()
        frames.append(image.render_image().resize((400, 400), Image.NEAREST))
    
    if RENDER:
        dir_path = Path(OUTPUT_FILE).parent
        if not Path.exists(dir_path):
            Path.mkdir(dir_path)
        base_image.save(OUTPUT_FILE, save_all=True, duration=200, append_images=frames)
        logger.info("Animation saved to %s", OUTPUT_FILE)        
    
    logger.info("Part 1: Lit=%d\n", image.lit_count)   
    
    # Part 2 - Stop at 50 cycles
    for i in range(2, 50):
        logger.debug("Image iteration %d", i)
        image = image.enhance()
        
    logger.info("Part 2: Lit=%d\n", image.lit_count)    
  
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)

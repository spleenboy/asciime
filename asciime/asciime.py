#! /usr/bin/python
import argparse
import ascii_map
from PIL import Image
from random import randint

ascii_resolution  =  3


class ASCII:
    def __init__(self, img, step = 5, grid = (3, 3), contrast = 128, invert = True, multiple = 1):
        self.img = img
        self.contrast = contrast
        self.step = step 
        self.grid = grid
        self.invert = invert
        self.multiple = multiple
        self.row = 0
        self.cols, self.rows = img.size

    def width(self):
        return self.cols / self.grid[0]

    def height(self):
        return self.rows / self.grid[1]

    def __iter__(self):
        return self 

    def next(self):
        self.row += self.step
        if self.row >= self.rows:
            raise StopIteration
        return self.line()

    def line(self):
        ascii = ""
        for x in xrange(0, self.cols, self.grid[0]):
            grid = self.get_grid(x)
            chars = self.find_characters(grid)
            if len(chars) > 0:
                char = ''
                for m in range(0, self.multiple):
                    char += chars[randint(0, len(chars) - 1)]
                ascii += char
            else:
                ascii += '  '
        return ascii

    def find_characters(self, grid):
        for x in xrange(0, len(ascii_map.characters), 2):
            chars = ascii_map.characters[x]
            if grid == chars:
                return ascii_map.characters[x + 1]
        return [' ']

    # Returns a 0/1 grid
    def get_grid(self, origin):
        grid = []
        for x in range(origin, origin + self.grid[0]):
            for y in range(self.row, self.row + self.grid[1]):
                grid.append(self.value(x, y))
        return grid

    # Returns a 0 or 1 based on the luminosity of the pixel
    def value(self, x, y):
        if x > self.cols or y >= self.rows:
            return 0
        lum = 255 - self.img.getpixel((x, y))
        pos = 0 if self.invert else 1
        neg = 1 if self.invert else 0
        return neg if lum < self.contrast else pos 




def prepare_image(file, width):
    img = Image.open(file)
    resized = image_resize(img, width)
    grayscale = resized.convert("L")
    return grayscale


def image_resize(img, width):
    old_width, old_height = img.size
    new_width = width * ascii_resolution
    ratio = float(new_width) / float(old_width)
    new_height = int(old_height * ratio)
    resized = img.resize((new_width, new_height), Image.ANTIALIAS)
    return resized

def main():

    parser = argparse.ArgumentParser(
            description='Turn an image into ASCII art')
    parser.add_argument('img', type=argparse.FileType('r'),
            help='The image to manipulate')
    parser.add_argument('-w', '--width', type=int, default=30, 
            help='The width in characters')
    parser.add_argument('-c', '--contrast', type=int, default=128, 
            help='The contrast (an int between 0 and 256)')
    parser.add_argument('-i', '--invert', action='store_true', 
            help='Invert the image')

    args = parser.parse_args()

    gray = prepare_image(args.img, args.width)
    ascii = ASCII(gray, contrast = args.contrast, invert = args.invert)
    for line in ascii:
        print line
    print "Printed %d x %d image" % (ascii.width(), ascii.height())

if __name__ == '__main__':
    main()

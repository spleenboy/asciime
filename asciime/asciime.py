#! /usr/bin/python
import argparse
import ascii_map
import imghdr
import re
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from StringIO import StringIO
from urllib2 import urlopen
from random import randint

ascii_resolution  =  3


class ASCII:
    def __init__(self, img, step = 6, grid = (3, 3), contrast = 128, invert = True, multiple = 1):
        self.img = img
        self.contrast = contrast
        self.step = step 
        self.grid = grid
        self.invert = invert
        self.multiple = multiple
        self.row = 0
        self.row_skip = step / grid[1]
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
                ascii += '?'
        return ascii

    def find_characters(self, grid):
        for x in xrange(0, len(ascii_map.characters), 2):
            chars = ascii_map.characters[x]
            if grid == chars:
                return ascii_map.characters[x + 1]
        return ['?']

    # Returns a 0/1 grid
    def get_grid(self, origin):
        grid = []
        top_y = self.row + (self.grid[1] * self.row_skip)
        top_x = origin + self.grid[0]
        for y in xrange(self.row, top_y, self.row_skip):
            for x in xrange(origin, top_x):
                grid.append(self.value(x, y))
        return grid

    # Returns a 0 or 1 based on the luminosity of the pixel
    def value(self, x, y):
        if x >= self.cols or y >= self.rows:
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


def get_file_from_url(url):
    rsp = urlopen(url)
    file = StringIO(rsp.read())
    return file


def find_image_file_at_url(url):
    file = get_file_from_url(url)
    type = imghdr.what(file)

    # Return a legitimate image file
    if type in ('jpeg', 'jpg', 'png', 'gif'):
        print "Loaded " + url
        return file

    # Otherwise, parse the text for a image path and return that instead
    contents = file.getvalue()

    # Instagram uses the css class 'photo', Twitter: 'media-slideshow-image'
    pattern = '<img class="photo|media-slideshow-image"[^>]+src="(?P<src>.+?)"'
    match = re.search(pattern, contents)
    if match:
        return find_image_file_at_url(match.group('src'))

    return None


def main():

    parser = argparse.ArgumentParser(
            description='Turn an image into ASCII art')
    parser.add_argument('--img', type=argparse.FileType('r'), nargs='?',
            help='The image to manipulate')
    parser.add_argument('--url', type=str, nargs='?',
            help='A url path to an image file')
    parser.add_argument('-w', '--width', type=int, default=30, 
            help='The width in characters')
    parser.add_argument('-c', '--contrast', type=int, default=128, 
            help='The contrast (an int between 0 and 256)')
    parser.add_argument('-i', '--invert', action='store_true', 
            help='Invert the image')
    parser.add_argument('-f', '--font',
            help='The .ttf font to use')
    parser.add_argument('-e', '--export', type=argparse.FileType('w'),
            help="The path to a file export location for the image")

    args = parser.parse_args()

    if args.img:
        img = args.img
    elif args.url:
        img = find_image_file_at_url(args.url)

    if img is None:
        parser.print_help()
        return

    gray = prepare_image(img, args.width)
    gray.show()
    ascii = ASCII(gray, contrast = args.contrast, invert = args.invert)

    if args.font:
        font_size = 30 
        bg = "black" if args.invert else "white"
        fg = "white" if args.invert else "black"
        ascii_image = Image.new("RGB", (ascii.width() * font_size, ascii.height() * font_size), bg)
        ascii_draw = ImageDraw.Draw(ascii_image)
        ascii_font = ImageFont.truetype(args.font, font_size)

    row = 0
    for line in ascii:
        print line
        if args.font:
            ascii_draw.text((0, row * font_size), line, font = ascii_font, fill = fg)
        row += 1
    print "Printed %d x %d image" % (ascii.width(), ascii.height())
    if args.font:
        ascii_image.show()
        if args.export:
            ascii_image.save(args.export)
 

if __name__ == '__main__':
    main()

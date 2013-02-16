#! /usr/bin/python
import argparse
from array import array

def main():
    parser = argparse.ArgumentParser(
            description='Generates an ASCII map')
    parser.add_argument('-x', '--width', type=int, default=3, 
            help='The width in pixels')
    parser.add_argument('-y', '--height', type=int, default=3, 
            help='The height in pixesl')

    args = parser.parse_args()

    quan = args.width * args.height
    num = 2 ** quan
    for i in range( 0, num + 1 ):
        n = bin(i).replace("0b", "").zfill(quan)
        print "# %d" %i
        msg = "[ \n"
        for row in range(0, args.height):
            for col in range(0, args.width):
                index = col + (row * args.width)
                msg += " %s," % n[index]
            msg += "\n"
        msg += "],\n[ ],"
        print msg

if __name__ == '__main__':
    main()

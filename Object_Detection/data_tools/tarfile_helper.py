#! /usr/bin/env python
# AUTHORS: Morgan Visnesky
# DATE: 01/16/2021
# FILENAME: tarfile_helper.py
#
###############################################################################
# INFO:
# - performs tarfile conversions

import os
import sys

def compressToTar(output_name, path_to_input):
    os.system('tar -cvf {} {}').format(output_name, path_to_input)
    print("Converted to .tar file \n")

def decompressFromTar(file_to_decompress):
    os.system('tar -xvf {}').format(file_to_decompress)
    print("Converted to .tar file \n")

def main():
    choice = input("Would you like to compress to or decompress from a tar file? (y/n)\n")
    if choice.lower() == 'y':
        outputName = input("Please enter what you would like the output to be named: \n")
        pathToInput = input("Please enter the path of the file to be compressed: \n")
        compressToTar(outputName, pathToInput)
    elif choice.lower() == 'n':
        fileToCompress = input("Enter the name of the tar file you would like to decompress: \n")
        decompressFromTar(fileToCompress)
    else:
        choice = input("Please enter 'y' or 'n' \n")


if __name__=="__main__":
    main()

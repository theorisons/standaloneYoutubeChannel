#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# Change the working directory.
# Use the parent one. Allows to import module from a parent directory.

from API.AWS.aws import Translate

fablesDirectory = "./fables"


def main():
    # Translate each fables in english
    # Need the french fable to be generated
    os.chdir(fablesDirectory)  # Move to fables directory

    books = os.listdir()  # Get all books

    translate = Translate()  #Init the connection

    for b in books:
        #Iterate on books
        os.chdir(b)  # Move to the book folder

        fables = os.listdir()  # Get all fables

        for f in fables:
            # Iterate on fables
            englishName = f[:-3]  # Remove .fr extension
            englishName = englishName + ".en"

            englishFable = open(englishName, "w")  # Create new file
            frenchFable = open(f, "r")  # Open french fable

            lines = frenchFable.readlines()

            for i in range(0, 2, 1):
                # Read the first 2 lines (Books + fable number)
                # \n are included
                line = lines[i]
                englishFable.write(line)

            for i in range(2, len(lines) - 1, 1):
                # Translate the fable
                # Add the final \n
                line = lines[i]
                translate.translation(line)
                englishFable.write(translate.getResult())
                englishFable.write("\n")

            # Write the final line. No \n to add.
            translate.translation(lines[-1])
            englishFable.write(translate.getResult())

            englishFable.close()
            frenchFable.close()
        os.chdir("..")  # Go back to parent directory


if __name__ == "__main__":
    main()
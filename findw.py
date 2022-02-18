#!/usr/bin/env python3

# A script that searches for a word in a ".txt" and plain text files inside a directory tree

import os, re, sys, getopt

os.system("") # to makes the ANSI escape sequence get processed correctly on Windows

#path = os.path.abspath("You can specify a permanent path here so you don't have to enter '-d' option each time you run the script.")
# If you choose to uncomment the above then comment out the 'path' variable below.

path = None
word = None # changing the value to 'sys.argv[1]' is especially useful if combined with the 'path' variable above. 
# Then the script could be used without needing to specify the '-w' and '-d' options since it would only search in one place on a disk. 
tree = None
foundFiles = None

# search for any passed arguments
try:
    if len(sys.argv) > 1:
        foundArgs = getopt.getopt(sys.argv[1:], "d:w:")[0]
        for arg, value in foundArgs:
            if arg in "-w":
                word = value
            elif arg in "-d":
                if value == "cwd" or value == "pwd":
                    path = os.getcwd()
                else:
                    path = value
except getopt.error as error:
    # show error if present
    print(f"\n-- {str(error)}\n")


def searchInput(tree, userInput):
    foundFiles = dict()
    for x in tree:
        cwd = x[0] # current working directory path
        for y in x[2]: # going through files
            try:
                with open(os.path.join(str(cwd), str(y)), "r") as file:
                    linecount = 0
                    for line in file:
                        linecount += 1
                        findLines = re.findall(rf'(.*{userInput}.*)', line, re.I) # matches a line with user's input
                        if findLines is not None and len(findLines) > 0: # if a match to user's input was found
                            for foundLine in findLines:
                                coloredline = foundLine.split()
                                wordcount = 0
                                for word in foundLine.split():
                                    if userInput[0].lower() in word.lower(): # 'findLines' regex from above already confirmed that the line contains user's input, so now we just need to find the starting position to color-code the output
                                        if len(userInput.split()) > 1:
                                            for wordToColor in coloredline[wordcount:wordcount+len(userInput.split())]:
                                                coloredline[coloredline.index(wordToColor)] = '\033[31m' + str(wordToColor) + '\033[0m'
                                        else:
                                            coloredline[wordcount] = '\033[31m' + str(coloredline[wordcount]) +  '\033[0m'
                                    else:
                                        wordcount += 1
                                line = " ".join(coloredline)
                            if str(cwd) in foundFiles: # if the path to the found file is already in the 'foundFiles' dictionary, then append a name of the file (the 'y') and a linecount to the already existing key
                                foundFiles[f'{cwd}'].append((y, linecount, line))
                            else: # otherwise, create a new key and assign a name of the the file and a linecount to it
                                foundFiles[f'{cwd}'] = [(y, linecount, line)] # value gets initiated as a tuple inside a list, so that if the match is found again in the same folder - which is used as a key in a dictionary - it could be appended to the list which is accessed by that key.
                                #Example:
                                #{'/mnt/ssd/Users/John/Destop': [(file1, 23, '\x1b[31mUserInput\x1b[0m'), (file2, 68, '\x1b[31mUserInput\x1b[0m'), (file3, 12, '\x1b[31mUserInput\x1b[0m')]}
            except:
                # the script reads all files; some of them are not in the text file format
                # so it gives out error:
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
                # I wanted this script to read both text files formats, those ending with ".txt" and those storred as plain text.
                # So it just skips over the files the format of which it cannot read.
                continue
    return foundFiles

try:
    if word is None:
        word = input("Enter a word to search: ")

    if path is None:
        path = input("Enter a folder to search: ")
        if path == "cwd" or path == "pwd" or path == "":
            path = os.getcwd()
except:
    print("\n")


if os.path.exists(path):
    tree = os.walk(path)
else:
    print("-- Couldn't find specified path.")

if word and tree:
    print(f'\n\033[41m——— Found input in the following files: ———\033[0m\n')
    foundFiles = searchInput(tree, word)

if foundFiles:
    for z in foundFiles:
        print(f'{z}:')
        for h in foundFiles[f'{z}']:
            print(f'—————— "{h[0]}" on line {h[1]}:\n {h[2]}\n\n')
else:
    print("-- No matches were found.\n")

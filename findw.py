#!/usr/bin/env python3

# A script that searches for a word in a ".txt" and plain text files inside a directory tree

import os, re, sys

cwd = os.getcwd()

tree = os.walk(cwd)

if len(sys.argv) > 1:
    word = sys.argv[1]
else:
    word = input("Enter a word to search: ")

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
                        findWord = re.search(rf'(?i:.*{userInput}.*)', line)
                        if findWord is not None: # if a match to user's input was found 
                            if str(cwd) in foundFiles: # if the path to the found file is already in the 'foundFiles' dictionary, then append a name of the file (the 'y') and a linecount to the already existing key  
                                foundFiles[f'{cwd}'].append((y, linecount))
                            else: # otherwise, create a new key and assign a name of the the file and a linecount to it
                                foundFiles[f'{cwd}'] = [(y, linecount)] # value gets initiated as a tuple inside a list, so that if the match is found again in the same folder - which is used as a key in a dictionary - it could be appended to the list which is accessed by that key.
                                #Example:
                                #{'/mnt/ssd/Users/John/Destop': [(file1, 23), (file2, 68), (file3, 12)]}
                            
            except: 
                # the script reads all files; some of them are not in the text file format
                # so it gives out error:
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
                # I wanted this script to read both text files formats, those ending with ".txt" and those storred as plain text.
                # So it just skips over the files the format of which it cannot read.
                continue
    return foundFiles

print(f'\nFound input in the following files:\n')

foundFiles = searchInput(tree, word)

if foundFiles:
    for z in foundFiles:
        print(f'{z}:')
        for h in foundFiles[f'{z}']:
            print(f'--- "{h[0]}" on line {h[1]}\n')
else:
    print("No matches were found.\n")

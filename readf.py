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
        cwd = x[0]
        for y in x[2]:
            try:
                with open(os.path.join(str(cwd), str(y)), "r") as file:
                    linecount = 0
                    for line in file:
                        linecount += 1
                        findWord = re.search(rf'.*{userInput}.*', line)
                        if findWord is not None:
                            if str(cwd) in foundFiles:
                                foundFiles[f'{cwd}'].append((y, linecount))
                            else:
                                foundFiles[f'{cwd}'] = [(y, linecount)]
                            
            except: 
                # the script reads all files; some of them are not in the text file format
                # so it give out error:
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
                # I wanted this script to read both text files formats, those ending with ".txt" and those storred as plain text.
                continue
    return foundFiles

print(f'\nFound words in following files:\n')

foundFiles = searchInput(tree, word)

for z in foundFiles:
    print(f'{z}:')
    for h in foundFiles[f'{z}']:
        print(f'--- "{h[0]}" on line {h[1]}\n')

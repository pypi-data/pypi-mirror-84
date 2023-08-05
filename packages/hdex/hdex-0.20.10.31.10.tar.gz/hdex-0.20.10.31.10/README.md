## Installation
'''pip install hdex'''

## How to use it?
It will generate words using keywords
Patterns 1987keyword keyword07 113@keyword keyword@67233 1987Keyword KEYWORD@67233
hdex.crunch(lowerlimit, upperlimit, ["keyword", "another keyword"], "special char", "file name")
to generate file
use any number at the place of "file name" for returning string

 '''hdex.crunch(4, 5, ["xyz", "abc", "ijkl"], "@", "dictionary.txt")'''
It will generate a file distionary

 '''str = hdex.crunch(4, 5, ["xyz", "abc"], "@", 1)'''
It will return values without generating any file

lower limit must be greater than 0
upper limit required
string must have at least one value ["name"]
only one special character required

## License
© Harsh Pratap Bhardwaj
This repository is licensed under the MIT license.
See LICENSE for details.

## Contact
Mail: harshpratap@outlook.in
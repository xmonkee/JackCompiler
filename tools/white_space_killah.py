# Author: Mayank Mandava
# Email: mayankmandava@gmail.com

def __removews(line):
    """Remove whitespaces from a string"""
    return ''.join(line.strip().split())


def __removecomments(line):
    """Removes comments from a string"""
    findcomment = line.find('//');
    if findcomment != -1:
        return line[:findcomment]
    else:
        return line


def kill_white_spaces(inlines, noComments):
    """Remove whitespaces, empty lines, and optionally comments from infile
    store results in outfile. noComments controls if comments are removed"""
    outlines = []
    for line in inlines:
        if noComments:
            line = __removecomments(line).strip()
        line = __removews(line)
        if line:
            outlines.append(line)
    return outlines



import sys
import os

from Utils import *


class File:
    """
    Simple file class containing file data: name and size
    """
    def __init__(self, name, size=0):
        self.name = name
        self.size = size

class Directory:
    def __init__(self, name, parent=None):
        # Directory data
        self.name = name
        # Reference to parent (containing) directory
        self.parent = parent
        # Total size of this directory's files
        self.size = 0
        # Dictionary of contained subdirectories
        self.subdirs = {}
        # Dictionary of contained files
        self.files = {}
        

    def add_file(self, file):
        """
        Adds a file to this directory
        """
        if file.name not in self.files:
            # Save ref. to file in this directory and index it by name
            self.files[file.name] = file
            # Increase directory size by this file's size
            # Also propagate size increment to parent directories
            self.size += file.size
            p = self.parent
            while p is not None:
                p.size += file.size
                p = p.parent
                

    def add_subdir(self, dir):
        """
        Adds a subdirectory to this directory
        """
        if dir.name not in self.subdirs:
            # Save ref. to subdir in this directory and index it by name
            self.subdirs[dir.name] = dir

def parse_filesystem(input):
    """
    Parse filesystem structure from input data and return reference to the root
    """
    # Define root directory
    root = Directory("/")
    # Saves reference to current working directory
    # To be able to move up and down the tree
    # By using cwd.subdirs and cwd.parent
    # Start with root
    cwd = root

    # Read input and create filesystem representation
    for line in input:
        if line.startswith("$"):
            # Got a command, parse it and its arguments
            try:
                # Try to get command with arguments
                _, cmd, args = line.split(" ")
                args = args.rstrip()
            except ValueError:
                # No arguments
                _, cmd = line.split(" ")
                args = None
            
            # Process commands
            if cmd == "cd":
                # Change dir
                if args == "/":
                    # We always start with root so do nothing
                    pass
                elif args == "..":
                    # Go to parent
                    cwd = cwd.parent
                else:
                    # Some specific subdirectory of the current one
                    # Navigate to subdir (set cwd to new dir)
                    cwd = cwd.subdirs[args]
        else:
            # Data line, add data for cwd
            if line.startswith("dir"):
                # New directory found, get its data
                _, dirname = line.split(" ")
                dirname = dirname.rstrip()
                # Save it to cwd
                cwd.add_subdir(Directory(dirname, cwd))
            else:
                # New file found
                size, filename = line.split(" ")
                size = int(size)
                filename = filename.rstrip()
                cwd.add_file(File(filename, size))

    return root

def part1(input):
    root = parse_filesystem(input)
    
    # Find out sum of directories with size <= SIZE_LIMIT
    total_size = 0
    SIZE_LIMIT = 100000

    # Start with root directory
    cwd = root
    if cwd.size <= SIZE_LIMIT:
        size_less_100k += cwd.size

    # While there are subdirectories to visit
    visit = list(cwd.subdirs.values())
    while len(visit) > 0:
        # Pop last element of visit list
        cwd = visit[-1]
        del visit[-1]
        
        # If its size is <= SIZE_LIMIT
        if cwd.size <= SIZE_LIMIT:
            total_size += cwd.size
        if len(cwd.subdirs) > 0:
            # Extend dirs to visit by appending the subdirectories of the cwd
            visit.extend(list(cwd.subdirs.values()))
    
    return total_size

def part2(input):
    root = parse_filesystem(input)

    disk_space = 70000000
    required_space = 30000000
    # Get total used space (size of root dir)
    used_space = root.size

    deleted_space = 0
    # Compute free space
    free_space = disk_space - used_space
    
    cwd = root
    if required_space > free_space:
        diff_space = required_space - free_space

        # Create list of directories sizes
        # While there are subdirectories to visit
        dir_spaces = [root.size]
        visit = list(cwd.subdirs.values())
        while len(visit) > 0:
            # Pop last element of visit list
            cwd = visit[-1]
            del visit[-1]
            
            dir_spaces.append(cwd.size)

            if len(cwd.subdirs) > 0:
                # Extend dirs to visit by appending the subdirectories of the cwd
                visit.extend(list(cwd.subdirs.values()))

        # Need to delete some *directory* to free up some space
        # Find the smallest directory whose size is > diff_space
        dir_spaces.sort()
        for s in dir_spaces:
            if s > diff_space:
                deleted_space = s
                break

    return deleted_space

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 95437)
    test_part(f"data/{filename}_test.txt", part2, 24933642)
    main(f"data/{filename}.txt")
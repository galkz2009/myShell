import os
import sys

def grep(file_path, pattern):
    """
    Search for a pattern in a file and print matching lines.
    :param file_path: the path to the file to search
    :param pattern: the pattern to search for
    :return: None
    """
    try:
        with open(file_path, "r") as f:
            for line in f:
                if pattern in line:
                    print(line, end="")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        grep(sys.argv[1], sys.argv[2])
    else:
        print("Usage: grep.py <file_path> <pattern>")
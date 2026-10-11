import os
import sys

def list_directory(path="."):
    """
    List the contents of a directory.
    :param path: the path to the directory to list (default is the current directory)
    :return: None
    """
    try:
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                item = f"[DIR] {item}"
            print(item)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        list_directory(sys.argv[1])
    else:
        list_directory()
import os
import sys

def hexdump(file_path):
    """
    Print the hexadecimal representation of a file's contents.
    :param file_path: the path to the file to dump
    :return: None
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            hex_content = ""
            ascii_content = ""
            counter = 0
            for byte in content:
                hex_content += f"{byte:02x} "
                ascii_content += chr(byte) if 32 <= byte <= 126 else "."
                counter += 1
                if counter % 16 == 0 and counter > 0:
                    hex_content += " " + ascii_content + "\n"
                    ascii_content = ""
            
            if ascii_content:
                hex_content += " " + ascii_content + "\n"
            print(hex_content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        hexdump(sys.argv[1])
    else:
        print("Usage: hexdump.py <file_path>")
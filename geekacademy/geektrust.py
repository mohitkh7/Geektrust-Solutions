from sys import argv
from src.main import GeekAcademy

def main():
    """
    Sample code to read inputs from the file
    """
    academy = GeekAcademy()
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    Lines = f.readlines()
    academy.execute(Lines)
    
if __name__ == "__main__":
    main()
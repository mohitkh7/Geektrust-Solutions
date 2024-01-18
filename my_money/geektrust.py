from sys import argv
from src.main import MyMoneyManager


def main():
    """
    Sample code to read inputs from the file
    """
    manager = MyMoneyManager()
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    lines = f.readlines()
    manager.execute(lines)


if __name__ == "__main__":
    main()

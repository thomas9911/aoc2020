import os
import sys

template = """
def main():
    with open("data.txt") as f:
        data = f.read()

if __name__ == "__main__":
    main()
"""

def touch(path):
    with open(path, "a"):
        os.utime(path, None)

def create(day):
    os.mkdir(day)

    with open(f"{day}/main.py", "w") as f:
        f.write(template)


    touch(f"{day}/data.txt")


def print_help():
    print("""
python gen_day.py [DAY]

Creates a day for advent of code    
    """)

def main():
    if len(sys.argv) <= 1:
        return print_help() 

    if sys.argv[1] in ["help", "h", "-h", "--help"]:
        return print_help()

    create(sys.argv[1])

if __name__ == "__main__":
    main()


import sys
from pickle import load as pload

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("ERROR: pass in exactly one txt file to be parsed for token list.")

    with open(sys.argv[1], "rb") as f:
        tokens = pload(f)

    

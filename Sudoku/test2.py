import sys; args = sys.argv[1:]

def main():
    PZLS = open(args[0]).read().split("\n")
    for idx, pzl in enumerate(PZLS):
        print(pzl)

if __name__ == "__main__":
    main()

#Dhruv Chandna Period 6 2025
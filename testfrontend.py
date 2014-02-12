from cllfrontend import CllCompilerFrontend
import sys

if __name__ == '__main__':
    cl = CllCompilerFrontend()
    cl.parseOptions(sys.argv[1:])
    cl.run()
    print(cl)
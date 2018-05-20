from ICA import *
from cec2014 import cec2014
if __name__ == "__main__":
  objetivo = lambda x: cec2014.cec14(x,19)
  ICA(objetivo, dim=10)

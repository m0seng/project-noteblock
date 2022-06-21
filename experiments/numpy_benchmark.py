import numpy as np
from timers import repeat_timer

audio = np.random.rand(2205, 2)
pan = np.random.rand(2)

@repeat_timer(iterations=1000)
def test():
    result = audio * pan

def main():
    test()

if __name__ == "__main__":
    main()
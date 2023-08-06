# __init__.pu主要执行的操作就是封包操作
from process import WavPro

def wavefunction(data):
    temp=WavPro(data)
    return temp

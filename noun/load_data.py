import pandas as pd
import pickle
import os.path

DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def loadData(pickle_name):
    unit_dic_path = os.path.join(DATAPATH, '{}.pickle'.format(pickle_name))
    with open(unit_dic_path, 'rb') as f:
        ret = pickle.load(f)

    return ret


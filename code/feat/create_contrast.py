from utils import STIM_DICT, CLUSTER_DICT

for i in range(len(CLUSTER_DICT)):
    scenario = list(CLUSTER_DICT.values())[i]
    contrast = ""
    for stim in STIM_DICT:
        if stim in scenario:
            contrast += "1 "
        else:
            contrast += "0 "
    print(contrast)
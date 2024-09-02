import matplotlib.pyplot as plt
import time
import numpy as np
import os
import hashlib
import matplotlib.patches as mpatches
import csv

ta_lower_bound = {
    "ta01": 1231, "ta02": 1244, "ta03": 1218, "ta04": 1175, "ta05": 1224, "ta06": 1238, "ta07": 1227, "ta08": 1217, "ta09": 1241, "ta10": 1241,
    "ta11": 1357, "ta12": 1367, "ta13": 1342, "ta14": 1345, "ta15": 1339, "ta16": 1360, "ta17": 1462, "ta18": 1377, "ta19": 1332, "ta20": 1348,
    "ta21": 1642, "ta22": 1561, "ta23": 1518, "ta24": 1644, "ta25": 1558, "ta26": 1591, "ta27": 1652, "ta28": 1603, "ta29": 1583, "ta30": 1528,
    "ta31": 1764, "ta32": 1774, "ta33": 1788, "ta34": 1828, "ta35": 2007, "ta36": 1819, "ta37": 1771, "ta38": 1673, "ta39": 1795, "ta40": 1651,
    "ta41": 1906, "ta42": 1884, "ta43": 1809, "ta44": 1948, "ta45": 1997, "ta46": 1957, "ta47": 1807, "ta48": 1912, "ta49": 1931, "ta50": 1833
}


def hash_color(value):
    value_str = str(value)
    hash_object = hashlib.md5(value_str.encode())
    hex_dig = hash_object.hexdigest()
    
    color = f'#{hex_dig[:6]}'
    return color

def draw(data, file_name, rule_ms, ta_LB, interval=10):

    min_ms = 1e6
    max_ms = -1e6
    min_tempature = ''
    for tmp in data.keys():
        for ms in data[tmp]:
            if ms < min_ms:
                min_tempature = tmp
            min_ms = min(min_ms, ms)
            max_ms = max(max_ms, ms)
    min_scope = min_ms - min_ms % 100
    max_scope = max_ms - max_ms % 100 + 100

    min_scope, max_scope = map(int, [min_scope, max_scope])

    max_height = 0
    for i, tmp in enumerate(data.keys()):
        _, bins, patches = plt.hist(data[tmp], bins=range(min_scope, max_scope, interval), alpha = 0.5, color=hash_color(10 * (i + 1)), edgecolor='black', label=tmp)

        heights, bin_edges = np.histogram(data[tmp], bins=range(min_scope, max_scope, interval))
        max_height = max(max_height, np.max(heights))


    plt.axvline(rule_ms, color='green', linestyle='--', linewidth=1)  

    plt.text(rule_ms, max_height * (0.60), f'MWKR={int(rule_ms)}', fontsize=12, verticalalignment='bottom', color='green')

    # rs method minimum line
    ##
    rs_min = min(min(data[tmp]) for tmp in data.keys())

    plt.axvline(rs_min, color='blue', linestyle='--', linewidth=1)
    plt.text(rs_min, max_height * (0.95), f'RS_opt={int(rs_min)}', fontsize=12, verticalalignment='bottom', color='blue')
    ##

    # ta lower bound
    ##
    plt.axvline(ta_LB, color='red', linestyle='--', linewidth=1)
    plt.text(ta_LB, max_height * (0.85), f'OR_opt={ta_LB}', fontsize=12, verticalalignment='bottom', color='red')
    ##


    plt.legend(title="Dataset Color Mapping", loc='upper right')

    plt.title('{}'.format(file_name))
    plt.xlabel(f'makespan: Opt is {min_tempature}')
    plt.ylabel('Frequency')

    os.makedirs('./histogram/10.0_1.0_0.1_0.01', exist_ok=True)
    plt.savefig('./histogram/10.0_1.0_0.1_0.01/{}.png'.format(file_name))
    plt.clf()

    time.sleep(1)

    return min_tempature
    

if __name__ == '__main__':
    data = []
    mwkr_ms = []
    with open('./result/mwkr/mwkr_test_result.txt', 'r') as inf:
        while True:
            line = inf.readline()
            if not line:
                break
            ms = float(line.split()[-4])
            mwkr_ms.append(ms)

    target_tmp = ['T=10.0','T=1.0', 'T=0.1', 'T=0.01']
    all_data = {}
    
    for rec in os.listdir('./result/draw'):
        tmp = rec[:-4][12:]
        if tmp not in target_tmp:
            continue

        with open('./result/draw/{}'.format(rec), 'r') as inf:
            while True:
                line = inf.readline()
                if not line:
                    break
                line = line.split()
                inst = line[2].split('/')[-1]
                if inst not in all_data:
                    all_data[inst] = {}
                
                if tmp not in all_data[inst]:
                    all_data[inst][tmp] = []
                
                all_data[inst][tmp].append(float(line[-4]))


    '''
    all_data = {
        'ta01' : {
            'T=0.1' : [1, 2, 3, 4, 5],
            'T=10.0': [3, 4, 5, 6, 7],
            ...
        }
        'ta02' : {
            'T=0.1' : [5, 3, 4, 5, 6, 1],
            ...
        }
        ...
    }
    '''
    min_tempature_list = []
    
    for idx, instance in enumerate(all_data.keys()):
        min_tempature_list.append(draw(all_data[instance], instance, mwkr_ms[idx], ta_lower_bound[instance]))
        
    with open('./histogram/10.0_1.0_0.1_0.01/opt_tempature.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(1, 51):
            writer.writerow(['ta' + str(i), min_tempature_list[i-1]])
            
    

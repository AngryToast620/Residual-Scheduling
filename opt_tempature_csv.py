import pandas as pd
import os

file_pathes = ['1.0_0.2_0.1',
               '1.0_0.2_0.05',
               '1.0_0.3_0.08_0.02',
               '2.0_0.2_0.02',
               '2.0_0.8_0.2_0.05_0.01',
               '10.0_1.0_0.1_0.01']

combined_df = pd.DataFrame()

# dataset = pd.DataFrame([['ta' + str(i+1) for i in range(50)]])
header = ['filename'] + ['ta' + str(i+1) for i in range(50)]

for file_name in file_pathes:
    df = pd.read_csv(f'./histogram/{file_name}/opt_tempature.csv', header=None, names=['label', 'value'])
    df = df.set_index('label').T
    df.insert(0, 'filename', file_name)
    # df['filename'] = file_name

    combined_df = pd.concat([combined_df, df])
    

combined_df.columns = header
combined_df.to_csv('opt.csv', index=False)
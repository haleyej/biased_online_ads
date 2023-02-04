import os
import pandas as pd
import numpy as np 
import re
import ast 

'''
Creates site look up table 
+ table of users to be sampled
'''

def create_site_look_up(user_id):
    '''
    Turns the commands file into a list of websites 
    that the simulated user visited and the asssociated
    suffixes in the image file names
    
    Naming convention works wether you use the 
    screenshot parts or the full image that has 
    been stitched together from the parts
    
    ARGS:
    user_id = used to identify the correct commands file 
    
    MSG TO SELF: 
    asssumes everyone has the same path to the commands file
    come back to file paths 
    
    hypothetically this only needs to be run once, 
    since all users should have the same file structure
    '''
    commands = pd.read_csv(f"example_folder/users/{user_id}/screenshot_0/commands_u{user_id[5:]}_s0.tsv", sep = "\t", header = None, index_col = 0).reset_index(drop = True)
    commands.columns = ['action', 'site']
    commands['site'] = commands.site.apply(ast.literal_eval)
    
    suffix_to_site = {}
    for idx, _ in commands.groupby(commands.index // 2):
        if commands.iloc[idx * 2]['action'] == 'GET' and commands.iloc[idx * 2 + 1]['action'] == 'FULL SCREENSHOT':
            site = commands.iloc[idx * 2]['site']['url']
            suffix = commands.iloc[idx * 2 + 1]['site']['suffix'][1:]
            suffix_to_site[suffix] = site
            
    site_look_up = pd.DataFrame.from_dict(suffix_to_site, orient = 'index').reset_index()
    site_look_up.columns = ['suffix', 'site']
    
    return site_look_up

def block_randomization(user_summary, sites, n):
    '''
    Combined user look up table with sites table 
    to get all possible combinations of 
    group/site pairs
    
    Performs block randomization on group/site combos, 
    to get n examples from each 
    
    Returns a dataframe with the info about the sampled 
    simulated users
    
    ARGS:
    user_summary = user-summary.csv in dataframe form 
    
    sites = .csv file created by the output of the
            create_site_look_up() function 
    
    n = number of examples to sample from each group/site combo
    '''
    users_df = user_summary.copy()
    users_df.user_id = users_df.user_id.apply(lambda s: f'user_{s}')
    users_df['key'] = 1
    users_df = users_df[['user_id', 'group', 'key']].values
    users_df = pd.DataFrame(users_df)
    users_df.columns = ['user', 'group', 'key']
    
    sites['key'] = 1
    
    all_sites = users_df.merge(sites, on = 'key', how = 'outer')
    all_sites = all_sites.drop(columns = 'key')
    
    sample_df = all_sites.groupby(['suffix', 'group']).sample(n, random_state = 42)
    
    return sample_df
    

def main():
    #run inside biased_online_ads directory
    user_summary = pd.read_csv("files/user-summary.csv")
    sites = create_site_look_up('user_1000')
    sites.to_csv('files/sites.csv')
    
    sample = block_randomization(user_summary, sites, 4)
    sample.to_csv("files/sampled_users.csv", index = False)

    return None 

if __name__ == "__main__":
    main()

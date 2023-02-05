import shutil
import os
import pandas as pd
import glob
import random


def get_targets(samples, samples_path):
    '''
    Creates a dictionary where keys are the 
    user id's to be sampled and the values 
    are names of the zip files with data
    for that user 

    Returns the dictionary

    ARGS:
        samples = pandas data frame with information 
                  about the users to be sampled 

        samples_path = path to hard drive containing
                       zip files to sample from 
    '''
    files = glob.glob(f"{samples_path}/*.zip")

    targets = {}
    for f in files: 
        zip_file = f.split("/")[-1]
        user = zip_file[:10]
        # fix minor naming discrepency 
        # bewteen samples file and folders on 
        # hard drive 
        if user[6] == '0':
            user = zip_file[:5] + zip_file[6:10]
        if user[7] == '0':
            user = zip_file[:5] + zip_file[7:10]
        if user in samples.user.values:
            targets[user] = zip_file
    return targets
    

def extract_samples(targets, samples, samples_path, extract_path, end_path):
    '''
    Iterates through all the users to sample from 
    Unpacks zip file with data for that user in extract_path
    Finds all the files matching the sampling criteria for that given user
    Randomly picks on of those files --> renames it 
    and moves it to end_path 

    Deletes extra data when done

    Returns None

    ARGS:
        targets = dictionary mapping of users to sample and the 
                  zip file with information about that user
        
        samples = pandas dataframe with information about
                  the users to be sampled

        samples_path = absolute path to the hard drive containg
                       all the data

        extract_path = absolute path to intermediate directory, where 
                       zip files are extracted to before being renamed
                       and moved to end_path

        end_path = absolute path to the final location of the 
                   sampled files
    '''
    failed = []

    for target, file in l:
        rows = samples[samples.user == target]
        full_path = f'{samples_path}/{file}'
        try:
            shutil.unpack_archive(full_path, extract_dir = extract_dir)
        except: 
            failed.append((target, "opening"))
            continue
        # get all examples from particular folder 
        for idx, vals in rows.iterrows():
            site = str(vals['suffix'])
            files = glob.glob(f'{extract_dir}/users/{target}/screenshot_0/data/screenshots/parts/*-_{site}-part*.png')
            try:
                file = random.choice(files)
            except:
                failed.append((target, 'site_match'))
                continue
            new_name = f'{target}_{site}.png'
            os.rename(file, f"{end_path}/{new_name}")
        # delete extra data when migration is done
        shutil.rmtree(f"{extract_dir}/users/{target}")
    
    failed_df = pd.DataFrame(failed, columns = ['user', 'cause'])
    return failed_df

def main():
    samples = pd.read_csv("/Users/haleyjohnson/Desktop/biased_online_ads/files/sampled_users.csv")

    # define absolute paths
    samples_path = '/Volumes/Sensitive Group Browsing/Sensitive Group Browsing/Screenshots'
    extract_path = '/Users/haleyjohnson/Desktop/samples'
    end_path = '/Users/haleyjohnson/Desktop/sample_screenshots'

    targets = get_targets(samples, samples_path)

    failed_df = extract_samples(targets, samples, samples_path, extract_path, end_path)
    failed_df.to_csv("../files/failed.csv", index = False)

if __name__ == "__main__":
    main()

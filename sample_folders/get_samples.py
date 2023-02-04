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
    for f in files[:1000]: 
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
    for target, file in list(targets.items()):
        rows = samples[samples.user == target]
        full_path = f'{samples_path}/{file}'
        shutil.unpack_archive(full_path, extract_path = extract_dir)
        # get all examples from particular folder 
        for idx, vals in rows.iterrows():
            site = str(vals['suffix'])
            # randomly selects one of the screenshots in the user file
            # that matches the site we want to sample from 
            files = glob.glob(f'{extract_path}/users/{target}/screenshot_0/data/screenshots/parts/*-_{site}-part*.png')
            img_file = random.choice(files)
            new_name = f'{target}_{site}.png'
            os.rename(img_file, f"{end_path}/{new_name}")
        # delete extra data when migration is done
        shutil.rmtree(f"{extract_path}/users/{target}")

    return None

def main():
    samples = pd.read_csv("/Users/haleyjohnson/Desktop/biased_online_ads/files/sampled_users.csv", index_col = 0)

    # define absolute paths
    samples_path = '/Volumes/Sensitive Group Browsing/Sensitive Group Browsing/Screenshots'
    extract_path = '/Users/haleyjohnson/Desktop/samples'
    end_path = '/Users/haleyjohnson/Desktop/sample_screenshots'

    targets = get_targets(samples, samples_path)

    extract_samples(targets, samples, samples_path, extract_path, end_path)

if __name__ == __main__():
    main()

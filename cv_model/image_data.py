
import pandas as pd
import cv2

class ImageData():
    def __init__(self, fname, colorway = cv2.COLOR_BGR2HLS, path = '', user_look_up = user_look_up, site_look_up = site_look_up):
        '''
        Class for screenshot data
        Mostly a convenience thing
        
        ARGS: 
        user_id = in the format 'user-####' (there can be any number of digits)
        fname = image file name
        colorway = colorway to read image in, default is HLS
        path = optional, if images are in another directory than current
        user_look_up = Pandas dataframe that associates user id's with the 
                       simulated user's protected class
        site_look_up = Pandas dataframe that associates the suffix used in the 
                       image filename (fname) with the website that was visited
                       
        '''
        self.user = fname.split("_")[1]
        self.img = cv2.cvtColor(cv2.imread(path + fname), colorway)
        self.shape = self.img.shape
        
        self.user_class = user_look_up[user_look_up.user_id == int(fname.split("_")[1])]['group'].values[0]
        self.site = site_look_up[site_look_up.suffix == int(fname.split("_")[-1][:-4])]['site'].values[0]
        

    def resize(self, w, h):
        '''
        Resizes the image
        Returns None
        
        ARGS:
        w = width of the image's new shape
        h = height of the image's new shape
        
        '''
        self.img = cv2.resize(self.img, (20, 20), interpolation = cv2.INTER_AREA)
        self.shape = self.img.shape
        
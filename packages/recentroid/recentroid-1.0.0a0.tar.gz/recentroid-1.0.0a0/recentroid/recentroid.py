import pandas as pd
from photutils import centroid_sources
from photutils import centroid_com,centroid_2dg
import copy

class Recentroid:
    """
    Recentroid computes centroids given initial locations in source_dict. This routine follows photutils.centroids implementation.
    #####
    + Example: https://photutils.readthedocs.io/en/stable/centroids.html
    #####
    + Inputs:
      - source_dict = a dict of key = source name and value = a dict with keys{'X','Y'} with values{pixel X,pixel Y} respectively.
      - data = 2D array of image
      - box_size = square box size in pixel to search for a centroid.
      - centroid_func = photutils.centroids object such as centroid_com, centroid_2dg, etc. 
        > Example: from photutils import centroid_2dg; centroid_func = centroid_2dg
        > if None, centroid_2dg is assigned.
    #####
    + Compute:
      - self.compute() to re-centroid after properly instantiated.
    #####
    + Output:
      - self.source_table_new
    """
    def __init__(self,source_dict,data,box_size,centroid_func=None):
        self.source_dict = source_dict
        self.source_table = self._source_table()
        self.data = data
        self.box_size = box_size
        self.centroid_func = centroid_func
        if self.centroid_func is None:
            self.centroid_func = centroid_2dg
    def compute(self):
        x_init,y_init = self.source_table.X,self.source_table.Y
        new_x,new_y = centroid_sources(self.data,x_init,y_init,box_size=self.box_size,centroid_func=self.centroid_func)
        source_table_new = copy.deepcopy(self.source_table)
        source_table_new['X'] = new_x
        source_table_new['Y'] = new_y
        self.source_table_new = source_table_new
    def _source_table(self):
        return pd.DataFrame(self.source_dict).T
        
    
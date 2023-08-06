import pandas as pd

class Disitribution():

    def __init__ (self, mean = 0):

        self.mean = mean
        self.df_data = pd.DataFrame()

    def read_data_file(self,file_name):

        self.df_data = pd.read_csv(file_name)

        return self.df_data


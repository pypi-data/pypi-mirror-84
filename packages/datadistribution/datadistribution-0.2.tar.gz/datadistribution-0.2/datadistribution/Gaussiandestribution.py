from .Generaldistribution import Disitribution

class Gaussian(Disitribution):

    def __init__(self):

        Disitribution.__init__(self)

    def column_list(self,file_name):

        self.df_data = self.read_data_file(file_name)

        self.column_list_data = self.df_data.select_dtypes(include=['float', 'int']).columns

        return self.column_list_data
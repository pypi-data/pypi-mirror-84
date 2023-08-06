from .Gaussiandestribution import Gaussian
from .Generaldistribution import Disitribution
import math

class Binomial(Gaussian):

    def __init__(self, mean=1,file_name='numbers.csv'):

        self.data_file = file_name

        Gaussian.__init__(self)
        Disitribution.__init__(self,mean)


    def calculate_mean(self):

        self.col_list = self.column_list(self.data_file)
        self.mean_list = []

        for col in self.col_list:
            self.col = col
            self.mean = 1.0 * sum(self.df_data[col]) / len(self.df_data[col])

            self.mean_list.append(str(self.col) + ':' + str(self.mean))

        return self.mean_list


    def calculate_stdev(self, sample=True):

        self.df_data = self.read_data_file(self.data_file)

        if sample:
            n = len(self.df_data) - 1
        else:
            n = len(self.df_data)


        self.data = self.calculate_mean()

        self.list = []

        for a in self.data:
            mean = a.split(':')[1]
            col = a.split(':')[0]

            self.sigma = 0

            for d in self.df_data[col]:
                self.sigma += (float(d) - float(mean)) ** 2

            self.sigma = math.sqrt(self.sigma / n)

            self.stdev = self.sigma

            self.list.append(str(col) + ':' + str(self.stdev))

        self.stdev = self.list


        return self.stdev

    def __add__(self,other):

        result = Binomial()
        self.mean = self.calculate_mean()
        other.mean = other.calculate_mean()

        a = 0
        self.mean_value = []

        for value1 in self.mean:
            b = 0
            for value2 in other.mean:
                if a == b:
                    value3 = float(value1.split(':')[1]) + float(value2.split(':')[1])
                else:
                    pass
                b += 1
            a += 1

            self.mean_value.append(str(value1.split(':')[0]) + ':' + str(value3))

        result.mean = self.mean_value

        self.stdev = self.calculate_stdev()
        other.stdev = other.calculate_stdev()

        a = 0
        self.stdev_value = []

        for value1 in self.stdev:
            b = 0
            for value2 in other.stdev:
                if a == b:
                    value3 = float(value1.split(':')[1]) + float(value2.split(':')[1])
                else:
                    pass
                b += 1
            a += 1

            self.stdev_value.append(str(value1.split(':')[0]) + ':' + str(value3))

        result.stdev = self.stdev_value

        return result

    def __repr__(self):

        return "Mean : {}  \nStandard Division : {} ".format(self.mean,self.stdev)

        #return "Cured: \n mean {}, standard deviation {}".format(self.mean,self.stdev)








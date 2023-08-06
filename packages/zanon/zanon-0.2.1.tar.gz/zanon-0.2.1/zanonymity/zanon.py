from .utils import *
from .evaluate_category import *
from .evaluate_output import *
from datetime import datetime, timedelta


class zanon(object):

    def __init__(self, deltat, z): 
        super(zanon, self).__init__()
        self.deltat = deltat
        self.z = z
        self.H = {}
        self.LRU = {}
        self.c = {}
        self.t_start = 0
        self.t_stop = 0

	
    def anonymize(self, line):
                
        t, u, a = read_next_visit(line)
            
        if self.t_start == 0:
            self.t_start = t
            f = open('output.txt', 'w+')
            f.close()
            f = open('simulation_output.txt', 'w+')
            f.close()
        
        self.t_stop = t
        
        #manage data structure
        manage_data_structure(t, u, a, self.H, self.LRU, self.c)
        #evict old users
        evict(t, self.H, self.LRU, self.c, self.deltat)
        #possibly outputs the data
        output = check_and_output(t, u, a, self.c, self.z)

        if output != None:
           # print(output)
            f = open('output.txt', 'a')
            f.write("\t".join(str(x) for x in output) + "\n")
            f.close()
            
    def duration(self):
        print('End of simulation (simulated time: {})'.format(str(timedelta(seconds = int(self.t_stop - self.t_start)))))

    def evaluate_output(self):
        evaluate_output()
        
    def evaluate_category(self,z):
        evaluate_cat(z)


		
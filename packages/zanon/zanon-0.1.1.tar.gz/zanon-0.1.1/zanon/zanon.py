import utils

class zanon(object):

    def __init__(self, deltat, z): 
        super(zanon, self).__init__()
        self.deltat = deltat
        self.z = z
        self.H = {}
        self.LRU = {}
        self.c = {}

	
    def anonymize(self, line, f):
        t, u, a = utils.read_next_visit(line)
            
        #manage data structure
        utils.manage_data_structure(t, u, a, self.H, self.LRU, self.c)
        #evict old users
        utils.evict(t, self.H, self.LRU, self.c, self.deltat)
        #possibly outputs the data
        output = utils.check_and_output(t, u, a, self.c, self.z)

        if output != None:
            print(output)
            f.write("\t".join(str(x) for x in output) + "\n")





		
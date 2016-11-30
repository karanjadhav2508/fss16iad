import sys
import os,subprocess
import logging,uuid

DEBUG= True
steps= 400

logging.basicConfig(filename='project.log',filemode='w',format='%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
class Parse():
    """
    Parse Prism output generated by
    prism negotiation.pm -simpath 10 filename

    To get the parse output call __str__ or get_output which gives output in JSON format
    """

    #return is format for get_output (status['purchase'],status['utility'],status['time'])

    matrix=[]
    purchase = 0
    time = sys.maxint
    utility = -sys.maxint-1


    def __init__(self,filename):
        def generate_matrix(filename):
            try:
                f = open ( filename , 'r')
                l = [ line.split(' ') for line in f ]
                return l
            except Exception as e:
                print ("Failed to initialize parse object due to ", e)
                sys.exit(1)

        self.matrix= generate_matrix(filename)
        self.get_purchase()
        self.get_time()
        self.get_utility()

    def get_matrix(self):
        if self.matrix == []:
             
	    logging.debug("Matrix was empty")
            #print ("Matrix is empty ..Exiting ")
            #sys.exit(1)

        else :
            return self.matrix

    def get_output(self):
        status={'time' : self.time, 'purchase':self.purchase , 'utility':self.utility }
        return int(status['purchase']),float(status['utility'])/float(status['time']),int(status['time'])
	

    def __str__(self):
        return str(self.get_output())

    def get_last_row(self):
        """
        Returns last row
        None if no purchased row
        """
        m=self.get_matrix()
	if m == [] or m == None : return ['-']
        last_row=len(m)-1
        return m[last_row]

    def get_purchase(self):
        self.purchase =1 if self.get_last_row()[0] == '[PURCHASE]' else 0

    def get_time (self) :
        #if purchase was made get the time of purchase
        if self.purchase == 1:
            self.time = self.get_last_row()[1]

    def get_utility (self) :
        #if purchase was made utility of last cbid or bid (whichever was made before)
        if self.purchase == 1:
            m=self.get_matrix()
	    if m == []: return
            for i in xrange((len(m)-1), -1, -1): # Efficient to parse list from last
                if m[i][0] == '[CBID]' :  self.utility = m[i][10] ; return ;
                if m[i][0] == '[BID]' : self.utility = m[i][3] ; return ;

def call_prism(prism_path,const):
	global steps
	model_file = "negotiation.pm"
	param1 = "-simpath"
	param2 = str(steps)
	const_list = ["B_RP", "S_RP", "B_IP", "S_IP", "Tb", "TbB", "Ts", "TsB", "bCinc", "bBinc", "sCdec", "sBdec", "Kb", "Ks","Offset"]	
	const_param = " ".join(["--const "+i+"="+str(j) for i,j in zip(const_list,const)])
	output_filename = "prism_output/sample_"+str(uuid.uuid4())+".txt"
	
	prism_command = " ".join([prism_path,model_file,param1,param2,output_filename,const_param])

	logging.debug(prism_command)
	try:	
		FNULL = open(os.devnull, 'w')
		subprocess.call(prism_command , shell=True,stdout= FNULL)
		return output_filename
	except :
		print "Exiting .. Check logs"
		sys.exit()

if __name__=='__main__':

    print Parse('sample/sampleoutput.txt')

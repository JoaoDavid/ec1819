class F2CSP_COUNTER:
    def __init__(self, inF = "", outF = "", nDom = 0, nVar = 0, nRes = 0, nAccept = 0, nReject = 0) :
        self.inFile = inF
        self.outFile = outF
        self.nDom = nDom
        self.nVar = nVar
        self.nRes = nRes
        self.nAccept = nAccept
        self.nReject = nReject

        
        
    def readFile(self) :
        self.inFile = input("Enter input file name:")
        self.outFile = input("Enter output file name:")  
        
        file = open(self.inFile,"r")
        
        
        markDom = 0
        markVar = 0
        markRes = 0
        markAccept = 0
        markReject = 0
        
        for line in file :
            line = line.split()
            for l in line :
                if(markDom == 1) :
                    markDom -= 1
                    self.nDom = int(l)
                
                if(markVar == 1) :
                    markVar -= 1
                    self.nVar = int(l)
                
                if(markRes == 1) :
                    markRes -= 1
                    self.nRes = int(l)
                    
                if(markAccept == 1) :
                    markAccept -= 1
                    self.nAccept += int(l)
                    
                if(markReject == 1) :
                    markReject -= 1
                    self.nReject += int(l)            
    
                if("Domains" in l) :
                    markDom += 1
                    
                if("Variables" in l) :
                    markVar += 1
                    
                if("Constraints:" in l) :
                    markRes += 1
                    
                if("Reject" in l) :
                    markReject += 1
                    
                if("Accept" in l) :
                    markAccept += 1        
                
        file.close()
                
    def writeStatistics(self) :
        f = open(self.outFile,"w+")
        
        f.write("Numero de Dominios: "+str(self.nDom))
        f.write("\n")
        f.write("Numero de Variaveis: "+str(self.nVar))
        f.write("\n")
        f.write("Numero de Restricoes: "+str(self.nRes))
        f.write("\n")
        f.write("Numero de Tuplos Aceites: "+str(self.nAccept))
        f.write("\n")
        f.write("Numero de Tuplos Rejeitados: "+str(self.nReject))
                

test = F2CSP_COUNTER()
test.readFile()
test.writeStatistics()
print("DONE")
class Domain():
    def __init__(self, name, start, end):
        self.name = name
        self.values = range(start,end+1)
        self.vars = []
        

    def addVariable(self,variable):
        self.vars.append(variable)

    def getValues(self):
        return self.values

    def getVars(self):
        return vars

    def strSelectVariables(self):
        print("vars"+str(self.vars))
        res = ""
        for v in self.vars:
            res += "?" + v + " "
        return res

    def __str__(self):
        res = ":" + self.name + " rdf:type :Domain ;\n" + "\t:values "
        for val in self.values[:-1]:
            res += str(val) + ", "
        res += str(self.values[-1]) + " ;\n\t:variables"
        for var in self.vars[:-1]:
            res += " :" + str(var) + ","
        res += " :" + self.vars[-1] + ".\n\n"
        return res

#Constraint ----------------------------------------------------------
class Constraint:
    def __init__(self):
        self.typeCons = ""
        self.vars = []
        self.values = []
        self.first = ""
        self.second = ""
        self.third = ""
    
    def addVar(self, var):
        self.vars.append(var)

    def addValue(self, value):
        self.values.append(value)

    def setTypeCons(self,typeCons):
        self.typeCons = typeCons
        if self.typeCons == "Reject:\n":
            self.first = " != "
            self.second = " || "
            self.third = " && "
        elif self.typeCons == "Accept:\n":
            self.first = " = "
            self.second = " && "
            self.third = " || "

    def __str__(self):
        print(self.values)
        print(self.vars)
        res = "\t\t( "
        for i in range(len(self.values)):
            res += "("
            for j in range(len(self.vars)):
                res += "?" + str(self.vars[j]) +  self.first +  str(self.values[i][j])
                if j == len(self.vars) - 1:
                    res += ")"                    
                else:
                    res += self.second

            if i != len(self.values) - 1:
                res += self.third
        res += " )\n"
        return res





class F2CSPtoRDF:
    def __init__(self):
        self.inFileName = ""
        self.outFileName = ""
        self.domains = {}
        self.fileOutRDF = None
        self.fileOutSPAQRL = None


    def writeDomains(self):
        for d in self.domains.keys():
            self.fileOutRDF.write(str(self.domains[d]))

    def parseConstraints(self, file, nConst):
        
        nConstParsed = 0
        for line in file:
            constraint = Constraint()
            if("Vars:" in line):
                if nConstParsed < nConst:
                    
                    nVars = int(file.readline())
                    for x in range(nVars):
                        var = file.readline().rstrip('\n')
                        constraint.addVar(var)
                    typeCons = file.readline()
                    constraint.setTypeCons(typeCons)
                    nValues = int(file.readline())
                    for x in range(nValues):
                        lineValue = file.readline().rstrip('\n')
                        constraint.addValue(lineValue.split())
                    if nConstParsed + 1 < nConst:
                        self.fileOutSPAQRL.write(str(constraint) + "\t\t&& \n")
                    else:
                        self.fileOutSPAQRL.write(str(constraint))
                    nConstParsed += 1

    def writeSelect(self):
        self.fileOutSPAQRL.write("SELECT ")
        for key, value in self.domains.items():
            self.fileOutSPAQRL.write(value.strSelectVariables())
        self.fileOutSPAQRL.write("\n")

    def writeWhere(self):
        self.fileOutSPAQRL.write("WHERE {\n")
        for key, value in self.domains.items():
            listVar = value.vars
            for v in listVar:
                self.fileOutSPAQRL.write("\t:D1 :values ?" + v + ".\n")
        self.fileOutSPAQRL.write("\tFILTER (\n")

    def writeFilter(self):
        print("DO")


    def run(self):
        self.inFileName = input("Enter input file name:")
        self.outFileName = input("Enter output file name:")
        self.fileOutRDF = open(self.outFileName + ".ttl","w+")
        self.fileOutRDF.write("@prefix : <http://www.w3.org> .\n")
        self.fileOutRDF.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n")
        self.fileOutSPAQRL = open(self.outFileName + ".rq","w+")
        self.fileOutSPAQRL.write("PREFIX : <http://www.w3.org>\n")
        self.fileOutSPAQRL.write("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n")

        file = open(self.inFileName, "r")
        for line in file:
            if("Domains:" in line):
                nDomains = int(file.readline())
                for n in range(nDomains):
                    currD = file.readline()
                    d = currD.split()
                    self.domains[d[0]] = Domain(d[0], int(d[1][0]),int(d[1][-1]))
            if("Variables:" in line):
                nVars = int(file.readline())
                for n in range(nVars):
                    currV = file.readline()
                    v = currV.split()
                    #self.domains[v[1]].vars.append(v[0])
                    self.domains[v[1]].addVariable(v[0])
                self.writeDomains()
            if("Constraints:" in line):
                self.writeSelect()
                self.writeWhere()
                self.parseConstraints(file,int(file.readline()))
                self.fileOutSPAQRL.write("\t)\n")
                self.fileOutSPAQRL.write("}")
                
                

                                



        #for x in self.domains.values():
        #    print(x.vars)
            #print(x)
        #print(self.domains["D1"])

        print("END")


            
scriptRun = F2CSPtoRDF()
scriptRun.run()
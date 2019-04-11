class Domain():
    def __init__(self, name, start, end):
        self.name = name
        self.values = range(start,end+1)
        self.vars = []
        

    def addVariable(self,variable):
        #print("IN ADD VAriable")
        #print(variable)
        self.vars.append(variable)

    def getValues(self):
        return self.values

    def getVars(self):
        return vars

    def __str__(self):
        res = ":" + self.name + " rdf:type :Domain ;\n" + "\t:values "
        for val in self.values[:-1]:
            res += str(val) + ", "
        res += str(self.values[-1]) + " ;\n\t:variables"
        for var in self.vars[:-1]:
            res += " :" + str(var) + ","
        res += " :" + self.vars[-1] + ".\n\n"
        return res

class Constraint:
    def __init__(self):
        self.type = ""
        self.vars = []
        self.values = [[]]
        self.first = ""
        self.second = ""
        self.third = ""
    
    def addVar(self, var):
        self.vars.append(var)

    def addValue(self, value):
        self.values.append(value)

    def setType(self,type):
        self.type = type
        if self.type == "Reject:":
            self.first = " != "
            self.second = " || "
            self.third = " && "
        elif self.type == "Accept:":
            self.first = " == "
            self.second = " && "
            self.third = " || "

    def __str__(self):
        res = "( "
        for i in range(len(self.values)):
            print(str(i) + " tou aqui")
            res += "("
            for j in range(len(self.vars)):
                res += "?" + self.vars[j] +  self.first +  self.values[i][j]
                print(res)
                if j <= len(self.vars):
                    res += self.second
                else:
                    res += ")"

            if i <= len(self.values):
                res += self.third
            else:
                res += " )"





class F2CSPtoRDF:
    def __init__(self):
        self.inFileName = "o4.txt"
        self.outFileName = "rdf4"
        self.domains = {}
        self.fileOutRDF = open(self.outFileName + ".ttl","w+")
        self.fileOutRDF.write("@prefix : <http://www.w3.org> .\n")
        self.fileOutRDF.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n")
        self.fileOutSPAQRL = open(self.outFileName + ".rq","w+")
        self.fileOutSPAQRL.write("PREFIX : <http://www.w3.org>\n")
        self.fileOutSPAQRL.write("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n\n")

    def writeDomains(self):
        for d in self.domains.keys():
            self.fileOutRDF.write(str(self.domains[d]))
            #self.fileOutRDF.write(":" + d.name + " rdf:type :Domain ;\n")
            #self.fileOutRDF.write(":values " + ",".join(str(i) for i in self.domains[d].getValues) + ";\n")
            #self.fileOutRDF.write(":variables")
            #for v in d.getVars():
            #    self.fileOutRDF.write(":" + v + " ")
            #self.fileOutRDF.write(str(d.vars))
            #self.fileOutRDF.write(".\n\n")
    
    def writeReject(self, f, vars):
        self.fileOutRDF.write(":" + vars[0] + " rdf:type :Variable ;\n")
        self.fileOutRDF.write("\t" + ":differsFrom :" + vars[1] + ".\n\n")  

    def writeAccept(self, f, vars, values):
        self.fileOutRDF.write(":" + str(vars[0]) + " rdf:type :Variable ;\n")
        self.fileOutRDF.write("\t" + ":value " + str(values[0]) + "." + "\n")  

    def parseConstraints(self, file, nConst):
        
        nConstParsed = 0
        for line in file:
            constraint = Constraint()
            if("Vars:" in line):
                if nConstParsed < nConst:
                    nConstParsed += 1
                    nVars = int(file.readline())
                    for x in range(nVars):
                        var = file.readline().rstrip('\n')
                        constraint.addVar(var)
                    constraint.setType(file.readline())
                    nValues = int(file.readline())
                    for x in range(nValues):
                        lineValue = file.readline().rstrip('\n')
                        constraint.addValue(lineValue.split())
                    file.write(str(constraint))

    def run(self):
        #self.inFileName = input("Enter input file name:")
        #self.outFileName = input("Enter output file name:")

        file = open(self.inFileName, "r")

        for line in file:
            #print(line)
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
                self.parseConstraints(file,int(file.readline()))
                

                                



        #for x in self.domains.values():
        #    print(x.vars)
            #print(x)
        #print(self.domains["D1"])

        print("END")


            
#scriptRun = F2CSPtoRDF()
#scriptRun.run()

constraint = Constraint()
constraint.setType("Reject:")
constraint.addVar("V11")
constraint.addVar("V12")
constraint.addValue([1,1])
constraint.addValue([2,2])
constraint.addValue([3,3])
constraint.addValue([4,4])
print(str(constraint))

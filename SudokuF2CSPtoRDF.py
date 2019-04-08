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


class F2CSPtoRDF:
    def __init__(self):
        self.inFileName = "o4.txt"
        self.outFileName = "rdf4.ttl"
        self.domains = {}
        self.fileOut = open(self.outFileName,"w+")
        self.fileOut.write("@prefix : <http://www.w3.org> .\n")
        self.fileOut.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n")

    def writeDomains(self):
        for d in self.domains.keys():
            self.fileOut.write(str(self.domains[d]))
            #self.fileOut.write(":" + d.name + " rdf:type :Domain ;\n")
            #self.fileOut.write(":values " + ",".join(str(i) for i in self.domains[d].getValues) + ";\n")
            #self.fileOut.write(":variables")
            #for v in d.getVars():
            #    self.fileOut.write(":" + v + " ")
            #self.fileOut.write(str(d.vars))
            #self.fileOut.write(".\n\n")
    
    def writeReject(self, f, vars):
        self.fileOut.write(":" + vars[0] + " rdf:type :Variable ;\n")
        self.fileOut.write("\t" + ":differsFrom :" + vars[1] + ".\n\n")  

    def writeAccept(self, f, vars, values):
        self.fileOut.write(":" + str(vars[0]) + " rdf:type :Variable ;\n")
        self.fileOut.write("\t" + ":value " + str(values[0]) + "." + "\n")  

    def parseConstraints(self, file, nConst):
        nConstParsed = 0
        for line in file:
            if("Vars:" in line):
                if nConstParsed < nConst:
                    nConstParsed += 1
                    nVars = int(file.readline())
                    vars = []
                    for x in range(nVars):
                        vars.append(file.readline().rstrip('\n'))
                    if "Reject:" in file.readline():
                        self.writeReject(file, vars)
                    else:
                        nValues = int(file.readline())
                        values = []
                        for x in range(nValues):
                            values.append(file.readline().rstrip('\n'))
                        self.writeAccept(file, vars, values)

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


            
scriptRun = F2CSPtoRDF()
scriptRun.run()



class FileHandler:
    def read_list(self, field: int, choice: int, reference: list):
        '''read the meta file and use it to read the list of options'''
        out: list = []

        file = open(file="res/image/menu/info.txt", mode="r")

        for line in file:
            line = line.replace("\n",",")
            fields = line.split(",")

            match(field):
                case 0:
                    if fields[field] not in out:
                        out.append(fields[field])
                case 1:
                    if fields[0] == reference[choice][0]:
                        if fields[1] not in out:
                            out.append(fields[field])
                case 2:
                    if fields[0] == reference[choice][0]:
                        if fields[1] == reference[choice][1]:
                            if fields[2] not in out:
                                out.append(fields[field])
        return out

    def find_gate(self, building: str)-> list:
        out: list = []

        file = open(file="res/image/menu/info.txt", mode="r")

        for line in file:
            line = line.replace("\n",",")
            line = line[:-1]
            fields = line.split(",")

            if fields[0]==building and fields[2]=="Gate":
                #print(line+" before") # DEBUG
                out.append(fields)
                #print(line[:-1]+" after") # DEBUG

        #print(out) # DEBUG
        return out


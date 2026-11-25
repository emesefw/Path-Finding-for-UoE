import handler

fh = handler.FileHandler()

class Generate:
    def __init__(self):
        self.checkpoints: list = []
        '''
        for the task of this class:
        1. break the command in to checkpoints
        2. breakdown each stages in checkpoints into actionable steps using a star
        '''

    def generate_checkpoints(self, u_input):
        '''produce a plan that is maximun out of 4 steps'''
        out: list = []
        command: tuple = ("","")

        if u_input[0][0] != u_input[1][0]: # different building
            array = fh.find_gate(u_input[0][0]) # find gate in origin building
            if all(row[1] != u_input[0][1] for row in array): # origin room is at different floor as gate

                address1 = u_input[0][0]+","+u_input[0][1]+","+u_input[0][2]
                address2 = u_input[0][0]+","+u_input[0][1]+",Elevator"
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

                address1 = array[0][0]+","+array[0][1]+",Elevator"
                address2 = array[0][0]+","+array[0][1]+","+array[0][2]
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

            else: # origin room is at the same floor as gate
                address1 = u_input[0][0]+","+u_input[0][1]+","+u_input[0][2]
                address2 = u_input[0][0]+","+u_input[0][1]+",Gate"
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

            array = fh.find_gate(u_input[1][0]) # find gate in destination building
            if all(row[1] != u_input[1][1] for row in array): # destination room is at different floor as gate
                address1 = array[0][0]+","+array[0][1]+","+array[0][2]
                address2 = array[0][0]+","+array[0][1]+",Elevator"
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

                address1 = u_input[1][0]+","+u_input[1][1]+",Elevator"
                address2 = u_input[1][0]+","+u_input[1][1]+","+u_input[1][2]
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

            else:
                address1 = u_input[1][0]+","+u_input[1][1]+",Gate"
                address2 = u_input[1][0]+","+u_input[1][1]+","+u_input[1][2]
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

        else: # same building
            if u_input[0][1] != u_input[1][1]: # rooms are on different floor
                address1 = u_input[0][0]+","+u_input[0][1]+","+u_input[0][2]
                address2 = u_input[0][0]+","+u_input[0][1]+",Elevator"
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

                address1 = u_input[1][0]+","+u_input[1][1]+",Elevator"
                address2 = u_input[1][0]+","+u_input[1][1]+","+u_input[1][2]
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

            else: # rooms are on the same floor
                address1 = u_input[0][0]+","+u_input[0][1]+","+u_input[0][2]
                address2 = u_input[1][0]+","+u_input[1][1]+","+u_input[1][2]
                command = (address1, address2)
                out.append(command)

                #print(command) # DEBUG

        #print(out) # DEBUG
        self.checkpoints = out


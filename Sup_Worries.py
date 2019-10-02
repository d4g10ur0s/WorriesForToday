import datetime
import pathlib
import os

#my Exceptions
class NotADateException(Exception):
    pass

class CollissionException(Exception):
    pass

class TodayException(Exception):
    pass

class NoWorryException(Exception):
    pass

# 1 Global Variables
# the main path
path_var = __file__
name_Dir = "myList"
name_txt = "\\Worries.txt"

def set_Up_pathvar():
    global path_var
    p = pathlib.PureWindowsPath(path_var)
    arr = []

    for i in p.parts:
        arr.append(i)

    arr.pop()
    path_var = arr.pop(0)
    for i in arr:
        path_var += i + '\\'

    path_var += name_Dir

#Create the txt for worries
def createWorryFile(temp_path = "D:\\mylist\\Worries.txt"):

    with open(temp_path,'w') as file:
        file.write("idl last_occur fr name\n")
        file.close()

#******************************************************************#

#Class for construction of an item
class Item:
    name = ""
    fr = ""
    last_occur = ""
    idl = ""

    def __init__(self,name = "", y = 2019, m = 1, d = 1, fr = 0):
        self.name = name

        if y == 2019  and m == 1 and d == 1:
            self.last_occur = str( datetime.date.today() )
        else:
            self.last_occur = str( datetime.date(y,m,d) )

        self.setFreq(fr)
#With this method, I make a length 2 string of numbers
    def setFreq(self,fr = 0):

        self.fr = str(fr)

        if len(self.fr)>1:
            pass

        else:
            self.fr = None
            self.fr = str(0) + str(fr)

#Saving stuff

    def getIdl(self):
        return self.idl
    def setIdl(self,idl = ""):
        self.idl = idl
    def getName(self):
        return self.name
    def getFreq(self):
        return self.fr

    def find_Idl(self):
        self.idl = len(self.name)%10
        self.idl = str(self.idl)+"00"

    def configure_Idl(self,tim = 0):
        self.idl = str( int(self.idl) + tim)



#get the info line, the line to be written
    def getInfoLine(self):
        #        3         1      10              1       2        1    4 + ??          1
        return self.idl + " " +self.last_occur + " " + self.fr + " " + self.name + "\n"

#*******************************************************************************
#SAVING STUFF
#save a Worry in a file
def hash_no_more(content = [], i = 0):
    try :
        a = content[i+1]
        return False
    except :
        return True



def saveWorry(obj = Item(),temp_path = "D:\\mylist\\Worries.txt"):

    file = open(temp_path,"r+")
    content = file.readlines()
    obj.find_Idl()
    temp_idl = obj.getIdl()

    if len(content) == 1:

        content.append( obj.getInfoLine() )
        file.seek(0,0)

#Improvements
        for line in content:
            file.write(line)

    else:

        for i in range(1,len(content)):
            line = content[i]

            #if this worry already exists
            if obj.getName() in line:
                raise CollissionException

            if line[0] == temp_idl[0]:
                obj.configure_Idl( int(line[0:3]) )
                content.insert(i,obj.getInfoLine())
                break

            elif int(line[0]) > int(temp_idl[0]) and has_no_more(content,i) :
                content.insert(i,obj.getInfoLine())
                break

            elif int(line[0]) < int(temp_idl[0]):
                dist = int(line[0:3])
                i+=dist
#Improvements
        file.seek(0,0)
        for line in content :
            file.write(line)


    file.close()


#*************************************************************
#needs Improvements
#*************************************************************
def Modify_Frequency(obj = Item()):
    global path_var
    global name_txt

    file = open(path_var+name_txt,"r+")
    content = file.readlines()
    obj.find_Idl()
    temp_id = obj.getIdl()

    for i in range(1,len(content)):
        line = content[i]

        if temp_id[0] == line[0]:

            if obj.getName() in line:

                if line[14:17] == obj.getFreq():
                     break

                else:
                    line = obj.getInfoLine()
                    break

            else:
                pass

        elif int(temp_idl[0]) > int(line[0]):
            dist = int(line[0:3])
            i+=dist

        elif int(temp_idl[0]) < int(line[0]):
            raise NoWorryException

        else:
            pass

    file.seek(0,0)

    for line in content:
        file.write(line)

    file.close()




#GETTING STUFF
def check_date(line = ""):

    month_dir = [31,[28,30],31,30,31,30,31,31,30,31,30,31]

    tod = str( datetime.date.today() )
    dat = line[4:14]
    freq = line[15:17]
    sum = 0
    m_distance = int(tod[5:7]) - int(dat[5:7])

    if m_distance == 0:
        sum = int(tod[8:]) - int(dat[8:])

    elif m_distance>0:

        for i in range(0,m_distance):
            #Get the days from the dictionary
            sum = sum + month_dir[int( dat[5:7] ) + i - 1]

        sum += ( int(tod[8:]) - int(dat[8:]) )

    else:

        m_distance = m_distance*(-1) - 11

        for i in range(0,m_distance):
            step = i+int(dat[5:7])-1

            if step > 11:
                step = step - 11

            #Get the days from the dictionary
            sum = sum + month_dir[step]

        sum += int(tod[8:]) - int(dat[8:])

    if sum == int(freq):
        return True
    else:
        return False

def getTWorries():
    global path_var
    global name_txt
    file = open(path_var+name_txt,"r+")
    content = file.readlines()
    content.pop(0)
    tod_arr = []
    for line in content:
        if check_date(line) :
            tod_arr.append(line)
        else:
            pass
    return tod_arr[:]
#If Today Is Empty
#Make Some Worries :( :( :(
def funtction_I():
    global path_var
    global name_txt

    print("No Worries For Today\n")
    print("Add A Worry For Today? (y/n)\n")
    inp = input()
    if inp == "y":

        print("Name\n")
        name = input()

        obj = Item(name)
        try :
            saveWorry(obj,path_var+name_txt)
            return True
        except :
            print("Item already exists are u sure you want to replace it? (y/n)")
            return False

#Print today's worries
def print_Today():
    global path_var
    global name_txt
    #today string
    tod = str( datetime.date.today() )

    if os.path.exists(path_var + "\\" + tod + ".txt"):
        #print the worries that exist
        file = open(path_var + "\\" + tod + ".txt","r+")
        content = file.readlines()
        for line in content:
            print(line)

    else:
        #first time for today
        createWorryFile(path_var + "\\" + tod + ".txt")
        tod_worries = getTWorries()
        file = open(path_var + "\\" + tod + ".txt","a+")

        if len(tod_worries) == 0:
            file.close()
            #funtction_I
            #There are no worries for Today
            if funtction_I():
                tod_worries = getTWorries()
            else:
                #things did not happen properly
                #No worries at all
                return False

        else:
            pass
        #write & print today's worries
        file = open(path_var + "\\" + tod + ".txt","a+")

        for line in tod_worries:
            file.write(line)

        file.seek(0,0)
        tod_worries = file.readlines()

        for line in tod_worries:
            print(line)

def add_days_worries():
    global path_var
    global name_txt

    print("Name\n")
    name = input()
    print("Frequency (In days)\n")
    freq = input()
    tod = str( datetime.date.today() )
    obj = Item(name,int(tod[:5]),int(tod[5:8]),int(tod[8:]),freq)

    file = open(path_var+"\\"+tod+".txt","a+")
    file.write(obj.getInfoLine())
    file.close()

    try:
        saveWorry(path_var+name_txt)
    except:
        print("A collision occured.Do you want to recalculate frequency? (y/n)\n")
        inp = input()
        sum = 0
        if inp == "y" or inp =="Y":
            if os.path.exists(path_var+obj.getName()+".txt"):
                file = open(path_var+obj.getName()+".txt","r+")
                content = file.readlines()
                if len(content) >= 10:
                    for fr in content:
                        sum += int(fr)
                    sum = round(sum/10)
                    file.seek(0,0)
                    file.write(str(sum))
                    file.close()
                    Modify_Frequency(obj)
            else:
                file = open(path_var+obj.getName()+".txt","w+")
                file.write( str( obj.getFreq() ) )
                file.close()



#*******************************************************************************



#First time using the programm
def createSystem():
    global path_var
    os.mkdir(path_var)


def lets_get_started():

    global path_var
    global name_txt
#Set the path correctly
    temp_path = path_var+name_txt

    print("Have Any Worries? (y/n)\n")
    inp = input()
    if inp == 'y':

        print("Name\n")
        name = input()

        print("When will it be occured?\n")
        print("Year\n")
        y = input()
        print("Month\n")
        m = input()
        print("Day\n")
        d = input()

        obj = Item(name,int(y),int(m),int(d))
        #it is sure that an Exception isn't going to be raised
        saveWorry(obj,temp_path)
        #return True

    else:
        pass
        #return False

#*********************************************************************************************

def main():

    global path_var
    global name_txt

#in the directory
    set_Up_pathvar()

#first time using the programm or not??
    if os.path.exists(path_var):
        pass

    else:
        createSystem()
        createWorryFile(path_var + name_txt)
        lets_get_started()

    inp = ""
    while not(inp=="Close" or inp == "close"):
        print_Today()
        print("****\n1)Worry for today\n2)Add a worry\n")
        inp = input()
        if inp == 1:
            add_days_worries()
        elif inp == 2:
            lets_get_started()

#if __name__ == "__main__":
 #   main()

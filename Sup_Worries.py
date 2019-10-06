import datetime
import pathlib
import os
#Bugs
#frequency txt
#next frequency doesnt occur
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

def has_no_more(arr = [],pos = 0):
    try :
        pos = arr[pos+1]
        return False
    except:
         return True

def set_Up_pathvar():
    global path_var
    mpath = path_var.split("\\")
    path_var = ""
    mpath.pop(len(mpath)-1)
    for word in mpath:
        path_var = path_var + word + "\\"
    path_var = path_var + name_Dir
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

    def setDate(self,y=2019,m=1,d=1):
        self.last_occur = str(datetime.date(y,m,d))
    def getDate(self):
        return self.last_occur

#Saving stuff

    def getIdl(self):
        return self.idl
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
                dist = int(line[1:3])
                if dist == 0:
                    content.insert(i+1,obj.getInfoLine())
                    break
                else:
                    i+=dist
#Improvements
        file.seek(0,0)
        for line in content :
            file.write(line)


    file.close()
    return obj


#*************************************************************
#needs Improvements
#*************************************************************
#set the frequency inside the main file
def Modify_Frequency(obj = Item()):
    global path_var
    global name_txt

    file = open(path_var+name_txt,"r+")
    content = file.readlines()
    obj.find_Idl()
    temp_id = obj.getIdl()
    toret = ""

    for i in range(1,len(content)):
        line = content[i]

        if temp_id[0] == line[0]:

            if obj.getName() in line:

                if line[14:17] == obj.getFreq():
                     return line[14:17]

                else:
                    toret = line[14:17]
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
    return toret

def setNextDate(obj = Item()):
    month_dir = [31,[28,30],31,30,31,30,31,31,30,31,30,31]
    fr = int(obj.getFreq())
    dat = obj.getDate().split("-")
    dat[2] = int(dat[2]) + int(fr)
    dat[1] = int(dat[1])

    if month_dir[int(dat[1])-1] < dat[2]:
        dat[2] = dat[2] - month_dir[int(dat[1])-1]
    else:
        pass
    if dat[1] >= 12:
        dat[1] -= 12
    else:
        pass
    obj.setDate(int(dat[0]),dat[1],dat[2])
    return obj.getInfoLine()


#GETTING STUFF
def check_date(line = ""):

    month_dir = [31,[28,30],31,30,31,30,31,31,30,31,30,31]

    tod = str( datetime.date.today() )
    dat = line[4:14]
    if tod == dat:
        return True
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
    return tod_arr
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
        except CollissionException:
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
        tod_worries = getTWorries()
        file = open(path_var + "\\" + tod + ".txt","r+")
        content = file.readlines()
        #in case something is not inside today's worries
        if len(content[1:])<len(tod_worries):

            tod_worries.insert(0,content[0])
            content = tod_worries
            file.seek(0,0)

            for line in content:
                file.write(line)
        else:
            pass

        print(content[0])

        for i in range(1,len(content)):
            print(str(i) + ")" + content[i])

    else:
        #first time for today
        createWorryFile(path_var + "\\" + tod + ".txt")
        tod_worries = getTWorries()

        if len(tod_worries) == 0:
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

        print(tod_worries[0])

        for i in range(1,len(tod_worries)):
            print(str(i) + ")" + tod_worries[i])


def add_days_worries():
    global path_var
    global name_txt
    set_Up_pathvar()

    print("Name\n")
    name = input()
    print("Frequency (In days)\n")
    freq = input()
    tod = str( datetime.date.today() )
    obj = Item(name,int(tod[:4]),int(tod[5:7]),int(tod[8:]),freq)
    sum = 0

    try :
        saveWorry(obj,path_var+name_txt)
    except CollissionException:
        print("A Collission Occured.Do You Want To Recalculate Frequency? (y/n)\n")
        inp = input()
        if inp == "y" or inp == "Y":

            if not os.path.exists(path_var+"\\"+obj.getName()+".txt"):
                toret = Modify_Frequency(obj)
                file = open(path_var+"\\"+obj.getName()+".txt","w+")
                file.write(toret+"\n")
                file.write(obj.getFreq()+"\n")
                file.close()
            else:
                file = open(path_var+"\\"+obj.getName()+".txt","r+")
                toret = Modify_Frequency()
                file.write(toret+"\n")
                content = file.readlines()
                for line in content:
                    sum+=int(line)
                sum = round(sum/len(content))
                obj.setFreq(sum)
                file.close()
                if len(content) == 10:
                    os.remove(path_var+"\\"+obj.getName()+".txt")
                else:
                    pass
        else:
            return 0

        Modify_Frequency(obj)

def change_line(line = ""):
    global path_var
    global name_txt
    file = open(path_var+name_txt,"r+")
    content = file.readlines()
    for i in range(1,len(content)):
        temp_idl = content[i]
        temp_idl = temp_idl[:3]
        if int(temp_idl[0]) < int(line[0]):
            i += int(temp_idl[1:3])
        elif line[:3] == temp_idl:
            content[i] = line
            break
        else:
            pass

    file.seek(0,0)
    file.writelines(content)
    file.close()


def worry_done():

    global path_var
    print("Number what worry\n")
    pos = input()
    tod = str(datetime.date.today())
    file = open(path_var + "\\" + tod + ".txt" ,"r+")
    content = file.readlines()
    target = content.pop(int(pos))
    file.seek(0,0)
    file.writelines(content)
    file.truncate()
    file.close()

    target = target.split(" ")
    temp_name = target[3]
    temp_name = temp_name[:len(temp_name)-1]
    obj = Item(temp_name)
    obj.setFreq(int(target[2]))
    obj.find_Idl()
    target = setNextDate(obj)
    change_line(target)


#*******************************************************************************



#First time using the programm
def createSystem():
    global path_var
    os.mkdir(path_var)


def lets_get_started():

    global path_var
    global name_txt
#Set the path correctly

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
        print("Any idea about the frequency? (y/n)\n")
        freq = 0
        inp = input()

        if inp == "y":
            print("Give me the moves\n")
            freq = input()
        else:
            pass

        obj = Item(name,int(y),int(m),int(d),freq)
        #it is sure that an Exception isn't going to be raised
        saveWorry(obj,path_var+name_txt)
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
        print("****\n1)Worry for today\n2)Add a worry\n3)Worry Done\n")
        inp = input()
        if inp == "1":
            add_days_worries()
        elif inp == "2":
            lets_get_started()
        elif inp == "3":
            worry_done()

if __name__ == "__main__":
    main()

import os
import datetime

#global vars
first_line = "Idl Last_Occur Fr Name\n"
Dir_name = "MWorries"
Txt_name = "\\Worries.txt"
one_time = "\\OneTimeWorry.txt"

path_var = __file__

class NoWorriesException(Exception):
    pass

class Item:
    name = ""
    last_occur = ""
    freq = ""
    id = ""

    def __init__(self,name ="",freq = 0,last_occur = ""):
        self.name = name
        self.last_occur = last_occur
        self.setFreq(freq)
        self.setId()


    def setFreq(self,freq = 0):
        freq = str(freq)
        if len(freq) == 1:
            freq = "0" + str(freq)
        else:
            freq = str(freq)
        self.freq = freq
    def getFreq(self):
        return self.freq

    def setId(self):
        self.id = str(len(self.name)%10)+"00"
    def ModifyId(self,id = ""):
        self.id = id
    def AddColission(self,id = ""):
        self.id = str(int(id)+1)
        if len(self.id) == 1:
            self.id = "00"+self.id
        else:
            pass
    def getId(self):
        return self.id

    def getLastOcc(self):
        return self.last_occur

    def getName(self):
        return self.name

    def getLine(self):
        return self.getId() + " " + self.getLastOcc() + " " + self.getFreq() + " " + self.getName() + "\n"


#Programm Interface

def SetUpPath():
    global path_var
    path_var = path_var.split("\\")
    path_var.pop(len(path_var)-1)
    temp_path = ""
    for word in path_var:
        temp_path+=word+"\\"
    path_var = temp_path
    return path_var

#1st time in the programm
def createDir():
    global path_var
    global Dir_name
    os.mkdir(path_var+Dir_name)
def createTxt():
    global path_var
    global Dir_name
    global Txt_name
    global first_line
    global one_time
    file = open(path_var+Dir_name+Txt_name,"w+")
    file.write(first_line)
    file.close()
    file = open(path_var+Dir_name+one_time,"w+")
    file.write(first_line)
    file.close()

#Basic For File Manipulation
def has_no_more(arr = [],i = 0):
    try:
        j = arr[i+1]
        return False
    except:
        return True
def saveWorry(obj = Item(),flag = False):
    global path_var
    global Dir_name
    global Txt_name
    global one_time
    file = ""

    if flag:
        file = open(path_var+Dir_name+one_time,"r+")
    else:
        file = open(path_var+Dir_name+Txt_name,"r+")

    content = file.readlines()
    if len(content) == 1:
        content.append(obj.getLine())
    else:
        for i in range(0,len(content)-1):
            temp_id = content[i+1].split(" ")
            temp_id = temp_id[0]
            obj_id = obj.getId()
            if int(obj_id[0]) < int(temp_id[0]):
                content.insert(i+1,obj.getLine())
                break
            elif int(obj_id[0])>int(temp_id[0]):
                if has_no_more(content,i+1):
                    content.append(obj.getLine())
                    break
                else:
                    gap = int(obj_id[1:])
                    i+=gap
            else:
                gap = obj_id[1:]
                if check_Colissions(obj,content[i+1:i+2+int(gap)]):
                    print("A Colission Has Occured Do You Want To Recalculate Frequency?(y/n)\n")
                    inp = input()
                    if inp == "Y" or inp == "y":
                        content[i+1] = Colission(obj,content[i+1])
                    else:
                        print("Item Cannot Be Saved\n")
                    break
                else:
                    obj.AddColission(temp_id)
                    content.insert(i+1,obj.getLine())
                    break

    file.seek(0,0)
    for line in content:
        file.write(line)
    file.close()

#update a worry in main file
def find_return_replace(obj = Item(),flag = False):
    global path_var
    global Dir_name
    global Txt_name
    global first_line

    file = open(path_var+Dir_name+Txt_name,"r+")
    content = file.readlines()
    content.pop(0)
    line = obj.getLine()
    line = line.split(" ")
    line = line[0]

    for i in range(0,len(content)):
        if line in content[i]:
            content[i] = obj.getLine()
            break
        elif int(line[0])>int(content[i][0]):
            i+=int(content[i][1:3])
        else:
            pass

    file.seek(0,0)
    content.insert(0,first_line)
    for item in content:
        file.write(item)
    file.close()

    if flag == True:
        return obj
    else:
        pass

def new_Worry():
    inp = ""
    dat = ""
    print("Name Your Worry\n")
    name = input()
    print("Any Frequency In Mind?(y/n)\n")
    inp = input()
    if inp == "Y" or inp == "y":
        print("Give Frequency\n")
        freq = input()
    else:
        freq = "0"
    while 1:
        print("When Is This Worry Going To Be Done?(yy/mm/dd)\n")
        inp = input()
        if len(inp) == 10 and len(freq) <=2:
            pass
        else:
            print("Input Is Not Correct\n")
        inp = inp.split("/")
        try:
            dat = str( datetime.date(int(inp[0]),int(inp[1]),int(inp[2]) ) )
            break
        except ValueError:
            print("Input Is Not Correct\n")

    obj = Item(name,int(freq),dat)

    if int( obj.getFreq() ) == 0:
        if ZFrequency(obj):
            saveWorry(obj,True)
        else:
            saveWorry(obj)
    else:
        saveWorry(obj)

#Create Item file
def It_file(obj = Item(),curr_freq = 0):
    global path_var
    global Dir_name
    if os.path.exists(path_var+Dir_name+"\\"+obj.getName()+".txt"):
        pass
    else:
        file = open(path_var+Dir_name+"\\"+obj.getName()+".txt","w+")
        file.write(curr_freq)
        file.close()
def saveFreq(obj = Item()):
    global path_var
    global Dir_name
    file = open(path_var+Dir_name+"\\"+obj.getName()+".txt","r+")
    freqs = file.readlines()
    if len(freqs) == 10:
        sum = 0
        for freq in freqs:
            sum += int(freq)
        sum = int(round(sum/10))
        file.seek(0,0)
        file.write(str(sum)+"\n")
        obj.setFreq(sum)
    else:
        file.seek(0,2)
        file.write("\n"+obj.getFreq()+"\n")
    file.close()
    return obj
#Colissions, returns new Line
def Colission(obj = Item(),line = ""):
    sp = line.split(" ")
    It_file(obj,sp[2])
    obj = saveFreq(obj)
    line = obj.getLine()
    return line
#returns True if a Colission has occured,else it returns False
def check_Colissions(obj = Item(),arr = []):
    if (len(arr) == 1) and (obj.getName() in arr[0]):
        return True
    elif len(arr) == 1:
        return False
    else:
        for item in arr:
            if obj.getName() in item:
                return True
            else:
                pass
        return False

#Check for Todays Worries
def createToday(tod_path = ""):
    global first_line
    file = open(tod_path,"w+")
    file.write(first_line)
    file.close()
#to Front
def calc_gap(line = ""):
    month_dir = [31,[28,29],31,30,31,30,31,31,30,31,30,31]
    dat = line.split(" ")
    dat = dat[1]
    year = int(dat[:4])
    month = int(dat[5:7])
    day = int(dat[8:])
    tod = str(datetime.date.today())
    if year == int(tod[:4]):
        if month == int(tod[5:7]):
            if day == int(tod[8:]):
                return 0
            else:
                return int(tod[8:])-day
        else:
            dgap = int(tod[8:])-day
            mgap = int(tod[5:7]) - month
            #to Back?
            if month > int(tod[5:7]):
                mgap = mgap *(-1)
            else:
                pass

            if mgap<0:
                mgap+=12
            else:
                pass
            for i in range(month,mgap+month):
                if i<=12:
                    dgap+=int(month_dir[i-1])
                else:
                    dgap+=int(month_dir[i-13])
            return dgap
#returns Boolean
def check_date(line = ""):
    temp_line = line.split(" ")
    gap = calc_gap(line)
    if gap == int(temp_line[2]):
        return True
    elif gap == 0:
        return True
    else:
        return False
#returns an array with todays lines
def return_TodWorries():
    global path_var
    global Dir_name
    global Txt_name
    global first_line
    file = open(path_var+Dir_name+Txt_name,"r+")
    content = file.readlines()
    file.close()
    if len(content) == 1:
        file.close()
        raise NoWorriesException
    else:
        today_array = []
        today_array.append(content.pop(0))
        for item in content:
            if check_date(item):
                today_array.append(item)
            else:
                pass
        return today_array
#if it doesnt exist it creates it
def check_Today():
    global path_var
    global Dir_name
    global Txt_name
    tod = str(datetime.date.today())
    if os.path.exists(path_var+Dir_name+"\\"+tod+".txt"):
        pass
    else:
        createToday(path_var+Dir_name+"\\"+tod+".txt")
#Is this Only For One Time?
def ZFrequency(obj = Item()):
    print("Frequency Is 0.Is This Worry For One Time Only?\n")
    inp = input()
    if inp == "Y" or inp == "y":
        saveWorry(obj,True)
        return True
    else:
        return False
#for today's file
def create_TodWorry():

    last_occur = str(datetime.date.today())

    print("Name Your Worry\n")
    name = input()

    print("Any Frequency In Mind?(y/n)\n")
    inp = input()

    if inp == "y" or inp == "Y":
        print("Give Frequency\n")
        fr = input()
        fr = int(fr)
    else:
        fr = 0

    obj = Item(name,fr,last_occur)

    if fr == 0:
        if ZFrequency(obj):
            saveWorry(obj,True)
        else:
            saveWorry(obj)
    else:
        saveWorry(obj)

def exc_funct():
    print("No Worries For Today\nDo You Have To Add Some?(y/n)\n")
    inp = input()
    if inp == "Y" or inp == "y":
        create_TodWorry()
        return True
    else:
        return False
#we need a try and a function to except
#returns True If today is formed correctly
def form_Today():
    global path_var
    global Dir_name

    try:
        tod = return_TodWorries()
    except:
        return exc_funct()
    else:
        todstr = str(datetime.date.today())
        file = open(path_var+Dir_name+"\\"+todstr+".txt","w+")
        for line in tod:
            file.write(line)
        file.close()
        return True
#print Today
def Print_Today():
    global path_var
    global Dir_name
    tod = str(datetime.date.today())
    file = open(path_var+Dir_name+"\\"+tod+".txt","r+")
    content = file.readlines()
    file.close()
    print("   "+content[0])
    for i in range(0,len(content)-1):
        print(str(i+1)+") "+content[i+1])
    content.pop(0)
    return content
#######################################################
#update the line and return an object about it
def get_Name(arr = []):
    name = ""
    for i in arr:
        name += i + " "

def Update_Worry(line = ""):
    month_dir = [31,[28,29],31,30,31,30,31,31,30,31,30,31]
    inf = line.split(" ")

    name = ""
    for item in inf[3:]:
        name += item + " "
    name = name[:len(name)-2]

    freq = inf[2]
    dat = inf[1]
    dat = dat.split("-")
    day = int(dat[2])+int(freq)
    month = int(dat[1])
    if int(month_dir[month-1])>=day:
        pass
    else:
        while day>int(month_dir[month-1]):
            month+=1
            day = day - month_dir[month-1] + 1
    dat = str( datetime.date( int(dat[0]) , month , int(day) ) )
    obj = Item(name,freq,dat)
    obj.ModifyId(inf[0])
    return obj

def Worry_Done(tod = []):
    global path_var
    global Dir_name
    global first_line

    if len(tod) == 0:
        print("You Have No Worries For Today\n")
    else:
        print("Number What Worry?\n")
        try:
            pos = int(input())
            fut = tod.pop(pos-1)
            #returns an obj updated
            fut = Update_Worry(fut)
            find_return_replace(fut)

        except ValueError:
            print("Not A Correct Input\n")

def Yes_Goes_Tod(items = []):
    tod = str(datetime.date.today())
    for item in items:
        item = item.split()
        item[1] = tod
        name = ""
        for word in item[3:]:
            name+=word+" "
        name = name[:len(name)-1]
        obj = Item(name,int(item[2]),tod)
        obj.ModifyId(item[0])
        find_return_replace(obj)

def Not_done_Worries():
    global path_var
    global Dir_name
    dat = str(datetime.date.today())
    dat = dat.split("-")
    dat[2] = int(dat[2])-1
    if dat[2] == 0:
        dat[1] = int(dat[1]) - 1
        if dat[1] == 0:
            dat[0] = int(dat[0])-1
            dat[1] = 12
        else:
            pass
        dat[2] = int(month_dir[ int(dat[1]) - 1] )
    else:
        pass
    dat = str( datetime.date( int(dat[0]), int(dat[1]), int(dat[2]) ) )
    try:
        file = open(path_var+Dir_name+"\\"+dat+".txt","r+")
        content = file.readlines()
        file.close()
        content.pop(0)
        if len(content) == 0:
            pass
        else:
            Yes_Goes_Tod(content)
        os.remove(path_var+Dir_name+"\\"+dat+".txt")
    except:
        pass


def main():
    global path_var
    global Dir_name
    path_var = SetUpPath()
    inp = ""
    tod = []

    if os.path.exists(path_var+Dir_name):
        pass
    else:
        createDir()
        createTxt()

    Not_done_Worries()

    while not(inp == "close" or inp == "Close"):

        check_Today()
        if form_Today():
            tod = Print_Today()
        else:
            continue


        print("****** Menu ******\n1)New Worry\n2)Worry For Today\n3)Worry Done\n")

        inp = input()
        if int(inp) == 1:
            new_Worry()
        elif int(inp) == 2:
            create_TodWorry()
        elif int(inp) == 3:
            Worry_Done(tod)

if __name__ == "__main__":
    main()

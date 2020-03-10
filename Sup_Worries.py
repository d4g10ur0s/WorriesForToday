import os
import datetime

class NoTodayException(Exception):
    pass
class ExitException(Exception):
    pass
class CollissionException(Exception):
    pass

class ZeroFrequencyException(Exception):
    pass

#global vars
path_var = __file__

dir_name1 = "Frequencies"
dir_name2 = "Dates"
txt_name = "\\Worries.txt"
first_line1 = "Idl Last_Occur Fr Name\n"
one_time = "\\OneTimeWorry.txt"
first_line3 = "Idl Last_Occur Name\n"
first_line2 = "Idl Flag"


class Item:
    name = ""
    id = ""
    last_occured = datetime.date.today()
    to_be_occured = datetime.date.today()
    freq = ""
    one_time = False

    def __init__(self,name = "it", last_occured = datetime.date.today(), freq = 1):
        self.name = name
        self.last_occured = last_occured
        self.setId()
        try:
            self.setFrq(freq)
        except ZeroFrequencyException:
            one_time = True

    def getName(self):
        return self.name
    def setName(self,name = ""):
        self.name = name

    def setOt(self):
        self.one_time = True
    def getOt(self):
        return self.one_time

    def setFrq(self,fr = 0):
        if fr == 0:
            raise ZeroFrequencyException
        else:
            fr = str(fr)
            if len(fr) == 1:
                self.freq = "0" + fr
            else:
                self.freq = fr
    def calc_freq(self):
        freq = int( self.last_occured.toordinal() ) - int( self.to_be_occured.toordinal() )
        if freq == 0:
            freq+=1
        self.setFrq(freq)
    def isOne(self):
        return only_one_time
    def retFreq(self):
        return self.freq

    def setId(self):
        self.id = str(len(self.name)%10)
        self.id = self.id + "00"
    def setIdManually(self,idl = ""):
        self.id = idl
    def getId(self):
        return self.id
    def getDigit(self):
        return self.id[0]
    def addGap(self,tim = 0):
        self.id = str(int(self.id)+tim+1)

    def set_to_be_occured(self):
        #need a dictionary for months
        month_dir = [31,31,30,31,30,31,31,30,31,30,31]
        d_gap = int(self.last_occured.day)+int(self.freq)
        month = int(self.last_occured.month)-1
        year = int(self.last_occured.year)
        #set Up month array
        if int(datetime.date.today().month) < month:
            if year % 100 == 0 or not(year%4==0) or not(year%400 == 0):
                month_dir.insert(1,28)
            else:
                month_dir.instert(1,29)
        else:
            if int(datetime.date.today().year) % 100 == 0 or not(int(datetime.date.today().year)%4==0) or not(int(datetime.date.today().year)%400 == 0):
                month_dir.insert(1,28)
            else:
                month_dir.insert(1,29)

        while d_gap > month_dir[month]:
            if month >= 12:
                month -= 12
                year += 1
            else:
                pass
            d_gap -= month_dir[month]
            month += 1

        self.to_be_occured = datetime.date(year,month+1,d_gap)
    def set_tboccured_manually(self,tbocc = datetime.date.today()):
        self.to_be_occured = tbocc
    def ret_to_be_occured(self):
        return self.to_be_occured

    def retDat(self):
        return self.last_occured
    def set_Dat_manually(self,dat = datetime.date.today()):
        self.dat = dat
    def return_line(self):
        return self.id +" "+ str(self.last_occured) +" "+ self.freq +" "+ self.name + "\n"
    def return_lin(self):
        return self.id + " " + "0"

#A function to create objects using CMD
def crt_obj_using_cmd(flag = 0):
    obj = ""
    #Set name
    while 1:
        try:
            print("Name your worry.\n")
            obj = Item(input())
            break
        except:
            print("Wrong Value For Name.\n")
            continue
    #Set frequency
    if flag == 0:
        while 1:
            print("Do you have any frequency in mind?\n(y/n)\n")
            fr = input()
            if fr == "y" or fr == "Y":
                print("Set frequency.\n")
                try:
                    obj.setFrq( int( input() ) )
                    obj.set_to_be_occured()
                    break
                except ZeroFrequencyException:
                    print("Can't have zero for frequency.\n")
                    continue
                except ValueError:
                    print("Incorrect value for frequency.\n")
                    continue
            else:
                flag = 1
                break
    #set to be occured
    if flag == 1 or flag == 2:
        while 1:
            print("When is this worry going to be occured?\n(yyyy-mm-dd)\n")
            dat = input().trim("-")
            try:
                obj.set_tboccured_manually(datetime.date(int(dat[0]) ,int(dat[1]) ,int(dat[2]) ) )
                if flag == 1:
                    #if flag == 2 is an onetime worry
                    obj.calc_freq()
                else :
                    pass
            except:
                print("Wrong values for date.\n")
                continue


    return obj

#A function to get next date in a line
def next_date(line = ""):
    freq = int(line[15:18])

    obj = Item()
    obj.setFrq(freq)
    obj.set_to_be_occured()
    obj.setIdManually(line[:3])
    obj.setName(line[19:])

    saveToDate(path,obj)

    return obj.return_line()


#Useful Functions
#path set up
def SetUpPath():
    global path_var
    path_var = path_var.split("\\")
    path_var.pop(len(path_var)-1)
    temp_path = ""
    for word in path_var:
        temp_path+=word+"\\"
    path_var = temp_path
    return path_var
def create_dir(path="" ,keyword = ""):
    os.mkdir(path+keyword)
def create_WorryFile(path = "",keyword="",first_line = ""):
    file = open(path+keyword,"w")
    file.write(first_line)
    file.close()
def Program_SetUp(temp_path = ""):
    global path_var
    global txt_name
    global first_line1
    global dir_name1
    global dir_name2
    global one_time

    create_dir(temp_path,dir_name1)
    create_dir(temp_path,dir_name2)
    create_WorryFile(temp_path,txt_name,first_line1)
    create_WorryFile(temp_path,one_time,first_line3)

#Update Previous Dates and Today File
#merge ,part of mergesort
def m_merge(arr1 = [],arr2 = []):
    if len(arr1) == 0:
        return arr2
    elif len(arr2) == 0:
        return arr1
    else:
        ret = []
        i = 0
        j = 0
        while len(arr1) > i and len(arr2) > j:
            if arr1[i] > arr2[j]:
                ret.append(arr1[i])
                i+=1
            else:
                ret.append(arr2[j])
                j+=1
        if i < len(arr1):
            ret+=arr2[j:]
        elif j<len(arr2):
            ret+=arr1[i:]
        else : pass
        return ret
#mergesort algorithm
def m_mergesort(arr = []):
    if len(arr) == 0 or len(arr) == 1:
        return arr
    elif len(arr)%2 == 0:
        return m_merge(m_mergesort(arr[: int(len(arr)/2) ]) ,m_mergesort(arr[ int(len(arr)/2) :] ) )
    else:
        return m_merge(m_mergesort(arr[: int( (len(arr)-1) /2) ] ) ,m_mergesort(arr[int( (len(arr)-1) /2) :] ))
#Return today content
def read_today(path = ""):
    file = open(path+"//"+str(datetime.date.today())+".txt","r+")
    fcontent = file.readlines()
    fcontent.pop(0)
    file.close()
    return fcontent
#update an old file and delete it
def update_file(path = ""):
    file = open(path,"r+")
    fcontent = file.readlines()
    #close File
    file.close()
    #pop 1st line
    fcontent.pop(0)
    for item in fcontent:
        temp = item.split(" ")
        #change date to today
        temp[1] = str(datetime.date.today())
        #update the whole line
        item = temp[0] + " " + temp[1] + " 1"
        #delete unecessary file
        os.remove(path)
    return fcontent
#General Function
def Return_Today(path = ""):
    today_array = []
    dates = os.listdir(path)
    for file in dates :
        if datetime.date(int(file[:4]),int(file[5:7]),int(file[8:10])).toordinal() <= datetime.date.today().toordinal():
            today_array += update_file(path+"\\"+file)
        else: pass
    #today_array += get_today(path)
    return m_mergesort(today_array)

#A helpful function to format a seeker
def format_Seeker(array = []):
    seeker = 0
    for i in array:
        seeker+=len(i)
    #It can't be 0 because 1st line is always in array
    return seeker-1
def recalculateFrequency(obj = Item()):
    global dir_name1
    path = SetUpPath()
    if os.path.exists(path+"\\"+dir_name1+"\\"+obj.getName()):
        file = open(path+"\\"+dir_name1+"\\"+obj.getName(),"r+")
        content = file.readlines()
        if len(content) == 9:
            sum = 0
            for num in content:
                sum+=num
            sum = round(sum/10)
            file.seek(0,0)
            file.write(sum+"\n")
            file.close()
            obj.setFrq(sum)
        else:
            file.seek(2,0)
            file.write(obj.retFreq()+"/n")
            file.close()
    else:
        file = open(path+"\\"+dir_name1+"\\"+obj.getName(),"w")
        file.write(obj.retFreq()+"/n")
        file.close()

    return obj

#CollisionMechanism
def CollissionMechanism(line = "",obj = Item()):
    print("A collision has occured\n"+ line + obj.return_line() +"\nDo you want to replace?\n(y/n)\n")
    while 1:
        inp = input()
        if inp == "Y" or inp == "y":
            print("Do you want to recalculate frequency?\n(y/n)\n")
            inp = input()
            while 1:
                if inp == "Y" or inp == "y":
                    obj = recalculateFrequency(obj)
                    return obj.return_line()
                elif inp == "N" or inp == "n":
                    obj.setIdManually(line[:3])
                    obj.setFrq(int(line[4:6]))
                    return obj.return_line()
                else:
                    pass
        elif inp == "N" or inp == "n":
            return -1
        else:
            pass
#Save_to_date
#Save a Worry
def saveWorry(path = "",obj = Item()):
    global txt_name
    global one_time

    file = None
    if obj.getOt():
        #if is one time worry open the appropriate file
        file = open(path+one_time,"r+")
    else:
        file = open(path+txt_name,"r+")

    content = file.readlines(2)

    #1st time in worry file...no worries exist
    try:
        next_line = content[1]
    except:
        file.seek(0,2)
        file.write(obj.return_line())
        file.close()
        saveToDate(path,obj)
        return

    indx = 0
    while 1:

        if next_line == "":
            file.write(obj.return_line())
            file.close()
            break
        elif next_line[0] == obj.getDigit():
            temp_content = file.readlines(int(next_line[1:3]))
            temp_content.insert(0,next_line)
            seeker = checkCollision(obj,temp_content)
            if seeker == 0:
                pass
            elif seeker == -1:
                print("Worry isn\'t going to be saved.\n")
                return None
            else:
                #if there is a collission
                temp_content[seeker] = CollisionMechanism(temp_content[seeker], obj)
                seeker = format_Seeker(content)
                temp_content+=file.readlines()
                file.seek(0,seeker)
                for i in range(0,len(temp_content)):
                    file.write(temp_content[i])
                file.close()
                break

            #NoCollissionHasOccured
            obj.addGap(int(next_line[1:3]))
            seeker = format_Seeker(content)
            temp_content.insert(0,obj.return_line())
            temp_content+=file.readlines()
            file.seek(seeker,0)
            for i in range(0,len(temp_content)):
                file.write(temp_content[i])
            file.close()
            break

        elif int(nextline[0])<int(obj.getDigit()):
            content.append(nextline)
            content+=file.readlines(int(next_line[1:3]))
            nextline = file.readline()

        else:
            seeker = format_Seeker(content)
            temp_content = f.readlines()
            temp_content.insert(0,obj.return_line())
            file.seek(seeker,0)
            for i in range(0,len(temp_content)):
                file.write(temp_content[i])
            file.close()
            break

        saveToDate(path,obj)

#if there are to no worries 4 today
def No_Worries_4_Today(path = ""):
    print("You have no worries for today\n")
    print("Do you want to add some?\n(y/n)\n")
    inp = input()
    if inp == "Y" or inp == "y":
        print("Is this worry for one time?\n(y/n)\n")
        while 1:
            inp = input()
            if inp == "y" or inp == "Y":
                saveWorry(path ,crt_obj_using_cmd(2))
                break
            elif inp == "n" or inp == "N":
                saveWorry(path ,crt_obj_using_cmd())
                break
            else:
                continue
    else:
        pass

#A worry is done
def worry_done(path = "",content = [],num = 0):
    global dir_name2

    paths = [path + txt_name, path + dir_name2 + "\\" + str(datetime.date.today()) + ".txt" ]
    entry = content.pop(num)
    entry = entry[:3]

    j = 0
    while j < 2:
        #1 update from worries txt
        #2 Delete from today file
        file = open(paths[j],"r+")
        txt_content = file.readlines()
        for i in range(1,len(txt_content)):
            if int(entry[0]) > int(txt_content[i][0]):
                gap = int(txt_content[i][1:3])
                i+=gap
            elif int(entry) == int(txt_content[i][:3]):
                seeker = format_Seeker(txt_content[:i])
                file.seek(seeker,0)
                if j == 0 :
                    txt_content[i] = next_date(txt_content[i])
                    txt_content = txt_content[i:]
                else:
                    txt_content = txt_content[i+1:]
                    for line in content :
                        file.write(line)
                        break
            else:
                pass

        file.close()
        j+=1

    return content

def main():
    global path_var
    global first_line1
    global txt_name
    global dir_name1
    global dir_name2
    global one_time

    #create temporary path
    path_var = SetUpPath()
    today_content = []

    while 1:
        if os.path.exists(path_var+txt_name):
            today_content = Return_Today(path_var+dir_name2)
        else:
            #1st time using the program
            Program_SetUp(path_var)

        if len(today_content) == 0:
            No_Worries_4_Today(path_var)
            continue
        else:
            i = 0
            for line in today_content:
                print(str(i)+") "+line)

            while 1:
                try:
                    print("*"*5+" Main Menu "+"*"*5+"\n1) Add worries.\n2) Worry done.\n3)Close.\n")
                    #Main Menu
                    inp = int(input())
                    #Add worries
                    if inp == 1:
                        print("Is this worry for one time?\n(y/n)\n")
                        inp = input()
                        while 1 :
                            obj = None
                            if inp == "Y" or inp == "y":
                                obj = crt_obj_using_cmd(2)
                                break
                            elif inp == "n" or inp == "N":
                                obj = crt_obj_using_cmd()
                                break
                            else:
                                continue
                        saveWorry(path_var,obj)
                    #A worry is done
                    elif inp == 2:
                        print("Number what worry?\n")
                        while 1:
                            try:
                                inp = int(input())
                                today_content = worry_done(path_var,today_content,inp)
                                break
                            except:
                                print("Wrong value.\nAre you sure you have a worry done?\n(y/n)\n")
                                inp = input()
                                if inp == "y" or inp == "Y":
                                    continue
                                else:
                                    print("No worries done!\n")
                                    break

                    else:
                        pass
                except:
                    print("Xazoulhs\n")
                    break

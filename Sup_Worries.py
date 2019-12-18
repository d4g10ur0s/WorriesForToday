import os
import datetime

class NoTodayException(Exception):
    pass
class ExitException(Exception):
    pass
class SaveException(Exception):
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
                month_dir.instert(1,29)

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
    if flag == 1:
        while 1:
            print("When is this worry going to be occured?\n(yyyy-mm-dd)\n")
            dat = input().trim("-")
            try:
                obj.set_tboccured_manually(datetime.date(int(dat[0]) ,int(dat[1]) ,int(dat[2]) ) )
                obj.calc_freq()
            except:
                print("Wrong values for date.\n")
                continue

    return obj
#checks if content[i+1] exists
def has_more(content = [], i = 0):
    try:
        exists = content[i]
        return True
    except:
        return False
#A function for ordering using id
def merge(content_1 = [],content_2 = []):
    i = 0
    j = 0
    to_ret = []

    try:
        while has_more(content_1,i) and has_more(content_2,j):
            #Implementation of merge
            if int(content_1[i][:3]) >= int(content_2[j][:3]):
                to_ret.append(content_2[j])
                j+=1

            else:
                to_ret.append(content_1[i])
                i+=1

        if has_more(content_1,i):
            to_ret+=content_1

        elif has_more(content_2,j):
            to_ret+=content_2
    except:
        #if there are only 2 strings
        if int(content_1[:3])>= int(content_2[:3]):
            to_ret.append(content_2)
            to_ret.append(content_1)
        else:
            to_ret.append(content_1)
            to_ret.append(content_2)
        return to_ret
#Using merge sort to sort ids...
def IdOrdering(content = []):
    size = len(content)
    if size == 0:
        return []
    elif size == 1:
        return content[0]
    else:
        if size%2==0:
            return merge(IdOrdering(content[:int(size/2)]), IdOrdering(content[int(size/2):]))
        else:
            return merge(IdOrdering(content[:int(size-1/2) ] ), IdOrdering(content[int(size-1/2):] ) )
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
#Format the seeker from where do i start writing
def format_Seeker(content = []):
    if len(content) == 0:
        return 0
    else:
        i = 0
        for line in content:
            i+=len(line)-1
        return i
#which date is earlier
def is_earlier(line = [],dat = datetime.date.today()):
    if int(line[0])<int(dat.year):
        return True
    else:
        if int(line[1])<int(dat.month):
            return True
        else:
            if int(line[2])<int(dat.day):
                return True
            else:
                return False
#returns new frequency
#is called after a collision has occured
#1->id,2->Last_Occur,3->frequency,4...->name
def days_lost(obj = Item(), line = ""):
    #need a dictionary for months
    month_dir = [31,[28,29],31,30,31,30,31,31,30,31,30,31]

    last_occur = line.split(" ")
    last_occur = last_occur[1]
    last_occur = last_occur.split("-")

    d_gap = 0
    if is_earlier(last_occur,obj.retDat()):
        y_gap = int(obj.retDat().year) - int(last_occur[0])
        m_gap = int(obj.retDat().month) - int(last_occur[1])
        d_gap = int(obj.retDat().day) - int(last_occur[2])
        for i in range(0,m_gap):
            month = int(last_occur[1])+i-1
            if month > 11:
                month -= 11
            else:
                pass
            d_gap += int(month_dir[month])
    else:
        d_gap = obj.retFreq()

    for i in range(0,y_gap):
        d_gap += 365

    return d_gap
#Check and handle collision
def checkCollision(obj = Item(),content = []):
    indx = 0
    for line in content:
        if obj.getName() in line:
            print("A Collission has occured on line:\n"+line+obj.return_line()+"Do You Want To Replace?(y/n)\n")
            inp = input()
            if inp == "y" or inp == "Y":
                obj.setFrq(days_lost(obj,line))
                obj.set_To_be_occured()
                obj.setId(line[:3])
                ret_tuple = (indx,obj)
                return ret_tuple
            else:
                return (-1)
        else:
            indx+=1
    return (0)
#Save the worrry to dates file
def saveToDate(path = "",obj = Item()):
    global dir_name2
    dat ="\\" + str(obj.ret_to_be_occured())+".txt"
    if os.path.exists(path+dir_name2+dat):
        file = open(path+dat,"r+")
        content = file.readlines(2)
        first_line = content.pop(0)
        if len(content) == 0:
            file.seek(len(first_line)-1)
            file.write(obj.return_lin())
            file.close()
        else:
            indx = 0
            next_line = content[0]
            while 1:
                if next_line[0] == obj.getDigit():
                    content.insert(indx,obj.return_lin())
                    break
                elif int(next_line[:3]) > int(obj.getId()):
                    content.insert(indx,obj.return_lin())
                    break
                else:
                    gap = int(next_line[0:3])
                    content = content + file.readlines(gap)
                    indx += gap+1
                    next_line = content[len(content)-1]
            temp_content = content[indx-1:] + file.readlines()
            content = content[:indx-1]
            seeker = format_Seeker(content)
            file.seek(seeker,0)
            for line in temp_content:
                file.write(line)
            file.close()
    else:
        file = open(path+dir_name2+dat,"w+")
        file.write("idl flag\n"+obj.return_lin())
        file.close()
#Save a Worry
#ret_tuple = (indx,content[indx],obj)
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
    first_line = content.pop(0)

    try:
        next_line = content[0]
        indx = 0
        while 1:

            if next_line[0] == obj.getDigit():
                gap = int(next_line[0:3])
                temp_content = file.readlines(gap)
                tup = checkCollision(obj,temp_content)
                if len(tup) == 1:
                    if int(tup[0]) == -1:
                        raise SaveException
                    else:
                        content.insert(indx,obj.return_line())
                        break
                else:
                    indx = int(tuple[0])
                    content[indx] = tuple[1].return_line()
                    break
            elif int(next_line[0])>int(obj.getDigit()):
                content.insert(indx,obj.return_line())
                break
            else:
                gap = int(next_line[0:3])
                content += file.readlines(gap+1)
                indx += gap+1
                next_line = content[indx]

            temp_content = content[indx-1:]+file.readlines()
            content = content[:indx-1]

            seeker = format_Seeker(content)
            seeker+=len(first_line)-1
            file.seek(seeker,0)

            for line in temp_content:
                file.write(line)
            file.close()

    except:
        file.write(obj.return_line())
        file.close()
    finally:
        if obj.getOt():
            pass
        else:
            saveToDate(path,obj)
def find_by_Idl(content = [],path = ""):
    global Txt_name
    file = open(path+Txt_name,"r+")
    temp_content = file.readlines(2)
    first_line = temp_content.pop(0)
    i = 0
    j = 0
    while 1:
        next_idl = content[i]
        next_line = temp_content[j]
        if next_line[:3] == next_idl:
            content[i] = next_line
            i+=1
            j+=1
            temp_content = temp_content+file.readlines(1)
            if has_more(content,i):
                pass
            else:
                break
        elif next_line[0] == next_idl[0]:
            j+=1
            temp_content = file.readlines(1)
        elif int(next_line[0])<int(next_idl[0]):
            gap = int(next_line[0:3])
            j+=gap+1
            temp_content = temp_content+file.readlines(gap+1)
        else:
            print("Malakeiaaaaa!!!!!!\n")
            break
    content.insert(0,first_line)
    return content
#handle_no_worries 4 today
def handle_no_worries(path = ""):
    print("You have no worries for today.\nDo you want to add some?(y/n)\n")
    inp = input()
    if inp == "y" or inp == "Y":
        return True
    else:
        return False
#return today when opening the program
def ReturnToday(path = "", content = []):
    file = open(path,"r+")
    rcontent = file.readlines()
    file.close()
    rcontent.pop(0)
    i = 0
    j = 0
    while has_more(content,i):
        if content[i][:3] == rcontent[j][:3]:
            content.pop(i)
            content.insert(i,rcontent.pop(j));
            i+=1
            j+=1
        elif content[i][0] == rcontent[j][0]:
            gap = int(rcontent[j][0:3])-int(content[i][0:3])
            content.pop(i)
            content.insert(i,rcontent.pop(j));
            i+=1
            j+=1
        elif int(content[i][0]) > int(rcontent[j][0]):
            gap = rcontent[j][0:3]
            j += int(gap) + 1
        else:
            pass
    return content
#print content in the correct format
def printContent(content = [], first_line = ""):
    print("***"+first_line)
    i = 0
    for item in content:
        print(i+") "+item)
        i+=1
#Create a New Worry
def newWorry(path = ""):
    global Dir_name
    global Txt_name
    global one_time
    print("1) One time Worry\n2) Regular Worry\n")
    inp = input()
    try :
        obj = createObjCMD(int(inp)-1)
        saveWorry(path,int(inp)-1)
    except ValueError:
        print("Incorrect Argument\nDo You Want To Create A New Worry?\n(y/n)\n")
        inp = input()
        if inp == "Y" or inp == "y":
            newWorry(path)
        else:
            pass

def updateFiles(path):
    global first_line2
    txts = os.listdir(path)
    content = []
    for file in txts:
        #Most complex line ever written...xD
        if datetime.date(int(file[:4]),int(file[5:7]),int(file[8:10])).toordinal() <= datetime.date.today().toordinal():
            seeker = open(path+"\\"+file,"r+")
            content = seeker.readlines()
            seeker.close()
            #pop first line
            content.pop(0)
            for item in content:
                item = item[:len(item)-1] + "1"
            if datetime.date(int(file[:4]),int(file[5:7]),int(file[8:10])).toordinal() == datetime.date.today().toordinal():
                pass
            else: os.remove(path+"\\"+file)
        else:
            pass
    #if len(content) == 0 there are not any old worries
    if len(content) == 0:
        return 0
    else:
        pass
    #write the updated worries
    try :
        file = open(path+"\\"+str(datetime.date.today())+".txt","r+")
        content = file.readlines() + content
        content.pop(0)
        content = IdOrdering(content)
        file.seek(0,0)
        content.insert(0,first_line2)
        for line in content:
            file.write(line)
        file.close()
    except:
        content = IdOrdering(content)
        file = open(path+"\\"+str(datetime.date.today())+"txt","w+")
        file.write(first_line2)
        for line in content:
            file.write(line)
        file.close()
    return content[0:]


def main():
    global path_var
    global first_line1
    global txt_name
    global dir_name1
    global dir_name2
    global one_time

    today_content = 0
    path_var = SetUpPath()

    if os.path.exists(path_var+txt_name):
        today_content = updateFiles(path_var+dir_name2)
    else:
        Program_SetUp(path_var)

    while 1:
        if today_content:
            today_content = ReturnToday(path_var+txt_name,today_content)
            printContent(today_content,first_line1)
            #4 onetime is missing
            while 1:
                try:
                    #Main Menu
                    print("*"*5+" Main Menu "+"*"*5+"\n1) Add worries.\n2) Worry done.\n3)Close.\n")
                    inp = int(input())
                    if inp == 1:
                        pass
                    elif inp == 2:
                        pass
                    else:
                        pass
                except:
                    print("Xazoulhs\n")
                    break
        #if today doesn't exist
        else:
            if handle_no_worries():
                while 1:
                    print("How many worries do you have?\n")
                    try:
                        inp = int(input())
                        for i in range(0, inp):
                            obj = ""
                            print("Is this worry for one time?\n(y/n)\n")
                            inp = input()
                            if inp == "y" or inp == "Y":
                                #if flag>1 -> OneTimeWorry
                                obj = crt_obj_using_cmd(2)
                            else:
                                obj = crt_obj_using_cmd()
                                obj.set_tboccured_manually(datetime.date.today())
                            try:
                                saveWorry(path_var,obj)
                            except:
                                print("Error on saving.\nTry again.\n")
                                i-=1
                                continue
                        break
                    except:
                        print("Incorrect value.\nYou must give an integer.\nTry Again.\n")
                        continue
            else:
                continue

#if __name__ == "__main__":
#    main()

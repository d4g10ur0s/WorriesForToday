import os
import datetime

class AllPastException(Exception):
    pass
class ObjectException(Exception):
    pass
#0123 56 89
#yyyy-mm-dd

#Basic String tb         lt
#012 4567 9a cd  f01 23 45 67 89ab..
#idl yyyy-mm-dd yyyy-mm-dd fr name...
################################################################################
#Global Variables
#directories
f_dir = 'Frequencies'
w_dir = 'Worries'
d_dir = 'Dates'
#files
o_file = 'OneTime.txt'
w_file = 'Worries.txt'
#first lines
# idl will_occur had_occured fr name
# idl

################################################################################
class Item:
    _name = ''
    _id = ''
    _tb = str(datetime.date.today())
    _lt = str(datetime.date.today())
    fr = 0

    def __init__(self, name):
        self._name = name
        self._id = str(len(name)%10)+"00"

    #manipulating id and name
    def set_name(self, name):
        self._name = name
        self._id = str(len(name)%10)+"00"
    def set_id(self,id):
        self._id=id
    def set_gap(self,gap = 0):
        self._id = gap+1
    def get_name(self):
        return self._name
    def get_id(self):
        return self._id

    #manipulating frequency
    def set_frequency(self, fr):
        self.fr = fr
    def calc_frequency(self):
        self.fr = self._lt.toordinal() - self._tb.toordinal()
    def get_frequency(self):
        return int(self.fr)

    #manipulating dates
    def convert_from_string(st = ""):
        return datetime.date(int(st[:4]), int(st[5:7]), int(st[8:]) )
    def set_tb(self,tb = datetime.date.today()):
        #returns True if lt<tb
        if tb.toordinal()>=self._lt.toordinal():
            self._tb = str(tb)
            return True
        else:
            return False
    def get_tb(self):
        return self._tb
    def set_lt(self,lt = datetime.date.today()):
        self._lt = str(lt)
    def get_lt(self):
        return self._lt
    def last_goes_next(self):
        self._lt=self._tb
    def next_date(self, on = False):
        #months with 31 days
        arr = [1,3,5,7,8,10,12]

        day = int(self._lt[8:]) + int(self.fr)
        month = int(self._lt[5:7])
        year = int(self._lt[:4])

        if (month in arr) and (day>31):
            day-=31
            month+=1

        elif month==2 and day>28:
            day-=28
            month+=1

        else:
            day-=30
            month+=1
            if month > 12:
                month = 1
                year+=1
            else:
                pass
        #set next date
        if on:
            pass
        else:
            self._lt = self._tb

        self._tb = str(datetime.date(year,month,day))

    #manipulating basic string
    def create_from_string(self,st = ""):
        try:
            #set dates
            self.set_lt(self.convert_from_string(st[14:23]))
            if self.set_tb(self.convert_from_string(st[4:13])):
                pass
            else:
                return False
            #set name and id
            self.set_name(st[27:])
            self.set_id(st[:3])
            #set frequency
            self.calc_frequency()
            #item constructed properly
            return True
        except:
            return False
    def return_basic_string(self):
        return self._id + " " + self._tb + " " + self._lt + " " + self.fr + " " + self._name +'\n'
################################################################################
#Input Data

#Date
def get_inp_date():
    inp = str(input())
    inp = datetime.date(int(inp[:4]), int(inp[5:7]), int(inp[8:]) )
    return inp
#String
def get_inp_str():
    return str(input())
#Int
def get_inp_int():
    return int(input())

#Construct a Today Item via CMD
def today_item():
    print("Give name.\n")
    return Item(get_inp_str())
#Construct Using Dates
def occured_today_but_done_date():
    i = 0
################################################################################
    print("Give name.\n")
    obj = Item(get_inp_str())
    while i < 3:
        try:
            print("When is it going to be occured?\n\n(Format : yyyy-mm-dd)\n")
            if obj.set_tb( get_inp_date() ):
                break
            else:
                i+=1
        except:
            i+=1
            continue
    if i == 3:
        #prepei na valw exception kai handling se hpshlotero epipedo
        pass
    else:
        obj.calc_frequency()
        return obj
#Happened Today and Have a Frequency
def occured_today_but_done_frequency():
    i=0
################################################################################
    print("Give name.\n")
    obj = Item(get_inp_str())
    while i<3:
        try:
            print("Give frequency.\n")
            obj.set_frequency(get_inp_int())
            break
        except:
            i+=1
            continue
    obj.next_date()
    return obj
#Happened in the past , set with date
def happened_past_date():
    i = 0
    kati = ["did","is going",""," to"]
################################################################################
    print("Give name.\n")
    obj = Item(get_inp_str())

    for j in range(0,2):
        while i<3:
            try:
                print("When "+ kati[j] +" it "+ kati[j+2] +" occur?\n\nFormat : yyyy-mm-dd\n")
                if j==0:
                    obj.set_lt(get_inp_date())
                else:
                    obj.set_tb(get_inp_date())
                i = 0
                break
            except:
                i+=1
                continue
            #8elw exception gia i == 3
    obj.calc_frequency()
    return obj
#Happened in the past , set with frequency
def happened_past_frequency():
    i = 0
################################################################################
    print("Give name.\n")
    obj = Item(get_inp_str)
    while i<3:
        try:
            print("When did it occur?\n\nFormat : yyyy-mm-dd\n")
            obj.set_lt(get_inp_date())
            i = 0
            break
        except:
            i+=1
            continue
        #8elw exception gia i = 3
    while i<3:
        try:
            print("Give frequency.\n")
            obj.set_frequency(get_inp_int())
            i = 0
            break
        except:
            i+=1
            continue
        #8elw exception gia i==3
    obj.next_date(True)
    #prepei na valw ena exception gia to ti ginetai ann ola einai palia...
    return obj

################################################################################
#File management
def set_up_path_var():
    path_var = __file__
    path_var = path_var.split('/')
    for i in range(0,len(path_var)-1):
        path_var+=path_var+'/'
#Set up environment
def set_up_environment(path_var = ""):
    global w_dir
    global w_file
    global o_file
    global f_dir
    global d_dir

    os.mkdir(path_var+w_dir)
    f = open(path_var+w_dir+"/"+w_file+'.txt',"w+")
    f.close()
    f = open(path_var+w_dir+"/"+o_file+'.txt',"w+")
    f.close()

    os.mkdir(path_var+f_dir)
    os.mkdir(path_var+d_dir)
################################################################################
def are_there_worries(path_var=""):
    if len(os.listdir())==0:
        return False
    else:
        return True
#sort items by id
def m_merge(arr1 = [], arr2 = []):
    temp_content = []

    if len(arr1) == 0:
        return arr2
    elif len(arr2) == 0:
        return arr1
    else:
        i = 0
        j = 0

        while not(i==len(arr1)) and not(j==len(arr2)):
            if int(arr1[i])>int(arr2[j]):
                temp_content.append(arr1[i])
                i+=1
            else:
                temp_content.append(arr2[j])
                j+=1

            if i == len(arr1):
                temp_content+=arr2[j:]
                return temp_content
            elif j == len(arr2):
                temp_content+=arr1[i:]
                return temp_content
            else:
                pass
def m_mergesort(arr = []):
    if len(arr) == 0 or len(arr) == 1:
        return arr
    elif len(arr)%2 == 0:
        return m_merge(m_mergesort(arr[:len(arr)/2]),m_mergesort(arr[len(arr)/2:]))
    else:
        return m_merge(m_mergesort(arr[:int( (len(arr)-1)/2 ) ]), m_mergesort(arr[int( (len(arr)-1)/2 ): ]))
#old worries are updated
def past_goes_now(path_var=""):
    files = os.listdir()
    obj = Item()
    content = []

    for file in files:
        if obj.convert_from_string(file[:10]).toordinal() <= datime.date.today():
            file = open(path_var+'/'+file,"r+")
            content += file.readlines()
            file.close()
            os.remove(file)
        else:
            pass
    content = m_mergesort(content)
    file = open(path_var+'/'+str(datetime.date.today())+'.txt','w+')
    for id in content:
        file.write(str(id)+'\n')
    file.close()
#save worries, must return the object formated
def save_worry(obj = Item(), path_var = ""):
    global w_dir
    global d_dir
    global w_file

    file = open(path_var+w_dir+'/'+w_file,"r+")
    content = file.readlines()
    indx = 0
    while 1:
            #skip whatever is greater
        if int(obj.get_id()[0])<int(content[indx][0]):
            indx+=int(content[indx][1:3])+1
        #test for colission
        #test for incrementation
        elif int(obj.get_id()[0])==int(content[indx][0]):
            temp_content = content[indx: int(content[indx][1:3])+indx+1]
            for item in temp_content:
                if obj.get_name() in item:
                    #there is a colission
                    file.close()
                    raise ObjectException
            obj.set_gap(int(content[indx][1:3]))
            break
        elif int(obj.get_id()[0]) > int(content[indx][0]):
            break
        else:
            print("ekanes malakeia")

        #have to insert the obj basic string in content
        content.insert(indx, obj.return_basic_string())
        #seeker
        seeker = 0
        for i in range(0,indx):
            seeker += len(content[indx])+1
        file.seek(seeker,0)
        #save things
        content = content[indx:]
        for item in content:
            file.write(item)
        file.close()
        return obj
#Save to date file
def save_to_date(obj = Item(), path_var = ""):
    if obj.get_tb()+".txt" in os.listdir(path_var):
        file = open(path_var+'/'+obj.get_tb()+".txt","r+")
        content = file.readlines()
        indx = 0
        while 1:
            if obj.get_id()[0] == content[indx][0]:
                break
            elif int(obj.get_id()[0]) > int(content[indx][0]):
                break
            else:
                indx += int(content[indx][1:3])+1
            #save things
        content.insert(indx,obj.get_id()+'\n')
        file.seek(indx*3,0)
        content = content[indx:]
        for item in content:
            file.write(item)
        file.close()
    else:
        file = open(path_var+'/'+obj.get_tb()+".txt","w+")
        file.write(obj.get_id()+"\n")
        file.close()
#my menus
def print_menu(ch = 0):
    if ch == 0:
        print(12*"*"+"\n"+"1)Worry Done\n"+"2)New Worry\n"+12*"*"+"\n")
    else:
        print(12*"*"+'\n'+"1)Today Worry\n"+"2)Occured Today but Done\n***(set by date)***\n"+"3)Occured Today but Done\n***(set by frequency)***\n"+"4)Happened in the past but will occur\n***(set by date)***\n"+"5)Happened in the past but will occur\n***(set by frequency)***\n")


#get today's worries
def get_today(path_var = ""):
    global d_dir
    global w_dir
    global w_file
    #read today
    file = open(path_var+d_dir+'/'+str(datetime.date.today())+'.txt',"r+")
    content = file.readlines()
    file.close()
    #find info in worries file
    indx = 0
    file = open(path_var+w_dir+'/'+w_file,"r+")
    while 1:
        #to exit loop...
        if indx == len(content) or indx == len(content)-1:
             break
        else:
            next_line = file.readline()
            if next_line[:3] == content[indx]:
                content[indx] = next_line
                indx+=1
            elif int(next_line[0]) == int(content[indx][0]):
                gap = int(next_line[1:3]) - int(content[indx][1:3])
                for i in range(0,gap):
                    file.readline()
            elif int(next_line[0])<int(content[indx][0]):
                gap = int(next_line[1:3])+1
                for i in range(0,gap):
                    file.readline()
    return content
#print today
def print_today(arr = []):
    print("* Id  Last Time  Next Time  Fr  Name        *\n")
    for i in range(0,len(arr)):
        print(str(i)+')'+str(arr[i])+'\n')
################################################################################
#main
def main():
    w_exists = True
    global w_dir
    global d_dir
    global w_file
    path_var = set_up_path_var()
    #First time in program?
    if os.path.exists(path_var+'/'+w_dir):
        pass
    else:
        set_up_environment(path_var)
    while 1:
        #Are there any worries?
        if are_there_worries(path_var+d_dir):
            today = get_today(path_var)
            print_today(today)
        else:
            print("There are no Worries saved.\n")
            w_exists = False

        if w_exists :
            print_menu()
        else:
            while 1:
                print("There are no Worries for today\nDo you want to add some?\n(y/n)\n")
                inp = str(input())
                if inp == 'y' or inp == 'Y':
                    print_menu(1)
                    try:
                        inp = int(input())
                        if inp == 1:
                            #today's item
                            obj = today_item()
                        elif inp ==2:
                            obj = occured_today_but_done_date()
                        elif inp ==3:
                            obj = occured_today_but_done_frequency()
                        elif inp ==4:
                            obj = happened_past_date()
                        elif inp ==5:
                            obj = happened_past_frequency()
                        save_worry(obj ,path_var+w_dir+'/'+w_file)
                        save_to_date(obj ,path_var+d_dir)
                        break
                        #
                        #afou anoiksa hdh arxeia kalo 8a htan na to apefeuga...
                        #
                    #Exceptions
                    except ObjectException:
                        pass
                        #ti 8a kaneis magka mou???
                        #
                        #
                        #
                elif inp == 'n' or inp == 'N':
                    break

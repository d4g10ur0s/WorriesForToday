import os
import datetime
#0123 56 89
#yyyy-mm-dd

#Basic String tb         lt
#012 4567 9a cd  f01 23 45 67 89ab..
#idl yyyy-mm-dd yyyy-mm-dd fr name...

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
    def set_lt(self,lt = datetime.date.today()):
        self._lt = str(lt)
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

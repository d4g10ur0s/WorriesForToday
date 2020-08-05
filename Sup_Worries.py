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
    def next_date(self):
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

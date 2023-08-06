import calendar
import datetime
import re
from rutimeparser import parse

months = {3: "Martius",
          4: "Aprilis",
          5: "Maius",
          6: "Iunius",
          7: "Iulius",
          8: "Augustus",
          9: "September",
          10: "October",
          11: "November",
          12: "December",
          1: "Ianuarius",
          2: "Februarius"}

num = {1: "I",
       2: "II",
       3: "III",
       4: "IIII",
       5: "V",
       6: "VI",
       7: "VII",
       8: "VIII",
       9: "IX",
       10: "X",
       11: "XI",
       12: "XII",
       13: "XIII",
       14: "XIIII",
       15: "XV",
       16: "XVI",
       17: "XVII",
       18: "XVIII",
       19: "XIX"}

def abl(month):
    if month.endswith('us'):
        return '{}is'.format(month[:-2])
    elif month.endswith('er'):
        return '{}ribus'.format(month[:-2]) 
    elif month == "Aprilis":
        return 'Aprilibus'
    
def acc(month):
    if month.endswith('us'):
        return '{}as'.format(month[:-2])
    elif month.endswith('er'):
        return '{}res'.format(month[:-2]) 
    elif month == "Aprilis":
        return 'Apriles'

class Converter(object):
    '''
    берет произвольную фразу на русском языке, ищет в ней дату и возвращает строку римской даты
    '''
    
    def conv(self, russian_string):
        processed_string = self.proc_rus_date(russian_string)
        roman_date = self.convert2roman(processed_string)
        return roman_date
        

    def proc_rus_date(self, s):
        
        if re.search("[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}", s): # костыль, чтобы rutimeparser понимал даты вида dd-mm-yyyy
            res = re.search("([0-9]{1,2})-([0-9]{1,2})-([0-9]{4})", s)
            s = "{}.{}.{}".format(res.group(1), res.group(2), res.group(3))
        
        if 'феврал' in s.lower() and re.search("\\b29\\b", s): # без этого костыля rutimeparser не понимает, что у февраля 29 дней
            if re.search("\\b[0-9]{4}\\b", s):
                year = int(re.search("\\b([0-9]{4})\\b", s).group(1))
            else:
                year = 2020
            d = datetime.date(year, 2, 29)
        else:
            d = parse(s, allowed_results=[datetime.date, None])
        
        
        if not d:
            return None
        
        if re.search("\\b[0-9]{4}\\b", s): # костыль, потому что rutimeparser внезапно (!) неправильно видит год 
            year = int(re.search("\\b([0-9]{4})\\b", s).group(1))
            if year != d.year:
                d = datetime.date(year, d.month, d.day)
        else:
            now = datetime.datetime.now()
            if now.year != d.year:
                d = datetime.date(now.year, d.month, d.day)
        return d
    
    def convert2roman(self, d):
        
        if not d:
            return "Kalendis Graecis"
    
        if d.month in [3, 5, 7, 10]:
            idus = 15
            nonae = 7
        else:
            idus = 13
            nonae = 5
        
        if d == datetime.date(d.year, d.month, 1):
            date_string = "Kalendis {}".format(abl(months[d.month])) 
        
        elif datetime.date(d.year, d.month, 1) < d < datetime.date(d.year, d.month, nonae):
            before = datetime.date(d.year, d.month, nonae) - d
            days_before = before.days
            if days_before == 1:
                date_string = "pridie Nonas {}".format(acc(months[d.month]))
            else:
                date_string = "ante diem {} Nonas {}".format(num[days_before+1], acc(months[d.month]))
        
        elif d == datetime.date(d.year, d.month, nonae):
            date_string = "Nonis {}".format(abl(months[d.month])) 
            
        elif datetime.date(d.year, d.month, nonae) < d < datetime.date(d.year, d.month, idus):
            before = datetime.date(d.year, d.month, idus) - d
            days_before = before.days
            if days_before == 1:
                date_string = "pridie Idus {}".format(acc(months[d.month]))
            else:
                date_string = "ante diem {} Idus {}".format(num[days_before+1], acc(months[d.month]))
        
        elif d == datetime.date(d.year, d.month, idus):
            date_string = "Idibus {}".format(abl(months[d.month])) 
            
        elif datetime.date(d.year, d.month, idus) < d:
            last_day = calendar.monthrange(d.year, d.month)[1]
            if d.day == last_day and d.month != 12:
                date_string = "pridie Kalendas {}".format(acc(months[d.month+1]))
            elif d.day == 31 and d.month == 12:
                date_string = "pridie Kalendas {}".format(acc(months[1]))
            else:
                before = datetime.date(d.year, d.month, last_day) - d
                if d.month == 2 and last_day == 29 and d.day < 26:
                    if d.day < 25:
                        days_before = before.days + 1
                    elif d.day == 25:
                        days_before = 6
                else:
                    days_before = before.days + 2
                if d.month ==  12:
                    next_month = 1
                else:
                    next_month = d.month + 1
                date_string = "ante diem {} Kalendas {}".format(num[days_before], acc(months[next_month]))
        else:
            date_string = "Kalendis Graecis"
        return date_string


if __name__ == '__main__':
    import sys
    rus = ' '.join(sys.argv[1:])
    c = Converter()
    print(c.conv(rus))

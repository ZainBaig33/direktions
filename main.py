import numpy as np
import pandas as pd
import datetime as datetime
from pandas import read_csv
import json
import time
import pdfkit


AABS = 'AABS.csv'
abbs_report = 'AABS_report.csv'
ABL = 'ABL.csv'
abl_report = 'ABL_report.csv'
ABOT ='ABOT.csv'
abot_report ='ABOT_report.csv'
AGTL ='AGTL.csv'
agtl_report ='AGTL_report.csv'
ENGRO ='ENGRO.csv'
engro_report ='ENGRO_report.csv'


name = [AABS,ABL,ABOT,AGTL,ENGRO]
rep = [abbs_report,abl_report,abot_report,agtl_report,engro_report]


buy_date = []
sell_date = []
s_date = []

lastdate = input('last working date: ')
InputDate = datetime.datetime.strptime(lastdate, '%d-%m-%Y')

def month_string_to_number(string):
    m = {
         'jan':"01",
        'feb':"02",
        'mar':"03",
        'apr':"04",
         'may':"05",
         'jun':"06",
         'jul':"07",
         'aug':"08",
         'sep':"09",
         'oct':"10",
         'nov':"11",
         'dec':"12"
    }
    s = string.lower()

    out = m[s]
    return out
def month_number_to_string(string):
    m = {
         '01':"Jan",
        '02':"Feb",
        '03':"Mar",
        '04':"Apr",
         '05':"May",
         '06':"Jun",
         '07':"Jul",
         '08':"Aug",
         '09':"Sep",
         '10':"Oct",
         '11':"Nov",
         '12':"Dec"
    }
    s = string.lower()

    out = m[s]
    return out

def Signal_rate_date(repo):
    for i in repo['Buy Date']:
        convert_str = str(i)
        month = convert_str[3:6]
        month_num = month_string_to_number(month)
        con_mon_num = str(month_num)
        date = i.split('-')[0]
        year = i.split('-')[2]
        buy_date.append(date + "-" + con_mon_num + "-20" + year)

    for i in repo['Sell Date']:
        convert_str = str(i)
        month = convert_str[3:6]
        month_num = month_string_to_number(month)
        con_mon_num = str(month_num)
        date = i.split('-')[0]
        year = i.split('-')[2]
        sell_date.append(date + "-" + con_mon_num + "-20" + year)

    InputDate = datetime.datetime.strptime(lastdate, '%d-%m-%Y')

    l = [InputDate - datetime.datetime.strptime(i, '%d-%m-%Y') for i in buy_date]
    x = buy_date[l.index(min(i for i in l if i > datetime.timedelta(0)))]

    m = [InputDate - datetime.datetime.strptime(i, '%d-%m-%Y') for i in sell_date]
    y = sell_date[m.index(min(i for i in m if i > datetime.timedelta(0)))]

    if (x < y):
        last_signal_date = x
        today_signal = 'Buy'
    else:
        last_signal_date = y
        today_signal = 'Sell'

    if (today_signal == 'Buy'):
        for i in buy_date:
            if (i == last_signal_date):
                index_val = buy_date.index(i)
                last_signal_rate = repo._get_value(index_val, 'Buy Price')

    elif (today_signal == 'Sell'):
        for j in sell_date:
            if (j == last_signal_date):
                index_val = sell_date.index(j)
                last_signal_rate = repo._get_value(index_val, 'Sell Price')

    buy_date.clear()
    sell_date.clear()
    return last_signal_date,last_signal_rate


def closing_rates(data):


    for i in data['Date']:
        conv_str = str(i)
        month = conv_str[3:6]
        month_num = month_string_to_number(month)
        con_mon_num = str(month_num)
        date = i.split('-')[0]
        year = i.split('-')[2]
        s_date.append(date + "-" + con_mon_num + "-" + year)

    n = [InputDate - datetime.datetime.strptime(i, '%d-%m-%Y') for i in s_date]
    z = s_date[n.index(min(i for i in n if i > datetime.timedelta(0)))]

    for k in s_date:
        if (k == z):
            index_no = s_date.index(k)
            closing_rate = data._get_value(index_no, 'Close')
            high_rate = data._get_value(index_no, 'High')
            low_rate = data._get_value(index_no, 'Low')

    s_date.clear()
    return closing_rate,high_rate,low_rate


def related_data(closing_rate,high_rate,low_rate):

    pivot_point = (high_rate + low_rate + closing_rate) / 3
    first_res = (2 * pivot_point) - low_rate
    first_supt = (2 * pivot_point) - high_rate
    second_res = pivot_point + (high_rate - low_rate)
    second_supt = pivot_point - (high_rate - low_rate)
    third_res = high_rate + 2 * (pivot_point - low_rate)
    third_supt = low_rate - 2 * (high_rate - pivot_point)

    return pivot_point,first_res,first_supt,second_res,second_supt,third_res,third_supt


def Last_satus(file):
    AA=[]
    si_date=[]
    with open(file) as f:
        lines = f.readlines()
        A = list(line.split() for line in lines)
        flat_list = [item for sublist in A for item in sublist]
        new_list = [s.replace("]", "") for s in flat_list]
        new_1list = [s.replace("[", "") for s in new_list]
        new_2list = [s.replace("(", "") for s in new_1list]
        new_3list = [s.replace(")", "") for s in new_2list]
        new_4list = [s.replace(",", "") for s in new_3list]
        new_5list = [s.replace("'", "") for s in new_4list]
        for i in range(0, len(new_5list), 2):
            AA.append(new_5list[i])
        for i in AA:
            month = i[3:6]
            month_num1 = month_string_to_number(month)
            con_mon_num = str(month_num1)
            date = i.split('-')[0]
            year = i.split('-')[2]
            si_date.append(date + "-" + con_mon_num + "-" + year)

        n = [InputDate - datetime.datetime.strptime(i, '%d-%m-%Y') for i in si_date]
        z = si_date[n.index(min(i for i in n if i > datetime.timedelta(0)))]
        zz = str(z)
        dat = zz[3:5]
        con_dat = month_number_to_string(dat)
        date = zz.split('-')[0]
        year = zz.split('-')[2]
        s = (date + "-" + con_dat + "-" + year)
        ss = str(s)
        index = new_5list.index(ss)
        Z = new_5list[index + 1]

        AA.clear()
        si_date.clear()

        return Z


Singnal_file=['AABS_Signals.txt','ABL_Signals.txt','ABOT_Signals.txt','AGTL_Signals.txt','ENGRO_Signals.txt']
Symbol = ['AABS','ABL','ABOT','AGTL','ENGRO']


last_signal = []
last_status = []
last_rate =[]
clossig_value = []
high_value = []
low_value = []
pp = []
R1 = []
S1 = []
R2 = []
S2 = []
R3 = []
S3 = []


for i in rep:
    repo_data = read_csv(i)
    o,e= Signal_rate_date(repo_data)
    last_signal.append(o)
    last_rate.append(e)

for i in name:
    data = read_csv(i)
    a,b,c = closing_rates(data)
    clossig_value.append(a)
    high_value.append(b)
    low_value.append(c)


for i in range(5):
    a,b,c,d,e,f,g = related_data(clossig_value[i],high_value[i],low_value[i])
    k = Last_satus(Singnal_file[i])
    last_status.append(k)
    pp.append(round(a,3))
    R1.append(round(b,3))
    S1.append(round(c,3))
    R2.append(round(d,3))
    S2.append(round(e,3))
    R3.append(round(f,3))
    S3.append(round(g,3))

np.savetxt(lastdate+' Daily_Trading_Signal.csv', np.c_[Symbol,last_signal,last_rate,clossig_value,pp,S1,S2,S3,R1,R2,R3,last_status], delimiter=',', header = 'Name,Last Signal Date,Last Signal Rate,Closing Rate,Pivot Point,Support 1,Support 2,Support 3,Resistance 1,Resistance 2,Resistance 3,Todays Signal', comments = '',fmt='%10s')

CSV = pd.read_csv(lastdate+' Daily_Trading_Signal.csv')
CSV.to_html('MYCSV.html')

# INSTALL wkhtmltopdf AND SET PATH IN CONFIGURATION
# These two Steps could be eliminated By Installing wkhtmltopdf -
# - and setting it's path to Environment Variables
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

pdfkit.from_file('MYCSV.html', 'Daily_Trading_Signal.pdf', configuration=config)
import pandas as pd
import numpy as np
import math

def convert_excel_timetable2_c_header(
            input_excel_timetable):
    name,weeks = extract_excel_data(input_excel_timetable)
    return data_to_header(name, weeks)

def extract_excel_data(input_excel_timetable):
    data = pd.read_excel(input_excel_timetable, engine="openpyxl")
    name = data.columns[0]
    data.fillna('', inplace=True)
    numberOfWeeksFilled = int(len(list(filter(lambda x: x != '', data.values[0]))))
    weeks = []
    for week in range(numberOfWeeksFilled):
        compressColumnCondition = np.full(numberOfWeeksFilled*2, False)
        compressColumnCondition[week*2] = True
        a1 = np.compress(compressColumnCondition, data.values, axis=1)
        compressColumnCondition[week*2] = False
        compressColumnCondition[week*2+1] = True
        a2 = np.compress(compressColumnCondition, data.values, axis=1)
        weekName = a1[0][0]
        a1 = np.delete(a1,0,0)
        a2 = np.delete(a2,0,0)
        first = True
        gaps = []
        for hour in zip(a1,a2):
            hour = np.array(hour)
            hour = hour.flatten()
            if first:
                startTime = hour[0]
                first = False
                continue
            elif hour[0] == '':
                break
            elif hour[1] == '':
                endTime = hour[0]
            else:
                gaps.append((hour[0],hour[1]))
        weeks.append((weekName, startTime, endTime, gaps))

    return (name, weeks)


def data_to_header(name, weeks):
    nameUppercase = name.upper()
    text = """#ifndef APPS_AGENDA_"""+nameUppercase+"""_DEF_H
#define APPS_AGENDA_"""+nameUppercase+"""_DEF_H

#include "agenda_types.h"

const AgendaDef agenda_"""+name.lower()+""" =
{
    .name = \""""+name+"""",
    .days = {
"""+",\n".join([week_to_header(w) for w in weeks])+"""
    }
};

#endif //APPS_AGENDA_"""+nameUppercase+"""_DEF_H"""
    return text

def str_to_header_time(str):
    tab = str.split('h')
    return "{"+tab[0]+","+tab[1]+"}"

def week_to_header(week):
    text = """    // """+week[0]+"""
    {
        """+str_to_header_time(week[1])+""", // Start Time
        """+str(len(week[3]))+""", // gapsCount
        {
"""+",\n".join([gap_to_header(g) for g in week[3]])+"""
        },
        """+str_to_header_time(week[2])+""" // End Time
    }"""
    return text

def gap_to_header(gap):
    text = """            {"""+str_to_header_time(gap[0])+""",
             """+str_to_header_time(gap[1])+"""}"""
    return text

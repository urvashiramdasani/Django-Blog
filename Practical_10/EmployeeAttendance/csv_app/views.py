from django.shortcuts import render
import pandas as pd

# Create your views here.

def home(request):
    if request.POST:
        file = request.FILES['file_input']
        if not '.csv' in str(file):
            return render(request,'index.html',{'error':"File not valid!"})
        data = pd.read_csv(file)
        Row_list = []
        for index, rows in data.iterrows():
            present = "".join(list(rows.values)[2:]).count('P')
            absent = "".join(list(rows.values)[2:]).count('A')
            total = len("".join(list(rows.values)[2:]))
            percentage = present*100/total
            my_list = {'eid': rows['Employee ID'], 'TotalDays': total, 'present': present,
                       'absent': absent, 'percentage': percentage}

            for days_key in rows.keys():
                if 'day' in days_key:
                    my_list[days_key] = rows[days_key]

            Row_list.append(my_list)

        return render(request,'index.html',{'data':Row_list})
    return render(request,'index.html')

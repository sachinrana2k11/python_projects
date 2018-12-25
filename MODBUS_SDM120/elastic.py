data = []
form ={"Volts": 231, "Current": 3, "Active_Power": 138, "Apparent_Power": 236, "Reactive_Power": 283, "Power_Factor": 1, "Phase_Angle": 174, "Frequency": 55, "Import_Active_Energy": 130, "Export_Active_Energy": 177, "Import_Reactive_Energy": 179, "Export_Reactive_Energy": 141, "Total_Active_Energy": 137, "Total_Reactive_Energy": 242}
for i in form:
    raw_form = {"meter": '1234',"name": i,"value": form[i],"timestamp": '456'}
    data.append(raw_form)
print(data)
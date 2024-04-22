# Given data
OB = {'Dose': '11 mmol', 'Dose2': '11 mmol'}
OB2 = {'Dose': '11 mmol', 'Dose2': '11 mmol'}
OB3 = {'Dose': 'true', 'Dose2': 'false'}
 

# Iterate over the enumerated keys of the dictionary
for index, key in enumerate(OB):
    keys_list = list(OB.keys())
    print(f"| {keys_list[index]} {' ' * 10}| {OB[key]} {' ' * 10}| {OB[key]} {' ' * 10}|{OB3[key]}  0 ")
   

    

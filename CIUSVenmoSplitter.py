import csv
from hashlib import new
import re
import pandas as pd
# path = "/Users/srijithvenkat/Desktop/Projects/"
file_name = "venmo_statement.csv"
data = pd.read_csv(file_name, skiprows=2)
# print(data.columns)
actual_data = data[1:-1]
ids = actual_data['ID']
names = actual_data['From']
descriptions = actual_data['Note']
payments = actual_data['Amount (total)']
new_data = list(zip(ids,names,descriptions,payments))

new_header = ["Name","Description","Quantity","Price"]


seen = {}
created_file_count = 0
while True:
    event_key = input("Enter Event Search Key: ")
    payment_keys = input("Enter Event Payment Required: ").split(",")

    curr_event = []
    total_tickets = 0
    total_revenue = 0

    for row in new_data:
        if row[0] not in seen:
            if '+' in row[3]:
                if event_key.lower() in row[2].lower():
                    paid_amount = float(re.findall('\d*\.?\d+',row[3])[0])
                    for pay_key in payment_keys:
                        if paid_amount% float(pay_key) == 0:
                            row_data = [row[1],row[2],paid_amount//float(pay_key), paid_amount]
                            total_tickets += paid_amount//float(pay_key)
                            total_revenue += paid_amount
                            curr_event.append(row_data)
                            seen[row[0]] = 0
                            
    curr_event.append(['','',total_tickets,total_revenue])

    with open(event_key+'.csv', 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(new_header) 
        
        # writing the data rows 
        csvwriter.writerows(curr_event)
    
    csvfile.close()
    created_file_count += 1

    quit = input("Do you want to Quit?: ")
    if(quit.lower() == "q"):
        break


irregulars = []

for row in new_data:
    if row[0] not in seen:
        paid_amount = float(re.findall('\d*\.?\d+',row[3])[0])
        for pay_key in payment_keys:
            if paid_amount% float(pay_key) == 0:
                row_data = [row[1],row[2],paid_amount//float(pay_key), paid_amount]
                irregulars.append(row_data)

with open('irregulars.csv', 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(new_header) 
    
    # writing the data rows 
    csvwriter.writerows(irregulars)
        
print("Created {} files successfully.".format(created_file_count))











import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv
import os
from requests_file import FileAdapter


def get_table_data():
    s = requests.Session()
    s.mount('file://', FileAdapter())
    # response = requests.get('https://hcraj.nic.in/displayboard/jaipur.php')

    response = s.get('file:///C:/Users/1383l/OneDrive/Desktop/Rajasthan%20High%20Court%201.html')
    # print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table')  # Adjust class name accordingly
        if table:
            data = []
            
            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                court_number = columns[0].text.strip()
                item_number = columns[1].text.strip()
                court_number_id = get_courtNumberId(court_number)
                data.append((timestamp,court_number_id, item_number))
            # all_table_data.append(data)
            return data
        else:
            print("Table not found on the page.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


def get_courtNumberId(scrapped_court_number):
    scrapped_court_number_id = None
    

    if os.path.exists('court_number_table.csv'):
        with open('court_number_table.csv','r' , newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            print('@@')
            for row in reader:
                if  row['court_number'] == scrapped_court_number:
                    print(".....")
                    scrapped_court_number_id = row['court_number_id']
                    return scrapped_court_number_id
                
    if not os.path.exists('court_number_table.csv'):  
        get_court_numer_header()

    if scrapped_court_number_id is None:
        with open('court_number_table.csv','a', newline='') as csvFile:
            writer = csv.writer(csvFile)

            # Generate a new court_number_id (you might want to use a better strategy)
            new_court_number_id = len(open('court_number_table.csv').readlines())
            
            # Write the new court_number and court_number_id to the CSV file
            print(new_court_number_id,"and",scrapped_court_number,"added in court_number_table file...")
            writer.writerow([ new_court_number_id, scrapped_court_number])
            scrapped_court_number_id = new_court_number_id
            return scrapped_court_number_id
        
def get_court_numer_header():
    with open('court_number_table.csv','a', newline='') as csvFile:   
            fieldnames = ['court_number_id', 'court_number']
            writer = csv.DictWriter(csvFile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()


def time_series_table_header(file_path='time_series_data.csv'):
    with open(file_path, 'a', newline='') as file:
        fieldnames = ['Timestamp', 'court_number_id', 'item_number']
        csv_writer = csv.DictWriter(file , delimiter=',', fieldnames=fieldnames)
        csv_writer.writeheader()

def save_data_to_csv(data, file_path='time_series_data.csv'):
    with open(file_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        for timestamp, court_number_id, item_number in data:
            csv_writer.writerow([timestamp, court_number_id,item_number])

if __name__ == "__main__":
    url = "https://hcraj.nic.in/displayboard/jaipur.php"
    start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,10,30,0)
    end_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 16, 30, 0)  # 4:30 PM

    # if datetime.now() > end_time or datetime.now() < start_time:
    #     print("You are out of Court Working Hours. Start the script between 10:30AM to 4:30PM...")
    if not os.path.exists('time_series_data.csv'):
       time_series_table_header()
    while True : #datetime.now() <= end_time and datetime.now() >= start_time:
        table_data = get_table_data()
        if table_data:
            save_data_to_csv(table_data)
            print("Data saved to CSV.")
        else:
            print("No data extracted. Feel Today is Holiday...")
        time.sleep(10)  # Sleep for 10 seconds before the next iteration
# print(get_table_data())
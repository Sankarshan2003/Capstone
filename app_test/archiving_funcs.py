import csv
from dotenv import load_dotenv
import pandas as pd
import mysql.connector
import os
def connect_to_db():
    load_dotenv()
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connection
def disconnect_from_db(connection):
    connection.close()
def search_db(connection,barcodeID):
    cursor = connection.cursor()
    query = "SELECT department FROM reg_tt_dataset where tt_id = %s"
    try:
        res=cursor.fetchall()
    except Exception as e:
        print(e)
    try:
        cursor.execute(query,(barcodeID,))
        res=cursor.fetchall()
        if not res:
            res = '0'
            return res
        else:
            return res
    except Exception as e:
        print(e)
    return res



def search_csv_by_tt_id(csv_filename, keyword):
    print("search csvvvv")
    csv_filename = r'C:\Users\sanka\OneDrive\Desktop\capstone\gantry-pick-place\python_scripts\reg_tt_dataset.csv'
    try:
        with open(csv_filename, 'r', encoding='utf-8-sig') as file:
            # print(file)
            csv_reader = csv.DictReader(file)
            print(csv_reader)
            # while not row['tt_id'] == keyword:
            for row in csv_reader:
                # print(keyword)
                # print(row)
                # print(row['tt_id'] == keyword)
                if row['tt_id'] == keyword:
                    # if row['isCompleted']:
                    print("Search from CSV")
                    print(row['first_name'])
                    return row['department']
                    # else:
                        # return '0'

                #     # from main import update_patient_detss
                #     # update_patient_dets('NA','NA','NA','NA','Vacuum Tube Barcode Not Valid')
                    # print("Search from CSVbad is")
            return '0'
    except:
        print("Error")
        
        
def	get_emp_slot(pallet_tray):
    
    for row_idx, row in enumerate(pallet_tray):
        if 0 in row:
            col_idx = row.index(0)
            pallet_tray[row_idx][col_idx] = 1
            return [row_idx, col_idx]
        
        
        
def tray_id_to_xy(pallet_tray,row,column,type):#takes the coord array and pos array
    dist_x = 20.5
    dist_y = 20.5

    if type=="source":
        x_coord = pallet_tray[0] + (row*dist_x)
        y_coord = pallet_tray[1] - (column*dist_y)
        
    elif type=="dest":
        x_coord = pallet_tray[0] + (row*dist_x)
        y_coord = pallet_tray[1] - (column*dist_y)

    # print(x_coord, y_coord)
    return x_coord,y_coord
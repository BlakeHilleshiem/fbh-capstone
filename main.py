import csv

import os

from time import sleep

from functions import *

import sqlite3
connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

def format_to_table(lst_of_tuple_query_results):
    tuple_query_results = lst_of_tuple_query_results
    header = []
    column_sizes = []

    names = list(map(lambda x: x[0], cursor.description))
    for i in names:
        header.append(str(i).replace('_',' ').title())

    for i in range(len(names)):
        count = 1
        max_col_len = 0
        for column in tuple_query_results: 
            if max_col_len < len(str(column[i])):
                max_col_len = len(str(column[i]))

            if count == len(tuple_query_results):
                column_sizes.append(max_col_len)

            count += 1

    for i in range(len(names)):
        if column_sizes[i] < len(str(header[i])):
            print(f' {header[i]:{len(str(header[i])) + 2}}', end = '')
        else:
            print(f' {header[i]:{column_sizes[i] + 2}}', end = '')
    print()

    for i in range(len(names)):
        if column_sizes[i] < len(str(header[i])):
            print('','-' * (len(str(header[i])) + 2), end = '')
        else:
            print('','-' * (column_sizes[i] + 2), end = '')

    for e in tuple_query_results:
        print()
        for i in range(len(names)):
            if column_sizes[i] < len(str(header[i])):
                print(f' {str(e[i]):{len(str(header[i])) + 2}}', end = '')
            else:
                print(f' {str(e[i]):{column_sizes[i] + 2}}', end = '')
    print()
    print()



# --- verify user -----------------------

os.system('clear')
print('''=======================
  Competency Tracker:  
=======================''')


user_check = verify_user()
# try:
while True:
    if user_check[0] == 'manager':
        os.system('clear')
        print('======= Welcome =======\n')
        while True:

            print('''What would you like to do?

 (1)  View all users
 (2)  Search user by name or user id
 (3)  View the Competency Results Summary for all users
 (4)  View a user's competency level report
 (5)  View a user's list of assessments
 (6)  Add to the database
 (7)  Edit the database
 (8)  Delete assessment result
 (9)  Generate CSV files to Export
 (10) Import assesment results from a CSV file

 <enter> to quit and close program
    ''')
            next_act = input('>>> ')
            if next_act == '':
                # os.system('clear')
                print('\n-- Goodbye --\n')
                sleep(2)
                os.system('clear')
                break
            
            elif next_act == '1':
                os.system('clear')
                view_all_users()
                input('\n-- <enter> to continue --\n')
                os.system('clear')
            
            elif next_act == '2':
                os.system('clear')
                search_user()
                input('\n-- <enter> to continue --\n')
                os.system('clear')
            
            elif next_act == '3':
                os.system('clear')
                # ---- works in functions x( ...
                rows = list(cursor.execute('SELECT competency_id, name FROM Competencies'))
                lst_results = []
                for i in rows:
                    lst_results.append(i)
                format_to_table(lst_results)
                try:
                    comp = input("Enter the competency id of the report you'd like to view: ")
                    os.system('clear')
                    comp_result_sum(comp)
                    input('\n-- <enter> to continue --\n')
                    os.system('clear')
                except:
                    input('-- Error Unkown Competency id entered. --\n -- <enter> to continue --\n')
                    os.system('clear')
                    pass

            elif next_act == '4':
                os.system('clear')
                try:
                    user_id = input('Enter the user id of the summary you wish to view: ')
                    view_comp_sum(user_id)
                    input('\n-- <enter> to continue --\n')
                    os.system('clear')
                except:
                    print('\n-- User has no assessments to view --\n')
                    input('\n-- <enter> to continue --\n')
                    os.system('clear')
                    pass
            
            elif next_act == '5':
                os.system('clear')
                user_id = input('Enter the user id of the summary you wish to view: ')
                print()
                if view_assessments(user_id) == 'error':
                    pass
                else:
                    input('\n-- <enter> to continue --\n')
                    os.system('clear')
            
            elif next_act == '6':
                while True:
                    os.system('clear')
                    table_sel = input('''What would you like to add? \n(1) new user \n(2) new competency \n(3) new assessment for competency \n(4) new assessment result for a user \n\n <enter> to return to main menu\n\n>>> ''')
                    
                    if table_sel == '':
                        break
                    
                    if table_sel == '1':
                        mngr_add('1')
                        conf = input('''Add another item to the database? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break
                    if table_sel == '2':
                        mngr_add('2')
                        conf = input('''Add another item to the database? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break
                    if table_sel == '3':
                        mngr_add('3')
                        conf = input('''Add another item to the database? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break
                    if table_sel == '4':
                        mngr_add('4')
                        conf = input('''Add another item to the database? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break
            
            elif next_act == '7':
                while True:
                    os.system('clear')
                    table_sel = input('''What would you like to edit? \n (1) user info \n (2) competency \n (3) assessment info \n (4) assessment result \n\n>>> ''')

                    if table_sel == '1':
                        os.system('clear')
                        while True:
                            print("Enter the user id of record you'd like to update:\n")
                            format_to_table(cursor.execute('SELECT user_id, first_name, last_name from Users').fetchall())
                            user_sel = input('>>> ')
                            if check_valid_fk('user_id','Users',user_sel) == 'all good':
                                break
                            
                            elif user_sel == '':
                                break

                            else:
                                os.system('clear')
                                print('-- Error: unrecognized user id --\n')
                        if user_sel == '':
                            os.system('clear')
                            continue

                        os.system('clear')
                        mngr_update('Users',user_sel)
                        # mngr_update_user()
                        conf = input('''Would you update another item? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break

                    if table_sel == '2':
                        os.system('clear')
                        while True:
                            print("Enter the competency id of record you'd like to update:\n")
                            format_to_table(cursor.execute('SELECT competency_id, name, date_created from Competencies').fetchall())
                            user_sel = input('>>> ')
                            if check_valid_fk('competency_id','Competencies',user_sel) == 'all good':
                                break
                            
                            elif user_sel == '':
                                break

                            else:
                                os.system('clear')
                                print('-- Error: unrecognized competency id --\n')
                        if user_sel == '':
                            os.system('clear')
                            continue

                        os.system('clear')
                        mngr_update('Competencies',user_sel)
                        # mngr_update_user()
                        conf = input('''Would you update another item? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break

                    if table_sel == '3':
                        os.system('clear')
                        while True:
                            print("Enter the assessment id of record you'd like to update:\n")
                            format_to_table(cursor.execute("""SELECT 
                                assessment_id as 'Assessment Id',
                                cad.name as 'Assessment Name',
                                cad.date_created as 'Date Created',
                                competency_type as 'Competency Id',
                                c.name as 'Competency Name'
                            FROM Competency_Assessment_Data as cad
                            JOIN Competencies as c
                            ON cad.competency_type = c.competency_id;""").fetchall())
                            user_sel = input('>>> ')
                            if check_valid_fk('assessment_id','Competency_Assessment_Data',user_sel) == 'all good':
                                break
                            
                            elif user_sel == '':
                                break

                            else:
                                os.system('clear')
                                print('-- Error: unrecognized assessment id --\n')
                        if user_sel == '':
                            os.system('clear')
                            continue

                        os.system('clear')
                        mngr_update('Competency_Assessment_Data',user_sel)
                        # mngr_update_user()
                        conf = input('''Would you update another item? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break

                    if table_sel == '4':
                        os.system('clear')
                        while True:
                            print("Enter the test result id of record you'd like to update:\n")
                            format_to_table(cursor.execute("""SELECT car.date_taken as 'Date Taken', test_result_id as 'Test Result Id', car.user_id as 'User Id', 
                                u.first_name as 'Employee Name', assessment_id as 'Assmt. Id', 
                                cad.name as 'Assessment Name', score as 'Score'
                            FROM Competency_Assessment_Results as car
                            JOIN Users as u
                            ON car.user_id = u.user_id
                            JOIN Competency_Assessment_Data as cad
                            ON car.assessment = cad.assessment_id
                            ORDER BY car.date_taken DESC""").fetchall())
                            user_sel = input('>>> ')
                            if check_valid_fk('test_result_id','Competency_Assessment_Results',user_sel) == 'all good':
                                break
                            
                            elif user_sel == '':
                                break

                            else:
                                os.system('clear')
                                print('-- Error: unrecognized test result id --\n')
                        if user_sel == '':
                            os.system('clear')
                            continue

                        os.system('clear')
                        mngr_update('Competency_Assessment_Results',user_sel)
                        # mngr_update_user()
                        conf = input('''Would you update another item? \n (y) yes   (n) no \n\n>>> ''')
                        if conf.lower() == 'y':
                            os.system('clear')
                            continue
                        else:
                            os.system('clear')
                            break
                    else: 
                        os.system('clear')
                        break    
            
            elif next_act == '8':
                print('Remove function coming...')

            elif next_act == '9':
                os.system('clear')
                while True:
                    generate_csv()
                    cont = input('Generate another CSV? \n (y) yes (n) no \n\n>>> ')
                    if cont.lower == 'y':
                        os.system('clear')
                        continue
                    else:
                        os.system('clear')
                        break

            elif next_act == '10': 
                print('Import CSV File coming... ')
            
            
            else:
                os.system('clear')


    elif user_check[0] == 'user':
        # print('user options')
        user_id = user_check[1]
        os.system('clear')
        print('======= Welcome ========\n')
        while True:

            print('''What would you like to do?
 (1) View assessments
 (2) View list of all competencies
 (3) Edit user info

 <enter> to quit and close program
    ''')
            next_act = input('>>> ')

            if next_act.lower() == '':
                # os.system('clear')
                print('\n-- Goodbye --\n')
                sleep(2)
                os.system('clear')
                break

            elif next_act == '1':
                user_id = user_check[1]
                os.system('clear')
                if view_assessments(user_id) == 'error':
                    pass
                else:
                    input('\n-- <enter> to continue --\n')
                    os.system('clear')
                # try:
                #     view_assessments(user_id)
                #     input('\n-- <enter> to continue --\n')
                #     os.system('clear')
                # except:
                #     print('\n-- You have no assessments to display --')
                #     input('\n-- <enter> to continue --\n')
                #     os.system('clear')

            elif next_act == '2':
                os.system('clear')
                user_view_comp_sum(str(user_id))
                input('\n-- <enter> to continue --\n')
                os.system('clear')

            elif next_act == '3':
                # user_id = user_check[1]
                os.system('clear')
                user_update(user_id)
            
            os.system('clear')


    elif user_check == 'close program':
        # os.system('clear')
        print('\n-- Goodbye --\n')
        sleep(2)
        os.system('clear')

    break

# except:
    # print('''-- There was an unexpected Error. Please log instance and send details to IT. --''')
    # next_act = input('Reload Program? (y) yes (n) no \n')
    # if next_act.lower() == 'y':
    #     os.system('python3 main.py')
    # else:
    #     os.system('clear')


# ----program^^^
# in update for the CAD competency_type gives a weird print message for the conf




# def format_to_table(lst_of_tuple_query_results):
#     tuple_query_results = lst_of_tuple_query_results
#     header = []
#     column_sizes = []

#     names = list(map(lambda x: x[0], cursor.description))
#     for i in names:
#         header.append(str(i).replace('_',' ').title())

#     for i in range(len(names)):
#         count = 1
#         max_col_len = 0
#         for column in tuple_query_results: 
#             if max_col_len < len(str(column[i])):
#                 max_col_len = len(str(column[i]))

#             if count == len(tuple_query_results):
#                 column_sizes.append(max_col_len)

#             count += 1

#     for i in range(len(names)):
#         if column_sizes[i] < len(str(header[i])):
#             print(f' {header[i]:{len(str(header[i])) + 2}}', end = '')
#         else:
#             print(f' {header[i]:{column_sizes[i] + 2}}', end = '')
#     print()

#     for i in range(len(names)):
#         if column_sizes[i] < len(str(header[i])):
#             print('','-' * (len(str(header[i])) + 2), end = '')
#         else:
#             print('','-' * (column_sizes[i] + 2), end = '')

#     for e in tuple_query_results:
#         print()
#         for i in range(len(names)):
#             if column_sizes[i] < len(str(header[i])):
#                 print(f' {str(e[i]):{len(str(header[i])) + 2}}', end = '')
#             else:
#                 print(f' {str(e[i]):{column_sizes[i] + 2}}', end = '')
#     print()
#     print()



# rows = list(cursor.execute('SELECT competency_id, name FROM Competencies'))
# lst_results = []
# for i in rows:
#     lst_results.append(i)
# format_to_table(lst_results)
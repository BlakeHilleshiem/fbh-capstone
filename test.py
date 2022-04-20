# https://stackoverflow.com/questions/61353255/getting-a-password-to-matches-with-its-hash-in-a-login-function-using-python-sq

# try-except blocks
# try:
#   print(x)
# except NameError:
#   print("-- Error: Variable x is not defined --")
# except:
#   print("-- Something else went wrong -- ")

# try:
#   print(x)
# except:
#   print("An exception occurred")

# ----------------- eg. of try except block in loop:
# while True:
#     try:

#         print(x)
#         if x == True:
#             break
    
#     except:
#         print('\n-- An error occured. Please make note and send documentation to IT. \n-- Sorry for the inconvience. Program closed.\n')
#         break

# ---------------------

# password = 'MyPassWord'

# bytePwd = password.encode('utf-8')

# print(bytePwd)

# # Generate salt
# mySalt = bcrypt.gensalt()

# # Hash password
# hash = bcrypt.hashpw(bytePwd, mySalt)

'''
SELECT cad.name as 'Assessment Name', c.name as 'Competency Type', car.score as 'Score', u.first_name as 'Issued By', car.date_taken as 'Date Taken'
FROM Competency_Assessment_Results as car
JOIN Competency_Assessment_Data as cad
ON car.assessment = cad.assessment_id
JOIN Competencies as c
ON cad.competency_type = c.competency_id
JOIN Users as u
ON car.manager = u.user_id
WHERE car.user_id = 2
ORDER BY car.date_taken DESC
'''


def display_active_table(table):
    rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
    cursor.execute(f'SELECT * FROM {table}').fetchall()

    header = []
    column_sizes = []

    names = list(map(lambda x: x[0], cursor.description))
    for i in names:
        header.append(str(i).replace('_',' ').title())

    for i in range(len(names)):
        count = 1
        max_col_len = 0
        for column in rows: 
            if max_col_len < len(str(column[i])):
                max_col_len = len(str(column[i]))

            if count == len(rows):
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

    rows = cursor.execute(f'SELECT * FROM {table} WHERE active = 1')

    for e in rows:
        print()
        for i in range(len(names)):
            if column_sizes[i] < len(str(header[i])):
                print(f' {str(e[i]):{len(str(header[i])) + 2}}', end = '')
            else:
                print(f' {str(e[i]):{column_sizes[i] + 2}}', end = '')
    print()
    print()

# import os


# input('hit enter to continue')
# os.system('clear')
# print('next page')
# input('next item: ')


# ------------------------
import os
from time import sleep

# # Printing Some Text
# print(1)
# print(2)
# print(3)
# print(4)
# print(5)
# print("Screen will now be cleared in 5 Seconds")

# # Waiting for 5 seconds to clear the screen
# sleep(5)

# # Clearing the Screen
# os.system('clear')



# print('.', end='')

# print('.', end='')


# works-------
# print('hi')
# print('>>> Goodbye.', end=''),sleep(1)
# print('.')

# sleep(1)

# os.system('clear')

import sqlite3
connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

def view_comp_sum(str_user_id):

    def most_recent(str_comp_name,query_results):
        lst_of_attempts = []
        for i in query_results:
            if str_comp_name in i:
                lst_of_attempts.append(i)

        most_current = ''
        largest = '0'

        for i in lst_of_attempts:
            qck_lst = list(i)
            if qck_lst[7] > most_current:
                largest = qck_lst[4]
            
        return largest 

    user_id = str_user_id
    rows = cursor.execute('''SELECT car.user_id, u.first_name, u.last_name, c.name, car.score, u.phone, u.email, car.date_taken
    FROM Competency_Assessment_Results as car
    JOIN Competency_Assessment_Data as cad
    ON car.assessment = cad.assessment_id
    JOIN Competencies as c
    ON cad.competency_type = c.competency_id
    JOIN Users as u
    ON car.user_id = u.user_id
    WHERE car.user_id = ?
    ''', (user_id))


    lst_results = []
    for i in rows:
        lst_results.append(i)

    print(lst_results)

    comp = cursor.execute('''SELECT name FROM Competencies''')

    lst_comp = []
    for i in comp:
        lst_comp.append(str(i).replace(',','').strip('()').strip('\'\''))

    # print()
    # print(lst_results)
    data = list(lst_results[0])
    # print(data)

    # print()
    # print(lst_comp)
    # print()



    # print(greatest_score('Databases',lst_results))


    total = []
    for i in lst_comp:
        total.append(int(most_recent(i,lst_results)))
    avg_comp_score = f'{sum(total) / len(lst_comp):.2f}'

    lst_headers = ['User Id:','Name:','Avg. Comptency Score:', 'Phone:', 'Email:']
    lst_data = [user_id, data[1] + ' ' + data[2], avg_comp_score, data[5], data[6]]

    column_sizes = []
    for i in lst_data:
        column_sizes.append(len(i))

    # print(column_sizes)
    print()
    count = 0
    for i in column_sizes:
        if i < len(lst_headers[count]):
            print(f"{lst_headers[count]:{len(lst_headers[count])+2}}", end = '')
        else:
            print(f"{lst_headers[count]:{i+2}}", end = '')
        count += 1
    print()
    count = 0
    for i in column_sizes:
        if i < len(lst_headers[count]):
            print(f"{'-'*(len(lst_headers[count])+1):{len(lst_headers[count])+2}}", end = '')
        else:
            print(f"{'-'*(i+1):{i+2}}", end = '')
        count += 1
    print()
    count = 0
    for i in column_sizes:
        if i < len(lst_headers[count]):
            print(f"{lst_data[count]:{len(lst_headers[count])+2}}", end = '')
        else:
            print(f"{lst_data[count]:{i+2}}", end = '')
        count += 1
    print()
    # print(data[1] + ' ' + data[2])

    # print(f"{'User Id:'}{'Name:'}{'Avg. Competency Score'}{'Phone'}{'Email:'}")
    # print()
    # print(f'''
    # User id: {user_id} Name: {data[1]} {data[2]} Avg. Comptency Score: {avg_comp_score}

    # Phone: {data[5]} Email: {data[6]}
    # ''')

    # ------------------- Needs to be most recent score not the highest...
    print(f"\n{' Competencies:':28} {'Score:':7}")
    print(f" {'-'*17:27} {'-'*6:7}")
    for i in lst_comp:
        length = len(i)
        print(f" {i} {'.'* (28-length)} {most_recent(i,lst_results)}")
    print()

os.system('clear')
# try:
# user_id = input('Enter the user id of the summary you wish to view: ')
view_comp_sum('3')
input('\n-- <enter> to continue --\n')
os.system('clear')
# except:
#     print('error')



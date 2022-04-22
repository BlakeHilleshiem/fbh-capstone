import csv

import os

from time import sleep

import bcrypt

import sqlite3
connection = sqlite3.connect('competency_tracker.db')
cursor = connection.cursor()

from datetime import datetime
dateTimeObj = datetime.now()
timestamp_str = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")


def verify_user():
    while True:
        print('-- Login below: --\n')
        email = input('  email: ')
        password = input('  password: ')
        byte_pwd = password.encode('utf-8')

        emails = cursor.execute('SELECT email FROM Users')
        lst_emails = []
        for i in emails:
            lst_emails.append(i)
        
        if email == '' and password == '':
            return 'close program'

        elif email not in lst_emails:
            os.system('clear')
            print('** Unrecognized login. Please enter valid email and password. **')
            print(' ** (or double <enter> to close program) ** \n')

        row = cursor.execute('SELECT email, password, user_type, active, user_id FROM Users WHERE email = ?',(email,))

        
        for i in row:
            check = list(i)

        try:
            if check[0] == email and bcrypt.checkpw(byte_pwd, check[1]) == True:
                if check[2] == 'user':
                    return ['user',check[4]]
                elif check[2]== 'manager':
                    return ['manager',check[4]]
                else:
                    print('-- User has not been assigned a user type --\n')

            elif check[3] == 0:
                print('-- Invalid login. Account is inactive. -- ')
                return('close program')

            else:
                os.system('clear')
                print('** Unrecognized login. Please enter valid email and password. **')
                print(' ** (or double <enter> to close program) ** \n')
                    
        except:
            pass




def format_to_table(fetchall_qry):
    rows = fetchall_qry

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

    for e in rows:
        print()
        for i in range(len(names)):
            if column_sizes[i] < len(str(header[i])):
                print(f' {str(e[i]):{len(str(header[i])) + 2}}', end = '')
            else:
                print(f' {str(e[i]):{column_sizes[i] + 2}}', end = '')




def view_assessments(user_id_str):
    user_id = user_id_str
    rows = cursor.execute(f'''
    SELECT cad.name as 'Assessment Name', c.name as 'Competency Type', car.score as 'Score', u.first_name as 'Issued By', car.date_taken as 'Date Taken'
    FROM Competency_Assessment_Results as car
    JOIN Competency_Assessment_Data as cad
    ON car.assessment = cad.assessment_id
    JOIN Competencies as c
    ON cad.competency_type = c.competency_id
    JOIN Users as u
    ON car.manager = u.user_id
    WHERE car.user_id = ?
    ORDER BY car.date_taken DESC''',(user_id,)).fetchall()

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
        try:
            if column_sizes[i] < len(str(header[i])):
                print(f' {header[i]:{len(str(header[i])) + 2}}', end = '')
            else:
                print(f' {header[i]:{column_sizes[i] + 2}}', end = '')
        except:
            os.system('clear')
            print('-- You have no assessments to display --')
            input('\n-- <enter> to continue --\n')
            os.system('clear')
            return 'error'
    print()

    for i in range(len(names)):
        if column_sizes[i] < len(str(header[i])):
            print('','-' * (len(str(header[i])) + 2), end = '')
        else:
            print('','-' * (column_sizes[i] + 2), end = '')

    for e in rows:
        print()
        for i in range(len(names)):
            if column_sizes[i] < len(str(header[i])):
                print(f' {str(e[i]):{len(str(header[i])) + 2}}', end = '')
            else:
                print(f' {str(e[i]):{column_sizes[i] + 2}}', end = '')
    print()
    print()
    return




def conf_cont():
    print('''Would you like to make a different change?
  (y) yes   (n) no
''')
    conf = input('>>> ')
    if conf.lower() == 'y':
        os.system('clear')
        return 'y'
    else:
        return 'n'







def update_pass(new_value,user_id):
    password = new_value
    byte_pwd = password.encode('utf-8')
    my_salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(byte_pwd,my_salt)
    cursor.execute('UPDATE Users SET password = ? WHERE user_id = ?',(hash_pw,user_id))
    connection.commit()




def user_update(user_id):
    edit_fields = ['First name', 'Last name', 'Phone number', 'Email']
    data = cursor.execute('SELECT first_name, last_name, phone, email FROM Users WHERE user_id = ?',(user_id,)).fetchone()
    data = list(data)
    input_dict = {
            '1':'first_name',
            '2':'last_name',
            '3':'phone',
            '4':'email',
            '5':'password'
        }

    while True:
        print('\nPlease select which field you would like to update: \n  (<enter> to return to main menu)\n ')
        for i in range(4):
            print(f'   ({i+1}) {edit_fields[i]}: {data[i]}')
        print('   (5) Password : #####...')
        update_num = input('\n>>> ')

        if update_num == '':
            os.system('clear')
            break
        if update_num.isdigit() == True:
            if int(update_num) > 0 and int(update_num) < 6:
                for i in input_dict:
                    if i == str(update_num):
                        update_field = input_dict[i]

                while True:
                    new_value = input(f'\nEnter the new {str(input_dict[update_num]).lower()}: ')

                    if update_num == '4' and new_value == '' or update_num == '5' and new_value == '':
                        print('\n-- Error: this field cannot be blank --')
                        continue
                    else:
                        break
                    
                if update_num == '5':
                    print(f'\nUpdate the {str(input_dict[update_num]).lower()} to: {new_value}?\n  (y) yes   (n) no\n')
                    conf = input('>>> ')

                    if conf.lower() == 'y':
                        update_pass(new_value,user_id)
                        print('\n-- User updated --\n')
                        conf = conf_cont()
                        if conf == 'n':
                            break
                        else:
                            continue
                    else:
                        print('\n-- Action Cancelled --\n')
                        conf = conf_cont()
                        if conf == 'n':
                            break
                        else:
                            continue

                print(f'\nUpdate the {str(input_dict[update_num]).lower()} to: {new_value}?\n  (y) yes   (n) no\n')
                conf = input('>>> ')

                if conf.lower() == 'y':
                    cursor.execute(f'UPDATE Users SET {update_field} = ? WHERE user_id = ?',(new_value,user_id))
                    connection.commit()
                    print('\n-- User updated --\n')
                    conf = conf_cont()
                    if conf == 'n':
                        break
                    else:
                        continue
                else:
                    print('\n-- Action Cancelled --\n')
                    conf = conf_cont()
                    if conf == 'n':
                        break
                    else:
                        continue
            else:
                print('\n-- Error: invalid option --\n')
                continue
        else:
            print('\n-- Error: invalid option --\n') 




def view_all_users():
    rows = cursor.execute(f'''
    SELECT user_id, first_name, last_name, phone, email, date_created, hire_date, active, user_type FROM Users;
    ''').fetchall()
    print()
    format_to_table(rows)




def search_user():
    search_term = input('Enter search term: ')
    if search_term.isdigit() == True:
        search_term = int(search_term)
    search_term = f'%{search_term}%'
    rows = cursor.execute(f"""SELECT user_id, first_name, last_name, phone, email, date_created, hire_date, active, user_type 
    FROM Users WHERE first_name LIKE ? OR last_name LIKE ? OR user_id LIKE ? """,(search_term, search_term, search_term)).fetchall()
    print()
    # print(rows)
    # if rows == []:
    #     print('-- There are no users in the system ')
    format_to_table(rows)

# search_term = f"%{1}%"
# rows = cursor.execute(f"""SELECT user_id, first_name, last_name, phone, email, date_created, hire_date, active, user_type 
# FROM Users WHERE first_name LIKE ? OR last_name LIKE ? OR user_id LIKE ? """,(search_term, search_term, search_term)).fetchall()
# print(rows)


# def greatest_score(str_comp_name,query_results):
#     try:
#         lst_of_attempts = []
#         for i in query_results:
#             if str_comp_name in i:
#                 lst_of_attempts.append(i)

#         lst_of_scores = []
#         for i in lst_of_attempts:
#             qck_lst = list(i)
#             lst_of_scores.append(qck_lst[4])
  
#         return(max(lst_of_scores))
#     except:
#         return '0'




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


# view_comp_sum('1')


def user_view_comp_sum(str_user_id):

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

    comp = cursor.execute('''SELECT name FROM Competencies''')

    lst_comp = []
    for i in comp:
        lst_comp.append(str(i).replace(',','').strip('()').strip('\'\''))

    # ------------------- Needs to be most recent score not the highest...
    print(f"\n{' Competencies:':28} {'Score:':7}")
    print(f" {'-'*17:27} {'-'*6:7}")
    for i in lst_comp:
        length = len(i)
        print(f" {i} {'.'* (28-length)} {most_recent(i,lst_results)}")
    print()





def comp_result_sum(str_comp_id):
        
    def most_recent_2(user_id,str_comp_name,query_results):
        lst_of_attempts = []
        for i in query_results:
            # print(i)
            if str_comp_name in i:
                lst_of_attempts.append(i)
        # print('list of attempts: ', lst_of_attempts)
        most_current = ''
        largest = '0'

        # print(lst_of_attempts)

        for i in lst_of_attempts:
            # print(i)
            qck_lst = list(i)
            if str(qck_lst[0]) == str(user_id) and qck_lst[6] > most_current:
                largest = [qck_lst[3],qck_lst[4],qck_lst[6]]

            
        return largest   


    competency_id = str_comp_id

    rows = cursor.execute('''
        SELECT car.user_id as 'User Id', u.first_name as 'First Name', u.last_name as 'Last Name', car.score as 'Score', cad.name as 'Assessment Name', 
            c.name as 'Competency Type', car.date_taken as 'Date Taken'
        FROM Competency_Assessment_Results as car
        JOIN Users as u
        ON car.user_id = u.user_id
        JOIN Competency_Assessment_Data as cad
        ON car.assessment = cad.assessment_id
        JOIN Competencies as c
        ON cad.competency_type = c.competency_id
        WHERE cad.competency_type = ? AND u.active = 1
    ''',(competency_id,))

    lst_result = []
    for i in rows:
        lst_result.append(i)

    lst_test_name = []
    for i in lst_result:
        lst_test_name.append(i[4])

    lst_date_taken = []
    for i in lst_result:
        lst_date_taken.append(i[6])

    users = cursor.execute('SELECT user_id, first_name, last_name FROM Users WHERE active = 1')
    lst_users = []
    for i in users:
        lst_users.append(i)

    competencies = {
        '1'	 :'Data Types',
        '2'	 :'Variables',
        '3'	 :'Functions',
        '4'	 :'Boolean Logic',
        '5'	 :'Conditionals',
        '6'	 :'Loops',
        '7'	 :'Data Structures',
        '8'	 :'Lists',
        '9'	 :'Dictionaries',
        '10' :'Working with Files',
        '11' :'Exception Handling',
        '12' :'Quality Assurance (QA)',
        '13' :'Object-Oriented Programming',
        '14' :'Recursion',
        '15' :'Databases',
        '16' :'Verbal Communication'
    }

    competency_type = competencies[competency_id]

    lst_user_id = []
    for i in lst_users:
        qck_lst = list(i)
        lst_user_id.append(qck_lst[0])

    test_results = []
    for i in lst_user_id:
        try:
            score = int(most_recent_2(i,competency_type,lst_result)[0])
            test_results.append(score)
        except:
            test_results.append(score)

    avg = f"{sum(test_results) / len(lst_user_id):.2f}"

    print(f'\nCompetency: {competency_type} \n\nAverage competency score of all users: {avg}\n')

    print(f" {'User Id':^7}   {'Name':20} {'Score':8} {'Assessment Name':35} {'Date Taken'}")
    print(f" {'-'*8:^7}  {'-'*19:20} {'-'*7:8} {'-'*34:35} {'-'*20}")

    count = 0
    for i in lst_users:
        try:
            print(f" {i[0]:^7}   {(str(i[1]) + ' ' + str(i[2])):20} {str(most_recent_2(lst_user_id[count], competency_type,lst_result)[0]):8} {most_recent_2(lst_user_id[count], competency_type,lst_result)[1]:35} {most_recent_2(lst_user_id[count], competency_type,lst_result)[2]}")
            count += 1
        except:
            print(f" {i[0]:^7}   {(str(i[1]) + ' ' + str(i[2])):20} {'0':8} {'':35} {''}")
            count += 1
    print()



def check_email(str_email_to_check):
    rows = cursor.execute('SELECT email FROM Users')
    lst_emails = []
    for i in rows:
        lst_emails.append(str(i).strip('()').replace(',','').replace('\"','').replace('\'',''))
    print(lst_emails)
    if str_email_to_check in lst_emails:
        return 'error'
    else:
        return 'all good'




def add_user():
    columns = ['first name', 'last name','phone','email','password','active','date created','hire date','user type']

    lst_answers = []
    count = 0
    for i in range(len(columns)):

        if columns[i] == 'active':
            ans = input(f"Make account {columns[i]}? (y) yes   (n) no \n>>> ")
            if ans.lower() == 'n':
                lst_answers.append('0')
                os.system('clear')
                continue
            else:
                lst_answers.append('1')
                os.system('clear')
                continue

        if columns[i] == 'date created':
            lst_answers.append(timestamp_str)
            os.system('clear')
            continue      

        if columns[i] == 'hire date':
            ans = input(f"Enter the {columns[i]} in the following format (YYYY-MM-DD hh:mm:ss): ")
            lst_answers.append(ans)
            os.system('clear')
            continue

        if columns[i] == 'user type':
            ans = input(f"Enter {columns[i]}: (1) user   (2) manager \n>>> ")
            if ans.lower() == '2':
                lst_answers.append('manager')
                os.system('clear')
                continue
            else:
                lst_answers.append('user')
                os.system('clear')
                continue

        # if columns[i] == 'email':
        #     while 
        #     if ans == '':
        #         os.system('clear')
        #         print('-- error: field cannot be blank --')
        #         ans = input(f"Enter the {columns[i]}: ")
        #     if check_email(ans) == 'error':
        #         os.system('clear')
        #         print('-- error: email already exsists --')
        #         ans = input(f"Enter the {columns[i]}: ")
        #     else:
        #         lst_answers.append(ans)
        #         os.system('clear')
        #         break

        os.system('clear')
        ans = input(f"Enter the {columns[i]}: ")

        while columns[i] == 'first name' and ans == '':
            os.system('clear')
            print('-- Error: field cannot be blank --')
            ans = input(f"Enter the {columns[i]}: ")

        while columns[i] == 'email' and ans == '' or columns[i] == 'email' and check_email(ans) == 'error':
            if ans == '':  
                os.system('clear')
                print('-- Error: field cannot be blank --')
                ans = input(f"Enter the {columns[i]}: ")
            if check_email(ans) == 'error':
                os.system('clear')
                print('-- Error: email already exsists --')
                ans = input(f"Enter the {columns[i]}: ")
        
        # while columns[i] == 'password' and ans == '':
        #     os.system('clear')
        #     print('-- error: field cannot be blank --')
        #     ans = input(f"Enter the {columns[i]}: ")
        while columns[i] == 'password': 
            if ans == '':
                os.system('clear')
                print('-- error: field cannot be blank --')
                ans = input(f"Enter the {columns[i]}: ")
            if ans != '':
                password = ans
                byte_pwd = password.encode('utf-8')
                my_salt = bcrypt.gensalt()
                ans = bcrypt.hashpw(byte_pwd,my_salt)
                break

        
        lst_answers.append(ans)
        os.system('clear')

    for i in lst_answers:
        print(f"{i:len(i)+2}")
    conf = input('''
    Add this record to the database? \n (y) yes   (n) no \n>>> ''')

    if conf.lower() == 'y':
        cursor.execute('''INSERT INTO Users (
        first_name,
        last_name,
        phone,
        email,
        password,
        active,
        date_created,
        hire_date,
        user_type)
        VALUES (
            ?,?,?,?,?,?,?,?,?
        )''',(lst_answers[0],lst_answers[1],lst_answers[2],lst_answers[3],lst_answers[4],lst_answers[5],lst_answers[6],lst_answers[7],lst_answers[8]))
        connection.commit()
        print('\n-- User Added --\n')

    else:
        print('\n-- Action Cancelled --\n')



def check_for_dupl(field,check_str):
    data = cursor.execute(f"SELECT {field} FROM Users")
    lst_data = []
    for i in data:
        lst_data.append(str(i).strip('()').replace("\'",'').replace(',',''))

    if check_str in lst_data:
        return 'error'
    if check_str == '':
        return 'blank error'
    else:
        return 'all good'


# print(check_for_dupl('email','manager_test@email.com'))
# print(check_for_dupl('user_id','1'))


def check_valid_id(user_id_str):
    data = cursor.execute("SELECT user_id FROM Users")
    lst_id = []
    for i in data:
        lst_id.append(i)
    if user_id_str in lst_id:
        return 'all good'
    else:
        return 'error'
    





def mngr_update_user():
    os.system('clear')
    fields = {
        '1':'user_id',
        '2':'first_name',
        '3':'last_name',
        '4':'phone',
        '5':'email',
        '6':'password',
        '7':'active',
        '8':'date_created',
        '9':'hire_date',
        '10':'user_type'
    }

    user_id = input('Enter user id of account to update: ')

    data = list(cursor.execute('SELECT user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type FROM Users WHERE user_id = ?',(user_id)).fetchone())

    if str(data[6]) == '1':
        active_sts = 'active'
    elif str(data[6]) == '0':
        active_sts = 'inactive'

    field_sel = input(f'''
What would you like to update? 

 (1)  User Id:        {data[0]}
 (2)  First Name:     {data[1]}
 (3)  Last Name:      {data[2]}
 (4)  Phone:          {data[3]}
 (5)  Email:          {data[4]}
 (6)  Password:       #####...
 (7)  Active Status:  {active_sts}
 (8)  Date Created:   {data[7]}
 (9)  Hire Date:      {data[8]}
 (10) User Type:      {data[9]}
    
    >>> ''')
    print()
    str_field = fields[field_sel]
    str_field = str_field.replace('_',' ')


    # print(data)

    # print(fields[field_sel])

    # print(type(fields[field_sel]))
    # if fields[field_sel] == 'active':
    #     print('True')
    # else:
    #     print('False')

    if fields[field_sel] == 'active':
        if str(data[6]) == '1':
            check = input(f"Change {data[1] + ' ' + data[2]} to inactive? \n (y) yes   (n) no \n\n>>> ")
            if check.lower() == 'y':
                change_val = '0'
            
            else:
                change_val = '1'
            

        elif str(data[6]) == '0':
            check = input(f"Change {data[1] + ' ' +  data[2]} to active? \n (y) yes   (n) no \n\n>>> ")
            if check.lower() == 'y':
                change_val = '1'
            
            else:
                change_val = '0'
            

    elif fields[field_sel] == 'user_type':
        if str(data[9]) == 'manager':
            check = input(f"Change {data[1] + ' ' +  data[2]}'s user type to 'user'? \n (y) yes   (n) no \n\n>>> ")
            if check.lower() == 'y':
                change_val = 'user'
                
            else:
                change_val = 'manager'
            

        elif str(data[9]) == 'user':
            check = input(f"Change {data[1] + ' ' +  data[2]}'s user type to 'manager'? \n (y) yes   (n) no \n\n>>> ")
            if check.lower() == 'y':
                change_val = 'manager'
            
            else:
                change_val = 'user'

    elif fields[field_sel] == 'phone':
        change_val = input(f'Enter the new {str_field} #: ')

    elif fields[field_sel] == 'date_created':
        change_val = input(f'Enter the new {str_field} in the following format (YYYY-MM-DD hh:mm:ss): ')

    elif fields[field_sel] == 'hire_date':
        change_val = input(f'Enter the new {str_field}: in the following format (YYYY-MM-DD hh:mm:ss)')
            
    else:
        while True:
            change_val = input(f'Enter the new {str_field}: ')
            if fields[field_sel] == 'user_id' and change_val == '' or fields[field_sel] == 'email' and change_val == '' or fields[field_sel] == 'password' and change_val == '' or fields[field_sel] == 'first_name' and change_val == '':
                print('\n-- Error: field cannot be blank --\n')
            elif fields[field_sel] == 'user_id' and check_for_dupl(fields[field_sel],change_val) == 'error' or fields[field_sel] == 'email' and check_for_dupl(fields[field_sel],change_val) == 'error':
                print(f'\n-- Error: this {str_field} is assigned to another user --\n')
            else:
                break
    
    if fields[field_sel] == 'user_type' and check.lower() == 'y' or fields[field_sel] == 'active' and check.lower() == 'y':
        cursor.execute(f'''UPDATE Users SET {fields[field_sel]} = ? WHERE user_id = ?''',(change_val,user_id))
        connection.commit()
        print('\n-- User Updated -- \n')

    elif fields[field_sel] == 'user_type' and check.lower() == 'n' or fields[field_sel] == 'active' and check.lower() == 'n':
        print('\n-- Action Cancelled --\n')

    elif fields[field_sel] == 'password':
        print()
        conf = input(f"Update {data[1] + ' ' +  data[2]}'s {str_field} to: {change_val}? \n (y) yes   (n) no \n\n>>> ")
        if conf.lower() == 'y':
            password = change_val
            byte_pwd = password.encode('utf-8')
            my_salt = bcrypt.gensalt()
            hash_pw = bcrypt.hashpw(byte_pwd,my_salt)
            cursor.execute(f'''UPDATE Users SET password = ? WHERE user_id = ?''',(hash_pw,user_id))
            connection.commit()
            print('\n-- User Updated -- \n')
        else:
            print('\n-- Action Cancelled --\n')


    # if fields[field_sel] != 'user_type' or fields[field_sel] != 'active':
    # else:
    # print('\npreview\n')
    else:
        print()
        conf = input(f"Update {data[1] + ' ' +  data[2]}'s {str_field} to {change_val}? \n (y) yes   (n) no \n\n>>> ")
        # from {data[int(field_sel)-1]} 
        if conf.lower() == 'y':
            cursor.execute(f'''UPDATE Users SET {fields[field_sel]} = ? WHERE user_id = ?''',(change_val,user_id))
            connection.commit()
            print('\n-- User Updated -- \n')
        else:
            print('\n-- Action Cancelled --\n')



def check_for_dupl_2(field,table,check_str):
    data = cursor.execute(f"SELECT {field} FROM {table}")
    lst_data = []
    for i in data:
        lst_data.append(str(i).strip('()').replace("\'",'').replace(',',''))

    if check_str in lst_data:
        return 'error'
    if check_str == '':
        return 'blank error'
    else:
        return 'all good'


def int_pk_check(field,table):
    while True:
        # field = str(field).replace('_',' ')
        if field == 'assessment_id':
            ans = input('Enter an assessment id: ')
        else:
            ans = input(f'Enter a {field}: ')

        if ans == '':
            os.system('clear')
            print(f'-- Error: {field} cannot be blank -- \n')

        if ans.isdigit() == True:  
            if check_for_dupl_2(field,table,ans) == 'error':
                os.system('clear')
                print(f'-- Error: {field} entered is already in use --\n')
                continue
            else:
                return ans
       
        
        if ans != '' and ans.isdigit() == False:
            os.system('clear')
            print(f'-- Error: {field} must be a number -- \n')


def create_preview(lst_headers,lst_answers):
    print()
    count = 0
    for i in lst_headers:
        if lst_headers[count] == 'password':
            col_size = max((len(str(lst_headers[count]))),len('#####...'))
            print(f"{str(i).replace('_',' ').title() + ': ' :{col_size + 2}}", end = ' ')
        else:
            col_size = max(len(str(lst_headers[count])),len(str(lst_answers[count])))
            print(f"{str(i).replace('_',' ').title() + ': ' :{col_size + 2}}", end = ' ')
        count += 1
    print()
    count = 0
    for i in lst_headers:
        if lst_headers[count] == 'password':
            col_size = max((len(str(lst_headers[count]))),len('#####...'))
            print(f"{ '-' * (int(col_size) + 1):{col_size + 2}}", end = ' ')
        else:    
            col_size = max(len(str(lst_headers[count])),len(str(lst_answers[count])))
            print(f"{ '-' * (int(col_size) + 1):{col_size + 2}}", end = ' ')
        count += 1
    print()
    count = 0
    for i in lst_answers:
        if lst_headers[count] == 'password':
            col_size = max((len(str(lst_headers[count]))),len('#####...'))
            print(f"{ '#####...' :{col_size + 3}}", end = '')
        else:
            col_size = max((len(str(lst_headers[count]))),len(str(lst_answers[count])))
            print(f"{ str(i) :{col_size + 3}}", end = '')
        count += 1

    print()
    print()

def check_valid_fk(str_field, str_table, str_check_val):
    data = cursor.execute(f'SELECT {str_field} FROM {str_table}')
    lst_data = []
    for i in data:
        # print(i)
        lst_data.append((str(i).replace('\'','').replace(',','').strip('()')))
        # lst_data.append(str(i).strip('()').replace(',','').replace('\"',''))

    # print(lst_data)
    # print(str_check_val)

    if str_check_val in lst_data:
        return 'all good'
    elif str_check_val == '':
        return 'blank'
    else:
        return 'error'


def check_valid_mngr(str_check_val):
    data = cursor.execute(f"SELECT user_id FROM Users WHERE active = '1' and user_type = 'manager'")
    lst_data = []
    for i in data:
        lst_data.append(str(i).strip('()').replace(',',''))

    # print(lst_data)

    if str_check_val in lst_data:
        return 'all good'
    elif str_check_val == '':
        return 'blank'
    else:
        return 'error'




def mngr_add(sel):

    lst_fields = []
    lst_values = []
    table_dict = {
        '1':'Users',
        '2':'Competencies',
        '3':'Competency_Assessment_Data',
        '4':'Competency_Assessment_Results'
    }

    table = table_dict[f"{sel}"]
    cursor.execute(f"SELECT * FROM {table}")
    names = list(map(lambda x: x[0], cursor.description))
    print(names)
    for i in names:
        os.system('clear')
        # print(i)
        lst_fields.append(i)

        if i == 'competency_id':
            os.system('clear')
            lst_values.append(int_pk_check(i,table))
            # lst_values.append(pk_check(i,table))
            continue

        if i == 'user_id' and table == 'Users':
            os.system('clear')
            lst_values.append(int_pk_check(i,table))
            continue

        if i == 'assessment_id':
            os.system('clear')
            lst_values.append(int_pk_check(i,table))
            continue

        if i == 'email':
            os.system('clear')
            while True:
                ans = input('Enter a email: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: email cannot be blank --\n')
                    continue
                if check_for_dupl_2('email','Users',ans) == 'error':
                    os.system('clear')
                    print('-- Error: email already in use --\n')
                    continue

                else:
                    lst_values.append(ans)
                    break
            continue
        
        if i == 'password':
            os.system('clear')
            while True:
                ans = input('Enter a password: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                if ans != '':
                    password = ans
                    byte_pwd = password.encode('utf-8')
                    my_salt = bcrypt.gensalt()
                    ans = bcrypt.hashpw(byte_pwd,my_salt)
                    lst_values.append(ans)
                    break
            continue
        
        if i == 'active':
            os.system('clear')
            ans = input('Make user active?: \n (y) yes   (n) no \n\n>>> ')
            if ans.lower() == 'n':
                lst_values.append('0')
                continue
            else:
                lst_values.append('1')
                continue

        if i == 'user_type':
            os.system('clear')
            ans = input('Select user type: \n (1) user   (2) manager \n\n>>> ')
            if ans == '2':
                lst_values.append('manager')
                continue
            else:
                lst_values.append('user')
                continue

        if 'date' in i:
            if i == 'date_taken':
                while True:
                    ans = input(f"Enter the {str(i).replace('_',' ')} in the following format (YYYY-MM-DD hh:mm:ss): ")
                    if ans == '':
                        os.system('clear')
                        print('-- Error: field cannot be blank --\n')
                        continue
                    else:
                        lst_values.append(ans)
                        break
            else:
                os.system('clear')
                ans = input(f"Enter the {str(i).replace('_',' ')} in the following format (YYYY-MM-DD hh:mm:ss): ")
                lst_values.append(ans)

            continue

        if i == 'user_id' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter a user id: ")
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                    continue
                if check_valid_fk(i,table,ans) == 'error':
                    os.system('clear')
                    print('-- Error: user_id not found --\n')
                    continue
                else:
                    lst_values.append(ans)
                    break
            continue

        if i == 'assessment' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter an assessment id: ")
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                    continue
                if check_valid_fk(i,table,ans) == 'error':
                    os.system('clear')
                    print('-- Error: assessment_id not found. Must select an active test --\n')
                    continue
                else:
                    lst_values.append(ans)
                    break
            continue

        if i == 'competency_type' and table == 'Competency_Assessment_Data':
            os.system('clear')
            while True:
                format_to_table(cursor.execute('SELECT * FROM Competencies').fetchall())
                print()
                print()
                ans = input("Assign to which competency? Enter a competency id: ")
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                    continue
                if check_valid_fk(i,table,ans) == 'error':
                    os.system('clear')
                    print('-- Error: competency id not found --\n')
                    continue
                else:
                    lst_values.append(ans)
                    break
            continue

        if i == 'score' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter the user's score: ")
                if ans.isdigit() == False and ans != '':
                    os.system('clear')
                    print('-- Error: invalid score input --\n')
                    # input('enter to continue (in option 1)')
                    continue
                if check_valid_fk(i,'Scores',ans) == 'error':
                    os.system('clear')
                    print('-- Error: invalid score input --\n')
                    # input('enter to continue (in option 2)')
                    continue
                if ans == '':
                    lst_values.append('-')
                    break
                else:
                    lst_values.append(ans)
                    break
            continue

        if i == 'manager' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter the manager's user id: ")
                if check_valid_mngr(ans) == 'error':
                    os.system('clear')
                    print('-- Error: invalid user id --\n')
                    continue
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n ')
                    continue
                else:
                    lst_values.append(ans)
                    break
            continue

        if i == 'name' and table == 'Competencies':
            while True:
                ans = input('Enter name of the competency: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                else:
                    lst_values.append(ans)
                    break
            continue
        
        if i == 'name' and table == 'Competency_Assessment_Data':
            while True:
                ans = input('Enter a name for the assessment: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                else:
                    lst_values.append(ans)
                    break
            continue


        os.system('clear')
        ans = input(f"Enter a {str(i).replace('_',' ')}: ")
        lst_values.append(ans)

    str_lst_fields = str(lst_fields).strip('[]').replace('\'','')
    # print(str_lst_fields)

    data_bind = '?,' * len(lst_fields)
    data_bind = f"({data_bind.strip(',')})"
    # print(data_bind)

    tuple_values = tuple(lst_values)
    # print(tuple_values)
    
    os.system('clear')
    create_preview(names,lst_values)

    conf = input('Add this record to the database? \n (y) yes   (n) no \n\n>>> ')
    if conf.lower() == 'y':
        cursor.execute(f'INSERT INTO {table} ({str_lst_fields}) VALUES {data_bind}',tuple_values)
        # connection.commit()
        os.system('clear')
        print('\n-- Record Added --\n')
    else:
        os.system('clear')
        print('\n-- Action Cancelled --\n')

# mngr_add('4')




def mngr_update(table,identifier):
    pk = {
    'Users':'user_id',
    'Competencies':'competency_id',
    'Scores':'score',
    'Competency_Assessment_Data':'assessment_id',
    'Competency_Assessment_Results':'test_result_id'
    }
    some_id = pk[table]

    data = list(cursor.execute(f"SELECT * FROM {table} WHERE {some_id} = ?",(identifier,)).fetchone())
    names = list(map(lambda x: x[0], cursor.description))
    # print(data)
    os.system('clear')
    while True:
        print('Which field would you like to update?\n')
        # print('---------------------------------------')

        count = 1
        for i in names:
            if str(i) == 'password':
                print(f"({count}) {str(i).replace('_',' ') + ':':17} {'#####...'}")
                count += 1
                continue
            
            if i == 'active':
                if str(data[count - 1]) == '1':
                    print(f"({count}) {'active status:':17} {'active'}")
                    count += 1
                    continue
                elif str(data[count-1]) == '0':
                    print(f"({count}) {'active status:':17} {'inactive'}")
                    count += 1
                    continue

            print(f"({count}) {str(i).replace('_',' ') + ':':17} {data[count-1]}")
            count += 1


        col_name = input('\n>>> ')

        if col_name.isdigit() == True and col_name != '': 
            if int(col_name) in range(len(names)+1):
                os.system('clear')
                break
        if col_name == '':
            os.system('clear')
            return
        else:
            os.system('clear')
            print('-- Error: must select number from the following options --\n')

    col_name = names[int(col_name) - 1]
    # print(col_name)

    # update_val = input(f"Enter the new {str(col_name).replace('_',' ')}: ")
    

    # for i in names:
    #     os.system('clear')
    #     # print(i)
    #     lst_fields.append(i)
    while True:
        if col_name == 'competency_id':
            os.system('clear')
            update_val = int_pk_check(col_name,table)
            # lst_values.append(pk_check(i,table))
            break

        if col_name == 'user_id' and table == 'Users':
            os.system('clear')
            update_val = int_pk_check(col_name,table)
            break

        if col_name == 'assessment_id':
            os.system('clear')
            update_val = int_pk_check(col_name,table)
            break

        if col_name == 'test_result_id':
            os.system('clear')
            update_val = int_pk_check(col_name,table)
            break

        if col_name == 'email':
            os.system('clear')
            while True:
                ans = input('Enter a email: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: email cannot be blank --\n')
                    continue
                if check_for_dupl_2('email','Users',ans) == 'error':
                    os.system('clear')
                    print('-- Error: email already in use --\n')
                    continue

                else:
                    update_val = ans
                    break
            break
        
        if col_name == 'password':
            os.system('clear')
            while True:
                ans = input('Enter a password: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                if ans != '':
                    side_store_pw = ans
                    password = ans
                    byte_pwd = password.encode('utf-8')
                    my_salt = bcrypt.gensalt()
                    ans = bcrypt.hashpw(byte_pwd,my_salt)
                    update_val = ans
                    break
            break
        
        if col_name == 'active':
            break

        if col_name == 'user_type':
            os.system('clear')
            ans = input('Select user type: \n (1) user   (2) manager \n\n>>> ')
            if ans == '2':
                update_val = 'manager'
                break
            else:
                update_val = 'user'
                break

        if 'date' in col_name:
            if col_name == 'date_taken':
                while True:
                    ans = input(f"Enter the {str(i).replace('_',' ')} in the following format (YYYY-MM-DD hh:mm:ss): ")
                    if ans == '':
                        os.system('clear')
                        print('-- Error: field cannot be blank --\n')
                        continue
                    else:
                        update_val = ans
                        break
            else:
                os.system('clear')
                ans = input(f"Enter the {str(i).replace('_',' ')} in the following format (YYYY-MM-DD hh:mm:ss): ")
                update_val = ans
                break

            break

        if col_name == 'user_id' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter a user id: ")
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                    continue
                if check_valid_fk(col_name,table,ans) == 'error':
                    os.system('clear')
                    print('-- Error: user_id not found --\n')
                    continue
                else:
                    update_val = ans
                    break
            break

        if col_name == 'assessment' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter an assessment id: ")
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                    continue
                if check_valid_fk(i,table,ans) == 'error':
                    os.system('clear')
                    print('-- Error: assessment_id not found. Must select an active test --\n')
                    continue
                else:
                    update_val = ans
                    break
            break

        if col_name == 'competency_type' and table == 'Competency_Assessment_Data':
            os.system('clear')
            while True:
                format_to_table(cursor.execute('SELECT * FROM Competencies').fetchall())
                print()
                print()
                ans = input("Assign to which competency? Enter a competency id: ")
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                    continue
                if check_valid_fk(col_name,table,ans) == 'error':
                    os.system('clear')
                    print('-- Error: competency id not found --\n')
                    continue
                else:
                    update_val = ans
                    break
            break

        if col_name == 'score' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter the user's score: ")
                if ans.isdigit() == False and ans != '':
                    os.system('clear')
                    print('-- Error: invalid score input --\n')
                    # input('enter to continue (in option 1)')
                    continue
                if check_valid_fk(i,'Scores',ans) == 'error':
                    os.system('clear')
                    print('-- Error: invalid score input --\n')
                    # input('enter to continue (in option 2)')
                    continue
                if ans == '':
                    update_val = '-'
                    break
                else:
                    update_val = ans
                    break
            break

        if col_name == 'manager' and table == 'Competency_Assessment_Results':
            os.system('clear')
            while True:
                ans = input("Enter the manager's user id: ")
                if check_valid_mngr(ans) == 'error':
                    os.system('clear')
                    print('-- Error: invalid user id --\n')
                    continue
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n ')
                    continue
                else:
                    update_val = ans
                    break
            break

        if col_name == 'name' and table == 'Competencies':
            while True:
                ans = input('Enter name of the competency: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                else:
                    update_val = ans
                    break
            break
        
        if col_name == 'name' and table == 'Competency_Assessment_Data':
            while True:
                ans = input('Enter a name for the assessment: ')
                if ans == '':
                    os.system('clear')
                    print('-- Error: field cannot be blank --\n')
                else:
                    update_val = ans
                    break
            break
        
        else:
            update_val = input(f"Enter the new {str(col_name).replace('_',' ')}: ")
            break

    os.system('clear')

    if col_name == 'password':
        print(f'Update password to: {side_store_pw}? \n (y) yes   (n) no \n')
    if col_name == 'active':
        print(f"Make user active? \n (y) yes   (n) no \n")
    else:
        print(f"Update {str(col_name).replace('_',' ')} to: {update_val}? \n (y) yes   (n) no \n")
    
    conf = input('>>> ')

    if conf.lower() == 'y' and col_name == 'active':
        update_val = '1'
        cursor.execute(f"""
        UPDATE {table} SET {col_name} = ? WHERE {some_id} = ?""",(update_val,identifier))
        connection.commit()
        os.system('clear')
        print('-- Record Updated --\n')
    if conf.lower() == 'n' and col_name == 'active':
        update_val = '0'
        cursor.execute(f"""
        UPDATE {table} SET {col_name} = ? WHERE {some_id} = ?""",(update_val,identifier))
        connection.commit()
        os.system('clear')
        print('-- Record Updated --\n')
    elif conf.lower() == 'y':
        cursor.execute(f"""
        UPDATE {table} SET {col_name} = ? WHERE {some_id} = ?""",(update_val,identifier))
        connection.commit()
        os.system('clear')
        print('-- Record Updated --\n')
    else:
        os.system('clear')
        print('-- Action Cancelled --\n')


def delete_assessment():
    os.system('clear')
    while True:
        print("Enter the test result id of the record you would like to delete: \n")
        format_to_table(cursor.execute("""SELECT car.user_id as 'User Id', u.first_name as 'Employee Name', car.assessment as 'Assmt Id', cad.name as 'Assessment Name', car.score as 'Score', car.date_taken as 'Date Taken', car.test_result_id as 'Test Result Id'
        FROM Competency_Assessment_Results as car
        JOIN Competency_Assessment_Data as cad
        ON car.assessment = cad.assessment_id
        JOIN Users as u
        ON car.user_id = u.user_id;""").fetchall())
        print()
        select = input('\n>>> ')

        if select == '':
            os.system('clear')
            return

        if check_valid_fk('test_result_id','Competency_Assessment_Results',select) == 'all good':
            os.system('clear')
            break
        else:
            os.system('clear')
            print('-- Error: unrecognized test result id --\n')
    
    format_to_table(cursor.execute("""SELECT car.user_id as 'User Id', u.first_name as 'Employee Name', car.assessment as 'Assmt Id', cad.name as 'Assessment Name', car.score as 'Score', car.date_taken as 'Date Taken', car.test_result_id as 'Test Result Id'
    FROM Competency_Assessment_Results as car
    JOIN Competency_Assessment_Data as cad
    ON car.assessment = cad.assessment_id
    JOIN Users as u
    ON car.user_id = u.user_id 
    WHERE test_result_id = ?""",(select,)).fetchall())
    print()
    print()
    conf = input('Delete this record from the database? \n (y) yes   (n) no \n\n>>> ')
    
    if conf.lower() == 'y':
        cursor.execute('DELETE FROM Competency_Assessment_Results WHERE test_result_id == ?',(select,))
        connection.commit()
        os.system('clear')
        print('-- Record Deleted --\n')
    else:
        os.system('clear')
        print('-- Action Cancelled --\n')

# delete_assessment()
# mngr_update('Competency_Assessment_Results','1')

def generate_csv():
    user_sel = input('Select which file you would like to export: \n (1) Competencies \n (2) Competency Assessment Data \n (3) Users \n (4) Compentcy Assessment Results\n\n>>> ')

    if user_sel == '':
        os.system('clear')
        return

    if user_sel == '1':
        data = cursor.execute("SELECT * FROM Competencies")
        names = list(map(lambda x: x[0], cursor.description))

        lst_of_lsts = [names]

        for i in data:
            lst_of_lsts.append(list(i))

        with open('Competencies.csv', 'w') as comp_csv:
            wrt = csv.writer(comp_csv)
            wrt.writerows(lst_of_lsts)

        os.system('clear')
        print('-- CSV file generated named : Competencies.csv --\n')

    if user_sel == '2':
        data = cursor.execute("SELECT * FROM Competency_Assessment_Data")
        names = list(map(lambda x: x[0], cursor.description))

        lst_of_lsts = [names]

        for i in data:
            lst_of_lsts.append(list(i))

        with open('Comp_Assess_Data.csv', 'w') as comp_csv:
            wrt = csv.writer(comp_csv)
            wrt.writerows(lst_of_lsts)

        os.system('clear')
        print('-- CSV file generated named : Comp_Assess_Data.csv --\n')

    if user_sel == '3':
        data = cursor.execute("SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type  FROM Users")
        names = list(map(lambda x: x[0], cursor.description))

        lst_of_lsts = [names]

        for i in data:
            lst_of_lsts.append(list(i))

        with open('Users.csv', 'w') as comp_csv:
            wrt = csv.writer(comp_csv)
            wrt.writerows(lst_of_lsts)

        os.system('clear')
        print('-- CSV file generated named : Users.csv --\n')
    
    if user_sel == '4':
        data = cursor.execute("SELECT * FROM Competency_Assessment_Results")
        names = list(map(lambda x: x[0], cursor.description))

        lst_of_lsts = [names]

        for i in data:
            lst_of_lsts.append(list(i))

        with open('Comp_Assess_Results.csv', 'w') as comp_csv:
            wrt = csv.writer(comp_csv)
            wrt.writerows(lst_of_lsts)

        os.system('clear')
        print('-- CSV file generated named : Comp_Assess_Results.csv --\n')


# generate_csv()

# for Competency_Assessment_Results
# def import_csv():

def import_csv():
    conf = input('Import data from the Import_Comp_Results.csv? \n*** NOTE: This will permanately delete currently existing data in the Competency Assessement Results table.\n\n (y) yes   (n) no \n\n>>> ')

    if conf.lower() == 'y':
        with open('Import_Comp_Results.csv', 'r') as csvfile:
            results = []
            for line in csvfile:
                words = line.split(',')
                results.append(words)

            num_values = len(results.pop(0))

            cursor.execute("PRAGMA foreign_keys = OFF;")
            cursor.execute('DROP TABLE Competency_Assessment_Results;')
            cursor.execute("""CREATE TABLE Competency_Assessment_Results (
            'user_id' INTEGER,
            'assessment' INTEGER,
            'score' INTEGER,
            'date_taken' TEXT NOT NULL,
            'manager' INTEGER,
            'test_result_id' INTEGER PRIMARY KEY,
            FOREIGN KEY (user_id) REFERENCES Users (user_id),
            FOREIGN KEY (assessment) REFERENCES Competency_Assessment_Data (assessment_id),
            FOREIGN KEY (score) REFERENCES Scores (score),
            FOREIGN KEY (manager) REFERENCES Users (user_id));""")

            if num_values == 4:
                for i in results:
                    try:
                        i = list(i)
                        # print(i[0],i[1],i[2],i[3])
                        cursor.execute(f'''INSERT INTO Competency_Assessment_Results (user_id, assessment,score, date_taken) VALUES (?,?,?,?)''',(i[0],i[1],i[2],i[3]))
                    except:
                        continue
                cursor.execute('PRAGMA foreign_keys = ON;')
                connection.commit()
                os.system('clear')
                print('-- Data Imported --\n')

            if num_values == 5:
                for i in results:
                    try:
                        i = list(i)
                        # print(i[0],i[1],i[2],i[3])
                        cursor.execute(f'''INSERT INTO Competency_Assessment_Results (user_id, assessment,score, date_taken,manager) VALUES (?,?,?,?,?)''',(i[0],i[1],i[2],i[3],i[4]))
                    except:
                        continue
                cursor.execute('PRAGMA foreign_keys = ON;')
                connection.commit()
                os.system('clear')
                print('-- Data Imported --\n')
            
            if num_values == 6:
                for i in results:
                    try:
                        i = list(i)
                        # print(i[0],i[1],i[2],i[3])
                        # print(i[4])
                        # input('enter to continue')
                        cursor.execute(f'''INSERT INTO Competency_Assessment_Results (user_id, assessment,score, date_taken,manager,test_result_id) VALUES (?,?,?,?,?,?)''',(i[0],i[1],i[2],i[3],i[4],i[5]))
                    except:
                        continue
                cursor.execute('PRAGMA foreign_keys = ON;')
                connection.commit()
                os.system('clear')
                print('-- Data Imported --\n')
            
    else:
        os.system('clear')
        print('-- Action Cancelled --\n')


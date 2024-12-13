import mysql.connector as con

mycon = con.connect(host="localhost", user="root", passwd="password", database="messdatabase")
if mycon.is_connected():
    print("Successfully connected to MySQL db")
else:
    print("Connection Unsuccessful")

cursor = mycon.cursor()

def execute(command):
    cursor.execute(command)

execute("Drop table MealHistory")
execute("Drop table StudentMessDetails")
execute("Drop table Menu")
execute("Drop table Login")

t1 = "CREATE TABLE StudentMessDetails(RegNo VARCHAR(7) PRIMARY KEY, RollNo VARCHAR(8) UNIQUE, Name VARCHAR(30), Mess VARCHAR(15))"
t2 = "CREATE TABLE MealHistory(SerialNo INT AUTO_INCREMENT PRIMARY KEY, RegNo VARCHAR(7), FOREIGN KEY (RegNo) REFERENCES StudentMessDetails(RegNo), MealDate DATE, Meal VARCHAR(9))"
t3 = "Create table Menu(DayNum INT, Mess VARCHAR(11), Meal VARCHAR(9), Items VARCHAR(200))"
t4 = "CREATE TABLE Login(User VARCHAR(15) PRIMARY KEY, Password VARCHAR(30))"
execute(t1)
execute(t2)
execute(t3)
execute(t4)

studentInfo = ("('2210226', '221AI004', 'Swati M', 'Girls Mess1')", 
               "('2310449', '231EC208', 'Ashmita Das', 'Girls Mess1')", 
               "('2310465', '231EE247', 'Sahasra Pulumati', 'Girls Mess1')", 
               "('2410226', '241MN023', 'Shreyas Kaluri', 'Boys Mess2')", 
               "('2110006', '211CS107', 'Joshua Seth', 'Boys Mess1')")
mealInfo = ('("2210226", "2024-10-02", "Breakfast")',
            '("2310449","2024-10-03", "Lunch")')
loginInfo = ("('Girls Mess1', 'Password')", 
             "('Girls Mess2', 'Password')", 
             "('Boys Mess1', 'Password')", 
             "('Boys Mess2', 'Password')",
             "('Hostel Office', 'Password')")

for i in studentInfo:
    x = 'insert into studentmessdetails values' + i
    execute(x)
for i in mealInfo:
    x = 'insert into mealhistory (RegNo, MealDate, Meal) values' + i
    execute(x)
for i in loginInfo:
    x = 'insert into login values' + i
    execute(x)


mess = ["Girls Mess1", "Girls Mess2", "Boys Mess1", "Boys Mess2"]
meals = ["Breakfast", "Lunch", "Snacks", "Dinner"]
for i in range(1,8,1):
    for j in mess:
        for k in meals:
            query = "Insert into Menu values ('{}','{}','{}','')".format(i,j,k)
            execute(query)

mycon.commit()
mycon.close()

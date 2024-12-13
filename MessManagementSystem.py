from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector as con
import datetime


# Node class for creating nodes in linked lists
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Create a LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    # Method to insert a node at the beginning of the linked list
    def insertAtBegin(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    # Method to remove first node of linked list
    def remove_first_node(self):
        if(self.head == None):
            return
        self.head = self.head.next

    # Method to delete the entire linked list
    def delete_entire_list(self):
        while self.head is not None:
            self.remove_first_node()  # Remove each node starting from the head

    # Method to search for a node with specific data and return True/False
    def search(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                return True
            current_node = current_node.next
        return False 

    
    # Method to return the size of linked list
    def sizeOfLL(self):
        size = 0
        if(self.head):
            current_node = self.head
            while(current_node):
                size = size+1
                current_node = current_node.next
            return size
        else:
            return 0

    # Method to print the linked list data
    def printLL(self):
        current_node = self.head
        while(current_node):
            print(current_node.data)
            current_node = current_node.next


# Double node class for creating nodes in a doubly linked list
class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None 


# Circular Doubly Linked List class
class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None 
   
    # Method to insert a node at the end of the list
    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            # List is empty, new_node points to itself
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            tail = self.head.prev  # Last node in the list
            new_node.next = self.head  # New node's next is the head
            new_node.prev = tail  # New node's prev is the last node
            tail.next = new_node  # Last node's next is the new node
            self.head.prev = new_node  # Head's prev is the new node

    # Method to delete a specific node 
    def delete_node(self, node):
        if self.head is None or node is None:
            return  # If the list is empty or node is None, do nothing
        
        if node == self.head and self.head.next == self.head:
            # Case when there is only one node in the list
            self.head = None
        else:
            prev_node = node.prev
            next_node = node.next
            prev_node.next = next_node
            next_node.prev = prev_node

            if node == self.head:
                self.head = next_node  # Update the head if the deleted node was the head

        node = None  # Delete the node


#Linked list object that interacts with sql
class dataLL(LinkedList):
    def __init__(self):
        super().__init__()

    #Creates a linked list of students who belong to a specific mess(user)
    def makeMessRegNoLL(self,user):
        query = "Select RegNo from StudentMessDetails where Mess = '"+user+"'"
        cur.execute(query)
        regNos = cur.fetchall()
        for i in regNos:
            self.insertAtBegin(i[0])

    #Creates a linked list of all the students who already completed the current meal
    def makeMealCompletedLL(self,meal, date):
        query = "Select RegNo from MealHistory where MealDate='{}' and Meal='{}'".format(date,meal)
        cur.execute(query)
        regNos = cur.fetchall()
        for i in regNos:
            self.insertAtBegin(i[0])
    
    #Data from linked list of new students is added to StudentMessDetails, checks for duplicate RegNo and RollNo
    def writeStudentMessDetails(self):
        sql = "Insert into StudentMessDetails values (%s, %s, %s, %s)"
        current_node = self.head
        
        while current_node:
            row = current_node.data
            
            # Check for duplicate registration number
            check_reg = "SELECT COUNT(*) FROM StudentMessDetails WHERE RegNo = %s"
            cur.execute(check_reg, (row[0],))
            reg_exists = cur.fetchone()[0] > 0
            
            # Check for duplicate roll number
            check_roll = "SELECT COUNT(*) FROM StudentMessDetails WHERE RollNo = %s"
            cur.execute(check_roll, (row[1],))
            roll_exists = cur.fetchone()[0] > 0
            
            if reg_exists:
                messagebox.showinfo("Duplicate Entry", f"Registration number {row[0]} already exists. Ignoring.")
            elif roll_exists:
                messagebox.showinfo("Duplicate Entry", f"Roll number {row[1]} already exists. Ignoring.")
            else:
                cur.execute(sql, row)  # Only insert if no duplicates found

            # Remove node after processing the current one
            self.remove_first_node()
            current_node = current_node.next  # Move to the next node
        
        mycon.commit()  # Commit once after processing all records

    #Data from linked list of students who have eaten the current meal is added to MealHistory table        
    def writeMealHistory(self):
        sql = "Insert into MealHistory (RegNo, MealDate, Meal) values " #('','','','')
        current_node = self.head
        while current_node:
            row = current_node.data

            # Check for duplicate registration number
            check_reg = "SELECT COUNT(*) FROM MealHistory WHERE RegNo = '{}' and MealDate = '{}' and Meal = '{}'".format(row[0], row[1], row[2])
            cur.execute(check_reg)
            reg_exists = cur.fetchone()[0] > 0
            if reg_exists == 0:
                rowText = "('{}','{}','{}')".format(row[0],row[1],row[2])
                cur.execute(sql+rowText)
            else:
                messagebox.showerror("Error", 'Duplicate entry. Ignored.')
            self.remove_first_node()
            current_node = current_node.next
        mycon.commit()

    def removeFromStudentMessDetails(self):
        current_node = self.head
        while current_node:
            delSQL = "DELETE FROM StudentMessDetails WHERE RegNo = '{}'".format(current_node.data)
            cur.execute(delSQL)
            self.remove_first_node()
            current_node = current_node.next
        mycon.commit()

    def updateStudentMessDetails(self): 
        current_node = self.head
        while current_node:
            updateSQL = "UPDATE StudentMessDetails SET mess = '{}' WHERE RegNo = '{}'".format(current_node.data[1],current_node.data[0])
            cur.execute(updateSQL)
            self.remove_first_node()
            current_node = current_node.next
        mycon.commit()

#Circular doubly linked list object that interacts with sql
class dataCDLL(CircularDoublyLinkedList):
    def __init__(self):
        super().__init__()

    #Creates a doubly circular linked list of the menus of a week of the specified mess(user)
    def readMenu(self, user):
        query = "Select daynum, meal, items from Menu where mess='{}'".format(user)
        cur.execute(query)
        menuRows = cur.fetchall()
        for i in range(0,len(menuRows),4):
            dayList = [menuRows[i], menuRows[i+1], menuRows[i+2],menuRows[i+3]]
            self.insert_at_end(dayList)
    
    def updateMenu(self,dayNum, user, meal, items):
        updatsql="UPDATE Menu set items='{}' where daynum={} and mess='{}' and meal='{}'".format(items,dayNum,user,meal)
        cur.execute(updatsql)
        mycon.commit()

# Used in making mess drop down box
def makeMessArray():
    query = "Select user from login where user != 'Hostel Office'"
    cur.execute(query)
    users = cur.fetchall()
    messArray = []
    for i in users:
        messArray.append(i[0])
    return messArray

#Changing the mainframes, called in next and back
def changePage(n, user="none"):
    for widgets in root.winfo_children():
        widgets.destroy()

    if n == 1:
        loginPage()

    elif n == 2 and user != "Hostel Office":
        messPage(user)

    elif n == 2 and user == "Hostel Office":
        hostelOfficePage()

def exitProgram():
    root.destroy()   

def changePassword(user, actFrm):

    def set_pass():
        query = "Select password from login where user='{}'".format(user)
        cur.execute(query)
        old = cur.fetchone()[0]
        if old != oldPass.get():
            messagebox.showerror('Error', 'Please enter correct old password.')
        elif newPass.get() != confirmPass.get():
            messagebox.showerror('Error', 'New password does not match confirm password.')
        elif (len(newPass.get()) > 30):
            messagebox.showerror('Error', 'Exceeding limit of 30 characters.')
        elif(newPass.get() == oldPass.get()):
            messagebox.showerror('Error', 'Please enter a new password.')
        elif (len(newPass.get()) == 0):
            messagebox.showerror('Error', 'Enter new password.')
        else:
            update_pass = "Update login set password = '{}' where user='{}'".format(newPass.get(), user)
            cur.execute(update_pass)
            mycon.commit()
            messagebox.showinfo('Password', 'Password update is successful')
            oldPass.delete(0,END)
            newPass.delete(0,END)
            confirmPass.delete(0,END)

    Label(actFrm, text='Old Password').grid(row=0, column=0, sticky='w')
    Label(actFrm, text='New Password').grid(row=1, column=0, sticky='w')
    Label(actFrm, text='Confirm Password').grid(row=2, column=0, sticky='w')
    
    oldPass = Entry(actFrm, width=30, show='*')
    oldPass.grid(row=0, column=1, sticky='w', padx=5, pady=10)
    newPass = Entry(actFrm, width=30, show='*')
    newPass.grid(row=1, column=1, sticky='w', padx=5, pady=10)
    confirmPass = Entry(actFrm, width=30, show='*')
    confirmPass.grid(row=2, column=1, sticky='w', padx=5, pady=10)

    Button(actFrm, text='Set Password', command=lambda: set_pass(), width=15).grid(row=3, column=0, pady=10, sticky='w')

def loginPage():
    F1 = Frame(root)
    F1.rowconfigure(0, weight=1, minsize=100)
    F1.rowconfigure(1, weight=1, minsize=150)
    F1.rowconfigure(2, weight=1, minsize=70)
    F1.rowconfigure(3, weight=1, minsize=180)
    F1.columnconfigure(0, weight=1, minsize=750)

    titleFrm = Frame(master=F1, borderwidth=1)
    Label(master=titleFrm, text='Login', font=('Georgia', 30)).pack()
    titleFrm.grid(row=0, column=0, sticky='nsew')

    passFrm = Frame(master=F1, borderwidth=1)
    Label(master=passFrm, text='Username', width=10).grid(row=0, column=0, sticky='nse', pady=10)
    usernmTxt = Entry(master=passFrm, width=20)
    Label(master=passFrm, text='Password', width=10).grid(row=1, column=0, sticky='nse')
    passwdTxt = Entry(master=passFrm, width=20, show='*')
    usernmTxt.grid(row=0, column=1, sticky='nsw', pady=10)
    passwdTxt.grid(row=1, column=1, sticky='nsw')
    passFrm.grid(row=1, column=0, sticky='s')

    #  Checks if entered username and password are correct
    def checkPass():
        UN = usernmTxt.get()
        PW = passwdTxt.get()
        cur.execute('Select user, password from login')
        loginInfo = cur.fetchall()
        for i in loginInfo:
            if i[0] == UN and i[1] == PW:
                changePage(2, UN)
                break
        else:
            messagebox.showerror("Error", 'Wrong username and/or password.')

    Button(master=passFrm, text='Enter', width=5, command=checkPass).grid(row=1, column=2, sticky='nsw', padx=2)

    #  Show password checkbox
    chkFrm = Frame(F1, borderwidth=1)
    chkFrm.grid(row=2, column=0, pady=5)

    def show():
        if var.get() == 1:
            passwdTxt.config(show='')
        else:
            passwdTxt.config(show='*')

    var = IntVar()
    Checkbutton(chkFrm, text='Show Password', variable=var, command=show).pack()
    F1.pack()

# Three sub pages: 
# Meal - Takes student RegNo for every meal and validates it
# Menu - Displays each day's menu, provides function to update it
# Password - Change password
def messPage(user):
    F2 = Frame(root)
    F2.rowconfigure(0, weight=1, minsize=500)
    F2.columnconfigure(0, weight=1, minsize=100)
    F2.columnconfigure(1, weight=1, minsize=650)

    # Options frame
    optFrm = Frame(F2, bd=1, relief=RAISED)
    # Activity frame
    actFrm = Frame(F2)

    # List of students belonging to specified mess
    validStudentsLL=dataLL()

    # Helper function to write to database and then execute a given function: Meal, Menu, Password, Back, Exit
    def execute_with_db_update(action):
        validStudentsLL.writeMealHistory()
        action()

    def clear_actFrm():
        for widgets in actFrm.winfo_children():
            widgets.destroy()

    def Meal():
        clear_actFrm()

        # Checks if the RegNo is valid, entered within the meal timings and has already eaten the current meal or not
        def validateRegNo():
            meal = "invalid"
            currentTime = datetime.datetime.now()
            hour= int(currentTime.strftime("%H"))
            minutes=int(currentTime.strftime("%M"))
            date = currentTime.strftime('%Y-%m-%d')
            time_in_minutes = hour * 60 + minutes

            if 420 <=time_in_minutes <=900: #change to 600
                meal = "Breakfast"
            elif 720 <= time_in_minutes <= 840:
                meal = "Lunch"
            elif 990 <= time_in_minutes < 1080:
                meal = "Snacks"
            elif 1170 <= time_in_minutes <= 1320:
                meal = "Dinner"

            #Updates the database if list size is 20 or the meal timing is over
            if validStudentsLL.sizeOfLL() == 2 or meal == "invalid": 
                validStudentsLL.writeMealHistory() 

            if meal == "invalid":
                messagebox.showerror("Error", 'Mealtime is over')
                return
            
            # Checks if student is registered to the mess
            regNo = regNoInput.get()
            regNoInput.delete(0,END)
            if not (studentsLL.search(regNo)):
                messagebox.showerror("Error", 'Invalid RegNo')
                return
            
            # Checks if the student has eaten the current meal or not
            alreadyEatenLL = dataLL()
            alreadyEatenLL.makeMealCompletedLL(meal,date)
            
            if not (alreadyEatenLL.search(regNo)):
                validStudentsLL.insertAtBegin([regNo, date, meal])
            else:
                messagebox.showerror("Error", 'Meal already eaten')

            
        studentsLL = dataLL()
        studentsLL.makeMessRegNoLL(user)

        Label(actFrm, text="Registration No").grid(row=0, column=0, sticky='w')
        regNoInput = Entry(actFrm, width=20, borderwidth=2)
        regNoInput.grid(row=0, column=1, pady=20, sticky='ew')
        Button(actFrm, text='Enter', command=lambda: validateRegNo(), width=9).grid(row=1, column=0, padx=5, sticky='ew')       
    

    def Menu():
        clear_actFrm()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        def getInfoFromNode(Node):
            menuInfo = Node.data
            dayNum = menuInfo[0][0]
            day = days[dayNum-1]
            return [day, menuInfo]
        
        def updateMenuDisplay(node):
            nonlocal menuInfo 
            menuInfo = getInfoFromNode(node)
            day_label.config(text=menuInfo[0])   # Update day

            #Update Items
            breakfast_items_text.delete(1.0, END)
            lunch_items_text.delete(1.0, END)
            snacks_items_text.delete(1.0, END)
            dinner_items_text.delete(1.0, END)

            breakfast_items_text.insert('1.0',menuInfo[1][0][2])
            lunch_items_text.insert('1.0',menuInfo[1][1][2])
            snacks_items_text.insert('1.0',menuInfo[1][2][2])
            dinner_items_text.insert('1.0',menuInfo[1][3][2])
        
        def nextDayMenu():
            nonlocal currentNode  # Access the currentNode from outer scope
            currentNode = currentNode.next  
            updateMenuDisplay(currentNode)  
            
        def prevDayMenu():
            nonlocal currentNode
            currentNode = currentNode.prev  
            updateMenuDisplay(currentNode)  

        def updateMenuInfo(meal):
            updatedItems = ""
            mealName = ""
            if meal == 0:
                updatedItems = breakfast_items_text.get('1.0', "end-1c")
                mealName = "Breakfast"
            elif meal == 1:
                updatedItems = lunch_items_text.get('1.0', "end-1c")
                mealName = "Lunch"
            elif meal == 2:
                updatedItems = snacks_items_text.get('1.0', "end-1c")
                mealName = "Snacks"
            elif meal == 3:
                updatedItems = dinner_items_text.get('1.0', "end-1c")
                mealName = "Dinner"
            
            dayNum = days.index(menuInfo[0])+1
            menuInfo[1][meal] = (dayNum, mealName, updatedItems)
            messMenuLL.updateMenu(dayNum,user,mealName,updatedItems)

        messMenuLL=dataCDLL()
        messMenuLL.readMenu(user)

        currentNode = messMenuLL.head

        menuInfo = getInfoFromNode(currentNode)

        # Create and display labels with menu info
        day_label = Label(actFrm, text=menuInfo[0], font=('Georgia', 14), width=9)
        day_label.grid(row=0, column=0, sticky='w')

        Label(actFrm, text="Breakfast").grid(row=1, column=0, sticky='w')
        Label(actFrm, text="Lunch").grid(row=2, column=0, sticky='w')
        Label(actFrm, text="Snacks").grid(row=3, column=0, sticky='w')
        Label(actFrm, text="Dinner").grid(row=4, column=0, sticky='w')
        
        breakfast_items_text = Text(actFrm, height=3, width=50) 
        breakfast_items_text.insert('1.0',menuInfo[1][0][2])#,text=menuInfo[1][0][2])
        breakfast_items_text.grid(row=1, column=1, sticky='w')

        lunch_items_text = Text(actFrm, height=3, width=50)#text=menuInfo[1][1][2])
        lunch_items_text.insert('1.0',menuInfo[1][1][2])
        lunch_items_text.grid(row=2, column=1, sticky='w')

        snacks_items_text = Text(actFrm, height=3, width=50)#text=menuInfo[1][2][2])
        snacks_items_text.insert('1.0',menuInfo[1][2][2])
        snacks_items_text.grid(row=3, column=1, sticky='w')

        dinner_items_text = Text(actFrm, height=3, width=50) #text=menuInfo[1][3][2])
        dinner_items_text.insert('1.0',menuInfo[1][3][2])
        dinner_items_text.grid(row=4, column=1, sticky='w')

        Button(actFrm, text='Update breakfast', command=lambda: updateMenuInfo(0), width=15).grid(row=1, column=2, sticky='w',pady=10, padx=5)
        Button(actFrm, text='Update lunch', command=lambda: updateMenuInfo(1), width=15).grid(row=2, column=2, sticky='w',pady=10, padx=5)
        Button(actFrm, text='Update snacks', command=lambda: updateMenuInfo(2), width=15).grid(row=3, column=2, sticky='w',pady=10, padx=5)
        Button(actFrm, text='Update dinner', command=lambda: updateMenuInfo(3), width=15).grid(row=4, column=2, sticky='w',pady=10, padx=5)

        # Create Next and Previous buttons with corresponding commands
        Button(actFrm, text='Next', command=nextDayMenu, width=10).grid(row=5, column=1, sticky='w', pady=10)
        Button(actFrm, text='Prev', command=prevDayMenu, width=10).grid(row=5, column=0, sticky='w', pady=10, padx=5)

    def Password():
        clear_actFrm()
        changePassword(user,actFrm)

    actFrm.grid(row=0, column=1, sticky='nws', ipadx=50, pady=10)

    Button(optFrm, text='Begin Meal', command=lambda: execute_with_db_update(Meal), width=9).grid(row=0, column=0, padx=10, pady=10)
    Button(optFrm, text='Menu', command=lambda: execute_with_db_update(Menu), width=9).grid(row=1, column=0, pady=10)
    Button(optFrm, text='Change Password', command=lambda: execute_with_db_update(Password), width=9, wraplength=90).grid(row=2, column=0, pady=10)

    bottomFrm = Frame(optFrm)
    Button(bottomFrm, text='Back', command=lambda: execute_with_db_update(changePage(1)), width=9).grid(row=1, column=0, sticky='s', pady=10)
    Button(bottomFrm, text='Exit', command=lambda: execute_with_db_update(exitProgram), width=9).grid(row=2, column=0, sticky='s', pady=10)

    bottomFrm.grid(row=4, column=0, sticky='s', pady=205)
    optFrm.grid(row=0, column=0, sticky='nsw')

    F2.pack()

# Four sub pages:
# AddStudents - Add new students and their details to the database
# RemoveStudents - Remove students from the database
# UpdateMess - Change the mess
# Password - Change password
def hostelOfficePage():
    F3 = Frame(root)
    F3.rowconfigure(0, weight=1, minsize=500)
    F3.columnconfigure(0, weight=1, minsize=100)
    F3.columnconfigure(1, weight=1, minsize=650)

    # Contains buttons
    optFrm = Frame(F3, bd=1, relief=RAISED)
    # Activity frame
    actFrm = Frame(F3)

    def clear_actFrm():
        for widgets in actFrm.winfo_children():
            widgets.destroy()

    # List used for drop down box
    messArray = makeMessArray()


    def AddStudents():
        newStudentsList = dataLL()
        clear_actFrm()
        Label(actFrm, text="Name").grid(row=0, column=0, sticky='w', pady=10)  
        nameTxt = Entry(actFrm, width=40)
        Label(actFrm, text="RegNo").grid(row=1, column=0, sticky='w', pady=10)
        regNoTxt = Entry(actFrm, width=40)
        Label(actFrm, text="RollNo").grid(row=2, column=0, sticky='w', pady=10)
        rollNoTxt = Entry(actFrm, width=40)
        Label(actFrm, text="Mess").grid(row=3, column=0, sticky='w', pady=10)
        messTxt = ttk.Combobox(actFrm, width=40, values=messArray, state="readonly")
        nameTxt.grid(row=0, column=1, sticky='w')
        regNoTxt.grid(row=1, column=1, sticky='w')
        rollNoTxt.grid(row=2, column=1, sticky='w')
        messTxt.grid(row=3, column=1, sticky='w')

        def clear_text():
            nameTxt.delete(0, END)
            regNoTxt.delete(0, END)
            rollNoTxt.delete(0, END)
            messTxt.delete(0, END)

        #Add valid students to newStudentsList
        def addToLL():
            if (regNoTxt.get() != '' and rollNoTxt.get() != '' and nameTxt.get() != '' and messTxt.get() != ''):
                llist = [regNoTxt.get(),rollNoTxt.get(),nameTxt.get(),messTxt.get()]
                newStudentsList.insertAtBegin(llist)
                newStudentsList.printLL()
            clear_text()

        def addToDB():
            addToLL()
            newStudentsList.writeStudentMessDetails()
            clear_text()

        Button(actFrm, text="Add to List", command=lambda: addToLL()).grid(row=4, column=0, sticky='w', pady=10)
        Button(actFrm, text="Add to Database", command=lambda: addToDB()).grid(row=5, column=0, sticky='w', pady=10)


    def RemoveStudents():
        toRemoveLL = dataLL()
        clear_actFrm()
        Label(actFrm, text="RegNo").grid(row=0, column=0, sticky='w')
        regNoTxt = Entry(actFrm, width=40)
        regNoTxt.grid(row=0, column=1, sticky='w', pady=10)
        def clear_text():
            regNoTxt.delete(0, END)

        def addToLL():
            if regNoTxt.get() != '':
                regNo = regNoTxt.get()
                toRemoveLL.insertAtBegin(regNo)
            clear_text()

        def removeFromDB():
            addToLL()
            toRemoveLL.removeFromStudentMessDetails()
            clear_text()
            
        Button(actFrm, text="Add to List", command=lambda: addToLL()).grid(row=1, column=0, sticky='w',pady=10)
        Button(actFrm, text="Delete from Database", command=lambda: removeFromDB()).grid(row=2, column=0, sticky='w',pady=10)

    def UpdateMess():
        toUpdateLL = dataLL()
        clear_actFrm()
        Label(actFrm, text="RegNo").grid(row=0, column=0, sticky='w')
        Label(actFrm, text="New Mess").grid(row=1, column=0, sticky='w',pady=10)
        regNoTxt = Entry(actFrm, width=40)
        newmessTxt = ttk.Combobox(actFrm, width=40, values=messArray, state="readonly")
        regNoTxt.grid(row=0, column=1, sticky='w',pady=10)
        newmessTxt.grid(row=1, column=1, sticky='w',pady=10)
        
        def clear_text():
            regNoTxt.delete(0, END)
            newmessTxt.delete(0, END)

        def addToLL():
            if (regNoTxt.get() != '' and newmessTxt != ''):
                updaterInfo = [regNoTxt.get(),newmessTxt.get()]
                toUpdateLL.insertAtBegin(updaterInfo)
                toUpdateLL.printLL()
            clear_text()

        def updateDB():
            addToLL()
            toUpdateLL.updateStudentMessDetails()
            clear_text()
            
        Button(actFrm, text="Add to List", command=lambda: addToLL()).grid(row=4, column=0, sticky='w',pady=10)
        Button(actFrm, text="Update Database", command=lambda: updateDB()).grid(row=5, column=0, sticky='w',pady=10)

    def Password():
        clear_actFrm()
        changePassword("Hostel Office", actFrm)

    actFrm.grid(row=0, column=1, sticky='nws', padx=10, pady=10)

    Button(optFrm, text='Add Students', command=lambda: AddStudents(), width=9, wraplength=90).grid(row=0, column=0, padx=10, pady=10)
    Button(optFrm, text='Remove Students', command=lambda: RemoveStudents(), width=9, wraplength=90).grid(row=1, column=0, pady=10)
    Button(optFrm, text='Update Mess', command=lambda: UpdateMess(), width=9, wraplength=90).grid(row=2, column=0, pady=10)
    Button(optFrm, text='Change Password', command=lambda: Password(), width=9, wraplength=90).grid(row=3, column=0, pady=10)

    bottomFrm = Frame(optFrm)
    Button(bottomFrm, text='Back', command=lambda: changePage(1), width=9).grid(row=1, column=0, sticky='s', pady=10)
    Button(bottomFrm, text='Exit', command=lambda: exitProgram(), width=9).grid(row=2, column=0, sticky='s', pady=10)

    bottomFrm.grid(row=4, column=0, sticky='s', pady=190)
    optFrm.grid(row=0, column=0, sticky='nsw')

    F3.pack()

geometry = '750x500+500+10'
root = Tk()
root.geometry(geometry)
root.title('Project')
root.resizable(False, False)

mycon = con.connect(host="localhost", user="root", passwd="password", database="messdatabase")
if mycon.is_connected():
    cur = mycon.cursor()
    changePage(1) #login page
else:
    print("Connection Unsuccessful")

root.mainloop()
    

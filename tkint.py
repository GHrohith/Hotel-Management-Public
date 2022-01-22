import mysql.connector as sq
import tkinter as tk
from datetime import date, timedelta
from tkinter import messagebox

con = sq.connect(host="localhost", user="root", passwd="1234", database="iptest")
cur = con.cursor()


def mainscreen():
    frm2.pack()
    checkdate()

def checkdate():                                                      #To show
    global curdate
    cur.execute('desc bookings')
    ret = cur.fetchall()
    dateno = len(ret) - 1
    dat = []
    for (a, b, c, d, e, f) in ret:
        if not a.isalpha():
            dat.append(date(int(a[0:4]), int(a[5:7]), int(a[8:10])))
    dbdate = min(dat)
    curdate = date.today()
    reqdate = curdate - timedelta(days=1)
    delta = (reqdate - dbdate).days
    if delta != 0:
        if delta >= dateno:
            changdate = dateno
        else:
            changdate = delta
        deldatlis = ''
        adddatlis = ''
        for i in range(0, changdate):
            deldatlis += ('drop ' + (dbdate + timedelta(days=i)).strftime('%Y_%m_%d') + ',')
        deldatlis = deldatlis[0:-1]
        for i in range(0, changdate):
            adddatlis += ('add ' + (reqdate + timedelta(days=(i + dateno - changdate))).strftime('%Y_%m_%d') + ' int,')
        adddatlis = adddatlis[0:-1]
        delcol = 'alter table bookings ' + deldatlis
        addcol = 'alter table bookings ' + adddatlis
        cur.execute(delcol)
        cur.execute(addcol)
        con.commit()


def viewroom():
    cur.execute("select * from bookings")
    res = cur.fetchall()
    cur.execute("desc bookings")
    des = cur.fetchall()
    for i in range(len(des)):
        tk.Label(frm8, text=des[i][0], fg='orange', width=10, font=('times', 17, 'bold', 'underline'), bg="#e6ffff").grid(row=2,
                                                                                                            column=i)
    tk.Label(frm8, bg="#e6ffff").grid(row=3, column=1)
    for i in range(len(res)):
        for j in range(len(res[i])):
            if res[i][j]:
                tex = res[i][j]
            else:
                tex = '---'
            tk.Label(frm8, text=tex, fg='blue', font=('times', 15), bg="#e6ffff").grid(row=i + 4, column=j)
    frm2.forget()
    frm8.pack()


def viewcust():
    cur.execute("select * from customers")
    res = cur.fetchall()
    cur.execute("desc customers")
    des = cur.fetchall()
    for i in range(len(des)):
        tk.Label(frm9, text=des[i][0], fg='orange', width=10, font=('times', 20, 'bold', 'underline'), bg="#e6ffff").grid(row=2,
                                                                                                            column=i)
    tk.Label(frm9, bg="#e6ffff").grid(row=3, column=1)
    for i in range(len(res)):
        for j in range(len(res[i])):
            if res[i][j]:
                tex = res[i][j]
            else:
                tex = '---'
            tk.Label(frm9, text=tex, fg='blue', font=('times', 15), bg="#e6ffff").grid(row=i + 4, column=j)
    frm2.forget()
    frm9.pack()


def backtomain():
    frm8.forget()
    frm9.forget()
    frm2.pack()


def destroy():
    root.destroy()


def book():
    global roomids, roomdays
    frm2.pack_forget()
    frm3.pack()
    roomids = []
    roomdays = []


def getphone():
    global pho
    pho = phone.get()
    if not pho:
        messagebox.showwarning("Enter phone", "Enter phone number")
    else:
        check()


def check():
    global custid, name
    cur.execute("select exists(select * from customers where Phone=%s)" % (pho))
    data = cur.fetchall()
    if bool(data[0][0]) == False:
        nameenter()
    else:
        frm3.forget()
        cur.execute('select CustId, Name from customers where Phone=%s' % (pho))
        res = cur.fetchall()
        custid = res[0][0]
        name = res[0][1]
        getroom()


def nameenter():
    frm3.pack_forget()
    frm4.pack()


def getname():
    global name
    name = namefield.get()
    if not name:
        messagebox.showwarning("Enter name", "Enter name")
    else:
        newcust()


def newcust():
    global custid
    cur.execute("select max(CustId) from customers")
    custid = cur.fetchall()[0][0] + 1
    cur.execute("insert into customers values (%s,'%s',%s,0)" % (custid, name, pho))
    con.commit()
    getroom()


def getroom():
    frm4.forget()
    frm5.pack()





def getstaydat():
    global stayday
    stayday = staydays.get()
    if not stayday:
        messagebox.showwarning("Select", "Select an option")
    else:
        finstayday()


def finstayday():
    global roomt, sillabel, goldlabel, platlabel, roomdays
    roomdays.append(stayday)
    roomnos()
    sillabel = tk.Radiobutton(frm6, text='Silver\t( ' + str(silroomno) + ' rooms available )', variable=roomt, value=1,
                              font=('times', 30), cursor="hand2", bg="#e6ffff")
    goldlabel = tk.Radiobutton(frm6, text='Gold\t( ' + str(goldroomno) + ' rooms available )', variable=roomt, value=2,
                               font=('times', 30), cursor="hand2", bg="#e6ffff")
    platlabel = tk.Radiobutton(frm6, text='Platinum\t( ' + str(platroomno) + ' rooms available )', variable=roomt,
                               value=3,
                               font=('times', 30), cursor="hand2", bg="#e6ffff")
    sillabel.pack(pady=10)
    goldlabel.pack(pady=10)
    platlabel.pack(pady=10)
    frm5.forget()
    frm6.pack()


def roomnos():
    global silroomno, goldroomno, platroomno, silroom, goldroom, platroom
    custdate = ''
    for i in range(0, stayday):
        custdate += ((curdate + timedelta(days=i)).strftime('%Y_%m_%d') + ' is null and ')
    custdate = custdate[0:-4]
    retrooms = 'select RoomId from bookings where ' + custdate
    cur.execute(retrooms)
    vacrooms = cur.fetchall()
    silroom = []
    goldroom = []
    platroom = []
    for (room,) in vacrooms:
        if room[0] == 'S':
            silroom.append(room)
        elif room[0] == 'G':
            goldroom.append(room)
        elif room[0] == 'P':
            platroom.append(room)
    silroomno = len(silroom)
    goldroomno = len(goldroom)
    platroomno = len(platroom)


def bookroom():
    global silroom, goldroom, platroom, roomt, stayday, custid, roomlabel, roomids
    roomtint = roomt.get()
    roomt.set(0)
    try:
        if roomtint == 1:
            assroom = silroom[0]
        elif roomtint == 2:
            assroom = goldroom[0]
        elif roomtint == 3:
            assroom = platroom[0]
        bookcust = ''
        for i in range(0, stayday):
            bookcust += ((curdate + timedelta(days=i)).strftime('%Y_%m_%d') + '=' + str(custid) + ', ')
        bookcust = bookcust[0:-2]
        query = "update bookings set " + bookcust + " where RoomId='" + assroom + "'"
        cur.execute(query)
        con.commit()
        roomids.append(assroom)
        frm6.forget()
        sillabel.destroy()
        goldlabel.destroy()
        platlabel.destroy()
        roomlabel = tk.Label(frm7, text=assroom, font=('times', 35, 'underline'), fg='blue', bg='orange')
        roomlabel.pack(pady=10)
        frm7.pack()
    except:
        messagebox.showwarning("Room Unavailable", "Select a valid room type")


def bookanother():
    frm7.forget()
    staydays.set(0)
    roomlabel.destroy()
    frm5.pack()


def backtostart():
    printbill()
    frm7.forget()
    phone.delete(0, tk.END)
    namefield.delete(0, tk.END)
    staydays.set(0)
    roomlabel.destroy()
    frm2.pack()
    checkdate()


def printbill():
    credates = sum(roomdays)
    cur.execute("update customers set Credits=Credits+%s where CustId=%s" % (credates, custid))
    con.commit()
    cur.execute("select Credits from customers where CustId=%s" % (custid))
    credits = cur.fetchall()[0][0]
    if credits >= 10:
        disc = True
        cur.execute("update customers set Credits=Credits-10 where CustId=%s" % (custid))
        con.commit()
    else:
        disc = False
    print('\n\t\t\tHOTEL NAME')
    print('-' * 60)
    print('Name :', name)
    print('Phone no :', pho)
    print('Customer id :', custid)
    print('-' * 60)
    print('Room\tRoom Type\tNo. of Days\t\tRate\t\tCost')
    totalcost = 0
    for i in range(len(roomids)):
        days = roomdays[i]
        roomname = roomids[i]
        if roomname[0] == 'S':
            rate = 2000
            cost = rate * days
            print(roomname, '\tSilver\t\t', days, '\t\t\tRs.', rate, '\tRs.', cost)
        elif roomname[0] == 'G':
            rate = 3000
            cost = rate * days
            print(roomname, '\tGold\t\t', days, '\t\t\tRs.', rate, '\tRs.', cost)
        elif roomname[0] == 'P':
            rate = 4000
            cost = rate * days
            print(roomname, '\tPlatinum\t', days, '\t\t\tRs.', rate, '\tRs.', cost)
        totalcost += cost
    print('\nTotal cost : Rs.', totalcost)
    if disc:
        discount = 0.1 * totalcost
        print('Discount : Rs.', discount)
        discountprice = totalcost - discount
        print('Discounted price : Rs.', discountprice)
        totalcost = discountprice


root = tk.Tk()
root.title("Bookings")
root.geometry('800x700')
root.configure(background="#e6ffff")


frm1 = tk.Frame(root, pady=10, bg="#e6ffff")
frm2 = tk.Frame(root, bg="#e6ffff")
frm3 = tk.Frame(root, bg="#e6ffff")
frm4 = tk.Frame(root, bg="#e6ffff")
frm5 = tk.Frame(root, bg="#e6ffff")
frm6 = tk.Frame(root, bg="#e6ffff")
frm7 = tk.Frame(root, bg="#e6ffff")
frm8 = tk.Frame(root, bg="#e6ffff")
frm9 = tk.Frame(root, bg="#e6ffff")

frm1.pack()



head = tk.Label(frm1, text="Hotel Name", font=('comic sans ms', 40, 'underline'), fg='red', bg="#e6ffff")
head.grid(column=2, row=1, pady=50)

Book = tk.Button(frm2, text="Book", command=book, font=('times', 25), cursor="hand2")
Book.pack(pady=20)
Roombutton = tk.Button(frm2, text="View rooms", command=viewroom, font=('times', 25), cursor="hand2")
Roombutton.pack(pady=20)
Custbutton = tk.Button(frm2, text="View Customer Records", command=viewcust, font=('times', 25), cursor="hand2")
Custbutton.pack(pady=20)
Quit = tk.Button(frm2, text="Quit", command=destroy, font=('times', 15), cursor="pirate")
Quit.pack(pady=30)

phone = tk.Entry(frm3, width=20, font=('times', 25))
phone.pack(side=tk.LEFT, pady=60)
enterpho = tk.Button(frm3, text="Enter phone no", command=getphone, font=('times', 25), cursor="hand2")
enterpho.pack(side=tk.LEFT, pady=60, padx=10)

namefield = tk.Entry(frm4, width=20, font=('times', 25))
namefield.grid(column=1, row=3)
entername = tk.Button(frm4, text="Enter name", command=getname, font=('times', 25), cursor="hand2")
entername.grid(column=2, row=3)

staydays = tk.IntVar()
staydays.set(0)
roomtyp = [('1 day', 1), ('2 days', 2), ('3 days', 3)]
for room, val in roomtyp:
    tk.Radiobutton(frm5, text=room, variable=staydays, value=val, font=('times', 25), cursor="hand2", bg="#e6ffff").pack(pady=10)
DateSel = tk.Button(frm5, text="Continue", command=getstaydat, font=('times', 25), cursor="hand2").pack()

roomt = tk.IntVar()
roomt.set(0)
roomselect = tk.Button(frm6, text='Continue', command=bookroom, font=('times', 25), cursor="hand2").pack(side=tk.BOTTOM, pady=20)

tk.Label(frm7, text="Your room number is", font=('times', 25), bg="#e6ffff").pack(pady=10)
tk.Button(frm7, text="Finish", command=backtostart, font=('times', 25), cursor="hand2").pack(side=tk.BOTTOM, pady=15)
tk.Button(frm7, text="Book another room", command=bookanother, font=('times', 25), cursor="hand2").pack(side=tk.BOTTOM, pady=30)

tk.Button(frm8, text="Back", command=backtomain, font=('times', 15), cursor="hand2").grid(rows=1)

tk.Button(frm9, text="Back", command=backtomain, font=('times', 15), cursor="hand2").grid(rows=1)

mainscreen()
root.mainloop()

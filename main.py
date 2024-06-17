import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, PhotoImage
import mysql.connector
import PyPDF2

root = Tk()
root.title("College Management - Server")
root.geometry("1250x650")
root.config(bg="#1f97b5")

answer_pdf = open(r'E:/Arunai_CSE_Projects/Automatic Answer Evaluation/Answer_PDF.pdf', mode='rb')

allocated_mark = 0
pdfdoc = PyPDF2.PdfReader(answer_pdf)
total_pages = len(pdfdoc.pages)

passshow_icon = PhotoImage(file='Images/eye.png')
passhide_icon = PhotoImage(file='Images/hide.png')
upload_icon = PhotoImage(file='Images/icon.png')
a_img = PhotoImage(file="Images/analyse.png")
process_icon = PhotoImage(file='Images/process.png')

password_mode = True
mark = 0
result = 0

try:
    login_frame = tk.Frame(root, width=350, height=335, bg="#1f97b5")
    signup_frame = tk.Frame(root, width=350, height=420, bg="#1f97b5")

    db = mysql.connector.connect(host='localhost',
                                 port=3306,
                                 database='college_details',
                                 user='root',
                                 password='')
    cursor = db.cursor()


    def change_signin():

        signup_frame.place_forget()
        login_frame.place(x=730, y=150)

        login_head = tk.Label(login_frame, text='College Login', bg="#1f97b5", fg='white',
                              font=('Microsoft YaHei UI Light', 23, 'bold'))
        login_head.place(x=70, y=10)

        def signin():
            username = login_user_entry.get()
            password = login_pass_entry.get()

            if username == 'Username' or password == 'Password':
                messagebox.showwarning("Warning", "Please enter missing Username or Password !!!")
            elif username == 'Vijay' and password == '1234':
                try:
                    # db = mysql.connector.connect(host='localhost',
                    #                              port=3306,
                    #                              database='evaluate_details',
                    #                              user='root',
                    #                              password='')
                    # cursor = db.cursor()

                    messagebox.showinfo("Success", "Login Successfully ...")

                    login_img.place_forget()
                    login_frame.place_forget()
                    login_title.place_forget()

                    def analyse_pdf():
                        global filename
                        name = student_name.get()
                        reg = student_reg.get()
                        subject = student_subject.get()
                        dept = student_dept.get()
                        deg = student_deg.get()
                        college = student_college.get()

                        if name == 'Student Name' or reg == 'Student Register No' or subject == 'Student Subject' or dept == 'Student Department' or deg == 'Student Degree' or college == 'Student College':
                            messagebox.showwarning("Warning", "Please enter student details to proceed ..")
                        else:
                            for p in range(0, total_pages):
                                pdf_page = pdfdoc.pages[p]
                                pdf_page = pdf_page.extract_text().split('. ')
                                for a in range(0, len(pdf_page)):
                                    with open('Answer_Key.txt', 'r') as f:
                                        if pdf_page[a] in f.readline():
                                            allocated_mark += 1
                            mark = allocated_mark
                            if mark > 35:
                                result = 'P'
                            else:
                                result = 'F'

                            cursor.execute("insert into evaluate_content values(%s,%s,%s,%s,%s,%s,%s,%s)",
                                           (name, reg, subject, dept, deg, college, mark, result))
                            db.commit()

                            student_name.delete('0', 'end')
                            student_name.insert('0', 'Student Name')
                            student_reg.delete('0', 'end')
                            student_reg.insert('0', 'Student Register No')
                            student_subject.delete('0', 'end')
                            student_subject.insert('0', 'Student Subject')
                            student_dept.delete('0', 'end')
                            student_dept.insert('0', 'Student Department')
                            student_deg.delete('0', 'end')
                            student_deg.insert('0', 'Student Degree')
                            student_college.delete('0', 'end')
                            student_college.insert('0', 'Student College')

                            score_lable = Label(root, text="Score => " + str(mark),
                                                font=('Microsoft YaHei UI Light', 16, 'bold'))
                            score_lable.config(bg='#1f97b5', fg='white')
                            score_lable.place(x=540, y=510)
                            emoji = PhotoImage(file="Images/poor.png")
                            emj_code = Label(root, image=emoji, bg='#1f97b5')
                            emj_code.place(x=560, y=540)

                            messagebox.showinfo("Success", "Paper Evaluated and Result stored in Database ..")

                            score_lable.place_forget()
                            emj_code.place_forget()

                    def upload_pdf():
                        global filename
                        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                              filetype=(('PDF Files', '.pdf'), ('All Files', '*.*')))

                    project_title = Label(root, text="Automatic Answer Evaluation System")
                    project_title.config(font=('Microsoft YaHei UI Light', 24, 'bold'), bg='#1f97b5', fg='orange')
                    project_title.place(x=70, y=25)

                    analyse_img = Label(root, image=a_img, bd=0, bg='#1f97b5')
                    analyse_img.place(x=630, y=65)

                    upload_label = Label(root, text="Upload Answersheet PDF format here")
                    upload_label.config(bg='#1f97b5', fg='white', font=('Microsoft YaHei UI Light', 12))
                    upload_label.place(x=180, y=180)

                    upload_doc = Button(root, image=upload_icon, bd=0, bg='#1f97b5', activebackground='#1f97b5',
                                        fg='white')
                    upload_doc.config(command=upload_pdf)
                    upload_doc.place(x=280, y=90)

                    def name_enter(e):
                        student_name.delete('0', 'end')

                    def name_leave(e):
                        name = student_name.get()
                        if name == '':
                            student_name.insert('0', "Student Name")

                    student_name = Entry(root, width=32, font=('Microsoft YaHei UI Light', 12))
                    student_name.insert('0', "Student Name")
                    student_name.place(x=178, y=240)
                    student_name.bind('<FocusIn>', name_enter)
                    student_name.bind('<FocusOut>', name_leave)

                    def reg_enter(e):
                        student_reg.delete('0', 'end')

                    def reg_leave(e):
                        reg = student_reg.get()
                        if reg == '':
                            student_reg.insert('0', "Student Register No")

                    student_reg = Entry(root, width=32, font=('Microsoft YaHei UI Light', 12))
                    student_reg.insert('0', "Student Register No")
                    student_reg.place(x=178, y=290)
                    student_reg.bind('<FocusIn>', reg_enter)
                    student_reg.bind('<FocusOut>', reg_leave)

                    def subject_enter(e):
                        student_subject.delete('0', 'end')

                    def subject_leave(e):
                        subject = student_subject.get()
                        if subject == '':
                            student_subject.insert('0', "Student Subject")

                    student_subject = Entry(root, width=32, font=('Microsoft YaHei UI Light', 12))
                    student_subject.insert('0', "Student Subject")
                    student_subject.place(x=178, y=340)
                    student_subject.bind('<FocusIn>', subject_enter)
                    student_subject.bind('<FocusOut>', subject_leave)

                    def dept_enter(e):
                        student_dept.delete('0', 'end')

                    def dept_leave(e):
                        dept = student_dept.get()
                        if dept == '':
                            student_dept.insert('0', "Student Department")

                    student_dept = Entry(root, width=32, font=('Microsoft YaHei UI Light', 12))
                    student_dept.insert('0', "Student Department")
                    student_dept.place(x=178, y=390)
                    student_dept.bind('<FocusIn>', dept_enter)
                    student_dept.bind('<FocusOut>', dept_leave)

                    def deg_enter(e):
                        student_deg.delete('0', 'end')

                    def deg_leave(e):
                        deg = student_deg.get()
                        if deg == '':
                            student_deg.insert('0', "Student Degree")

                    student_deg = Entry(root, width=32, font=('Microsoft YaHei UI Light', 12))
                    student_deg.insert('0', "Student Degree")
                    student_deg.place(x=178, y=440)
                    student_deg.bind('<FocusIn>', deg_enter)
                    student_deg.bind('<FocusOut>', deg_leave)

                    def college_enter(e):
                        student_college.delete('0', 'end')

                    def college_leave(e):
                        college = student_college.get()
                        if college == '':
                            student_college.insert('0', "Student College")

                    student_college = Entry(root, width=32, font=('Microsoft YaHei UI Light', 12))
                    student_college.insert('0', "Student College")
                    student_college.place(x=178, y=490)
                    student_college.bind('<FocusIn>', college_enter)
                    student_college.bind('<FocusOut>', college_leave)

                    process_doc = Button(root, image=process_icon, bd=0, bg='#1f97b5', activebackground='#1f97b5')
                    process_doc.config(command=analyse_pdf)
                    process_doc.place(x=280, y=540)

                except:
                    print("Can't connect to MySQL Server.. If not, Please connect with MySQL Database in Xampp..")

        def user_on_enter(e):
            login_user_entry.delete(0, 'end')

        def user_on_leave(e):
            login_username = login_user_entry.get()
            if login_username == '':
                login_user_entry.insert(0, 'Username')

        login_user_entry = tk.Entry(login_frame, width=25, border=0, bg="#1f97b5", fg='white',
                                    font=('Microsoft YaHei UI Light', 11))
        login_user_entry.place(x=30, y=80)
        login_user_entry.insert(0, 'Username')
        login_user_entry.bind('<FocusIn>', user_on_enter)
        login_user_entry.bind('<FocusOut>', user_on_leave)

        tk.Frame(login_frame, width=295, height=2, bg='black').place(x=25, y=107)

        def pass_on_enter(e):
            login_pass_entry.delete(0, 'end')
            login_pass_entry.config(show='*')
            login_pass_show.config(image=passhide_icon)

        def pass_on_leave(e):
            login_pass_entry.config(show='')
            login_pass_show.config(fg='#fff', image='')
            login_password = login_pass_entry.get()
            if login_password == '':
                login_pass_entry.insert(0, 'Password')

        def passshow():
            global password_mode

            if password_mode:
                login_pass_show.config(image=passshow_icon)
                login_pass_entry.config(show='')
                password_mode = False
            else:
                login_pass_show.config(image=passhide_icon)
                login_pass_entry.config(show='*')
                password_mode = True

        login_pass_entry = tk.Entry(login_frame, width=25, border=0, bg="#1f97b5", fg='white',
                                    font=('Microsoft YaHei UI Light', 11))
        login_pass_entry.place(x=30, y=150)
        login_pass_entry.insert(0, 'Password')
        login_pass_entry.bind('<FocusIn>', pass_on_enter)
        login_pass_entry.bind('<FocusOut>', pass_on_leave)

        login_pass_show = tk.Button(login_frame, image='', border=0, bg='#1f97b5', activebackground='#1f97b5',
                                    command=passshow)
        login_pass_show.place(x=280, y=135, width=50, height=50)

        tk.Frame(login_frame, width=295, height=2, bg='black').place(x=25, y=177)

        login_login_btn = tk.Button(login_frame, width=42, pady=7, text='Sign in', bg='orange', fg='white', border=0,
                                    command=signin)
        login_login_btn.place(x=25, y=225)

        signup_label = tk.Label(login_frame, text="Don't have an account?", bg="#1f97b5", fg='white',
                                font=('Microsoft YaHei UI Light', 9))
        signup_label.place(x=75, y=280)

        signup_btn = tk.Button(login_frame, width=6, text='Sign Up', border=0, bg="#1f97b5", fg='white', cursor='hand2',
                               activebackground='#1f97b5', activeforeground='white', command=change_signup)
        signup_btn.place(x=215, y=280)


    def change_signup():
        login_frame.place_forget()
        signup_frame.place(x=730, y=150)

        login_head = tk.Label(signup_frame, text='College Register', bg="#1f97b5", fg='white',
                              font=('Microsoft YaHei UI Light', 23, 'bold'))
        login_head.place(x=50, y=10)

        def signup():
            username = register_user_entry.get()
            password = register_pass_entry.get()
            college = register_college_entry.get()
            univ = register_univ_entry.get()

            if username == 'Username' or password == 'Password' or college == 'College Name' or univ == 'University Name':
                messagebox.showwarning("Warning", "Please enter missing elements to complete registration !!!")
            else:
                # cursor.execute("insert into college_content values(%s,%s,%s,%s)", (username, college, univ, password))
                # db.commit()
                messagebox.showinfo("Success", "Registered Successfully!!")

        def user_on_enter(e):
            register_user_entry.delete(0, 'end')

        def user_on_leave(e):
            register_username = register_user_entry.get()
            if register_username == '':
                register_user_entry.insert(0, 'Username')

        register_user_entry = tk.Entry(signup_frame, width=25, border=0, bg="#1f97b5", fg='white',
                                       font=('Microsoft YaHei UI Light', 11))
        register_user_entry.place(x=30, y=80)
        register_user_entry.insert(0, 'Username')
        register_user_entry.bind('<FocusIn>', user_on_enter)
        register_user_entry.bind('<FocusOut>', user_on_leave)

        tk.Frame(signup_frame, width=295, height=2, bg='black').place(x=25, y=110)

        def college_on_enter(e):
            register_college_entry.delete(0, 'end')

        def college_on_leave(e):
            register_college = register_college_entry.get()
            if register_college == '':
                register_college_entry.insert(0, 'College Name')

        register_college_entry = tk.Entry(signup_frame, width=25, border=0, bg="#1f97b5", fg='white',
                                          font=('Microsoft YaHei UI Light', 11))
        register_college_entry.place(x=30, y=140)
        register_college_entry.insert(0, 'College Name')
        register_college_entry.bind('<FocusIn>', college_on_enter)
        register_college_entry.bind('<FocusOut>', college_on_leave)

        tk.Frame(signup_frame, width=295, height=2, bg='black').place(x=25, y=170)

        def univ_on_enter(e):
            register_univ_entry.delete(0, 'end')

        def univ_on_leave(e):
            register_univ = register_univ_entry.get()
            if register_univ == '':
                register_univ_entry.insert(0, 'University Name')

        register_univ_entry = tk.Entry(signup_frame, width=25, border=0, bg="#1f97b5", fg='white',
                                       font=('Microsoft YaHei UI Light', 11))
        register_univ_entry.place(x=30, y=200)
        register_univ_entry.insert(0, 'University Name')
        register_univ_entry.bind('<FocusIn>', univ_on_enter)
        register_univ_entry.bind('<FocusOut>', univ_on_leave)

        tk.Frame(signup_frame, width=295, height=2, bg='black').place(x=25, y=230)

        def pass_on_enter(e):
            register_pass_entry.delete(0, 'end')
            register_pass_entry.config(show='*')
            register_pass_show.config(image=passhide_icon)

        def pass_on_leave(e):
            register_pass_entry.config(show='')
            register_pass_entry.insert(0, 'Password')
            register_pass_show.config(fg='#fff', image='')

        def passshow():
            global password_mode

            if password_mode:
                register_pass_show.config(image=passshow_icon)
                register_pass_entry.config(show='')
                password_mode = False
            else:
                register_pass_show.config(image=passhide_icon)
                register_pass_entry.config(show='*')
                password_mode = True

        register_pass_entry = tk.Entry(signup_frame, width=25, border=0, bg="#1f97b5", fg='white',
                                       font=('Microsoft YaHei UI Light', 11))
        register_pass_entry.place(x=30, y=260)
        register_pass_entry.insert(0, 'Password')
        register_pass_entry.bind('<FocusIn>', pass_on_enter)
        register_pass_entry.bind('<FocusOut>', pass_on_leave)

        register_pass_show = tk.Button(signup_frame, image='', border=0, bg='#1f97b5', activebackground='#1f97b5',
                                       command=passshow)
        register_pass_show.place(x=280, y=250, width=50, height=50)

        tk.Frame(signup_frame, width=295, height=2, bg='black').place(x=25, y=290)

        signup_btn = tk.Button(signup_frame, width=37, pady=3, text='Sign up', bg='orange', fg='white', border=0,
                               command=signup,
                               font=('Microsoft YaHei UI Light', 10))
        signup_btn.place(x=25, y=325)

        signup_label = tk.Label(signup_frame, text="Already have an account?", bg="#1f97b5", fg='white',
                                font=('Microsoft YaHei UI Light', 9))
        signup_label.place(x=65, y=375)

        signup_btn = tk.Button(signup_frame, width=6, text='Sign In', border=0, bg="#1f97b5", fg='white',
                               cursor='hand2',
                               activebackground='#1f97b5', activeforeground='white', command=change_signin)
        signup_btn.place(x=215, y=375)


    change_signin()

    login_title = Label(root, text="Automatic Answer Evaluation System")
    login_title.config(font=('Microsoft YaHei UI Light', 24, 'bold'), bg='#1f97b5', fg='orange')
    login_title.place(x=630, y=25)

    l_img = PhotoImage(file="Images/login.png")
    login_img = Label(root, image=l_img, bd=0, bg='#1f97b5')
    login_img.place(x=80, y=85)

    root.mainloop()

except:
    print("Can't connect to MySQL Server.. If not, Please connect with MySQL Database in Xampp..")

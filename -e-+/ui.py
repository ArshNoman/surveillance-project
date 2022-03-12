from email.mime.multipart import MIMEMultipart
from ttkthemes import themed_tk as tk
from email.mime.text import MIMEText
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import smtplib
import shutil
from tkinter import *
import os
import cv2
import pymysql
import ast
from PIL import ImageTk,Image
import glob


username = ''; password = ''; logged_in = False; session_user = ''

# 连接到 MySQL 数据库

db = pymysql.connect(
    host="byyikg99odchbcly6vrw-mysql.services.clever-cloud.com",
    user="ubyvkstgmoy2hv2b",
    password="glxQ8H6nSNzoNROmdPqt",
    database="byyikg99odchbcly6vrw",
    autocommit=True)

cursor = db.cursor()

db.ping()  # reconnecting mysql
if cursor.connection is None:
    db.ping()

# 登录功能
def main_login():

    # 创建APP窗口

    login_root = Tk()
    login_root.geometry('375x150')
    login_root.title("Login")
    login_root.resizable(False, False)

    usernamelabel = Label(login_root, text="Username | 用户名", relief=RIDGE)
    emptyrow = Label(login_root)
    emptycolumn = Label(login_root)
    emptyrow2 = Label(login_root)
    passwordlabel = Label(login_root, text="Password | 密码", relief=RIDGE)
    usernameentry = Entry(login_root, relief=GROOVE)
    passwordentry = Entry(login_root, relief=GROOVE, show='*')

    # 职能

    def register():
        def register_user():

            username = username_entry_register.get()
            password = password_entry_register.get()
            email = email_entry_register.get()

            if username == "" or password == "" or email == "":
                messagebox.showerror('Empty space found', 'All fields are required to be filled | 所有字段都必须填写')

            try:
                db.ping()
                cursor.execute("INSERT INTO users VALUES (%s, %s, %s, '[]')", (username, password, email))

            except pymysql.err.IntegrityError:  # 这将检查用户名或电子邮件是否已经存在
                messagebox.showerror('Username or email taken', 'The username or email is already registered | 用户名或电子邮件已注册')
            db.ping()

            username_entry_register.delete(0, END)
            password_entry_register.delete(0, END)
            email_entry_register.delete(0, END)

            reg_success = Label(register_screen, text="Registration Success | 注册成功", fg="green", font=("Calibri", 11))
            welcome_reg = Label(register_screen, text='欢迎, Welcome {}'.format(username), fg="green", font=("Calibri", 11))
            reg_success.pack()
            welcome_reg.pack()
            register_screen.destroy()

        # 创建新的APP窗口

        register_screen = Toplevel(login_root)
        register_screen.title("Register | 登记")
        register_screen.geometry("250x220")
        register_screen.resizable(False, False)

        username_reg = Label(register_screen, text="Username").pack()
        username_entry_register = Entry(register_screen)
        username_entry_register.pack()
        password_reg = Label(register_screen, text="Password").pack()

        password_entry_register = Entry(register_screen, show='*')
        password_entry_register.pack()
        email_reg = Label(register_screen, text='Email address')
        email_reg.pack()

        email_entry_register = Entry(register_screen)
        email_entry_register.pack()
        Label(register_screen, text="").pack()
        Button(register_screen, text="Register", width=10, height=1, command=register_user).pack()

    def login():
        global logged_in, session_user

        username_given = usernameentry.get()
        password_given = passwordentry.get()
        usernameentry.delete(0, END)
        passwordentry.delete(0, END)

        if username_given == "" or password_given == "":
            messagebox.showerror('Empty space found', 'All fields are required to be filled | 所有字段都必须填写')

        try:
            cursor.execute("SELECT password FROM users WHERE username = (%s)", username_given) # 访问数据库
            passw = cursor.fetchall()[0][0]

            if passw == password_given:

                label = Label(login_root, text='Success | 成功', fg='green', font=('Calbri', 11, 'bold'))
                label.grid(row=4, column=3)
                logged_in = True
                if logged_in:
                    session_user = username_given
                    login_root.destroy()
                    app()

            else:
                messagebox.showerror("Login failed", 'Username or password is incorrect | 用户名或密码不正确')
        except Exception as e:
            print(e)
            messagebox.showerror("Login failed", 'Username or password is incorrect | 用户名或密码不正确')

    def contact():
        messagebox.showinfo('接触', '电子邮件: arshnoman2270@gmail.com\n')

    def exit():
        login_root.destroy()

    def app():
        global session_user

        # 创建APP窗口

        root = tk.ThemedTk()
        root.get_themes()
        root.set_theme('scidgrey')
        root.title('Project')
        root.geometry('1000x750')
        root.resizable(False, False)

        image = PhotoImage(file='static/bg.png')
        background_label = Label(root, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def view_violations():

            # 创建APP窗口

            violation_root = Toplevel(root)
            violation_root.title("View Violations | 查看违规行为")
            violation_root.geometry("750x500")
            violation_root.resizable(False, False)

            def viewclass():
                global label
                db.ping()
                cursor.execute("SELECT classes FROM users WHERE username = (%s)", (session_user,))
                clist = ast.literal_eval(cursor.fetchall()[0][0])

                selected = listbox.curselection()
                selected = int(selected[0])
                selected_class = clist[selected]

                cursor.execute("SELECT violations FROM classes WHERE user = (%s) and name = (%s)", (session_user, selected_class))
                violations = ast.literal_eval(cursor.fetchall()[0][0])
                index = 0; images = []

                files = glob.glob('pics/*')
                for f in files:
                    os.remove(f)

                # 从数据库中访问违规图像并将其保存在本地

                if violations != []:
                    for i in violations:
                        with open(f'pics/img{index}.png', 'wb') as file:
                            file.write(i)
                            file.close()
                        index += 1

                    for x in range(len(violations)):
                        im = Image.open(f'pics/img{x}.png')
                        im = im.resize((500, 350))
                        im.save(f'pics/img{x}.png')
                        images.append(ImageTk.PhotoImage(Image.open(f'pics/img{x}.png')))

                    viewing = Toplevel(root)
                    viewing.title("Violations | 违规行为")
                    viewing.geometry("750x500")
                    viewing.resizable(False, False)

                    status = Label(viewing, text=f'Image 1/{len(violations)}', font=('Arial'))
                    label = Label(viewing, image=images[0])
                    label.grid(row=0, column=0, columnspan=3)
                    status.grid(row=3, column=1)

                    def next(img_num): # 移动到下一张图片的功能
                        global label
                        global button_forward
                        global button_back
                        global status

                        label.grid_forget()
                        label = Label(viewing, image=images[img_num - 1])
                        button_back = Button(viewing, text="<<", command=lambda: back(img_num - 1))
                        button_forward = Button(viewing, text=">>", command=lambda: next(img_num + 1))

                        if img_num == len(images):
                            button_forward = Button(viewing, text=">>", state=DISABLED)
                            status = Label(viewing, text=f'Image {img_num}/{len(violations)}', font=('Arial'))
                            status.grid(row=3, column=1)

                        label.grid(row=0, column=0, columnspan=3)
                        button_back.grid(row=1, column=0)
                        button_forward.grid(row=1, column=2)

                    def back(img_num): # 移动到上一张图像的功能
                        global label
                        global button_forward
                        global button_back
                        global status

                        label.grid_forget()
                        label = Label(viewing, image=images[img_num - 1])
                        button_back = Button(viewing, text="<<", command=lambda: back(img_num - 1))
                        button_forward = Button(viewing, text=">>", command=lambda: next(img_num + 1))

                        if img_num == 1:
                            button_back = Button(viewing, text="<<", state=DISABLED)

                        status = Label(viewing, text=f'Image {img_num}/{len(violations)}', font=('Arial'))
                        status.grid(row=3, column=1)

                        label.grid(row=0, column=0, columnspan=3)
                        button_back.grid(row=1, column=0)
                        button_forward.grid(row=1, column=2)

                    button_back = Button(viewing, text='<<', command=lambda: back())
                    button_quit = Button(viewing, text='Exit | 出口', command=viewing.destroy())
                    button_forward = Button(viewing, text='>>', command=lambda: next(2))

                    button_back.grid(row=1, column=0)
                    button_quit.grid(row=1, column=1)
                    button_forward.grid(row=1, column=2)

                    viewing.mainloop()
                else:
                    pass
                    

            listbox = Listbox(violation_root)
            empty = Label(violation_root)
            viewv = Button(violation_root, text='View Violations | 查看违规行为', width=15, command=viewclass)
            select = Label(violation_root, text='Select a class | 选课')
            listbox.config(width=100)

            db.ping()
            cursor.execute("SELECT classes FROM users WHERE username = (%s)", (session_user,))
            class_list = ast.literal_eval(cursor.fetchall()[0][0])

            empty.grid(row=0, column=0)
            try:
                if class_list != []:
                    for files_1 in class_list:
                        index = len(class_list)
                        listbox.insert(index, files_1)
                        listbox.grid(row=0, column=1)
                        index -= 1
                else:
                    listbox.insert(0, 'No Classes Available | 没有课程')
                    listbox.grid(row=0, column=1)
            except:
                pass

            viewv.grid(row=0, column=2)
            select.grid(row=1, column=1)

        def manage_classes():

                # 创建APP窗口

                classes = Toplevel(root)
                classes.title("Class Management")
                classes.geometry("750x500")
                # open_files.iconbitmap("C:/Users/PC/Desktop/7/logo.ico")
                classes.resizable(False, False)

                def removeclass(): # 从数据库中删除一个类
                    db.ping()
                    cursor.execute("SELECT classes FROM users WHERE username = (%s)", (session_user,))
                    clist = ast.literal_eval(cursor.fetchall()[0][0])

                    selected = listbox.curselection()
                    selected = int(selected[0])
                    selected_class = clist[selected]

                    db.ping()

                    cursor.execute("SELECT classes FROM users WHERE username = (%s)", (session_user))
                    current_classes = ast.literal_eval(cursor.fetchall()[0][0])
                    current_classes.remove(selected_class)
                    current_classes = str(current_classes)

                    cursor.execute("UPDATE users SET classes = (%s) WHERE username = (%s)", (current_classes, session_user))

                    cursor.execute("DELETE FROM classes WHERE user = (%s) AND name = (%s)", (session_user, selected_class))

                    classes.destroy()

                def addclass(): # 向数据库中添加一个类

                    new_folder = Toplevel(root)
                    new_folder.title("Add a class | 添加一个类")
                    new_folder.geometry("320x220")
                    new_folder.resizable(False, False)

                    # new_folder.iconbitmap("C:/Users/PC/Desktop/7/logo.ico")

                    def adddclass():

                        if title.get() == '':
                            messagebox.showerror('Name Empty', 'Your class name cannot be empty! | 类名不能为空！')
                        else:
                            db.ping()

                            cursor.execute("SELECT classes FROM users WHERE username = (%s)", (session_user))
                            current_classes = ast.literal_eval(cursor.fetchall()[0][0])
                            classname = title.get()
                            current_classes.append(classname)
                            current_classes = str(current_classes)

                            cursor.execute("UPDATE users SET classes = (%s) WHERE username = (%s)", (current_classes, session_user))

                            cursor.execute("INSERT INTO classes VALUES (%s, '[]', %s)", (session_user, classname))

                        new_folder.destroy()
                        classes.destroy()

                    title = ttk.Entry(new_folder, width=48)
                    confirm_create = Button(new_folder, text='Add new class | 添加新班级', command=adddclass)

                    Label(new_folder).grid(row=0, column=0)
                    Label(new_folder).grid(row=0, column=1)
                    Label(new_folder, text='Enter class name | 输入班级名称').grid(row=1, column=2)
                    Label(new_folder).grid(row=2, column=1)
                    title.grid(row=3, column=2)
                    Label(new_folder).grid(row=4, column=1)
                    Label(new_folder).grid(row=5, column=1)
                    Label(new_folder).grid(row=6, column=1)
                    confirm_create.grid(row=7, column=2)

                listbox = Listbox(classes)
                empty = Label(classes)
                add_classes = Button(classes, text='Add a class | 添加新班级', width=15, command=addclass)
                remove_classes = Button(classes, text='Remove class | 删除类', width=15, command=removeclass)
                your_classes_label = Label(classes, text='Your classes | 你的课')
                listbox.config(width=100)

                db.ping()
                cursor.execute("SELECT classes FROM users WHERE username = (%s)", (session_user,))
                class_list = ast.literal_eval(cursor.fetchall()[0][0])

                empty.grid(row=0, column=0)
                try:
                    if class_list != []:
                        for files_1 in class_list:
                            index = len(class_list)
                            listbox.insert(index, files_1)
                            listbox.grid(row=0, column=1)
                            index -= 1
                    else:
                        listbox.insert(0, 'No Classes Available | 没有课程')
                        listbox.grid(row=0, column=1)
                except: pass

                add_classes.grid(row=0, column=2)
                remove_classes.grid(row=1, column=2)
                your_classes_label.grid(row=3, column=1)

                classes.mainloop()

        def contact():
                messagebox.showinfo('接触', '电子邮件: arshnoman2270@gmail.com\n')

        def log_out():
                root.destroy()
                main_login()

        view = ttk.Button(root, text='View Violations | 查看违规行为', command=view_violations, width=20)
        manage_classes = ttk.Button(root, text='Manage classes | 管理课程', command=manage_classes, width=20)

        menu_app = Menu(root)
        root.config(menu=menu_app)
        submenu_app = Menu(menu_app, tearoff=0)

        menu_app.add_cascade(label='Settings | 设置', menu=submenu_app)
        submenu_app.add_command(label='Contact | 接触', command=contact)
        submenu_app.add_command(label='Log out | 登出', command=log_out)

        Label(root).grid(row=0, column=0)
        view.grid(row=1, column=1)

        Label(root).grid(row=2, column=0)
        manage_classes.grid(row=3, column=1)

        root.protocol('WM_DELETE_WINDOW', exit)
        root.mainloop()

    # Tkinter GUI

    login_button = Button(login_root, text='Login | 登录', command=login, relief=GROOVE)
    register_button = Button(login_root, relief=GROOVE, text='Register | 登记', command=register)

    menu_login = Menu(login_root)
    login_root.config(menu=menu_login)
    submenu_login = Menu(menu_login, tearoff=0)

    menu_login.add_cascade(label='Settings | 设置', menu=submenu_login)
    submenu_login.add_command(label='Contact | 接触', command=contact)
    submenu_login.add_command(label='Exit | 出口', command=exit)

    usernamelabel.grid(row=0, column=0)
    emptyrow.grid(row=1, column=0)
    emptyrow2.grid(row=3, column=0)
    emptycolumn.grid(row=0, column=1)
    passwordlabel.grid(row=2, column=0)
    usernameentry.grid(row=0, column=2)
    passwordentry.grid(row=2, column=2)
    login_button.grid(row=4, column=0)
    register_button.grid(row=4, column=2)

    # Main Loop

    login_root.mainloop()


if __name__ == '__main__':
    main_login()

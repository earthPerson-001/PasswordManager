from tkinter import *
from tkinter import messagebox
from random import *
from encryp import *
import threading


generated_password = ''
username = ''
password = ''

conn = sqlite3.connect('passwords.db')
c = conn.cursor()

main_app = Tk()
main_app.title('Password Manager')
main_app.geometry('460x400')

input_1 = Entry(main_app)
input_2 = Entry(main_app)
input_4 = Entry(main_app)


def login_page_shifter():
    display_login_frame()


def multi(func):
    many = threading.Thread(target=func)
    many.start()


def generate_password():
    global input_1, input_2, generated_password, input_4
    generated_password = ''
    length = int(input_2.get())
    if input_1.get() == "weak":
        list_1 = "abcdefghijklmnopqrstuvwxyz"
        for i in range(length):
            generated_password = generated_password + list_1[randint(0, len(list_1) - 1)]
    elif input_1.get() == "strong":
        list_1 = "a1b2c3d4e5f6g7h8i9j0AkBlCmDnEoFpGqHrIsJtKuLvMwNxOyPzQRSTUVWXYZ"
        for i in range(length):
            generated_password = generated_password + list_1[randint(0, len(list_1) - 1)]
    else:
        list_1 = "a1b2c3d4e5f6g7h8i9j0k!l@m#n$o%p^q&r*s(t)u_v+w=x~y.z<>,/?':A*BCDEFG_-HIJKLMN`OPQRS{][]}TUVWXYZ"
        for i in range(length):
            generated_password = generated_password + list_1[randint(0, len(list_1) - 1)]
    input_4.delete(0, END)
    input_4.insert(0, generated_password)


def save_to_vault(username1):
    def save(user_input):
        conn1 = sqlite3.connect('encrypted.db')
        name = str(input_3.get())
        c1 = conn1.cursor()
        credentials = [{"id": name,
                        "p_word": encrypter(username1, name, user_input)}]
        c1.executemany("""INSERT INTO
                        passwords_""" + username1 + """
                          VALUES
                          (:id, :p_word)""", credentials)
        conn1.commit()
        c1.close()
        display_saved_password_frame(username)
    forget_frame()
    save_to_vault_frame.grid()
    label_6 = Label(save_to_vault_frame, text="Name")
    label_7 = Label(save_to_vault_frame, text="Password")
    input_3 = Entry(save_to_vault_frame, font=("calibre", 10))
    input_5 = Entry(save_to_vault_frame, font=("calibre", 10))
    input_5.delete(0, END)
    input_5.insert(0, input_4.get())
    btn_4 = Button(save_to_vault_frame, text="Save", command=lambda: save(input_5.get()))
    input_3.grid(row=0, column=1)
    label_6.grid(row=0, column=0)
    btn_4.grid(row=2, column=1)
    label_7.grid(row=1, column=0)
    input_5.grid(row=1, column=1)


def display_password_generator_frame():
    global input_1, input_2, input_4
    forget_frame()
    password_generator_frame.grid()

    label_1 = Label(password_generator_frame, font=("calibre", 10), text="Password strength")
    label_2 = Label(password_generator_frame, font=("calibre", 10), text="(very strong, strong, weak)")
    label_3 = Label(password_generator_frame, font=("calibre", 10), text="Password length")
    label_4 = Label(password_generator_frame, font=("calibre", 10), text="(1-128)")
    label_5 = Label(password_generator_frame, font=("calibre", 10), text="Password")
    input_4 = Entry(password_generator_frame, font=("calibre", 10), bg="#add8e6", width=38)

    btn_1 = Button(password_generator_frame, font=("calibre", 10), text="Generate", command=generate_password, width=17, fg="#000044", bg="#00ff00")
    btn_2 = Button(password_generator_frame, font=("calibre", 10), text="Save to vault", command=lambda: save_to_vault(username), width=15, fg="#440000")
    btn_3 = Button(password_generator_frame, font=("calibre", 10), text="Exit", command=forget_frame, width=15, fg="#440000")

    input_1 = Entry(password_generator_frame, font=("times new roman", 11), bg="#add8e6")
    input_2 = Entry(password_generator_frame, font=("times new roman", 11), bg="#add8e6")

    input_1.insert(0, "strong")
    input_2.insert(0, "16")
    input_4.insert(0, "password")

    label_1.grid(row=0, column=0, padx=10, pady=10)
    input_1.grid(row=0, column=1, pady=10)
    label_2.grid(row=0, column=2, pady=10)

    label_3.grid(row=1, column=0, padx=10, pady=8)
    input_2.grid(row=1, column=1, pady=10)
    label_4.grid(row=1, column=2, pady=10)

    btn_1.grid(row=2, column=1)
    btn_2.grid(row=4, column=1)
    btn_3.grid(row=4, column=2)

    label_5.grid(row=3, column=0, padx=10, pady=10)
    input_4.grid(row=3, column=1, columnspan=2)


def show_password(name):
    def password_grabber(name1, rowid1):
        label_8 = Label(app2, text="Password incorrect")
        input_box1 = Entry(app2, font=("Times", 12))
        input_box2 = Entry(app2, font=("Times", 12))
        if login_verifier(username, input_box.get()):
            label_8.grid_forget()

            input_box1.insert(0, name1)
            input_box2.insert(0, decrypter(username, name1, rowid1)[0])
            Label(app2, text="login Credentials").grid(row=3, column=1, pady=15)
            Label(app2, text="Username").grid(row=4, column=0)
            Label(app2, text="Password").grid(row=5, column=0)
            input_box1.grid(row=4, column=1)
            input_box2.grid(row=5, column=1)
        else:
            label_8.grid(row=3, column=1, pady=15)
            input_box.delete(0, END)
            input_box1.delete(0, END)
            input_box2.delete(0, END)

    app2 = Toplevel()
    app2.geometry('400x400')
    input_box = Entry(app2, font=("Times", 12))
    Label(app2, text="Please enter the masterpassword to authenticate the account", font=("Times", 12)).grid(row=0, column=0, columnspan=2)
    Label(app2, text="Master password", font=("Times", 12)).grid(row=1, column=0)
    input_box.grid(row=1, column=1)
    btn1 = Button(app2, text="Submit", command=lambda: password_grabber(name[1], name[0]))
    btn1.grid(row=2, column=1)


def display_saved_password_frame(username1):
    forget_frame()
    saved_password_frame.grid()
    list1 = username_retuner(username1)
    for record in list1:
        Label(saved_password_frame, text=record[1], font=("Times", 12)).grid(row=list1.index(record), column=0)
        Button(saved_password_frame, text="Show Password", command=lambda: show_password(record), font=("Times", 9)).grid(row=list1.index(record), column=1, padx=25)


def display_check_password_security_frame():
    forget_frame()
    check_password_security_frame.grid()
    label_1 = Label(check_password_security_frame, text='', font=("calibre", 12))

    def check_security():
        strength = ''
        color = "#000000"
        if len(user_input.get()) > 0:
            if len(user_input.get()) < 8:
                if user_input.get().isalpha() and str(user_input.get().lower()) == user_input.get():
                    strength = "very weak"
                    color = 'red'
                elif not user_input.get().isalnum():
                    strength = "strong"
                    color = 'yellow'
                else:
                    strength = "weak"
                    color = 'orange'
            elif len(user_input.get()) > 8:
                if user_input.get().isalpha() or user_input.get().isnumeric():
                    strength = "weak"
                    color = 'orange'
                elif user_input.get().isalnum():
                    strength = "strong"
                    color = 'yellow'
                elif not user_input.get().isalnum():
                    strength = "very strong"
                    color = 'green'
            label_1.config(text='{}'.format(strength), bg='{}'.format(color), fg="black")
            label_1.grid(row=0, column=2)
        else:
            label_1.config(text="Enter a valid password", bg="#404040", fg="red")
            label_1.grid(row=0, column=2)
    user_input_label = Label(check_password_security_frame, text='Password')

    user_input = Entry(check_password_security_frame, font=("calibre", 12), bg="#add8e6")
    check_button = Button(check_password_security_frame, text="Check", command=check_security)

    user_input_label.grid(row=0, column=0, padx=10, pady=10)
    user_input.grid(row=0, column=1, padx=10, pady=10)
    check_button.grid(row=1, column=1, ipadx=20)


def display_logout_message_box():
    global username, password
    forget_frame()
    logout_message_box_frame.grid(row=0, column=0)
    message = messagebox.askyesno(title="Make sure", message="Do you want to logout?")
    if message == 'yes':
        username = ' '
        password = ' '
        login_page_shifter()


def display_vault_frame():
    def erase_vault():
        def delete():
            c = 0
            while c < 4:
                if login_verifier(username, input_box.get()):
                    table_deleter(username)
                else:
                    label9.config(text="Incorrect password, try again")
                    c += 1
        app3 = Toplevel()
        label9 = Label(app3, text="Please enter the masterpassword to remove your vault", font=("times", 12))
        label9.grid(row=0, column=0, columnspan=3)
        input_box = Entry(app3, font=("Times", 12))
        Label(app3, text="Password", font=("times", 12)).grid(row=1, column=0)
        input_box.grid(row=1, column=1)
        Button(app3, text="Delete", command=delete).grid(row=2, column=1)

    forget_frame()
    vault_frame.grid()
    Label(vault_frame, text="Vault Settings", font=("times", 12)).grid(row=0, column=1)
    Label(vault_frame, text=username, font=("times", 12)).grid(row=0, column=2, padx=30)
    Button(vault_frame, text="Erase Vault", font=("times", 12), command=erase_vault).grid(row=1, column=1, pady=20, padx=30)


def login(username2, password2, lbl):
    forget_frame()
    global username, password
    if login_verifier(username2, password2):
        username = username2
        password = password2
        lbl.config(text='Login successful', bg="#003300", fg="black")
        lbl.grid(row=0, column=1)

        def login_automator():
            login_tab.after(2000, lambda: display_saved_password_frame(username))
        multi(login_automator)

    else:
        def thread1():
            app1 = Toplevel()
            app1.geometry('300x300')
            app1.title('login failed')

            Label(app1, text='Login failed', fg="red", font=("times new roman", 18)).pack()
        multi(thread1)
        login_tab.after(2000, display_signup_frame())


def display_login_frame():
    forget_frame()
    login_tab.grid()
    label = Label(login_tab, text="Login Page", font=("calibre", 12), fg="red", bg="white", width=30)
    label1 = Label(login_tab, text="Username", font=("calibre", 12))
    username_input = Entry(login_tab, font=("calibre", 12), bg="#add8e6")
    label2 = Label(login_tab, text="Password", font=("calibre", 12))
    password_input = Entry(login_tab, font=("calibre", 12), bg="#add8e6")
    label.grid(row=0, column=1, pady=10)
    label1.grid(row=1, column=0, pady=5, padx=5)
    username_input.grid(row=1, column=1, pady=5, padx=5)
    label2.grid(row=2, column=0, pady=5, padx=5)
    password_input.grid(row=2, column=1, pady=5, padx=5)
    btn = Button(login_tab, text="login", command=lambda: login(username_input.get(), password_input.get(), label))
    btn.grid(row=3, column=1, ipadx=20)


def username_creator_verifier(u, p):
    if username_creator(u, p):
        username_creator(u, p)
        label = Label(login_tab, text="Login Page", font=("calibre", 12), fg="red", bg="#ffffff")
        login(u, p, label)

    elif not username_creator(u, p):
        def thread2():
            app2 = Toplevel()
            app2.geometry('400x400')
            app2.title('login successful')

            Label(app2, text="Signup failed : username already taken", fg="red", font=("times new roman", 15)).pack()

        multi(thread2)


def display_signup_frame():
    forget_frame()
    signup_frame.pack(expand=1, fill="both")
    label = Label(signup_frame, text="Signup Page", font=("calibre", 12), fg="red")
    label1 = Label(signup_frame, text="Username", font=("calibre", 12))
    username_input = Entry(signup_frame, font=("calibre", 12), bg="#add8e6")
    label2 = Label(signup_frame, text="Password", font=("calibre", 12))
    password_input = Entry(signup_frame, font=("calibre", 12), bg="#add8e6")
    label.grid(row=0, column=1, pady=10)
    label1.grid(row=1, column=0, pady=5, padx=5)
    username_input.grid(row=1, column=1, pady=5, padx=5)
    label2.grid(row=2, column=0, pady=5, padx=5)
    password_input.grid(row=2, column=1, pady=5, padx=5)
    btn = Button(signup_frame, text="Sign Up", command=lambda: username_creator_verifier(username_input.get(), password_input.get()))
    btn.grid(row=3, column=1, ipadx=20)
    username_input.delete(0, END)
    password_input.delete(0, END)


def forget_frame():
    password_generator_frame.grid_forget()
    saved_password_frame.grid_forget()
    check_password_security_frame.grid_forget()
    logout_message_box_frame.grid_forget()
    vault_frame.grid_forget()
    save_to_vault_frame.grid_forget()
    signup_frame.pack_forget()
    login_tab.grid_forget()


password_generator_frame = Frame(main_app, height=400, width=400)
saved_password_frame = Frame(main_app, height=400, width=400)
check_password_security_frame = Frame(main_app, height=400, width=400)
logout_message_box_frame = Frame(main_app, height=400, width=400)
vault_frame = Frame(main_app, height=400, width=400)
save_to_vault_frame = Frame(main_app, height=400, width=400)
login_tab = Frame(main_app, height=400, width=400)
signup_frame = Frame(main_app, height=400, width=400)


menu_bar = Menu(main_app)

pass_word = Menu(menu_bar)
pass_word.add_command(label="Generate Password", command=display_password_generator_frame)
pass_word.add_command(label="Saved Passwords", command=lambda: display_saved_password_frame(username))
pass_word.add_command(label="Check Password security", command=display_check_password_security_frame)

menu_bar.add_cascade(label="password", menu=pass_word)

settings = Menu(menu_bar)
settings.add_command(label="log in", command=display_login_frame)
settings.add_command(label="Sign up", command=display_signup_frame)
settings.add_command(label="log out", command=display_logout_message_box)
settings.add_command(label="vault", command=display_vault_frame)
settings.add_command(label="Exit", command=main_app.quit)

menu_bar.add_cascade(label="settings", menu=settings)

if username == '' and password == '':
    login_page_shifter()

main_app.config(menu=menu_bar)

conn.close()

main_app.mainloop()

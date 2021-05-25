from numpy import NaN
from DBOperations import DBManager
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd 
import matplotlib.pyplot as plt
import pandas as pd
import re


class MainUI():

    def __init__(self, root, dbname):
        self.__sneakername = StringVar()
        self.__dateworkout = StringVar()
        self.__distance = StringVar()
        self.__choise = IntVar()
        self.__root = root
        self.__db = DBManager(dbname)
    
    def initUI(self):
        self.__db.SetConnection()
        self.__choise.set(1)
        self.__root.title('SneakersWorkouts')
        self.__root.resizable(width=False, height=False)
        x = (self.__root.winfo_screenwidth() - self.__root.winfo_reqwidth()) / 2.5
        y = (self.__root.winfo_screenheight() - self.__root.winfo_reqheight()) / 3.5 
        self.__root.wm_geometry("270x360+%d+%d"  % (x, y))
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        main_menu = Menu()

        file_menu = Menu(tearoff=0)
        file_menu.add_command(label="Add to DB from CSV file", command=self.CSVtoDB)
        file_menu.add_command(label="Write from DB to CSV file", command=self.DBtoCSV)
        file_menu.add_command(label="Write from DB to XLSX file", command=self.DBtoXLSX)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command = self.on_closing) 

        print_menu = Menu(tearoff=0)
        print_menu.add_command(label="Show ratio chart", command=self.show_ratio)
        print_menu.add_command(label="Show intensity chart", command=self.show_inten)
        print_menu.add_command(label="Show statistics", command=self.show_statistics)
        print_menu.add_separator()
        print_menu.add_command(label="List of sneakers in DB", command = self.list_of_sneakers)

        about_menu = Menu(tearoff=0)
        about_menu.add_command(label="Help", command=self.help)

        main_menu.add_cascade(label="File", menu = file_menu)
        main_menu.add_cascade(label="Show", menu = print_menu)
        main_menu.add_cascade(label="About", menu = about_menu)
 
        self.__root.config(menu=main_menu) 

        model_label = Label(text="Sneaker model:")
        model_label.pack()

        model_entry = Entry(textvariable=self.__sneakername, width='40')
        model_entry.pack()
        
        date_label = Label(text="Date of workout in dd.mm.yy:")
        date_label.pack()

        date_entry = Entry(textvariable=self.__dateworkout, width='40')
        date_entry.pack()

        distance_label = Label(text="Distance in km:")
        distance_label.pack()

        distance_entry = Entry(textvariable=self.__distance, width='40')
        distance_entry.pack()

        walk_checkbutton = Radiobutton(text="Walk", value=1, variable=self.__choise)
        walk_checkbutton.pack()
        
        run_checkbutton = Radiobutton(text="Run", value=2, variable=self.__choise)
        run_checkbutton.pack()

        distance_label = Label(text="Operations with models:")
        distance_label.pack()

        add_model_button = Button(text="Insert model", width='30', command=self.add_sneaker_todb)
        add_model_button.pack()

        del_model_button = Button(text="Delete model", width='30', command=self.del_sneaker_fromdb)
        del_model_button.pack()

        distance_label = Label(text="Operations with workouts:")
        distance_label.pack()

        add_work_button = Button(text="Insert workout", width='30', command=self.add_workout_todb)
        add_work_button.pack()

        edit_work_button = Button(text="Edit workout", width='30', command=self.edit_workout)
        edit_work_button.pack()

        del_work_button = Button(text="Delete workout", width='30', command=self.del_workout_fromdb)
        del_work_button.pack()

        self.__root.mainloop()

    def add_sneaker_todb(self):
        if self.__sneakername.get() != "":
            if re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]{2,24}", self.__sneakername.get()) == None:
                messagebox.showinfo("Message", "Value of [Sneaker model] entry is not acceptable. See help.")
            else:
                messagebox.showinfo("Message", self.__db.CreateNewSneaker(self.__sneakername.get()))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def del_sneaker_fromdb(self):
        if self.__sneakername.get() != "":
            if re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]{2,24}", self.__sneakername.get()) == None:
                messagebox.showinfo("Message", "Value of [Sneaker model] entry is not acceptable. See help.")
            else:
                if messagebox.askokcancel("Warning!!!", "This action also will delete all workouts for selected sneaker. Are you sure?"):
                    messagebox.showinfo("Message", self.__db.DeleteSneaker(self.__sneakername.get()))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def add_workout_todb(self):
        if self.__sneakername.get() != "" and self.__dateworkout.get() != "" and self.__distance.get() != "":
            if re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]{2,24}", self.__sneakername.get()) == None or re.fullmatch(r"([0][1-9]|[1][0-9]|[2][0-9]|[3][0-1])[.]([0][1-9]|[1][0-2])[.][0-9][0-9]", self.__dateworkout.get()) == None or re.fullmatch(r"([1-9]|[1-9][0-9]|[1][0-9][0-9])[.][0-9][0-9]", self.__distance.get()) == None:
                messagebox.showinfo("Message", "Value of [Sneaker model] or [Date of workout] or [Distance] entries are not acceptable. See help.")
            else:
                type = None
                if self.__choise.get() == 1:
                    type = 'Walk'
                elif self.__choise.get() ==2:
                    type = 'Run'
                messagebox.showinfo("Message", self.__db.CreateNewWorkout(self.__sneakername.get(), (self.__dateworkout.get(), type, self.__distance.get())))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] and [Date of workout] and [Distance] entries")

    def edit_workout(self):
        if self.__sneakername.get() != "" and self.__dateworkout.get() != "" and self.__distance.get() != "":
            if re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]{2,24}", self.__sneakername.get()) == None or re.fullmatch(r"([0][1-9]|[1][0-9]|[2][0-9]|[3][0-1])[.]([0][1-9]|[1][0-2])[.][0-9][0-9]", self.__dateworkout.get()) == None or re.fullmatch(r"([1-9]|[1-9][0-9]|[1][0-9][0-9])[.][0-9][0-9]", self.__distance.get()) == None:
                messagebox.showinfo("Message", "Value of [Sneaker model] or [Date of workout] or [Distance] entries are not acceptable. See help.")
            else:
                if messagebox.askokcancel("Warning!!!", "Do you really want to make a change to workout?"):
                    type = None
                    if self.__choise.get() == 1:
                        type = 'Walk'
                    elif self.__choise.get() ==2:
                        type = 'Run'
                    messagebox.showinfo("Message", self.__db.EditWorkout(self.__sneakername.get(), (self.__dateworkout.get(), type, self.__distance.get())))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] and [Date of workout] and [Distance] entries")
    
    def del_workout_fromdb(self):
        if self.__sneakername.get() != "" and self.__dateworkout.get() != "" and self.__distance.get() != "":
            if re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]{2,24}", self.__sneakername.get()) == None or re.fullmatch(r"([0][1-9]|[1][0-9]|[2][0-9]|[3][0-1])[.]([0][1-9]|[1][0-2])[.][0-9][0-9]", self.__dateworkout.get()) == None or re.fullmatch(r"([1-9]|[1-9][0-9]|[1][0-9][0-9])[.][0-9][0-9]", self.__distance.get()) == None:
                messagebox.showinfo("Message", "Value of [Sneaker model] or [Date of workout] or [Distance] entries are not acceptable. See help.")
            else:
                if messagebox.askokcancel("Warning!!!", "Do you really want delete workout?"):
                    type = None
                    if self.__choise.get() == 1:
                        type = 'Walk'
                    elif self.__choise.get() ==2:
                        type = 'Run'
                    messagebox.showinfo("Message", self.__db.DeleteWorkout(self.__sneakername.get(), (self.__dateworkout.get(), type, self.__distance.get())))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] and [Date of workout] and [Distance] entries")

    def CSVtoDB(self):
        if self.__sneakername.get() != "":
            filename = fd.askopenfilename(filetypes = (("CSV files","*.csv"),("all files","*.*")))
            if filename != "":
                messagebox.showinfo("Message", self.__db.AddWorkoutsFromCSV(self.__sneakername.get(), filename))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def DBtoCSV(self):
        if self.__sneakername.get() != "":
            filename = fd.asksaveasfilename(defaultextension=".csv", filetypes = (("CSV files","*.csv"),("all files","*.*")))
            if filename != "":
                messagebox.showinfo("Message", self.__db.AddWorkoutsToCSV(self.__sneakername.get(), filename))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def DBtoXLSX(self):
        if self.__sneakername.get() != "":
            filename = fd.asksaveasfilename(defaultextension=".xlsx", filetypes = (("XLSX files","*.xlsx"),("all files","*.*")))
            if filename != "":
                messagebox.showinfo("Message", self.__db.AddWorkoutsToXLSX(self.__sneakername.get(), filename))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def show_ratio(self):
        if self.__sneakername.get() != "":
            df = self.__db.PrintWorkoutsForSneaker(self.__sneakername.get())
            if type(df) is pd.DataFrame and df.empty != True:
                walkkm = round(df[df.Type == 'Walk']['Distance'].sum(), 2)
                runkm = round(df[df.Type == 'Run']['Distance'].sum(), 2)
                totalkm = round(df['Distance'].sum(), 2)
                runper = round(runkm * 100 / totalkm)
                walkper = round(walkkm * 100 / totalkm)
                labels = 'Run', 'Walk'
                data = [runper, walkper]
                plt.pie(data, labels=labels, autopct='%1.1f%%')
                plt.axis('equal')
                plt.title("Percentage ratio betwen Run/Walk for sneaker", fontsize=12, fontweight="bold")
                plt.show()
            else:
                messagebox.showinfo("Message", "No such sneaker in DB or absent workouts for him")
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def show_inten(self):
        if self.__sneakername.get() != "":
            df = self.__db.PrintWorkoutsForSneaker(self.__sneakername.get())
            if type(df) is pd.DataFrame and df.empty != True:
                df.Date = pd.to_datetime(df.Date, dayfirst=True)
                df.set_index("Date", inplace=True)
                df[df.Type == 'Run']['Distance'].plot(marker='o', linestyle='--', label="Run")
                df[df.Type == 'Walk']['Distance'].plot(marker='o', linestyle='--', label="Walk")
                plt.xlabel('Dates of workouts', fontsize=12, fontweight="bold")
                plt.ylabel('Distance in km', fontsize=12, fontweight="bold")
                plt.legend()
                plt.title("Intensity curves of workouts for sneaker", fontsize=12, fontweight="bold")
                plt.grid(True)
                plt.yticks(range(0, int(df.Distance.max()), 2))
                plt.show()
            else:
                messagebox.showinfo("Message", "No such sneaker in DB or absent workouts for him")
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def show_statistics(self):
        if self.__sneakername.get() != "":
            df = self.__db.PrintWorkoutsForSneaker(self.__sneakername.get())
            if type(df) is pd.DataFrame and df.empty != True:
                walkkm = round(df[df.Type == 'Walk']['Distance'].sum(), 2)
                runkm = round(df[df.Type == 'Run']['Distance'].sum(), 2)
                totalkm = round(df['Distance'].sum(), 2)
                maxkmrun = df[df.Type == 'Run']['Distance'].max()
                minkmrun = df[df.Type == 'Run']['Distance'].min()
                maxdatrun = list(df[df.Distance == maxkmrun]['Date'])
                mindatrun = list(df[df.Distance == minkmrun]['Date'])
                if maxkmrun is not NaN and minkmrun is not NaN:
                    runstat = "Max km per workout for run: " + str(maxkmrun) + " at: \n" + str(maxdatrun) + "\n\n" + "Min km per workout for run: " + str(minkmrun) + " at: \n" + str(mindatrun) + "\n\n"
                else:
                    runstat = "No run workouts for this sneaker\n\n"
                maxkmwalk = df[df.Type == 'Walk']['Distance'].max()
                minkmwalk = df[df.Type == 'Walk']['Distance'].min()
                maxdatwalk = list(df[df.Distance == maxkmwalk]['Date'])
                mindatwalk = list(df[df.Distance == minkmwalk]['Date'])
                if maxkmwalk is not NaN and minkmwalk is not NaN:
                    walkstat = "Max km per workout for walk: " + str(maxkmwalk) + " at: \n" + str(maxdatwalk) + "\n\n" + "Min km per workout for walk: " + str(minkmwalk) + " at: \n" + str(mindatwalk)
                else:
                    walkstat = "No walk workouts for this sneaker"
                sumstat = "Sum km for walk: " + str(walkkm) + "\n" + "Sum km for run: " + str(runkm) + "\n" + "Total km: " + str(totalkm) + "\n\n"
                messagebox.showinfo("Statistics for sneaker", sumstat + runstat + walkstat)
            else:
                messagebox.showinfo("Message", "No such sneaker in DB or absent workouts for him")
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def list_of_sneakers(self):
        lst = self.__db.PrintSneakersNames()
        if lst:
            messagebox.showinfo("Sneakers in DB", "\n".join(str(name)[2:-3] for name in lst))
        else:
            messagebox.showinfo("Message", "No sneakers in DB")

    def help(self):
        mes = "How to use:\n\nTo add/delete sneaker specify name at [Sneaker model] entry;\n\nTo add/delete/edit workout for sneaker specify sneaker name at[Sneaker model], specify [Date of workout] and [Distance] entries and choise [Type] of workout as Walk/Run;\n\nTo watch statistics for sneaker specify its name at [Sneaker model] entry and choise appropriate item in [Show] menu;\n\nTo operate with CSV and XLSX files choise appropriate item in [File] menu.\n\nInput values format:\n\n[Sneaker model] format: from 3 to 25 symbols, first letter, only letters and numbers allowed;\n\n[Date of workout] format: string like dd.mm.yy;\n\n[Distance] format: float as ddd.dd from 0.00 to 999.99"
        messagebox.showinfo("Help", mes)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.__db.CloseConnection()
            self.__root.destroy()

def main(dbname: str):
    root = Tk()  
    ui = MainUI(root, dbname)
    ui.initUI()

if __name__=="__main__":
    main('SneakersWorkouts.db')
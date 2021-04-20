from DBOperations import DBManager
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd 
import matplotlib.pyplot as plt
import pandas as pd


class MainUI():

    def __init__(self, root, dbname):
        self.__sneakername = StringVar()
        self.__dateworkout = StringVar()
        self.__distance = StringVar()
        self.__choise = IntVar()
        self.__root = root
        self.__db = DBManager(dbname)
        self.initUI()
    
    def initUI(self):
        self.__db.SetConnection()
        self.__choise.set(1)
        self.__root.title('SneakersWorkouts')
        self.__root.resizable(width=False, height=False)
        x = (self.__root.winfo_screenwidth() - self.__root.winfo_reqwidth()) / 2.5
        y = (self.__root.winfo_screenheight() - self.__root.winfo_reqheight()) / 3.5 
        self.__root.wm_geometry("270x330+%d+%d"  % (x, y))
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        main_menu = Menu()

        file_menu = Menu(tearoff=0)
        file_menu.add_command(label="Add to DB from CSV file", command=self.CSVtoDB)
        file_menu.add_command(label="Write from DB to CSV file", command=self.DBtoCSV)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command = self.on_closing) 

        print_menu = Menu(tearoff=0)
        print_menu.add_command(label="Show graphic for walk", command=self.show_walk)
        print_menu.add_command(label="Show graphic for run", command=self.show_run)
        print_menu.add_command(label="Show statistics", command=self.show_statistics)

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

        del_model_button = Button(text="Insert workout", width='30', command=self.add_workout_todb)
        del_model_button.pack()

        del_model_button = Button(text="Edit workout", width='30', command=self.edit_workout)
        del_model_button.pack()

    def add_sneaker_todb(self):
        if self.__sneakername.get() != "":
            messagebox.showinfo("Message", self.__db.CreateNewSneaker(self.__sneakername.get()))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def del_sneaker_fromdb(self):
        if self.__sneakername.get() != "":
            if messagebox.askokcancel("Warning!!!", "This action also will delete all workouts for selected sneaker. Are you sure?"):
                messagebox.showinfo("Message", self.__db.DeleteSneaker(self.__sneakername.get()))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def add_workout_todb(self):
        if self.__sneakername.get() != "" and self.__dateworkout.get() != "" and self.__distance.get() != "":
            type = None
            if self.__choise.get() == 1:
                type = 'Walk'
            elif self.__choise.get() ==2:
                type = 'Run'
            messagebox.showinfo("Message", self.__db.CreateNewWorkout(self.__sneakername.get(), (self.__dateworkout.get(), type, self.__distance.get())))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] and [Date of workout] and [Distance] entry")

    def edit_workout(self):
        if self.__sneakername.get() != "" and self.__dateworkout.get() != "" and self.__distance.get() != "":
            if messagebox.askokcancel("Warning!!!", "Do you really want to make a change to workout?"):
                type = None
                if self.__choise.get() == 1:
                    type = 'Walk'
                elif self.__choise.get() ==2:
                    type = 'Run'
                messagebox.showinfo("Message", self.__db.EditWorkout(self.__sneakername.get(), (self.__dateworkout.get(), type, self.__distance.get())))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] and [Date of workout] and [Distance] entry")
    
    def CSVtoDB(self):
        if self.__sneakername.get() != "":
            filename = fd.askopenfilename()
            if filename != "":
                messagebox.showinfo("Message", self.__db.AddWorkoutsFromCSV(self.__sneakername.get(), filename))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def DBtoCSV(self):
        if self.__sneakername.get() != "":
            filename = fd.asksaveasfilename()
            if filename != "":
                messagebox.showinfo("Message", self.__db.AddWorkoutsToCSV(self.__sneakername.get(), filename))
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def show_walk(self):
        if self.__sneakername.get() != "":
            df = self.__db.PrintWorkoutsForSneaker(self.__sneakername.get())
            if type(df) is pd.DataFrame:
                df.set_index("Date", inplace=True)
                df[df.Type == 'Walk']['Distance'].plot()
                plt.show()
            else:
                messagebox.showinfo("Message", "No such sneaker in DB")
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def show_run(self):
        if self.__sneakername.get() != "":
            df = self.__db.PrintWorkoutsForSneaker(self.__sneakername.get())
            if type(df) is pd.DataFrame:
                df.set_index("Date", inplace=True)
                df[df.Type == 'Run']['Distance'].plot()
                plt.show()
            else:
                messagebox.showinfo("Message", "No such sneaker in DB")
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def show_statistics(self):
        if self.__sneakername.get() != "":
            df = self.__db.PrintWorkoutsForSneaker(self.__sneakername.get())
            if type(df) is pd.DataFrame:
                walkkm = round(df[df.Type == 'Walk']['Distance'].sum(), 2)
                runkm = round(df[df.Type == 'Run']['Distance'].sum(), 2)
                totalkm = round(df['Distance'].sum(), 2)
                maxkmwalk = df[df.Type == 'Walk']['Distance'].max()
                maxkmrun = df[df.Type == 'Run']['Distance'].max()
                maxdatwalk = list(df[df.Distance == maxkmwalk]['Date'])
                maxdatrun = list(df[df.Distance == maxkmrun]['Date'])
                messagebox.showinfo("Statistics for sneaker", "Sum km for walk: " + str(walkkm) + "\n" + "Sum km for run: " + str(runkm) + "\n" + "Total km: " + str(totalkm) +
                "\n\n" + "Max km per workout for walk: " + str(maxkmwalk) + " at: \n" + str(maxdatwalk) + "\n\n" + "Max km per workout for run: " + str(maxkmrun) + " at: \n" + str(maxdatrun))
            else:
                messagebox.showinfo("Message", "No such sneaker in DB")
        else:
            messagebox.showinfo("Message", "Input a value into [Sneaker model] entry")

    def help(self):
        mes = " Some help "
        messagebox.showinfo("Help", mes)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.__db.CloseConnection()
            self.__root.destroy()

def main(dbname: str):
    root = Tk()  
    ui = MainUI(root, dbname)
    root.mainloop()

if __name__=="__main__":
    main('SneakersWorkouts.db')
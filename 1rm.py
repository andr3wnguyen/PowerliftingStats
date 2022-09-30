from re import X
import sqlite3
import tkinter as tk
from tkinter import ACTIVE, DISABLED, END, LEFT, NORMAL, RIDGE, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import date

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs) #initiates the Tk window (in process becomes the controller)
        self.title("Powerlifting Helper")
        
        #design gui for each frame
        self.geometry("400x400")
        self.configure(background="purple", borderwidth=10)
        self.resizable("False", "False") #not resizable so able to use .place() more effectively

        #creates container for the frames
        container = tk.Frame(self, height=400, width=400)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        ##initiates dictionary of frames, each frame is set up to be in the container as an instance (container, self)
        self.frames = {}
        for F in (MainPage, OneRMPage, ProgrammesPage, HelpPage, Log, DatabaseTools):
            frame = F(container, self) 
            self.frames[F] = frame #adds iteration of the frame instance at key F into the self.frames dict
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage) #shows main page at default 

    #method below raises instance of the frame at key cont to the top (in view)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainPage(tk.Frame): #inherits from Frame
    def __init__(self, parent, controller): #initiates class, Frame is parent class, controller class is instance of the windows class.
        tk.Frame.__init__(self,parent) #initiates Frame class that this class inherits from
        label = tk.Label(self,text="Powerlifting Helper", relief="solid", font="verdana 20")
        label.place(x=50,y=150)

        oneRMButton = tk.Button(self,text="1 Rep Max Calculator", width=15, command=lambda:controller.show_frame(OneRMPage))
        oneRMButton.place(x=120,y=200)

        programmesButton = tk.Button(self,text="Programmes", width=15, command=lambda:controller.show_frame(ProgrammesPage))
        programmesButton.place(x=120,y=230)

        logButton = tk.Button(self, text="Lift Log", width=15, command=lambda:controller.show_frame(Log))
        logButton.place(x=120,y=260)

        helpButton = tk.Button(self, text="Help", width=15, command=lambda:controller.show_frame(HelpPage))
        helpButton.place(x=120,y=290)

        quitButton = tk.Button(self, text="Quit", width=15, command=lambda:windows.quit(self))
        quitButton.place(x=120,y=320)

class OneRMPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Calculate your 1RM", relief="solid").place(x=150, y=30)
        
        #buttons at top of page
        quit = tk.Button(self, text="Quit", command=lambda:windows.quit(self))
        quit.grid(row=0, column=3)

        helpButton = tk.Button(self, text="Help", command=lambda:messagebox.showinfo("Help", "Enter your the weight you have lifted into the 'Weight lifted:' box and select the number of completed repetitions from the drop-down. \nPress submit to see your estimated 1-rep maxes. These can be used for your workout programs. \n\nPress 'Show percentages' to see your working weight percentages."))
        helpButton.grid(row=0,column=2)

        backButton = tk.Button(self, text="Home", command = lambda:controller.show_frame(MainPage))
        backButton.grid(row=0, column=1)
               
        #result output
        console = tk.Label(self, height=13, width=51, background="grey", text = " ")
        console.place(x=10, y=165)

        #weight user input box; for user to put in weight lifted
        weightLabel = tk.Label(self, text="Weight lifted:", relief="ridge").place(x=100, y=60)
        userEntry = tk.Entry(self, width=6)
        userEntry.place(x=120,y=85, height=30)

        #number of reps at given weight; for user to put in repetitions performed
        repLabel = tk.Label(self, text="Number of repetitions:", relief="ridge").place(x=200, y=60)
        reps = [1,2,3,4,5,6,7,8,9,10]
        var = tk.StringVar(self)
        var.set("1")
        repsBox = tk.OptionMenu(self, var, *reps)
        repsBox.config(width=2)
        repsBox.place(x=220,y=85)
        
        #submit button to initiate calculations
        submitButton = tk.Button(self, text="Get 1RM", command=lambda:printMaxes())
        submitButton.place(x=165, y=130)


        # ==============methods for calculating 1rm Lombardi, brzycki, mcglothin and epley. Average calculated out for other uses ===============
        #calculations
        def epley(w,r):
            return int(w*(1+(r/30))) #r >1 

        def brzycki(w,r):
            return int(w* (36/(37-r)))

        def mcglothin(w,r):
            return int((100*w)/(101.3-(2.67123*r)))

        def lombardi(w,r):
            return int(w*(r**0.1))

        def averageLifts(w,r):
            return int((epley(w,r) + brzycki(w,r) + mcglothin(w,r) +lombardi(w,r))/4)
        #===================end of methods for calcaultions ======================================================================================

        #methods for returning user inputs for calculations
        def getReps():
            return int(var.get()) 

        def getWeight():
            #checks weight is number and returns weight
            try:
                return int(userEntry.get())
            except ValueError:
                console.config(text="Please enter a number for your weight!")

        #returns a string with the maxes calculated out using all the formula
        def calculateMaxes():
            w = getWeight()
            r = getReps()
            return "Estimated 1 rep maxes: " + "\n\nEpley:" + str(epley(w,r)) +  "\n Brzycki: " + str(brzycki(w,r)) + "\n McGlothin: " + str(mcglothin(w,r)) + "\n Lombardi: " + str(lombardi(w,r)) + "\n\n Average estimated 1RM: " + str(averageLifts(w,r))

        #prints to console for user to see
        def printMaxes():
            console.config(text=calculateMaxes())
            showPercentageButton.configure(state=ACTIVE)

        #============================ retrieve and print percentages ================================================================================#
        #method to calculate percentages
        def calcPercentages(lift, percent):
            return round(lift * percent/100)

        #method to return string listing percentages of the lift at 5% intervals
        def returnPercentages():
            resultStr = ""
            for i in range(100,50,-5):
                resultStr += str(i) + "% = " + str(calcPercentages(averageLifts(getWeight(),getReps()),i)) + "\n"
            return resultStr

        #method to print the percentages in the console
        def showPercentages():
            try:
                int(getWeight()) #checks if weight is entered
                console.configure(text = returnPercentages()) #changes the text in the console from 1 rep max to percentages
            except TypeError:
                console.configure(text="Please enter a weight and rep range") #changes text in the console to ask for a weight
    
        showPercentageButton = tk.Button(self, text = "Show Percentages", command=lambda:showPercentages(), state=DISABLED)
        showPercentageButton.place(x=140, y=335)



class ProgrammesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Programmes List",relief="solid").place(x=150, y=30)
        
        #buttons at top of page
        quit = tk.Button(self, text="Quit", command=lambda:windows.quit(self))
        quit.grid(row=0, column=3)

        helpButton = tk.Button(self, text="Help", command=lambda:messagebox.showinfo("Help", "Enter your calculated or actual 1RM values into the boxes and click on your preferred training regime! \n\nInformation for each programme will be shown at the bottom."))
        helpButton.grid(row=0,column=2)

        backButton = tk.Button(self, text="Home", command = lambda:controller.show_frame(MainPage))
        backButton.grid(row=0, column=1)

        #Frame for calendar weekly routine
        calendar = tk.Frame(self, width=350, height=200, bd=1, relief="ridge")
        calendar.place(x=15,y=170)

        #methods to populate calendar
        def populatecalendarDays():
            daysOfTheWeek=["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
            for i in range(7):
                tk.Label(calendar, text=daysOfTheWeek[i], width=5, height=2, padx=2, relief="ridge").grid(row=0, column=i+1)
        
        def populatecalendarLabels():
            lifts = ["Bench", "Squat", "Deadlift"]
            for i in range(len(lifts)):
                tk.Label(calendar, text=lifts[i], width=6,pady=3, height=2, relief="ridge").grid(row=i+1, column=0)

        populatecalendarDays()
        populatecalendarLabels()

        #entry boxes for lifts / before method (assignments)
        benchMaxEntry = tk.Entry(self, width=5)
        benchMaxEntry.place(x=90,y=60)
        squatMaxEntry = tk.Entry(self, width=5)
        squatMaxEntry.place(x=90, y=90)
        deadliftMaxEntry = tk.Entry(self, width=5)
        deadliftMaxEntry.place(x=90,y=120)

        #labels for entry boxes for lifts
        benchMaxLabel = tk.Label(self, text="1RM Bench", width=10, relief="ridge").place(x= 10, y=60)
        squatMaxLabel = tk.Label(self, text="1RM Squat", width=10, relief="ridge").place(x= 10, y=90)
        deadliftMaxLabel = tk.Label(self, text="1RM Deadlift", width=10, relief="ridge").place(x= 10, y=120)

        #methods to retrieve user data
        def getBench():
            try:
                float(benchMaxEntry.get())
                return int(benchMaxEntry.get())
            except:
                messagebox.showerror("Bench Error", "Please insert a number value (up to 1 d.p) for 1RM Bench.")

        def getSquat():
            try:
                float(squatMaxEntry.get())
                return int(squatMaxEntry.get())
            except:
                messagebox.showerror("Squat Error", "Please insert a numeric value (up to 1 d.p) for 1RM Squat.")

        def getDeadlift():
            try:
                float(deadliftMaxEntry.get())
                return int(deadliftMaxEntry.get())
            except:
                messagebox.showerror("Deadlift Error", "Please insert a numeric value (up to 1 d.p) for 1RM Deadlift.")





        #======================================= beginner programme methods linear +5% each session ====================================================

        #methods to calculate out weights and return an array to be iterated over
        def linearProgrammeNumbersBench(bench):
                return [str(int(bench)) + "kg \n 5x5", "x", str(int(bench*1.05)) + "kg \n 5x5", "x", str(int(bench*1.1)) + "kg \n 5x5", "x","x"]
        
        def linearProgrammeNumbersSquat(squat):
                return [str(int(squat)) + "kg \n 5x5", "x", str(int(squat*1.05)) + "kg \n 5x5", "x", str(int(squat*1.1)) + "kg \n 5x5", "x","x"]

        def linearProgrammeNumbersDeadlift(deadlift):
                return [str(int(deadlift)) + "kg \n 5x5", "x", str(int(deadlift*1.05)) + "kg \n 5x5", "x", str(int(deadlift*1.1)) + "kg \n 5x5", "x","x"]

        #methods to populate the calendar with linear program numbers
        def populateLinearProgrammeBench():
                for i in range(len(linearProgrammeNumbersBench(getBench()))):
                    tk.Label(calendar, text=linearProgrammeNumbersBench(getBench())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=1, column=i+1)
        
        def populateLinearProgrammeSquat():
                for i in range(len(linearProgrammeNumbersBench(getSquat()))):
                    tk.Label(calendar, text=linearProgrammeNumbersSquat(getSquat())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=2, column=i+1)
                    
        def populateLinearProgrammeDeadlift():
                for i in range(len(linearProgrammeNumbersBench(getDeadlift()))):
                    tk.Label(calendar, text=linearProgrammeNumbersDeadlift(getDeadlift())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=3, column=i+1)

        def populateLinearProgram():
            populateLinearProgrammeBench()
            populateLinearProgrammeSquat()
            populateLinearProgrammeDeadlift()
            tk.Label(self, text = "Add 5kg to your 1RM and repeat for 1 cycle if you succeed. \n If you fail, deload by 5kg and repeat until you can do 2 cycles.", relief="ridge", width = 49).place(x=15,y=330)



        #============================================ intermediate periodised progressive programme SBD calculations 5x5 BSD 60%, 70%, 80% +5 on each week ==============
        def progProgrammeNumbersBench(bench):
                return [str(int(bench*0.6)) + "kg \n 5x5", "x", str(int(bench*0.7)) + "kg \n 5x5", "x", str(int(bench*0.8)) + "kg \n 5x5", "x","x"]
        
        def progProgrammeNumbersSquat(squat):
                return [str(int(squat*0.6)) + "kg \n 5x5", "x", str(int(squat*0.7)) + "kg \n 5x5", "x", str(int(squat*0.8)) + "kg \n 5x5", "x","x"]

        def progProgrammeNumbersDeadlift(deadlift):
                return [str(int(deadlift*0.6)) + "kg \n 5x5", "x", str(int(deadlift*0.7)) + "kg \n 5x5", "x", str(int(deadlift*0.8)) + "kg \n 5x5", "x","x"]

        #methods to populate the calendar with progressive program numbers
        def populateProgProgrammeBench():
                for i in range(len(progProgrammeNumbersBench(getBench()))):
                    tk.Label(calendar, text=progProgrammeNumbersBench(getBench())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=1, column=i+1)
        
        def populateProgProgrammeSquat():
                for i in range(len(progProgrammeNumbersBench(getSquat()))):
                    tk.Label(calendar, text=progProgrammeNumbersSquat(getSquat())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=2, column=i+1)
                    
        def populateProgProgrammeDeadlift():
                for i in range(len(progProgrammeNumbersBench(getDeadlift()))):
                    tk.Label(calendar, text=progProgrammeNumbersDeadlift(getDeadlift())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=3, column=i+1)

        def populateProgProgram():
            populateProgProgrammeBench()
            populateProgProgrammeSquat()
            populateProgProgrammeDeadlift()
            tk.Label(self, text = "Add 5% to your 1RM and repeat for 2 cycles if you succeed. \n If you fail, deload by 10% and repeat until you can do 2 cycles.", relief="ridge", width = 49).place(x=15,y=330)

        #=========================================== powerbuilding 7-day split bsd ====================================== # 
        def powerProgrammeNumbersBench(bench):
                return [str(int(bench*0.9)) + "kg \n 3x3", "x", str(int(bench*0.8)) + "kg \n 5x5", "x", str(int(bench*0.6)) + "kg \n 3x8", "x",str(int(bench*0.5)) + "kg \n 3x12"]
        
        def powerProgrammeNumbersSquat(squat):
                return [str(int(squat*0.6)) + "kg \n 5x5", "x", str(int(squat*0.7)) + "kg \n 5x5", "x", str(int(squat*0.8)) + "kg \n 5x5",  str(int(squat*0.6)) + "kg \n 3x12","x"]

        def powerProgrammeNumbersDeadlift(deadlift):
                return ["x", str(int(deadlift*0.6)) + "kg \n 5x5", "x", "x", "x", str(int(deadlift*0.9))+ "kg \n 3x3", "x"]

        #methods to populate the calendar with progressive program numbers
        def populatePowerProgrammeBench():
                for i in range(len(powerProgrammeNumbersBench(getBench()))):
                    tk.Label(calendar, text=powerProgrammeNumbersBench(getBench())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=1, column=i+1)
        
        def populatePowerProgrammeSquat():
                for i in range(len(powerProgrammeNumbersBench(getSquat()))):
                    tk.Label(calendar, text=powerProgrammeNumbersSquat(getSquat())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=2, column=i+1)
                    
        def populatePowerProgrammeDeadlift():
                for i in range(len(powerProgrammeNumbersBench(getDeadlift()))):
                    tk.Label(calendar, text=powerProgrammeNumbersDeadlift(getDeadlift())[i],width=5, height=2,padx=2, pady=3, relief="ridge", anchor="center").grid(row=3, column=i+1)

        def populatePowerProgram():
            populatePowerProgrammeBench()
            populatePowerProgrammeSquat()
            populatePowerProgrammeDeadlift()
            tk.Label(self, text = "Add 5% to your 1RM and repeat for 1 cycle if you succeed. \n If you fail, deload by 5% and repeat until you can do 2 cycles.", relief="ridge", width = 49).place(x=15,y=330)

        # ============================================= end of programmes ============================================================

        #button for beginner programm - linear 
        #button for intermediate program - 5x5 progressive
        #button for intermediate program - powerbuilding split
        begProgButton = tk.Button(self, text="Beginner 5x5 Linear Progression", width=30, command=lambda:populateLinearProgram()).place(x=150, y=60)
        intProgButton = tk.Button(self, text="Intermediate 5x5 Weekly Progression", width=30, command=lambda:populateProgProgram()).place(x=150, y=90)
        advProgButton = tk.Button(self, text="Intermediate Powerbuilding Split", width=30, command=lambda:populatePowerProgram()).place(x=150, y=120)


class HelpPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Help Page").place(x=150, y=30)
        
        #buttons at top of page
        quit = tk.Button(self, text="Quit", command=lambda:windows.quit(self))
        quit.grid(row=0, column=3)

        helpButton = tk.Button(self, text="Help", command=lambda:messagebox.showinfo("Help"))
        helpButton.grid(row=0,column=2)

        backButton = tk.Button(self, text="Home", command = lambda:controller.show_frame(MainPage))
        backButton.grid(row=0, column=1)

        

#lets you log gym stats - bench, deadlift, squat stats (weights, dates, reps) - maybe a view progress/statisics page
class Log(tk.Frame): 
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Gym Log", relief="solid").place(x=150, y=30)
        
        #buttons at top of page
        quit = tk.Button(self, text="Quit", command=lambda:windows.quit(self))
        quit.grid(row=0, column=3)

        helpButton = tk.Button(self, text="Help", command=lambda:messagebox.showinfo("Help"))
        helpButton.grid(row=0,column=2)

        backButton = tk.Button(self, text="Home", command = lambda:controller.show_frame(MainPage))
        backButton.grid(row=0, column=1)

        #============================== layout
        #entry boxes for SBD weights
        squatWeightEntry = tk.Entry(self, width=3)
        squatWeightEntry.place(x=100,y=82)
        benchWeightEntry = tk.Entry(self, width=3)
        benchWeightEntry.place(x=100,y=112)
        deadliftWeightEntry = tk.Entry(self, width=3)
        deadliftWeightEntry.place(x=100, y=142) 

        #labels for SBD 
        squatLabel = tk.Label(self, text="Squat", relief="ridge",width=9, pady=2).place(x=10,y=80)
        benchLabel = tk.Label(self, text="Bench", relief="ridge", width=9, pady=2).place(x=10,y=110)
        deadliftLabel = tk.Label(self, text="Deadlift", relief="ridge", width=9, pady=2).place(x=10,y=140)

        #labels for SBD reps
        squatRepEntry = tk.Entry(self, width=3)
        squatRepEntry.place(x=170,y=82)
        benchRepEntry = tk.Entry(self, width=3)
        benchRepEntry.place(x=170,y=112)
        deadliftRepEntry = tk.Entry(self, width=3)
        deadliftRepEntry.place(x=170,y=142)
        repLabel = tk.Label(self, text="Reps", relief="ridge", width=9).place(x=147,y= 60)
        weightLabel = tk.Label(self, text="Weight", relief="ridge", width=9).place(x=78, y=60)

        #log lifts buttons, buttons to press to submit entry box values into the tb
        storeButton = tk.Button(self, text="Submit Squat", width=12, command=lambda:storeSquatData())
        storeButton.place(x=220,y=80)

        storeButton = tk.Button(self, text="Submit Bench", width=12,command=lambda:storeBenchData())
        storeButton.place(x=220,y=110)

        storeButton = tk.Button(self, text="Submit Deadlift", width=12, command=lambda:storeDeadliftData())
        storeButton.place(x=220,y=140)

        #methods to submit data to table in lifts database, creates table if it doesn't exist
        def storeSquatData():
            squatTableCreate()
            if type(getWeight("squat")) == int and type(getReps("squat")) == int:
                submitSquat()
                squatRepEntry.delete(0,END)
                squatWeightEntry.delete(0,END)
                messagebox.showinfo("Success", "Squat data stored for %s"%(date.today()))
            else:
                messagebox.showinfo("Error", "Missing parameter, check weight or number of reps is input correctly.")



        def storeBenchData():
            benchTableCreate()
            if type(getWeight("bench")) == int and type(getReps("bench")) == int:
                submitBench()
                benchRepEntry.delete(0,END)
                benchWeightEntry.delete(0,END)
                messagebox.showinfo("Success", "Bench press data stored for %s"%(date.today()))
            else:
                messagebox.showinfo("Error", "Missing parameter, check weight or number of reps is input correctly.")

        def storeDeadliftData():
            deadliftTableCreate()
            if type(getWeight("deadlift")) == int and type(getReps("deadlift")) == int:
                submitDeadlift()
                deadliftWeightEntry.delete(0,END)
                deadliftRepEntry.delete(0,END)
                messagebox.showinfo("Success", "Deadlift data stored for %s"%(date.today()))
            else:
                messagebox.showinfo("Error", "Missing parameter, check weight or number of reps is input correctly.")



        #create database and returns cursor to execute further queries
        def connectDB():
            return sqlite3.connect("lifts.db")

        
        def getWeight(lift):
            if lift == "bench":
                weight = int(float(benchWeightEntry.get()))
                return weight
            elif lift == "squat":
                weight = int(float(squatWeightEntry.get()))
                return weight
            elif lift == "deadlift":
                weight = int(float(deadliftWeightEntry.get()))
                return weight
            else: 
                return "Error"

        def getReps(lift):
            if lift == "bench":
                    if benchRepEntry.get() != "" and benchRepEntry.get() != None:
                        return int(benchRepEntry.get())
                    else:
                        messagebox.showerror("Please insert a value for number of reps")
            elif lift == "squat":
                    if squatRepEntry.get() != "" and squatRepEntry.get() != None:
                        return int(squatRepEntry.get())
                    else:
                        messagebox.showerror("Please insert a value for number of reps")
            elif lift == "deadlift":
                    if deadliftRepEntry.get() != "" and deadliftRepEntry.get() != None:
                        return int(deadliftRepEntry.get())
                    else:
                        messagebox.showerror("Please insert a value for number of reps")


        #db connector methods
        def squatTableCreate():
            conn = connectDB()
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS squatStats (date date, weight real, reps int)")
            conn.commit()
            conn.close()

        def deadliftTableCreate():
            conn = connectDB()
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS deadliftStats (date date, weight real, reps int)")
            conn.commit()
            conn.close()
    
        def benchTableCreate():
            conn = connectDB()
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS benchStats (date date, weight real, reps int)")
            conn.commit()
            conn.close()

        #method to send stats to database database 
        def submitSquat():
            conn = connectDB()
            c = conn.cursor()
            c.execute("INSERT INTO squatStats VALUES (:date, :weight, :reps)", {'date' : date.today(), 'weight': getWeight("squat"), 'reps': getReps("squat")})
            conn.commit()
            conn.close()
    
        def submitBench():
            conn = connectDB()
            c = conn.cursor()
            c.execute("INSERT INTO benchStats VALUES (:date, :weight, :reps)", {'date': date.today(), 'weight': getWeight("bench"), 'reps': getReps("bench")})
            conn.commit()
            conn.close()

        def submitDeadlift():
            conn = connectDB()
            c = conn.cursor()
            c.execute("INSERT INTO deadliftStats VALUES (:date, :weight, :reps)", {'date': date.today(), 'weight': getWeight("deadlift"), 'reps': getReps("deadlift")})
            conn.commit()
            conn.close()


        #method to view stats and progress
        def viewBench():
            conn = connectDB()
            c = conn.cursor()
            return list(c.execute("SELECT * from benchStats"))

        def viewSquat():
            conn = connectDB()
            c = conn.cursor()
            return list(c.execute("SELECT * from squatStats"))
        
        def viewDeadlift():
            conn = connectDB()
            c = conn.cursor()
            return list(c.execute("SELECT * from deadliftStats"))



        #frame to hold return info
        viewBox = tk.Frame(self, bd=1, relief="ridge", height=170, width=200)
        viewBox.place(x=160,y=195)

        #datalabels for results view

        dateLabelView = tk.Label(self, text = "Date")
        weightLabelView = tk.Label(self, text = "Weight")
        repsLabelView = tk.Label(self, text = "Reps")
        dateLabelView.place(x=180, y=170)
        weightLabelView.place(x=260, y=170)
        repsLabelView.place(x=320, y=170)

        #ScrolledText widget for results output (disabled text box), resultsBox returns view of results, viewBoxScroll is scrollbar
        resultsBox = ScrolledText(viewBox, height=10, width=23)
        resultsBox.pack(side="left")
        resultsBox.config(state=DISABLED)

        #formatting results returned from query
        def formatDeadliftData():
            a = viewDeadlift()
            resultString = ""
            for i in range(len(a)):
                resultString += str(a[i][0]) + "   " + str(a[i][1]) + "   " +str(a[i][2]) + "\n"
            return resultString

        def formatSquatData():
            a = viewSquat()
            resultString = ""
            for i in range(len(a)):
                resultString += str(a[i][0]) + "   " + str(a[i][1]) + "   " +str(a[i][2]) + "\n"
            return resultString

        def formatBenchData():
            a = viewBench()
            resultString = ""
            for i in range(len(a)):
                resultString += str(a[i][0]) + "   " + str(a[i][1]) + "   " +str(a[i][2]) + "\n"
            return resultString

        #return results to the text widget (resultBox)
        def getDeadlift():
            resultsBox.config(state=NORMAL)
            resultsBox.delete("1.0", END)
            resultsBox.insert("1.0",str(formatDeadliftData()))
            resultsBox.config(state=DISABLED)

        def getSquat():
            resultsBox.config(state=NORMAL)
            resultsBox.delete("1.0", END)
            resultsBox.insert("1.0",str(formatSquatData()))
            resultsBox.config(state=DISABLED)

        def getBench():
            resultsBox.config(state=NORMAL)
            resultsBox.delete("1.0", END)
            resultsBox.insert("1.0",str(formatBenchData()))
            resultsBox.config(state=DISABLED)

        #view buttons
        squatViewButton = tk.Button(self, text = "View Squats", width=12, command = lambda:getSquat())
        benchViewButton = tk.Button(self, text = "View Bench", width=12, command = lambda:getBench())
        deadliftViewButton = tk.Button(self, text = "View Deadlift", width=12, command = lambda:getDeadlift())
        squatViewButton.place(x=30, y=210)
        benchViewButton.place(x=30, y=240)
        deadliftViewButton.place(x=30, y=270)

        databaseToolsButton = tk.Button(self, text = "Database Tools", width=12, command = lambda:controller.show_frame(DatabaseTools))
        databaseToolsButton.place(x=30, y=330)




class DatabaseTools(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Database Tools",relief="solid").place(x=150, y=30)

        #buttons at top of page
        quit = tk.Button(self, text="Quit", command=lambda:windows.quit(self))
        quit.grid(row=0, column=3)

        helpButton = tk.Button(self, text="Help", command=lambda:messagebox.showinfo("Help", "Enter your calculated or actual 1RM values into the boxes and click on your preferred training regime! \n\nInformation for each programme will be shown at the bottom."))
        helpButton.grid(row=0,column=2)

        homeButton = tk.Button(self, text="Home", command = lambda:controller.show_frame(MainPage))
        homeButton.grid(row=0, column=1)

        def connectDB(): 
            return sqlite3.connect("lifts.db")



        #delete/reset tables
        def resetTable(lift):
            try:
                conn = connectDB()
                c = conn.cursor()
                try:
                    c.execute("DROP TABLE %s" %(lift))
                    c.close()
                    changeInfo.config(text="%s table reset successfully."%(lift).capitalize())
                except:
                    changeInfo.config(text="%s table does not exist.\n Please enter an entry through Log." %(lift).capitalize())
            except:
                changeInfo.config(text="%s database does not exist. \n Please enter an entry through Log." %(lift).capitalize())




        #delete specific
        def deleteSpecific(lift, date):
            pass


        #insert specific via date, weight, rep
        def insertSpecific(lift, date):
            pass
        

        #buttons to clear databases 
        resetSquat = tk.Button(self, text = "Clear Squat Data", width = 14, command = lambda: resetTable("squatStats"))
        resetBench = tk.Button(self, text = "Clear Bench Data", width = 14, command = lambda: resetTable("benchStats"))
        resetDeadlift = tk.Button(self, text = "Clear Deadlift Data", width = 14, command = lambda: resetTable("deadliftStats"))
        resetSquat.place(x=10, y=100)
        resetBench.place(x=10, y=130)
        resetDeadlift.place(x=10, y=160)

        #buttons to delete specific info at certain dates
        resetSquat = tk.Button(self, text = "Delete Squat", width = 14, command = lambda: resetTable("squat"))
        resetBench = tk.Button(self, text = "Delete Bench", width = 14, command = lambda: resetTable("bench"))
        resetDeadlift = tk.Button(self, text = "Delete Deadlift", width = 14, command = lambda: resetTable("deadlift"))
        resetSquat.place(x=130, y=100)
        resetBench.place(x=130, y=130)
        resetDeadlift.place(x=130, y=160)

        #buttons to add data at specific date
        addSquat = tk.Button(self, text = "Add Squat", width = 14, command = lambda: resetTable("squat"))
        addBench = tk.Button(self, text = "Add Bench", width = 14, command = lambda: resetTable("bench"))
        addDeadlift = tk.Button(self, text = "Add Deadlift", width = 14, command = lambda: resetTable("deadlift"))
        addSquat.place(x=250, y=100)
        addBench.place(x=250, y=130)
        addDeadlift.place(x=250, y=160)

        #label to confirm changes
        changeInfo = tk.Label(self, text ="", width = 30, height=3, relief=RIDGE)
        changeInfo.place(x=70,y=210)

        #back to log page
        backButton = tk.Button(self, text = "Back", width = 14, command = lambda:controller.show_frame(Log))
        backButton.place(x=130,y=300)








            



        #TODO: 
        #formatting retrieved results to not go onto next line/whitespace alterations
        #database tools form (delete or change entries, or add specific dates; new form with additional tools/widgets



            









        


if __name__ == "__main__":
    test = windows()
    test.mainloop()

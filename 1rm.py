from tkinter import *
from tkinter import messagebox

# interface window
window = Tk()
window.title("Lifting calculator")
window.configure(background="purple", borderwidth=10)
window.geometry("400x400")
window.resizable("False", "False")



#result output
console = Label(window, height=15, width=51, background="grey", text = " ")
console.place(x=10,y=135)

#weight user input box; for user to put in weight lifted
weightLabel = Label(window, text="Weight lifted:").place(x=100, y=10)
userEntry = Entry(window, width=6)
userEntry.place(x=120,y=50, height=30)

#number of reps at given weight; for user to put in repetitions performed
repLabel = Label(window, text="Number of repetitions:").place(x=200, y=10)
reps = [1,2,3,4,5,6,7,8,9,10]
var = StringVar(window)
var.set("1")
repsBox = OptionMenu(window, var, *reps)
repsBox.config(width=2)
repsBox.place(x=220,y=50)


#methods for calculating 1rm Lombardi, brzycki, mcglothin and epley. Average calculated out for other uses.
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

#GUI widgets

#submit button
submitButton = Button(window, text="Submit", command=lambda:printMaxes())
submitButton.place(x=165, y=100)

#frame
frame = Frame(window, relief=RAISED, bd=2)

window.mainloop()
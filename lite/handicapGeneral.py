# handicap.py

from Tkinter import *

class ScoreNeeded:

    def __init__(self,master):

        self.label1 = StringVar("")
        self.label2 = StringVar("")
        self.output1 = DoubleVar(0.0)
        self.output2 = DoubleVar(0.0)

        # row 0
        Label(master, text="Golf Handicap Calculator", fg='blue').grid(row=0,columnspan=2)

        # row 1
        Label(master, text="REQUIRED DATA", fg='red').grid(row=1,columnspan=2)

        # row 2
        Label(master, text="Current Handicap Index: ").grid(row=2,column=0,sticky=W)
        self.current = Entry(master)
        self.current.grid(row=2,column=1)

        # row 3
        Label(master, text="Replace Differential: ").grid(row=3,column=0,sticky=W)
        self.highestDiff = Entry(master)
        self.highestDiff.grid(row=3,column=1)

        # row 4
        Label(master, text="Course Rating: ").grid(row=4,column=0,sticky=W)
        self.courseRating = Entry(master)
        self.courseRating.grid(row=4,column=1)

        # row 5
        Label(master, text="Course Slope: ").grid(row=5,column=0,sticky=W)
        self.courseSlope = Entry(master)
        self.courseSlope.grid(row=5,column=1)

        # row 6
        Label(master, text="").grid(row=6)

        # row 7
        Label(master, text="OPTIONAL DATA", fg='red').grid(row=7,columnspan=2)

        # row 8
        Label(master, text="Best Unused Differential: ").grid(row=8,column=0,sticky=W)
        self.bestUnused = Entry(master)
        self.bestUnused.grid(row=8,column=1)

        # row 9
        Label(master, text="Score (ESC Gross): ").grid(row=9,column=0,sticky=W)
        self.score = Entry(master)
        self.score.grid(row=9,column=1)

        # row 10
        Label(master, text="Best Ever (Differential): ").grid(row=10,column=0,sticky=W)
        self.bestEver = Entry(master)
        self.bestEver.grid(row=10,column=1)

        # row 11
        Button(master,text="Run",command=self.run).grid(row=11,column=0,sticky=E+W,columnspan=2)

        # row 12
        Label(master, text="").grid(row=12)

        # row 13
        Label(master, text="OUTPUT", fg='red').grid(row=13,columnspan=2)

        # row 14
        Label(master, textvariable=self.label1, fg='red').grid(row=14,column=0,sticky=W)
        Label(master, textvariable=self.output1, fg='red').grid(row=14,column=1)

        # row 15
        Label(master, textvariable=self.label2, fg='red').grid(row=15,column=0,sticky=W)
        Label(master, textvariable=self.output2, fg='red').grid(row=15,column=1)

        # row 16
        Label(master, text="").grid(row=16)

        # row 17
        Label(master, text="INSTRUCTIONS", fg='red').grid(row=17,columnspan=3)

        # rows 18-20
        Label(master, text="Replace Differential: Enter the largest differential").grid(row=18,columnspan=2,sticky=W)
        Label(master, text="that contributes to your current handicap index, i.e.,").grid(row=19,columnspan=2,sticky=W)
        Label(master, text="the 10th best of your most recent 20 scores.").grid(row=20,columnspan=2,sticky=W)

        # row 21
        Label(master, text="").grid(row=21)

        # rows 22-24
        Label(master, text="Best Unused Differential: If the oldest differential").grid(row=22,columnspan=2,sticky=W)
        Label(master, text="contributing to your current handicap index is one of").grid(row=23,columnspan=2,sticky=W)
        Label(master, text="your 10 best, provide your 11th best differential here.").grid(row=24,columnspan=2,sticky=W)


    def run(self):
        c = float(self.current.get())
        hD = float(self.highestDiff.get())
        cR = float(self.courseRating.get())
        cS = float(self.courseSlope.get())

        bU = self.bestUnused.get()
        s = self.score.get()
        bE = self.bestEver.get()
        
        if s == "":            
            self.label1.set("Reduce Handicap: ")
            self.output1.set(int((int(10*hD-1/0.096)/10.0+0.0499)*(cS/113.0)+cR))
            if bE != "":
                bE = float(bE)
                self.label2.set("Best Ever: ")
                self.output2.set(int((bE-0.0501)*cS/113.0+cR))
            return
        else:
            self.label1.set("New Handicap Min: ")
            self.label2.set("New Handicap Max: ")
            s = float(s)
            sD = (s-cR)*(113.0/cS)
            if bU != "":
                bU = float(bU)
                nD = min(sD,bU)
                self.output1.set(int((round(c/0.096,1)-round(hD-nD,1))*0.96)/10.0)
                self.output2.set(int((round((c+0.1)/0.096,1)-round(hD-nD,1))*0.96)/10.0)
            elif sD >= hD: 
                self.output1.set(c)
                self.output2.set(c)
            else:
                self.output1.set(int((round(c/0.096,1)-round(hD-sD,1))*0.96)/10.0)
                self.output2.set(int((round((c+0.1)/0.096,1)-round(hD-sD,1))*0.96)/10.0)
            return

root = Tk()
app = ScoreNeeded(root)
root.mainloop()

# handicap.py

from Tkinter import *

class ScoreNeeded:

    def __init__(self,master):

        self.label1 = StringVar("")
        self.label2 = StringVar("")
        self.output1 = DoubleVar(0.0)
        self.output2 = DoubleVar(0.0)

        # row 0
        Label(master, text="Handicap Calculator", fg='blue').grid(row=0,columnspan=2)

        # row 1
        Label(master, text="Current Handicap: ").grid(row=1,column=0,sticky=W)
        self.current = Entry(master)
        self.current.grid(row=1,column=1)

        # row 2
        Label(master, text="Replace Differential: ").grid(row=2,column=0,sticky=W)
        self.highestDiff = Entry(master)
        self.highestDiff.grid(row=2,column=1)

        # row 3
        Label(master, text="Best Unused: ").grid(row=3,column=0,sticky=W)
        self.bestUnused = Entry(master)
        self.bestUnused.grid(row=3,column=1)

        # row 4
        Label(master, text="Course Slope: ").grid(row=4,column=0,sticky=W)
        self.courseSlope = Entry(master)
        self.courseSlope.grid(row=4,column=1)

        # row 5
        Label(master, text="Course Rating: ").grid(row=5,column=0,sticky=W)
        self.courseRating = Entry(master)
        self.courseRating.grid(row=5,column=1)

        # row 6
        Label(master, text="Score: ").grid(row=6,column=0,sticky=W)
        self.score = Entry(master)
        self.score.grid(row=6,column=1)

        # row 7
        Button(master,text="Run",command=self.run).grid(row=7,column=0,sticky=E+W,columnspan=2)

        # row 8
        Label(master, textvariable=self.label1, fg='red').grid(row=8,column=0,sticky=W)
        Label(master, textvariable=self.output1, fg='red').grid(row=8,column=1)

        # row 9
        Label(master, textvariable=self.label2, fg='red').grid(row=9,column=0,sticky=W)
        Label(master, textvariable=self.output2, fg='red').grid(row=9,column=1)

    def run(self):
        bestDiffEver = 6
        s = self.score.get()
        bU = self.bestUnused.get()
        c = float(self.current.get())
        hD = float(self.highestDiff.get())
        cS = float(self.courseSlope.get())
        cR = float(self.courseRating.get())
        if s == "":            
            self.label1.set("Reduce Handicap: ")
            self.output1.set(int(((-0.1)/0.096+hD)*(cS/113.0)+cR))
            self.label2.set("Best Ever: ")
            self.output2.set(int(bestDiffEver*cS/113.0+cR))
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

from Tkinter import *
import MySQLdb
import sys
import easygui

WINDOW_SIZE = '960x540'
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'AddieRose621'
DB_DB = 'handicap'
courses = {}

def initialize():
    try:
        conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DB)
        cursor = conn.cursor()
    except Exception as e:
        print 'Error connecting to MySQL: {0}'.format(e)
        sys.exit(1)
    try:
        columnString = 'course_name,tee,rating,slope,outYards,inYards,totalYards,outPar,inPar,totalPar'
        for k in range(18): columnString += (',hole'+str(k+1)+'Yards,hole'+str(k+1)+'Par')
        cursor.execute('SELECT {0} FROM courses'.format(columnString)) 
        for cn,t,r,s,oY,iY,tY,oP,iP,tP,h1Y,h1P,h2Y,h2P,h3Y,h3P,h4Y,h4P,h5Y,h5P,h6Y,h6P,h7Y,h7P,h8Y,h8P,h9Y,h9P,h10Y,h10P,h11Y,h11P,h12Y,h12P,h13Y,h13P,h14Y,h14P,h15Y,h15P,h16Y,h16P,h17Y,h17P,h18Y,h18P in cursor.fetchall(): 
            if not cn in courses: courses[cn] = {}
            courses[cn][t] = {
                'rating': r, 
                'slope': s,
                'hole1Yards': h1Y, 'hole1Par': h1P,
                'hole2Yards': h2Y, 'hole2Par': h2P,
                'hole3Yards': h3Y, 'hole3Par': h3P,
                'hole4Yards': h4Y, 'hole4Par': h4P,
                'hole5Yards': h5Y, 'hole5Par': h5P,
                'hole6Yards': h6Y, 'hole6Par': h6P,
                'hole7Yards': h7Y, 'hole7Par': h7P,
                'hole8Yards': h8Y, 'hole8Par': h8P,
                'hole9Yards': h9Y, 'hole9Par': h9P,
                'outYards': oY, 'outPar': oP,
                'hole10Yards': h10Y, 'hole10Par': h10P,
                'hole11Yards': h11Y, 'hole11Par': h11P,
                'hole12Yards': h12Y, 'hole12Par': h12P,
                'hole13Yards': h13Y, 'hole13Par': h13P,
                'hole14Yards': h14Y, 'hole14Par': h14P,
                'hole15Yards': h15Y, 'hole15Par': h15P,
                'hole16Yards': h16Y, 'hole16Par': h16P,
                'hole17Yards': h17Y, 'hole17Par': h17P,
                'hole18Yards': h18Y, 'hole18Par': h18P,
                'inYards': iY, 'inPar': iP,
                'totalYards': tY, 'totalPar': tP
                }
    except Exception as e:
        print 'Error loading courses from MySQL: {0}'.format(e)
        sys.exit(1)

def placeTitle(master,title,cSpan): return Label(master, text=title, fg="blue", font=("Times", 48)).grid(row=0,column=0,columnspan=cSpan)

class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        initialize()
        
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for c in (HomeScreen, EnterScoreScreen, AddCourseScreen):
            frame = c(container, self)
            self.frames[c] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(HomeScreen)
        
    def show_frame(self, c):
        try: 
            frame = self.frames[c]
            frame.tkraise()
        except KeyError: return
    
    def refresh_frame(self, container, c):
        try:
            frame = self.frames[c]
            frame.destroy()
            frame = c(container, self)
            self.frames[c] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        except KeyError: return

class AddCourseScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        placeTitle(self,"Add A New Course",8)
        Label(self, text="Enter Course Name: ").grid(row=1, column=0, columnspan=4, sticky=E)
        self.holeYards = self.holePar = [0]*18
        self.courseName = Entry(self)
        self.courseName.grid(row=1, column=4, columnspan=4)
        Label(self, text="Enter Tee: ").grid(row=2, column=0, columnspan=4, sticky=E)
        self.tee = Entry(self)
        self.tee.grid(row=2, column=4, columnspan=4)
        Label(self, text="Enter Course Rating: ").grid(row=3, column=0, columnspan=4, sticky=E)
        self.rating = Entry(self, width=4)
        self.rating.grid(row=3, column=4)
        Label(self, text="Enter Course Slope: ").grid(row=4, column=0, columnspan=4, sticky=E)
        self.slope = Entry(self, width=4)
        self.slope.grid(row=4, column=4)
        for k in range(18): Label(self, text=str(k+1)).grid(row=5, column=k+2)
        Label(self, text="Par").grid(row=6, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holePar[k] = Entry(self, width=3)
            self.holePar[k].grid(row=6, column=k+2)
        Label(self, text="Yardage").grid(row=7, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holeYards[k] = Entry(self, width=3)
            self.holeYards[k].grid(row=7, column=k+2)
        addCourseButton = Button(self, text='Submit', command=lambda: self.addCourse(parent, controller)).grid(row=8, column=2)

    def addCourse(self, parent, controller):
        if self.courseName.get() not in courses: courses[self.courseName.get()] = {}
        if self.tee.get() not in courses[self.courseName.get()]:
            teeDict = {'rating': float(self.rating.get()), 'slope': int(self.slope.get())}
            for k in range(18): 
                teeDict['hole'+str(k+1)+'Yards'] = int(self.holeYards[k].get())
                teeDict['hole'+str(k+1)+'Par'] = int(self.holePar[k].get())
            teeDict['outYards'] = sum([teeDict['hole'+str(k)+'Yards'] for k in range(1,10)])
            teeDict['outPar'] = sum([teeDict['hole'+str(k)+'Par'] for k in range(1,10)])
            teeDict['inYards'] = sum([teeDict['hole'+str(k)+'Yards'] for k in range(10,19)])
            teeDict['inPar'] = sum([teeDict['hole'+str(k)+'Par'] for k in range(10,19)])
            teeDict['totalYards'] = teeDict['outYards'] + teeDict['inYards']
            teeDict['totalPar'] = teeDict['outPar'] + teeDict['inPar']
            courses[self.courseName.get()][self.tee.get()] = teeDict
        else:
            easygui.msgbox('Already added {0} tees for {1}, no changes were made!'.format(self.tee.get(), self.courseName.get()), title='Error! Course/tee already exists')
            controller.refresh_frame(parent, HomeScreen)
            controller.show_frame(HomeScreen)
            return
        columnString = 'course_name, tee, rating, slope, outYards, inYards, totalYards'
        for k in range(18): columnString += (', hole'+str(k+1))
        valueString = "'{0}', '{1}', {2}, {3}, ".format(self.courseName.get(), self.tee.get(), self.rating.get(), self.slope.get())
        outYards, inYards = sum([int(self.holeYards[k].get()) for k in range(9)]), sum([int(self.holeYards[k].get()) for k in range(9,18)])
        totalYards = outYards+inYards
        valueString += '{0}, {1}, {2}, '.format(outYards, inYards, totalYards)
        self.holeYards[0] = self.holeYards[0].get()
        valueString += reduce(lambda x,y: x+', '+y.get(), self.holeYards)
        try:
            conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DB)
            cursor = conn.cursor()
        except Exception as e:
            print 'Error connecting to MySQL: {0}'.format(e)
            sys.exit(1)
        try: 
            cursor.execute('INSERT INTO courses ({0}) VALUES ({1})'.format(columnString, valueString)) 
            cursor.execute('COMMIT')
        except Exception as e:
            print 'Error loading course into MySQL: {0}'.format(e)
            sys.exit(1)
        else:
            controller.refresh_frame(parent, HomeScreen)
            controller.show_frame(HomeScreen)

class EnterScoreScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.totalScore = IntVar()
        self.totalPutts = IntVar()
        self.totalFairway = DoubleVar()
        self.totalPenalties = IntVar()
        self.totalSandShots = IntVar()
        self.holeScore = [0]*18
        self.holePutts = [0]*18
        self.holeFairway = ['-']*18
        self.holePenalties = [0]*18
        self.holeSandShots = [0]*18

        placeTitle(self,"Enter Score",8)
        Label(self, text="Select course: ").grid(row=1, column=0, columnspan=3, sticky=E)

        self.course,self.tee = StringVar(),StringVar()
        courseList = courses.keys()
        self.course.set(courseList[0])
        OptionMenu(self, self.course, *courseList).grid(row=1, column=3, columnspan=3, sticky=E)
        selectCourseButton = Button(self, text='Select Course', command=lambda: self.selectCourse(parent, controller)).grid(row=2, column=3, columnspan=3, sticky=E)

    def selectCourse(self, parent, controller):
        teeList = courses[self.course.get()].keys()
        self.tee.set(teeList[0])
        for i,t in enumerate(courses[self.course.get()]): Radiobutton(self, text=t, variable=self.tee, value=t).grid(row=3, column=3+3*i, columnspan=3, sticky=E)
        selectTeeButton = Button(self, text='Select Tee', command=lambda: self.selectTee(parent, controller)).grid(row=4, column=3, columnspan=3, sticky=E)
        
    def selectTee(self, parent, controller):
        c = self.course.get()
        t = self.tee.get()
        # hole row
        Label(self, text="Hole").grid(row=5, column=0, columnspan=2, sticky=E)
        for k in range(18): Label(self, text=str(k+1)).grid(row=5, column=2+k)
        Label(self, text="Total").grid(row=5, column=20)
        # yardage row
        Label(self, text="Yardage").grid(row=6, column=0, columnspan=2, sticky=E)
        for k in range(18): Label(self, text=str(courses[c][t]['hole'+str(k+1)+'Yards'])).grid(row=6, column=2+k)
        Label(self, text=str(courses[c][t]['totalYards'])).grid(row=6, column=20)
        # score row
        Label(self, text="Strokes").grid(row=7, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holeScore[k] = Entry(self, width=2)
            self.holeScore[k].grid(row=7, column=2+k)
            self.holeScore[k].bind("<KeyRelease>", self.updateTotalScore, '+')
        Label(self, textvariable=self.totalScore).grid(row=7, column=20)
        # putts row
        Label(self, text="Putts").grid(row=8, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holePutts[k] = Entry(self, width=2)
            self.holePutts[k].grid(row=8, column=2+k)
            self.holePutts[k].bind("<KeyRelease>", self.updateTotalPutts, '+')
        Label(self, textvariable=self.totalPutts).grid(row=8, column=20)
        # fairway row
        Label(self, text="Fairway").grid(row=9, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holeFairway[k] = Entry(self, width=2)
            self.holeFairway[k].grid(row=9, column=2+k)
            self.holeFairway[k].bind("<KeyRelease>", self.updateTotalFairway, '+')
        Label(self, textvariable=self.totalFairway).grid(row=9, column=20)
        # penalties row
        Label(self, text="Penalties").grid(row=10, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holePenalties[k] = Entry(self, width=2)
            self.holePenalties[k].grid(row=10, column=2+k)
        # sand shots row
        Label(self, text="Sand shots").grid(row=11, column=0, columnspan=2, sticky=E)
        for k in range(18):
            self.holeSandShots[k] = Entry(self, width=2)
            self.holeSandShots[k].grid(row=11, column=2+k)
        submitScoresButton = Button(self, text='Submit', command=lambda: self.submit(parent, controller)).grid(row=12, column=2)

    def updateTotalScore(self, event):
        tmpSum = 0
        for k in range(18): 
            if self.holeScore[k].get() != '': 
                try: tmpSum += int(self.holeScore[k].get())
                except ValueError: easygui.msgbox('Must enter integer!')
        self.totalScore.set(tmpSum)

    def updateTotalPutts(self, event):
        tmpSum = 0
        for k in range(18): 
            if self.holePutts[k].get() != '': 
                try: tmpSum += int(self.holePutts[k].get())
                except ValueError: easygui.msgbox('Must enter integer!')
        self.totalPutts.set(tmpSum)

    def updateTotalFairway(self, event):
        tmpSum = tmpDenom = 0
        for k in range(18): 
            if self.holeFairway[k].get() != '': 
                tmpSum += int(self.holeFairway[k].get() == 'Hit')
                tmpDenom += 1
        self.totalFairway.set(tmpSum*100.0/tmpDenom)

    def submit(self, parent, controller):
        self.totalScore.set(sum([int(self.holeScore[k].get()) for k in range(18)]))
        self.totalPutts.set(sum([int(self.holePutts[k].get()) for k in range(18)]))
        self.totalFairway.set(sum([self.holeFairway[k].get()=='Hit' for k in range(18)])*100.0/18.0)
        self.totalPenalties.set(sum([int(self.holePenalties[k].get()) for k in range(18)]))
        self.totalSandShots.set(sum([int(self.holeSandShots[k].get()) for k in range(18)]))
        print 'score = {0}, putts = {1}, fairway = {2}, penalties = {3}, sand shots = {4}'.format(self.totalScore.get(), self.totalPutts.get(), self.totalFairway.get(), self.totalPenalties.get(), self.totalSandShots.get())


        #TODO need to add score to database (well I need to collect other info first.. fairways, putts, etc)

class HomeScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        placeTitle(self,"Home",2)
        for k in range(6): Label(self, text=" ").grid(row=k+1)
        Label(self, text="What would you like to do?").grid(row=7, column=1, sticky=E)
        Button(self, text="Enter Score", command=lambda: self.enterScore(parent, controller)).grid(row=9, column=1, sticky=W)
        Button(self, text="Add a Course", command=lambda: self.addCourse(parent, controller)).grid(row=9, column=2, sticky=W)
        
    def enterScore(self, parent, controller):
        if len(courses) == 0: 
            easygui.msgbox('Please add a course before entering scores', title='Error: No Courses Available!')
            return
        controller.refresh_frame(parent, EnterScoreScreen)
        controller.show_frame(EnterScoreScreen)

    def addCourse(self, parent, controller):
        controller.refresh_frame(parent, AddCourseScreen)
        controller.show_frame(AddCourseScreen)







'''
        Label(self, text="Callback URL: ").grid(row=0, column=2, sticky=E)
        self.callback = Entry(self)
        self.callback.grid(row=0, column=3)
        Button(self, text="Refresh", command=lambda: self.refresh(parent, controller)).grid(row=0, column=4)
        Label(self, text="Hub Endpoint URL:  "+hubURL, fg="red").grid(row=1, column=0, sticky=W)
        for k in range(4): Label(self, text=" ").grid(row=k+2)
        Label(self, text="Topics", font=("Times",24)).grid(row=6, column=1, sticky=W)
        Label(self, text=currentSubscriber, fg="gray").grid(row=6, column=2, sticky=E)
        Label(self, text=" ").grid(row=7)
        for i,topic in enumerate(sorted(subscriptions)):
            Label(self, text="{0}.  {1}  ".format(i+1,topic)).grid(row=8+i, column=1, sticky=W)
            if currentSubscriber in subscriptions[topic]: Button(self, text="Unsubscribe", command=lambda t=topic: self.unsubscribe(t, parent, controller)).grid(row=8+i, column=2, sticky=E+W)
            else: Button(self, text="Subscribe", command=lambda t=topic: self.subscribe(t, parent, controller)).grid(row=8+i, column=2, sticky=E+W)

    def refresh(self, parent, controller):
        global currentSubscriber
        currentSubscriber = 'http://'+self.callback.get().lstrip('http://')
        controller.refresh_frame(parent, SubUnsubScreen)
        controller.show_frame(SubUnsubScreen)

    def subscribe(self, topic, parent, controller):
        runSubscribe(currentSubscriber, topic, 'sync')
        refreshSubscriptions()
        controller.refresh_frame(parent, SubUnsubScreen)
        controller.show_frame(SubUnsubScreen)

    def unsubscribe(self, topic, parent, controller):
        runUnsubscribe(currentSubscriber, topic, 'sync')
        refreshSubscriptions()
        controller.refresh_frame(parent, SubUnsubScreen)
        controller.show_frame(SubUnsubScreen)



class SubUnsubScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        placeTitle(self,"Subscribe Screen",1)
        Label(self, text="Callback URL: ").grid(row=0, column=2, sticky=E)
        self.callback = Entry(self)
        self.callback.grid(row=0, column=3)
        Button(self, text="Refresh", command=lambda: self.refresh(parent, controller)).grid(row=0, column=4)
        Label(self, text="Hub Endpoint URL:  "+hubURL, fg="red").grid(row=1, column=0, sticky=W)
        for k in range(4): Label(self, text=" ").grid(row=k+2)
        Label(self, text="Topics", font=("Times",24)).grid(row=6, column=1, sticky=W)
        Label(self, text=currentSubscriber, fg="gray").grid(row=6, column=2, sticky=E)
        Label(self, text=" ").grid(row=7)
        for i,topic in enumerate(sorted(subscriptions)):
            Label(self, text="{0}.  {1}  ".format(i+1,topic)).grid(row=8+i, column=1, sticky=W)
            if currentSubscriber in subscriptions[topic]: Button(self, text="Unsubscribe", command=lambda t=topic: self.unsubscribe(t, parent, controller)).grid(row=8+i, column=2, sticky=E+W)
            else: Button(self, text="Subscribe", command=lambda t=topic: self.subscribe(t, parent, controller)).grid(row=8+i, column=2, sticky=E+W)

    def refresh(self, parent, controller):
        global currentSubscriber
        currentSubscriber = 'http://'+self.callback.get().lstrip('http://')
        controller.refresh_frame(parent, SubUnsubScreen)
        controller.show_frame(SubUnsubScreen)

    def subscribe(self, topic, parent, controller):
        runSubscribe(currentSubscriber, topic, 'sync')
        refreshSubscriptions()
        controller.refresh_frame(parent, SubUnsubScreen)
        controller.show_frame(SubUnsubScreen)

    def unsubscribe(self, topic, parent, controller):
        runUnsubscribe(currentSubscriber, topic, 'sync')
        refreshSubscriptions()
        controller.refresh_frame(parent, SubUnsubScreen)
        controller.show_frame(SubUnsubScreen)
'''


if __name__ == "__main__":
    app = Application()
    app.title('Handicap Software')
    app.geometry(WINDOW_SIZE)
    app.mainloop()

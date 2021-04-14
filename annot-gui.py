import pandas as pd 
import os
from os import path
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog



class simpleapp_tk(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.index = 0

        self.datafile = datafile #name of the file currently working on
        self.result_df = d #dataframe

        self.speaker = self.result_df["Speaker"]
        self.orthography = self.result_df["Orthography"]
        self.record = self.result_df["Record #"]

        #intialize item attribute
        self.item = tk.StringVar()

        self.progress = tk.StringVar()
        #self.variables = []
        self.clausetype= tk.StringVar()
        self.speechact= tk.StringVar()
        self.comment = tk.StringVar()
        self.subQ = tk.StringVar()
        self.subI = tk.StringVar()
        self.followup = tk.IntVar()
        #as long as ShowExisting() comes after initialization, it's fine     

#Frame:textbox
        textFrame = tk.Frame(self)
        textFrame.grid(column=0, row = 0, rowspan = 25)
        #show the titile of the datafile
        label = tk.Label(textFrame, text = "Current file: "+ self.datafile)
        label.grid(column = 0, row = 0, sticky = "sw")
        #setup the textbox        
        self.text = tk.Text(textFrame, height=35, bg = "#f1f8e9")
        #3 styles of the text display
        self.text.tag_configure("bold", font=("Arial", 14, "bold"), background="#5FFB17")
        self.text.tag_configure("italics", font=("Arial", 14, "italic"), background="#FFDB58")
        self.text.tag_configure("normal", font = ("Arial", 14))
        self.text.grid(column=0, row=1, rowspan = 25)

        #initiate the progress bar
        self.progress = tk.StringVar()

        #display the textbox
        self.DisplayData()

        #display the annotation labels
        self.initialize()

        #when press x to close window, save before close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def DisplayData(self):
        #the progress bar: current record#/all record#
        self.progress.set(str(self.index+1)+"/"+str(len(self.record)))
        self.item.set("\n" + str(self.record[self.index]) + ". " + self.speaker[self.index] + ": " + self.orthography[self.index])

        self.text.configure(state='normal')
        self.text.delete(0.0,'end')
        
        self.prior = max(0, self.index-20)
        self.post = min(len(self.record), self.index+3)

        for i in range(self.prior, self.post):
            if i < self.index:
                self.text.insert("end", str(self.record[i]) + ". " + self.speaker[i] + ": " + self.orthography[i] +"\n", "normal")
            elif i == self.index:
                if self.result_df["SpeechAct"][self.index] == "Question":
                    self.text.insert("end", str(self.record[self.index]) + ". " + self.speaker[self.index] + ": " + self.orthography[self.index]+"\n" , "bold")
                else:
                    self.text.insert("end", str(self.record[self.index]) + ". " + self.speaker[self.index] + ": " + self.orthography[self.index]+"\n" , "italics")
 
            elif i > self.index :
                self.text.insert("end", str(self.record[i]) + ". " + self.speaker[i] + ": " + self.orthography[i]+"\n" , "normal")
        
        self.text.configure(state='disabled')

    #if there's existing data, read in and set value
    def ShowExisting(self):
        self.clausetype.set(self.result_df["ClauseType"][self.index])
        self.speechact.set(self.result_df["SpeechAct"][self.index])
        self.situation.set(self.result_df["Situation"][self.index])
        self.comment.set(self.result_df["Comments"][self.index])
        self.subI.set(self.result_df["SubI"][self.index])
        self.subQ.set(self.result_df["SubQ"][self.index])
        self.followup.set(self.result_df["FollowUp?"][self.index])
        self.uttgoals.set(self.result_df["UttGoals"][self.index])
        
        if self.result_df["SpeechAct"][self.index] == "Question":
            self.SubQStatus("normal")
        if self.result_df["ClauseType"][self.index] =="Interrogative":
            self.SubIStatus("normal")

        for [f,x] in self.synfeatures:
            if self.result_df[f][self.index] != None:
                x.set(self.result_df[f][self.index])
        for [feature,var] in self.discfeatures:
            if self.result_df[feature][self.index] != None:
                var.set(self.result_df[feature][self.index])
    #initialize the buttons

    def initialize(self):
        self.grid()
        #list of all buttons
        self.radios=[]
        #list of subQ and subI buttons
        self.subQ_buttons =[]
        self.subI_buttons =[]

        #buttons; ("label","writing in the coding file")
        speechActs = [("Assertion","Assertion"),("Question","Question"),("Request","Request"), ("Exclamative", "Exclamative"), ("Other","")]
        clauseTypes = [("Declarative","Declarative"),("Interrogative","Interrogative"),("Imperative","Imperative"),("Fragment","FRAG"), ("Exclamative", "Exclamative"), ("Other","")]

        #initialize attributes; need to come before self.showingexisting() is called
        self.clausetype= tk.StringVar()
        self.speechact= tk.StringVar()
        self.comment = tk.StringVar()
        self.subQ = tk.StringVar()
        self.subI = tk.StringVar()
        self.followup = tk.IntVar()

        #build the buttons
        #set up the row for the buttons
        i = 0

        #speechact buttons
        #label the category
        label = tk.Label(self,text="Speech Act")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        #build buttons for speech act
        for text,value in speechActs:
            b = tk.Radiobutton(self,text=text,variable=self.speechact,
                value=value,indicatoron=0,width=10,height=1, 
                command = lambda:self.EnableSubQ())
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        #setup the buttons for clause type
        label = tk.Label(self,text="Clause Type")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        for text,value in clauseTypes:
            b = tk.Radiobutton(self,text=text,variable=self.clausetype,
                value=value,indicatoron=0,width=10,height=1,
                command = lambda: self.EnableSubI())
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

# #subquestions
        self.InitSubs()
        self.SubIStatus("disabled")
        self.SubQStatus("disabled")
# utterance goals
        self.UttGoals()
#add syntactic features
        self.SynFeatures()

#Frame: discourse properties
        discFrame = tk.Frame(self, highlightbackground ="red", highlightcolor = "red", highlightthickness=4, bd=0)
        discFrame.grid(column=1, row = i, columnspan =3,sticky="w")        
        discfeatures = {
        #"FollowUp?":[1, "Same topic as the previous utterance?"],
        "HereNow": [1, "Is the event happening here and now?"],
        "ToAdults?": [1, "Is the utterance adult-to-adult?"]
        }
        #Followup Button: is the current utt a follou up of the previous utt?
        self.button_follow = tk.Checkbutton(discFrame, 
            text="Same topic as the previous utterance?",
            variable = self.followup)
        self.button_follow.grid(column=0,row=0,sticky="w")
        self.radios.append(self.button_follow)
        if self.index == 0:
            self.button_follow.configure(state = "disabled")
        j = 1 
        #other buttons
        self.discfeatures = []
        for feature in discfeatures:
            var = tk.IntVar()
            cb = tk.Checkbutton(discFrame, text = discfeatures[feature][1],
                variable = var)
            cb.grid(column= 0, row = j,sticky="w")
            # if self.result_df[feature][self.index] !=None:
            #     var.set([feature][self.index])
            self.discfeatures.append([feature, var])
            self.radios.append(cb)
            j += 1

#Frame: optional
        optFrame = tk.Frame(self)
        optFrame.grid(column = 4, row = i, columnspan = 4, rowspan =5)

        #situation column
        self.situation = tk.StringVar()
        label = tk.Label(optFrame,text="Situation")
        label.grid(column=1,row=1,sticky="s",columnspan=2)
        
        self.entry = tk.Entry(optFrame,textvariable=self.situation,
            width = 40)
        self.entry.grid(column=1,row=2,sticky="n",columnspan=3)
               
        #comment button
        label = tk.Label(optFrame,text="Comments (optional):")
        label.grid(column=1,row=4,sticky="s",columnspan=2)
        self.entry = tk.Entry(optFrame,textvariable=self.comment,width = 40)
        self.entry.grid(column=1,row=5,sticky="n",columnspan=3)

#Frame: buttons
        #Frame placed at the bottom rightcorner
        bottomFrame = tk.Frame(self)
        bottomFrame.grid(column = 3, row = 20)
        #previous button
        #use "self.index" as the go to number; Goto function will subtract 1 anyway
        #save the currect selection
        self.button_prev = tk.Button(bottomFrame,text=u"Prev",
                command = lambda: self.Goto(self.index))
        self.button_prev.grid(column=1,row=1)
        self.button_prev.configure(state="normal")
        self.bind("<Left>", lambda i: self.Goto(self.index)) 

        #next button, record results to df and reinitialize
        self.button_next = tk.Button(bottomFrame,text=u"Next",
                command = lambda: self.Goto(self.index+2))       
        self.button_next.grid(column=2,row=1)
        self.button_next.configure(state="normal")
        self.bind("<Right>", lambda i: self.Goto(self.index+2)) 

        #progress bar        
        label = tk.Label(bottomFrame,textvariable=self.progress)
        label.grid(column=3,row=1,sticky="s")

        #goto button
        num_label = tk.Label(bottomFrame,text="Go to #:")
        num_label.grid(column=1,row=2,sticky="s")
        self.num = tk.StringVar()
        self.num.set("")
        self.entry_num = tk.Entry(bottomFrame,textvariable=self.num, width = 5)
        self.entry_num.grid(column=2,row=2,sticky="n", columnspan=1)
        self.goto_button = tk.Button(bottomFrame, text=u"now!", 
            command = lambda: self.Goto(self.num.get()))
        self.goto_button.grid(column=3,row=2)
        self.goto_button.configure(state="normal")

        #save button,save df to csv
        self.button_save = tk.Button(bottomFrame,text=u"Save",
                                command=lambda: self.Save())
        self.button_save.grid(column=1,row=3)
        self.button_save.configure(state="normal")

        #exit button
        self.button_exit = tk.Button(bottomFrame,text=u"Exit",
                                command=lambda: self.Quit())
        self.button_exit.grid(column=2,row=3)
        self.button_exit.configure(state="normal")

        #if the catgory has recorded annotation, display previous annotation
        self.ShowExisting()
        #set everything in place
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()

    def UttGoals(self):        
#Frame: syntax
        self.uttgoals = tk.StringVar()
        uttFrame = tk.Frame(self)
        uttFrame.grid(column = 2, row = 0, columnspan = 2, rowspan = 11,  sticky = "n")

        uttGoals= [
        ("Drawing attention","Attention"),
        ("Teaching","Teaching"),
        ("Negotiating","Negotiating"),
        ("Discussing","Discussing"),
        ("Metacommunication","Meta"),
        ("Emoting","Emoting"),
        ("Verbal routines","Routine"),
        ("Immitation", "Immitation")
        ("Uninterpretable","")
        ]
        z = 0
        self.uttG_label = tk.Label(uttFrame, text = "Utterance Goals")
        self.uttG_label.grid(column = 0, row = z, sticky = "s", columnspan = 1)
        z += 1        

        for text,value in uttGoals:
            b = tk.Radiobutton(uttFrame, text=text, variable =self.uttgoals, 
                value = value, indicatoron = 0, width=15,height=1)
            b.grid(column=0, row = z, columnspan=1)
            self.radios.append(b)
            z += 1
    #subcategory buttons
    def InitSubs(self):
        subFrame = tk.Frame(self)
        subFrame.grid(column = 4, row = 0, columnspan = 2, rowspan = 11,  sticky = "n")
        
        subQuestions = [
        "PedagogicalGeneric", 
        "PedagogicalSpecific", 
        "SpecificInfo", 
        "CheckStatus", 
        "Clarification",  
        "AskForPermission", 
        "Attention"
        ]
        i = 0
        self.subQ_label = tk.Label(subFrame, text = "Subtypes of Questions")
        self.subQ_label.grid(column = 0, row = i, sticky = "s", columnspan = 1)
        i += 1
        for text in subQuestions:
            b = tk.Radiobutton(subFrame, text=text, variable =self.subQ, 
                value = text, indicatoron = 0, width=15,height=1)
            b.grid(column=0, row = i, columnspan=1)
            self.subQ_buttons.append(b)
            self.radios.append(b)
            i += 1
        
        subInt = ["Polar", "Wh", "Disjunctive"]
        self.subI_label = tk.Label(subFrame, text = "Subtypes of Interrogatives")
        self.subI_label.grid(column = 0, row = i, sticky = "s", columnspan = 1)
        i += 1
        for text in subInt:
            b = tk.Radiobutton(subFrame, text=text, variable =self.subI, 
                value = text, indicatoron = 0, width=15,height=1)
            b.grid(column=0, row = i, columnspan=1)
            self.subI_buttons.append(b)
            self.radios.append(b)
            i += 1   
    def SubQStatus(self, status):
        for b in self.subQ_buttons:
            b.configure(state=status)
        self.subQ_label.configure(state = status)
    def SubIStatus(self,status):
        for b in self.subI_buttons:
            b.configure(state=status)        
        self.subI_label.configure(state = status)

    #If "Question" or 'interrogative' is selected, then subcategories show up
    def EnableSubQ(self):
        if self.speechact.get() == "Question":
            self.SubQStatus("normal")
        else:
            self.SubQStatus("disabled")
            self.subQ.set("")
            self.result_df["SubQ"][self.index] == ""
    def EnableSubI(self):            
        if self.clausetype.get() == "Interrogative":
            self.SubIStatus("normal")
        else:
            self.SubIStatus("disabled")
            #reset subI and subQ, save the results of these two as empty
            self.subI.set("")
            self.result_df["SubQ"][self.index] == ""
    
        

    def SynFeatures(self):        
#Frame: syntax
        synFrame = tk.Frame(self)
        synFrame.grid(column = 6, row = 0, columnspan = 1, rowspan = 11)

        synfeatures= [
        "Subject",
        "Modal",
        "Modal_2",
        "DiscourseMarker",
        "TagType",
        "Q_status",
        "EmbeddingVerb",
        "S-lifting",
        "NEG",
        "MultiEmbedding",
        "Conventionalized",
        "PerlocutionaryEffect",
        "Offer?"
        ]
        
        k = 0
        self.synfeatures = []
        for f in synfeatures:
            x = tk.StringVar()
            label = tk.Label(synFrame, text = f)
            label.grid(column=1, row = k, sticky = "w")
            c = tk.Entry(synFrame, textvariable = x)
            if self.result_df[f][self.index]!=None:
                x.set(self.result_df[f][self.index])
            c.grid(column = 2, row = k)
            self.synfeatures.append([f,x])
            k +=1 

    #record the button click to results_df
    def dfResults(self):
        #write in the data
        self.result_df["SpeechAct"][self.index] =self.speechact.get()
        self.result_df["ClauseType"][self.index] =self.clausetype.get()
        self.result_df["Comments"][self.index] =self.comment.get()
        self.result_df["UttGoals"][self.index] =self.uttgoals.get()
        self.result_df["SubI"][self.index] =self.subI.get()
        self.result_df["SubQ"][self.index] =self.subQ.get()
        self.result_df["FollowUp?"][self.index] =self.followup.get()
        for [f,x] in self.synfeatures:
            self.result_df[f][self.index] = x.get()
        for [feature,var] in self.discfeatures:
            self.result_df[feature][self.index] =var.get()

        #self.result_df = self.result_df.fillna("")

    #save currect selection, jump to the Record number given
    def Goto(self,num):
        #save
        self.dfResults()
        #make sure the number doesn't exist 0 to the length of the dataset
        if int(num) < 1:
            self.index = 0
        elif int(num)>len(self.record):
            self.index = len(self.record)-1
        else:
            self.index = int(num)-1
        #setup next dataviewbox
        self.DisplayData()
        #reset buttons, columns
        self.comment.set("")
        for [f,x] in self.synfeatures:
            x.set("")
        self.SubQStatus("disabled")
        self.SubIStatus("disabled")        
        self.button_follow.configure(state="normal")
        #if the first item is accessed using this "Go to" method, "Followup" is disabled
        if self.index == 0:
            self.button_follow.configure(state = "disabled")        
        for b in self.radios:
            b.deselect()
        #show existing
        self.ShowExisting()


    #click on quit to write currect selection to df, and save df to csv file
    def Save(self):
        self.dfResults()
        #writing the resulting datafile to .csv file
        self.results = pd.DataFrame.from_dict(self.result_df, orient= "index").T
        self.results.to_csv(data_dir+"/"+datafile+"-annot.csv", index = False)   

    #save and quit    
    def Quit(self):
        self.Save()   
        #quit
        self.quit()

    #close window autosave
    def on_closing(self):
        self.Save()
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.destroy()


if __name__=="__main__":
    datafile = ""
    data_dir = ""
    #prompt dialogue box, same the name of the file and exit
    def file_opener():
        global datafile, data_dir
        input = filedialog.askopenfile(initialdir=os.getcwd(),title="Open File",
            filetypes=[("csv files", "*.csv")])
        datafile = os.path.basename(input.name).split(".")[0]
        data_dir = os.path.dirname(input.name)
        dialogue_box.destroy()
    #dialogue box for file name
    dialogue_box = tk.Tk()
    dialogue_box.geometry('150x150')
    tk.Button(dialogue_box, command=lambda: file_opener(), text='select a file', height = 2, width = 10).pack()
    dialogue_box.title("Open...")
    dialogue_box.mainloop()

    #clean up PHON output
    #read in data
    df = pd.read_csv(data_dir+"/"+datafile+".csv")
    df = df.fillna("") #get rid of "nan"

    # Renaming the columns; getting rid of the ":"s in the header
    df.rename(columns = {'Speaker:Name' :'Speaker'},inplace = True)
    #strip off the dot in "session:name"
    session =  df["Session:Name"].str.split('.', n=1, expand = True)
    session1 =session[0]+ session[1]
    df["Session"] = session1

    #child and session information
    child = session[0][0]
    df["Child"] = child
    session_name = session[1][0]

    # split the Segment column into 'start' and 'end'
    utt_dur = df['Segment'].str.split("-", n =1, expand = True)
    df['start_time'] = utt_dur[0]
    df["end_time"] = utt_dur[1]


    # Transform the Starting time and End time into seconds
    s_time = df['start_time'].str.split(':', n=1, expand = True)
    df["start_seconds"] = pd.to_numeric(s_time[0])*60+pd.to_numeric(s_time[1])
    e_time = df['end_time'].str.split(":", n=1, expand = True)
    df["end_seconds"] =pd.to_numeric(e_time[0])*60 + pd.to_numeric(e_time[1])


    # getting rid of the parentheses in "Orthography", save them in a new column 
    # new pandas default for regex will be False, so need to specify
    df["Orthography"] = df["Orthography"].str.replace(r'[\[\]\d]+', '', regex = True)

    #combine the columns "Situation" and "Notes" into "Situation"
    df["Situation"] = df["Notes"] +df["situation"]
    #reduce the columns of the dataframe
    df=df[["Record #", "Speaker", "Session", "Orthography", "Child", "start_seconds", "end_seconds",'Situation', "GRASP", "Morphology" ]]
    old_col = ["Record #", "Speaker", "Session", "Orthography", "Child", "start_seconds", "end_seconds",'Situation', "GRASP", "Morphology"  ]
    new_col = [
    "SpeechAct",
    "ClauseType",
    "UttGoals",
    "SubQ", 
    "SubI", 
    "Comments",
    "Subject",
    "Modal",
    "Modal_2",
    "DiscourseMarker",
    "TagType",
    "Q_status",
    "EmbeddingVerb",
    "S-lifting",
    "NEG",
    "MultiEmbedding",
    "Conventionalized",
    "PerlocutionaryEffect",
    "Offer?"
    ]
    int_col =[
   "FollowUp?", "HereNow","ToAdults?" 
    ] 

    if path.exists(data_dir+"/"+datafile+"-annot.csv"):
        result_df = pd.read_csv(data_dir+"/"+datafile+"-annot.csv")
        for x in old_col:
            result_df[x] =df[x]
        result_df = result_df.fillna("")
                 
    else:
        result_df = df
    for x in new_col:
        if x not in result_df.columns:
            result_df[x] = ""
    for x in int_col:
        if x not in result_df.columns:
            result_df[x] = 0    

    d = result_df.to_dict()

    app = simpleapp_tk(None)
    app.title("Annotation Tool")
    app.mainloop()

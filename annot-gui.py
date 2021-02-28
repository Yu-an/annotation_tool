import pandas as pd 
import os
import tkinter as tk
from tkinter import messagebox
from os import path


class simpleapp_tk(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.index = 0

        self.task = df
        self.result_df = d

        self.speaker = self.task["Speaker"]
        self.orthography = self.task["Orthography"]
        self.record = self.task["Record #"]

        #intialize item attribute
        self.item = tk.StringVar()
        #viewbox style
        self.text = tk.Text(self,height=35)
        self.text.tag_configure("bold", font=("Arial", 14, "bold"), background="#5FFB17")
        self.text.tag_configure("italics", font=("Arial", 14, "italic"), background="#FFDB58")
        self.text.tag_configure("normal", font = ("Arial", 14))

        self.progress = tk.StringVar()

        self.DisplayData()

        self.initialize()

        #when press x to close window, save before close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def DisplayData(self):

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
        if self.result_df["ClauseType"][self.index] != None:
            self.clausetype.set(self.result_df["ClauseType"][self.index])
        if self.result_df["SpeechAct"][self.index] != None:
            self.speechact.set(self.result_df["SpeechAct"][self.index])
        #enable subcategories if the result file has "question" or "interrogative" recorded
        if self.result_df["SpeechAct"][self.index] == "Question":
            self.SubQuestions("normal")
        if self.result_df["ClauseType"][self.index] =="Interrogative":
            self.SubQuestions("normal")

        if self.result_df["Comments"][self.index] != None:
            self.comment.set(self.result_df["Comments"][self.index])
        if self.result_df["SubI"][self.index] != None:
            self.subI.set(self.result_df["SubI"][self.index])
        if self.result_df["SubQ"][self.index] != None:
            self.subQ.set(self.result_df["SubQ"][self.index])
        if self.result_df["FollowUp?"][self.index] != None:
            self.followup.set(self.result_df["FollowUp?"][self.index])

    def initialize(self):
        self.grid()
        self.radios=[]
        #buttons; ("label","writing in the coding file")
        speechActs = [("Assertion","Assertion"),("Question","Question"),("Request","Request"), ("Exclamative", "Exclamative"), ("Other","Other")]
        clauseTypes = [("Declarative","Declarative"),("Interrogative","Interrogative"),("Imperative","Imperative"),("Fragment","FRAG"), ("Exclamative", "Exclamative"), ("Other","Other")]
        

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
                value=value,indicatoron=0,width=10,height=2, 
                command = lambda:self.GenerateSubs())
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        #setup the buttons for clause type
        label = tk.Label(self,text="Clause Type")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        for text,value in clauseTypes:
            b = tk.Radiobutton(self,text=text,variable=self.clausetype,
                value=value,indicatoron=0,width=10,height=2,
                command = lambda: self.GenerateSubs())
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        #Followup Button: is the current utt a follou up of the previous utt?
        self.button_follow = tk.Checkbutton(self, text="Follow up?", 
            indicatoron=0, variable = self.followup, width=15,height=3)
        self.button_follow.grid(column=1,row=i,columnspan=2)
        self.radios.append(self.button_follow)
        if self.index == 0:
            self.button_follow.configure(state = "disabled")
        i+=1

        #initialize SubQuestions (but disable the buttons)
        self.SubQuestions("disabled")

        #progress bar        
        label = tk.Label(self,textvariable=self.progress)
        label.grid(column=2,row=i+5,sticky="s")
        
        #text grid
####################################################
        #textgrid right now is the same height as the buttons
        #will try to embed this under a frame         
        self.text.grid(column=0,row=0, rowspan=i+2)

        #comment button
        label = tk.Label(self,text="Comments (optional):")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        self.entry = tk.Entry(self,textvariable=self.comment,width = 40)
        self.entry.grid(column=1,row=i+1,sticky="n",columnspan=3)

        #previous button
        #use "self.index" as the go to number; Goto function will subtract 1 anyway
        #save the currect selection
        self.button_prev = tk.Button(self,text=u"Prev",
                command = lambda: self.Goto(self.index))
        self.button_prev.grid(column=1,row=i+3)
        self.button_prev.configure(state="normal")

        #next button, record results to df and reinitialize
        self.button_next = tk.Button(self,text=u"Next",
                command = lambda: self.Goto(self.index+2))
        self.button_next.grid(column=2,row=i+3)
        self.button_next.configure(state="normal")

        #goto button
        num_label = tk.Label(self,text="Go to #:")
        num_label.grid(column=1,row=i+4,sticky="s")
        self.num = tk.StringVar()
        self.num.set("")
        self.entry_num = tk.Entry(self,textvariable=self.num, width = 5)
        self.entry_num.grid(column=2,row=i+4,sticky="n", columnspan=1)
        self.goto_button = tk.Button(self, text=u"now!", 
            command = lambda: self.Goto(self.num.get()))
        self.goto_button.grid(column=3,row=i+4)
        self.goto_button.configure(state="normal")

        #save button,save df to csv
        self.button_save = tk.Button(self,text=u"Save",
                                command=lambda: self.Save())
        self.button_save.grid(column=0,row=i+2)
        self.button_save.configure(state="normal")

        #exit button
        self.button_exit = tk.Button(self,text=u"Exit",
                                command=lambda: self.Quit())
        self.button_exit.grid(column=0,row=i+3)
        self.button_exit.configure(state="normal")

        #if the catgory has recorded annotation, display previous annotation
        self.ShowExisting()
        #set everything in place
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()

    #If "Question" or 'interrogative' is selected, then subcategories show up
    def GenerateSubs(self):
        if self.speechact.get() == "Question":
            self.SubQuestions("normal")
        elif self.clausetype.get() == "Interrogative":
            self.SubQuestions("normal")
    #subcategory buttons
    def SubQuestions(self, status):
        subQuestions = ["PedagogicalGeneric", "PedagogicalSpecific", "SpecificInfo", "CheckStatus", "Clarification", "Permission", "Commands", "Attention"]
        i = 0
        label = tk.Label(self, text = "Subtypes of Questions")
        label.grid(column = 3, row = i, sticky = "s", columnspan = 1)
        label.configure(state = status)
        i += 1
        for text in subQuestions:
            b = tk.Radiobutton(self, text=text, variable =self.subQ, 
                value = text, indicatoron = 0, width=15,height=1)
            b.grid(column=3, row = i, columnspan=1)
            b.configure(state=status)
            self.radios.append(b)
            i += 1
    #def SubInt(self):
    #not seperated from "subQ" because may include more subcategories like "here&now"
        subInt = ["Polar", "Wh", "Disjunctive"]
        label = tk.Label(self, text = "Subtypes of Interrogatives")
        label.grid(column = 3, row = i, sticky = "s", columnspan = 1)
        label.configure(state = status)
        i += 1
        for text in subInt:
            b = tk.Radiobutton(self, text=text, variable =self.subI, 
                value = text, indicatoron = 0, width=15,height=1)
            b.grid(column=3, row = i, columnspan=1)
            b.configure(state=status)
            self.radios.append(b)
            i += 1   
    #record the button click to results_df
    def dfResults(self):
        #write in the data
        self.result_df["SpeechAct"][self.index] =self.speechact.get()
        self.result_df["ClauseType"][self.index] =self.clausetype.get()
        self.result_df["Comments"][self.index] =self.comment.get()
        self.result_df["SubI"][self.index] =self.subI.get()
        self.result_df["SubQ"][self.index] =self.subQ.get()
        self.result_df["FollowUp?"][self.index] =self.followup.get()
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
        self.SubQuestions("disabled")
        self.button_follow.configure(state="normal")
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
    data_dir = "./data"
    datafile = input("file? ")

    # #set file
    # dialogue_box = tk.Tk()
    # datafile = ""
    # dataname = tk.StringVar()
    # tk.Label(dialogue_box, text='Which file are you going to work on? (no need to specify the extension)').pack()
    # entry = tk.Entry(dialogue_box, textvariable=dataname)
    # entry.pack()
    # entry.focus_set()
    # tk.Button(dialogue_box, command=lambda: dialogue_box.destroy(), text='Ok',).pack()
    # dialogue_box.bind("<Return>",lambda event: dialogue_box.destroy())
    # dialogue_box.mainloop()
    # datafile = dataname.get()

    # if data_dir.endswith("/"):
    #     data_dir = data_dir.strip("/")
    # if datafile.endswith(".csv"):
    #     datafile = datafile.rstrip("csv")
    #     datafile = datafile.strip(".")

    #clean up output data from PHON
    df = pd.read_csv(data_dir+"/"+datafile+".csv")
    df = df.fillna("")

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

    #combine "Situation and Notes" into "Comments"
    df["Comments"] = df["Notes"] +df["situation"]
    #reduce the columns of the dataframe
    df=df[["Record #", "Speaker", "Orthography", "Child", "start_seconds", "end_seconds",'Comments' ]]

    if path.exists(data_dir+"/"+datafile+"-annot.csv"):
        result_df = pd.read_csv(data_dir+"/"+datafile+"-annot.csv")
        if "FollowUp?" in result_df.columns:
            result_df["FollowUp?"] = result_df["FollowUp?"].fillna("0")
        new_col = ["SubQ", "SubI", "FollowUp?", "Comments"]
        for x in new_col:
            if x not in result_df.columns:
                result_df[x] = [None]*len(result_df)
    else:
        result_df = df
        result_df["SpeechAct"] = [None]*len(result_df)
        result_df["ClauseType"] = [None]*len(result_df)
        result_df["Comments"] = [None]*len(result_df)
        result_df["SubI"] = [None]*len(result_df)
        result_df["SubQ"] = [None]*len(result_df)
        result_df["FollowUp?"] = [None]*len(result_df)

    d = result_df.to_dict()
    df = df.to_dict()

    app = simpleapp_tk(None)
    app.title("Annotation Tool")
    app.mainloop()

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

        #intialize attributes
        self.item = tk.StringVar()
        self.progress = tk.StringVar()
        #self.variables = []
        self.clausetype= tk.StringVar()
        self.speechact= tk.StringVar()
        self.comment = tk.StringVar()
        self.subQ = tk.StringVar()
        self.subI = tk.StringVar()
        self.followup = tk.IntVar()     

#Frame:textbox
        textFrame = tk.Frame(self)
        textFrame.grid(column=0, row = 0, rowspan = 25)
        #add textbox to the frame
        self.text = tk.Text(textFrame, height=35, bg = "#f1f8e9")
        #define style
        self.text.tag_configure("bold", font=("Arial", 14, "bold"), background="#5FFB17")
        self.text.tag_configure("italics", font=("Arial", 14, "italic"), background="#FFDB58")
        self.text.tag_configure("normal", font = ("Arial", 14))
        self.text.grid(column=0, row=0, rowspan = 25)   

        #add text to textbox
        self.DisplayData()

        #initialize buttons
        self.initialize()

        #when press x to close window, save before close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    #add text to textbox; set progressbar number
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

    #initialize the buttons
    def initialize(self):
        self.grid()
        self.radios=[]
        #buttons; ("label","writing in the coding file")
        speechActs = [("Assertion","Assertion"),("Question","Question"),("Request","Request"), ("Exclamative", "Exclamative"), ("Other","NaN")]
        clauseTypes = [("Declarative","Declarative"),("Interrogative","Interrogative"),("Imperative","Imperative"),("Fragment","FRAG"), ("Exclamative", "Exclamative"), ("Other","NaN")]

        #build the buttons
        #set up the row# for the buttons
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
                value=value,indicatoron=0,width=10,height=1,
                command = lambda: self.GenerateSubs())
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        #initialize SubQuestions (but disable the buttons)
        self.SubQuestions("disabled")
        #add syntactic features
        self.SynFeatures()

#Frame: discourse properties
        discFrame = tk.Frame(self, highlightbackground ="red", highlightcolor = "red", highlightthickness=4, bd=0)
        discFrame.grid(column=1, row = i, columnspan =3,sticky="w")
        #Followup Button: is the current utt a follou up of the previous utt?
        self.button_follow = tk.Checkbutton(discFrame, 
            text="Same topic as the previous utterance?",
            variable = self.followup)
        self.button_follow.grid(column=0,row=1,sticky="w")
        self.radios.append(self.button_follow)
        if self.index == 0:
            self.button_follow.configure(state = "disabled")

        i += 1



#Frame: optional
        optFrame = tk.Frame(self)
        optFrame.grid(column = 1, row = i, columnspan = 3)
        #comment button
        label = tk.Label(optFrame,text="Comments (optional):")
        label.grid(column=0,row=2,sticky="w")
        self.entry = tk.Entry(optFrame,textvariable=self.comment,width = 40)
        self.entry.grid(column=0,row=3,sticky="w",columnspan=3)
        
        #don't forget to add to i!
        i += 1

#Frame: buttons
        #Frame placed at the bottom rightcorner
        bottomFrame = tk.Frame(self)
        bottomFrame.grid(column = 1, row = i, columnspan =3)
        #previous button
        #use "self.index" as the go to number; Goto function will subtract 1 anyway
        #save the currect selection
        self.button_prev = tk.Button(bottomFrame,text=u"Prev",
                height = 2, width = 5,
                command = lambda: self.Goto(self.index))
        self.button_prev.grid(column=1,row=1)
        self.button_prev.configure(state="normal")

        #next button, record results to df and reinitialize
        self.button_next = tk.Button(bottomFrame,text=u"Next",
                height = 2, width = 5,
                command = lambda: self.Goto(self.index+2))
        self.button_next.grid(column=2,row=1)
        self.button_next.configure(state="normal")
        
        #progress bar        
        label = tk.Label(bottomFrame,textvariable=self.progress, width = 8)
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
    
    def SynFeatures(self):        
#Frame: syntax
        synFrame = tk.Frame(self)
        synFrame.grid(column = 4, row = 0, columnspan = 3, rowspan = 11)

        features= [
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
        for f in features:
            x = tk.StringVar()
            label = tk.Label(synFrame, text = f)
            label.grid(column=0, row = k)
            c = tk.Entry(synFrame, textvariable = x)
            if self.result_df[f][self.index]!=None:
                x.set(self.result_df[f][self.index])
            c.grid(column = 1, row = k)
            self.synfeatures.append([f,x])
            k +=1 

    #record the button click to results_df
    def dfResults(self):
        #write in the data
        self.result_df["SpeechAct"][self.index] =self.speechact.get()
        self.result_df["ClauseType"][self.index] =self.clausetype.get()
        self.result_df["Comments"][self.index] =self.comment.get()
        self.result_df["SubI"][self.index] =self.subI.get()
        self.result_df["SubQ"][self.index] =self.subQ.get()
        self.result_df["FollowUp?"][self.index] =self.followup.get()
        for [f,x] in self.synfeatures:
            self.result_df[f][self.index] = x.get()

    #save currect selection, jump to the Record number given
    def Goto(self,num):
        #save
        self.dfResults()
        #make sure the number doesn't exist 0 to the length of the dataset
        # if num.isdigit() == False:
        #     self.goto_button.configure(state="disabled")
        try:
            int(num)
            if int(num) < 1:
                self.index = 0
            elif int(num)>len(self.record):
                self.index = len(self.record)-1
            else:
                self.index = int(num)-1
        except ValueError:
            tk.messagebox.showwarning(title="Error", message="Enter a number!")


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
        for [f,x] in self.synfeatures:
            if self.result_df[f][self.index] != None:
                x.set(self.result_df[f][self.index])

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

    new_col = [
    "SpeechAct",
    "ClauseType"
    "SubQ", 
    "SubI", 
    "FollowUp?", 
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
    "Offer?"]

    if path.exists(data_dir+"/"+datafile+"-annot.csv"):
        result_df = pd.read_csv(data_dir+"/"+datafile+"-annot.csv")
    else:
        result_df = df
    for x in new_col:
        if x not in result_df.columns:
            result_df[x] = [None]*len(result_df)
    if "FollowUp?" in result_df.columns:
        result_df["FollowUp?"] = result_df["FollowUp?"].fillna("0")
        result_df["FollowUp?"] = result_df["FollowUp?"].astype("Int64")

    d = result_df.to_dict()
    df = df.to_dict()

    app = simpleapp_tk(None)
    app.title("Annotation Tool")
    app.mainloop()

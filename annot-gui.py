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
        self.item = tk.StringVar()

        self.text = tk.Text(self,height=35)
        self.text.tag_configure("bold", font=("Arial", 12, "bold"), background="#5FFB17")
        self.text.tag_configure("italics", font=("Arial", 12, "italic"), background="#FFDB58")
        self.text.tag_configure("normal", font = ("Arial", 12))

        self.progress = tk.StringVar()

        self.result_df = d


        self.DisplayData()

        self.initialize()

        #when press x to close window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def DisplayData(self):

        self.progress.set(str(self.index+1)+"/"+str(len(self.task)-1))
        self.item.set("\n" + str(record[self.index]) + ". " + speaker[self.index] + ": " + orthography[self.index])

        self.text.configure(state='normal')
        self.text.delete(0.0,'end')
        
        self.prior = max(0, self.index-20)
        self.post = min(len(self.task), self.index+3)

        for i in range(self.prior, self.post):
            if i < self.index:
                self.text.insert("end", str(record[i]) + ". " + speaker[i] + ": " + orthography[i] +"\n", "normal")
            elif i == self.index:
                self.text.insert("end", str(record[self.index]) + ". " + speaker[self.index] + ": " + orthography[self.index]+"\n" , "bold")
            elif i > self.index :
                self.text.insert("end", str(record[i]) + ". " + speaker[i] + ": " + orthography[i]+"\n" , "normal")
        
        self.text.configure(state='disabled')

    #if there's existing data, read in and set value
    def ShowExisting(self):
        # categories = [("clausetype","ClauseType"), ("speechact","SpeechAct"), ("comment","comments")]
        # for cate, Cate in categories:
        #     if self.result_df[Cate][self.index] !=None:
        #         self.cate.set(self.result_df[Cate][self.index])
        if self.result_df["ClauseType"][self.index] != None:
            self.clausetype.set(self.result_df["ClauseType"][self.index])
        if self.result_df["SpeechAct"][self.index] != None:
            self.speechact.set(self.result_df["SpeechAct"][self.index])
        # if self.result_df["comments"][self.index] != None:
        #     self.comment.set(self.result_df["comments"][self.index])
  #arrange things; how
    # def activate(self):
    #     print("activated")
        # if self.speechact.get() and self.clausetype.get():
        #     self.button_next.configure(state="normal")
        # if self.result_df["ClauseType"][self.index] != None and self.result_df["SpeechAct"][self.index] != None:
        #     self.button_next.configure(state="normal")

    def initialize(self):
        self.grid()
        self.radios=[]
        #buttons; ("label","writing in the coding file")
        speechActs = [("Assertion","Assertion"),("Question","Question"),("Request","Request"), ("Exclamative", "Exclamative"), ("Other","Other")]
        clauseTypes = [("Declarative","Declarative"),("Interrogative","Intterogative"),("Imperative","Imperative"),("Fragment","FRAG"), ("Exclamative", "Exclamative"), ("Other","Other")]
        

        #initialize
        self.clausetype= tk.StringVar()
        self.speechact= tk.StringVar()

        self.ShowExisting()
        #build the buttons
        #speechact
        i = 0
        #label the category
        label = tk.Label(self,text="Speech Act")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        #build buttons for speech act
        for text,value in speechActs:
            b = tk.Radiobutton(self,text=text,variable=self.speechact,value=value,indicatoron=0,width=10,height=2)
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        #setup the buttons for clause type
        label = tk.Label(self,text="Clause Type")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        for text,value in clauseTypes:
            b = tk.Radiobutton(self,text=text,variable=self.clausetype,value=value,indicatoron=0,width=10,height=2)
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1



        ###############################
        if self.result_df["SpeechAct"][self.index] == "Question":
            #self.speechact.get() == "Question" or 
            self.SubQuestions()
##########################################

        #progress bar        
        label = tk.Label(self,textvariable=self.progress)
        label.grid(column=2,row=i+5,sticky="s")
        #text grid
        self.text.grid(column=0,row=0, rowspan=i+2)
        #comment button
        self.comment = tk.StringVar()
        self.comment.set("")
        self.entry = tk.Entry(self,textvariable=self.comment)
        self.entry.grid(column=1,row=i+1,sticky="n",columnspan=2)
        label = tk.Label(self,text="Comment (optional):")
        label.grid(column=1,row=i,sticky="s",columnspan=2)

        #previous button
        self.button_prev = tk.Button(self,text=u"Prev",
                command = lambda: self.Goto(self.index-1))
        self.button_prev.grid(column=1,row=i+3)
        self.button_prev.configure(state="normal")

        #next button, record results to df and reinitialize
        self.button_next = tk.Button(self,text=u"Next",
                command = lambda: self.OnButtonClick())
        self.button_next.grid(column=2,row=i+3)
        self.button_next.configure(state="normal")

        #goto button
        num_label = tk.Label(self,text="Go to #:")
        num_label.grid(column=3,row=i+3,sticky="s")
        self.num = tk.StringVar()
        self.num.set("")
        self.entry_num = tk.Entry(self,textvariable=self.num)
        self.entry_num.grid(column=4,row=i+3,sticky="n", columnspan=1)
        self.goto_button = tk.Button(self, text=u"now!", 
            command = lambda: self.Goto(self.num.get()))
        self.goto_button.grid(column=5,row=i+3)
        self.goto_button.configure(state="normal")

        #save button,save df to csv
        button_save = tk.Button(self,text=u"Save",
                                command=lambda: self.Save())
        button_save.grid(column=0,row=i+2)

        #exit button
        button_exit = tk.Button(self,text=u"Exit",
                                command=lambda: self.Quit())
        button_exit.grid(column=0,row=i+3)

        #set everything in place
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()


    def SubQuestions(self):
        subQuestions = ["PedagogicalGeneric", "PedagogicalSpecific", "InfoSeeking", "CheckStatus", "Clarification", "Permission", "SpecificInfo", "Commands", "Attention"]
        subInt = ["Polar", "wh", "Disjunctive"]
        i = 0
        self.subQ = tk.StringVar()
        label = tk.Label(self, text = "Subtypes of Questions")
        label.grid(column = 3, row = i, sticky = "s", columnspan = 1)
        i += 1
        for text in subQuestions:
            b = tk.Radiobutton(self, text=text, variable =self.subQ, value = text, indicatoron = 0, width=23,height=2)
            b.grid(column=2, row = i, columnspan=2)
            self.radios.append(b)
            i += 1

    #record the button click to results_df
    def dfResults(self):
        #write in the data
        self.result_df["SpeechAct"][self.index] =self.speechact.get()
        self.result_df["ClauseType"][self.index] =self.clausetype.get()
        self.result_df["comments"][self.index] =self.comment.get()
    
    #click on next to write results to results_df and reinitialize
    def OnButtonClick(self):
        self.dfResults()
        #reset index
        self.index += 1
        #setup next item
        self.DisplayData()
        #set the value for the next item; if already annotated, show value, if not, reset
        #self.comment.set("")
        self.button_next.configure(state="normal")
        for b in self.radios:
            b.deselect()
        self.ShowExisting()

    
    def Goto(self,num):
        # #check if user_input is a number
        # if num.isdigit() == False:
        #     tk.messagebox.showwarning("Warning", "Please input a number")
        # else:           
        #     go_to_num = int(num)
        #     #check if number is out of range
        #     if go_to_num > len(orthography):
        #         tk.messagebox.showwarning("Warning", "Number out of range!")
        self.index = int(num)-1
        self.DisplayData()
        self.ShowExisting()



    #click on quit to write currect selection to df, and save df to csv file
    def Save(self):
        self.dfResults()
        #writing the resulting datafile to .csv file
        self.results = pd.DataFrame.from_dict(self.result_df, orient= "index").T
        self.results.to_csv(datafile+"-annot.csv", index = False)   

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
    data_dir = "/Users/ceshi/Documents/Work/SpeechAct/EngCorp/scripts/annotation_tool"
    datafile = input("file? ")
    # #set directory
    # dialogue_box = tk.Tk()
    # data_dir = ""
    # dirname = tk.StringVar()
    # tk.Label(dialogue_box, text="Which directory?").pack()
    # entry = tk.Entry(dialogue_box, textvariable=dirname)
    # entry.pack()
    # #set the cursor in the entry box
    # entry.focus_set()
    # #close tk with button
    # tk.Button(dialogue_box, command=lambda: dialogue_box.destroy(), text='Ok',).pack()
    # #also ok with "return" key
    # dialogue_box.bind("<Return>",lambda event: dialogue_box.destroy())
    # dialogue_box.mainloop()
    # data_dir = dirname.get()


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

    # Renaming the columns; getting rid of the ":"s in the header
    df.rename(columns = {'Speaker:Name' :'Speaker'},inplace = True)
    #strip off the dot in "session:name"
    session =  df["Session:Name"].str.split('.', n=1, expand = True)
    session1 =session[0]+ session[1]
    df["Session"] = session1

    #child and session information
    child = session[0][0]
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

    df["Orthography"] = df["Orthography"].str.replace(r'[\[\]\d]+', '')


    # Add the previous utterance and the post utterance
    df["pre_utt"] = df.Orthography.shift(1)
    df['pre_speaker'] = df.Speaker.shift(1)
    df["post_starttime"] = df.start_seconds.shift(-1)
    df["post_utt"] = df.Orthography.shift(-1)
    df["post_speaker"] = df.Speaker.shift(-1)
    df["pause_after"] = df["post_starttime"]- df["end_seconds"]



    speaker = df['Speaker'].values #retrieving speaker info
    orthography = df['Orthography'].values #retrieving orthography info
    record = df["Record #"].values


    if path.exists(data_dir+"/"+datafile+"-annot.csv"):
        result_df = pd.read_csv(data_dir+"/"+datafile+"-annot.csv")
    else:
        result_df = df
        result_df["SpeechAct"] = [None]*len(result_df)
        result_df["ClauseType"] = [None]*len(result_df)
        result_df["comments"] = [None]*len(result_df)

    d = result_df.to_dict()


    app = simpleapp_tk(None)
    app.title("Annotation Tool")
    app.mainloop()

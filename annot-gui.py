import pandas as pd 
import tkinter as tk
from tkinter import messagebox


datafile = input("Which file are you going to work on? (no need to specify .csv) ")

#clean up output data from PHON
df = pd.read_csv(datafile+".csv")

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

result_df = df
result_df["SpeechAct"] = [None]*len(result_df)
result_df["ClauseType"] = [None]*len(result_df)
result_df["comments"] = [None]*len(result_df)

d = result_df.to_dict()


class simpleapp_tk(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.index = 0
        
        self.task = df
        self.item = tk.StringVar()
        self.item.set("\n" + str(record[self.index]) + ". " + speaker[self.index] + ": " + orthography[self.index])
        
        self.prior = max(0, self.index-20)
        self.post = min(len(self.task), self.index+3)

        self.text = tk.Text(self,height=35)
        self.text.tag_configure("bold", font=("Arial", 12, "bold"), background="#5FFB17")
        self.text.tag_configure("italics", font=("Arial", 12, "italic"), background="#FFDB58")
        self.text.tag_configure("normal", font = ("Arial", 12))

        for i in range(self.prior, self.post):
            if i < self.index:
                self.text.insert("end", str(record[i]) + ". " + speaker[i] + ": " + orthography[i] +"\n", "normal")
            elif i == self.index:
                self.text.insert("end", str(record[self.index]) + ". " + speaker[self.index] + ": " + orthography[self.index]+"\n" , "bold")
            elif i > self.index :
                self.text.insert("end", str(record[i]) + ". " + speaker[i] + ": " + orthography[i]+"\n" , "normal")
        

        self.text.configure(state='disabled')

        self.initialize()
  #arrange things; how
    def activate(self):
        if self.speechact.get() and self.clausetype.get():
            self.button_next.configure(state="normal")

    def initialize(self):
        self.grid()

        #initialize
        self.clausetype = tk.StringVar()
        self.clausetype.set("")
        self.speechact = tk.StringVar()
        self.speechact.set("")

        self.radios=[]
        #buttons; ("label","writing in the coding file")
        speechActs = [("Assertion","Assertion"),("Question","Question"),("Request","Request"), ("Exclamative", "Exclamative"), ("Other","Other")]
        clauseTypes = [("Declarative","Declarative"),("Interrogative","Intterogative"),("Imperative","Imperative"),("Fragment","FRAG"), ("Exclamative", "Exclamative"), ("Other","Other")]
        #build the buttons
        #speechact
        i = 0
        label = tk.Label(self,text="Speech Act")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        #renitialize when clicking "next"
        for text,value in speechActs:
            b = tk.Radiobutton(self,text=text,variable=self.speechact,value=value,indicatoron=0,width=10,height=2,command=self.activate)
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        label = tk.Label(self,text="Clause Type")
        label.grid(column=1,row=i,sticky="s",columnspan=2)
        i+=1
        for text,value in clauseTypes:
            b = tk.Radiobutton(self,text=text,variable=self.clausetype,value=value,indicatoron=0,width=10,height=2,command=self.activate)
            b.grid(column=1,row=i,columnspan=2)
            self.radios.append(b)
            i+=1

        self.progress = tk.StringVar()
        self.progress.set(str(self.index+1)+"/"+str(len(self.task)-1))
        label = tk.Label(self,textvariable=self.progress)
        label.grid(column=2,row=i+3,sticky="s")


        #next button
        self.button_next = tk.Button(self,text=u"Next",
                command = lambda: self.OnButtonClick("next"))

        self.text.grid(column=0,row=0, rowspan=i+2)
        self.button_next.grid(column=1,row=i+3)
        self.button_next.configure(state="disabled")



        #exit button
        button_exit = tk.Button(self,text=u"Exit",
                                command=self.quit)
        button_exit.grid(column=0,row=i+3)

        self.comment = tk.StringVar()
        self.comment.set("")
        self.entry = tk.Entry(self,textvariable=self.comment)
        self.entry.grid(column=1,row=i+1,sticky="n",columnspan=2)
        label = tk.Label(self,text="Comment (optional):")
        label.grid(column=1,row=i,sticky="s",columnspan=2)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        #self.geometry(self.geometry())       
    
 
    def OnButtonClick(self,annot):
        self.result_df = d
        self.result_df["SpeechAct"][self.index] =self.speechact.get()
        self.result_df["ClauseType"][self.index] =self.clausetype.get()
        self.result_df["comments"][self.index] =self.comment.get()
        

        #writing the resulting datafile to .csv file
        self.results = pd.DataFrame.from_dict(self.result_df, orient= "index").T
        self.results.to_csv(datafile+"-annot.csv")

        #reset index
        self.index += 1
        self.item.set("\n" + str(record[self.index]) + ". " + speaker[self.index] + ": " + orthography[self.index])
        self.progress.set(str(self.index+1)+"/"+str(len(self.task)-1))

        self.text.configure(state='normal')
        self.text.delete(0.0,'end')


        self.prior = max(0, self.index-20)
        self.post = min(len(self.task), self.index+3)
        #print(self.prior)
        #print(self.post)
        for i in range(self.prior, self.post):
            if i < self.index:
                self.text.insert("end", str(record[i]) + ". " + speaker[i] + ": " + orthography[i] +"\n", "normal")
            elif i == self.index:
                self.text.insert("end", str(record[self.index]) + ". " + speaker[self.index] + ": " + orthography[self.index]+"\n", "bold")
            else:
                self.text.insert("end", str(record[i]) + ". " + speaker[i] + ": " + orthography[i] +"\n", "normal")
        
        ShowExistingChoice()

        self.text.configure(state='disabled')
        self.comment.set("")
        self.button_next.configure(state="disabled")
        for b in self.radios:
            b.deselect()

if __name__=="__main__":
    app = simpleapp_tk(None)
    app.title("Annotation Tool")
    app.mainloop()

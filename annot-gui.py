import pandas as pd 
import tkinter as tk
from tkinter import messagebox


datafile = input("Which file are you going to work on? ")

index = 0
warning_appeared = False

#list options for each annotation category    
speechAct_types = ["Question", "Assertion", "Request", "Other"]
clauseType_types = ["Interrogative", "Declarative", "Imperative", "Fragment", "Other"]



window = tk.Tk()
window.title("Annotation Tool")
window.geometry("1360x420")


#clean up output data from PHON
df = pd.read_csv(datafile)

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

df["SpeechAct"]= [None]*len(df) 
df["ClauseType"]= [None]*len(df)
df["Comments"] = [None]*len(df)
d = df.to_dict()

#creating dict for labeled data (later to be saved to csv result file)
# d = {'Speaker':speaker,
#      'Orthography':orthography, 
#      "SpeechAct": [None] * len(df), 
#      "ClauseType": [None] * len(df), 
#      "Comments": [None] * len(df)}



def warnings():
    global warning_appeared
        
    if (speechAct_0_var.get() == 0
        and speechAct_1_var.get() == 0
        and speechAct_2_var.get() == 0 
        and speechAct_3_var.get() == 0 ):
        tk.messagebox.showwarning("Warning", "Please label SpeechAct!")
        warning_appeared = True
        return
    
    if (clauseType_0_var.get() == 0
        and clauseType_1_var.get() == 0
        and clauseType_2_var.get() == 0 
        and clauseType_3_var.get() == 0 
        and clauseType_4_var.get() == 0):
        tk.messagebox.showwarning("Warning", "Please label ClauseType!")
        warning_appeared = True
        return 

    return


def show_prev_choices():
    
    if d["SpeechAct"][index] != None:
        ind = speechAct_types.index(d["SpeechAct"][index])
        speechAct_vars[ind].set(1)
    else:
        speechAct_0.deselect()
        speechAct_1.deselect()
        speechAct_2.deselect()
        speechAct_3.deselect()
        
    if d["ClauseType"][index] != None:
        ind = clauseType_types.index(d["ClauseType"][index])
        clauseType_vars[ind].set(1)
    else:
        clauseType_0.deselect()
        clauseType_1.deselect()
        clauseType_2.deselect()
        clauseType_3.deselect()
        clauseType_4.deselect()
        
    
    if d["Comments"][index] != None:
        comments_label.insert(tk.END,d["Comments"][index])
    else:
        comments_label.delete("1.0", "end")
    
    

    

#NEXT step
previous_data = tk.Label(window, text = "\n" + str(index) + ". " + 
                         speaker[index] + ": " + orthography[index]+ "\n\n", 
                         font="Verdana 18 bold underline")
previous_data.grid(row=1, column=0, sticky = "w")


def previous_and_next(s):
    global index, warning_appeared

    warnings() 
    if warning_appeared == True:
        warning_appeared = False
        return
        

    if index == 0 and s == "previous":
        tk.messagebox.showwarning("Warning", "There is no previous data!")
        return
    
    
    #saving comments
    user_comments = comments_label.get("1.0", "end")
    d["Comments"][index] = user_comments

        
    if s == "previous":
        index -= 1
    elif s == "next":
        index += 1
        
        
    previous_data.configure(text = "\n" + str(index) + ". " + speaker[index] + ": " + orthography[index]+ "\n\n")
    
    speechAct_0.deselect()
    speechAct_1.deselect()
    speechAct_2.deselect()
    speechAct_3.deselect()
    
    clauseType_0.deselect()
    clauseType_1.deselect()
    clauseType_2.deselect()
    clauseType_3.deselect()
    clauseType_4.deselect()
    
    comments_label.delete("1.0", "end")
    
    
    #reshowing previous chosen labels
    show_prev_choices()

    result_df = pd.DataFrame.from_dict(d, orient = "index").T
    result_df.to_csv("labeled_data.csv")
    





def go_to():
    
    global index
    
    go_to_num = get_go_to_num.get("1.0", "end-1c")
    
    #check if user_input is a number
    if go_to_num.isdigit() == False:
        tk.messagebox.showwarning("Warning", "Please input a number")
    else:
        
        #saving comments
        user_comments = comments_label.get("1.0", "end")
        d["Comments"][index] = user_comments
        
        go_to_num = int(go_to_num)
        
        #check if number is out of range
        if go_to_num > len(orthography):
            tk.messagebox.showwarning("Warning", "Number out of range!")
        else:
            index = go_to_num
                
                
            previous_data.configure(text = "\n" + str(index) + ". " + speaker[index] + ": " + orthography[index]+ "\n\n")
            
            speechAct_0.deselect()
            speechAct_1.deselect()
            speechAct_2.deselect()
            speechAct_3.deselect()
            
            clauseType_0.deselect()
            clauseType_1.deselect()
            clauseType_2.deselect()
            clauseType_3.deselect()
            clauseType_4.deselect()
            
            comments_label.delete("1.0", "end")
            
            #reshowing previous chosen labels
            show_prev_choices()
        
            result_df = pd.DataFrame.from_dict(d, orient = "index").T
            result_df.to_csv("labeled_data.csv")
            
   
        
        
        
    
#EXIT
def close():
    
    #save comments before exiting
    user_comments = comments_label.get("1.0", "end")
    d["Comments"][index] = user_comments
    
    result_df = pd.DataFrame.from_dict(d, orient = "index").T
    result_df.to_csv("labeled_data.csv")
            
    window.destroy()




def add_speechAct(s):
    
    global warning_appeared
    
    if s == "Question":
        speechAct_1.deselect()
        speechAct_2.deselect()
        speechAct_3.deselect()
        
    elif s == "Assertion":
        speechAct_0.deselect()
        speechAct_2.deselect()
        speechAct_3.deselect()
    elif s == "Request":
        speechAct_0.deselect()
        speechAct_1.deselect()
        speechAct_3.deselect()
    elif s == "Other":
        speechAct_0.deselect()
        speechAct_1.deselect()
        speechAct_2.deselect()
        
    d["SpeechAct"][index] = s 
    
    warning_appeared = False
    
    
    
def add_clauseType(s):
    
    global warning_appeared
    
    if s == "Interrogative":
        clauseType_1.deselect()
        clauseType_2.deselect()
        clauseType_3.deselect()
        clauseType_4.deselect()
    elif s == "Declarative":
        clauseType_0.deselect()
        clauseType_2.deselect()
        clauseType_3.deselect()
        clauseType_4.deselect()
    elif s == "Inperative":
        clauseType_0.deselect()
        clauseType_1.deselect()
        clauseType_3.deselect()
        clauseType_4.deselect()
    elif s == "Fragment":
        clauseType_0.deselect()
        clauseType_1.deselect()
        clauseType_2.deselect()
        clauseType_4.deselect()
    elif s == "Other":
        clauseType_0.deselect()
        clauseType_1.deselect()
        clauseType_2.deselect()
        clauseType_3.deselect()
        
    d["ClauseType"][index] = s 
    
    warning_appeared = False





#SpeechAct
tk.Label(window, text="SpeechAct:", font=("Verdana", 14)).grid(row=8, column=0)
var1 = tk.StringVar()
speechAct_label = tk.Label(window, textvariable=var1, font=("Verdana", 14))
speechAct_label.grid(row=8, column=1)


speechAct_0_var = tk.IntVar()
speechAct_0 = tk.Checkbutton(window, text='Question', variable = speechAct_0_var, 
                             command = lambda: add_speechAct('Question'), width=18, 
                             bg='white', font=("Verdana", 14))
speechAct_0.grid(row=9, column=1, sticky = "nw")


speechAct_1_var = tk.IntVar()
speechAct_1 = tk.Checkbutton(window, text='Assertion', variable = speechAct_1_var, 
                             command = lambda: add_speechAct('Assertion'), width=18, 
                             bg='white', font=("Verdana", 14))
speechAct_1.grid(row=9, column=2, sticky = "nw")


speechAct_2_var = tk.IntVar()
speechAct_2 = tk.Checkbutton(window, text='Request', variable = speechAct_2_var, 
                             command = lambda: add_speechAct('Request'), width=18, 
                             bg='white', font=("Verdana", 14))
speechAct_2.grid(row=9, column=3, sticky = "nw")


speechAct_3_var = tk.IntVar()
speechAct_3 = tk.Checkbutton(window, text='Other', variable = speechAct_3_var, 
                             command = lambda: add_speechAct('Other'), width=18, 
                             bg='white', font=("Verdana", 14))
speechAct_3.grid(row=9, column=4, sticky = "nw")

#accessed when reshowing previous 
speechAct_vars = [speechAct_0_var, speechAct_1_var, speechAct_2_var, speechAct_3_var]




#ClauseType
tk.Label(window, text="ClauseType:", font=("Verdana", 14)).grid(row=12, column=0)
var2 = tk.StringVar()
clauseType_label = tk.Label(window, textvariable=var2,font=("Verdana", 14))
clauseType_label.grid(row=12, column=1, columnspan=4)


clauseType_0_var = tk.IntVar()
clauseType_0 = tk.Checkbutton(window, text="Interrogative", variable = clauseType_0_var, 
                              command = lambda: add_clauseType("Interrogative"), 
                              width=18, bg='white', font=("Verdana", 14))
clauseType_0.grid(row=13, column=1, sticky = "nw")


clauseType_1_var = tk.IntVar()
clauseType_1 = tk.Checkbutton(window, text="Declarative", variable = clauseType_1_var, 
                              command = lambda: add_clauseType("Declarative"), 
                              width=18, bg='white', font=("Verdana", 14))
clauseType_1.grid(row=13, column=2, sticky = "nw")


clauseType_2_var = tk.IntVar()
clauseType_2 = tk.Checkbutton(window, text="Imperative", variable = clauseType_2_var, 
                              command = lambda: add_clauseType("Imperative"), 
                              width=18, bg='white', font=("Verdana", 14))
clauseType_2.grid(row=13, column=3, sticky = "nw")


clauseType_3_var = tk.IntVar()
clauseType_3 = tk.Checkbutton(window, text="Fragment", variable = clauseType_3_var, 
                              command = lambda: add_clauseType("Fragment"), 
                              width=18, bg='white', font=("Verdana", 14))
clauseType_3.grid(row=13, column=4, sticky = "nw")


clauseType_4_var = tk.IntVar()
clauseType_4 = tk.Checkbutton(window, text="Other", variable = clauseType_4_var, 
                              command = lambda: add_clauseType("Other"), 
                              width=18, bg='white', font=("Verdana", 14))
clauseType_4.grid(row=13, column=5, sticky = "nw")

clauseType_vars = [clauseType_0_var, clauseType_1_var, clauseType_2_var, clauseType_3_var, clauseType_4_var]




# Comments
tk.Label(window, text = "Comments:", font=("Verdana", 14)).grid(row=16, column=0)
var3 = tk.StringVar()
comments_label = tk.Text(window, height = 3, width = 20)
comments_label.grid(row=17, column=1, columnspan = 3, sticky = "W"+"E")



#Previous, Save, Next, Exit
tk.Button(window, text="Previous", width=10, command = lambda: previous_and_next("previous"), 
          font="Verdana 16 bold").grid(row=25, column=4, pady = 36)

tk.Button(window, text="Next", width=10, command = lambda: previous_and_next("next"), 
          font="Verdana 16 bold").grid(row=25, column=5,pady = 36)

tk.Button(window, text="Exit", width=10, command = lambda: close(), 
          font="Verdana 16 bold").grid(row=25, column=6,pady = 36)



#Go to Option
tk.Label(window, text="Go to: ", width=10, font="Verdana 16").grid(row=26, column=4)
get_go_to_num = tk.Text(window, height = 1, width = 10)
get_go_to_num.grid(row = 26, column = 5)
tk.Button(window, text="Confirm", width=10,command = lambda: go_to(), font="Verdana 16 bold").grid(row=26, column=6)




window.mainloop()
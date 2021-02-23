import tkinter as tk

class simpleapp_tk(tk.Tk):
	def __init__(self, master):
		tk.Tk.__init__(self,master)
		self.master= master
		self.radios=[]
		cate = {
			"SpeechAct": ["Assertion", "Question"],
			"ClauseType": ["Dec", "Int"]
		}

		i = 0
		label = tk.Label(self, text = "Speech Act")
		label.grid(column=1,row=i,sticky="s",columnspan=2)
		i += 1

		for s in cate["SpeechAct"]:
			self.BuildButton(cate, "SpeechAct",s,i)

			#self.cute(c)
		self.grid()
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,True)
		self.update()
	#place a button on the GUI
	def BuildButton(self, dikt, categoryLabel, buttonLabel, row):
		self.categoryLabel = tk.StringVar() 
		#need to check if there is existing data, but could use another function
		for buttonLabel in dikt[categoryLabel]:
			b = tk.Radiobutton(self,text=buttonLabel,variable=self.categoryLabel,value=buttonLabel,indicatoron=0,width=10,height=2,command=lambda:self.cute(buttonLabel))
			b.grid(column=1,row=row,columnspan=2)
			self.radios.append(b)
			row+=1 

		#tk.Button(self, text = textlabel, command = lambda: self.cute(cutie)).pack()

	#what does each button do
	def cute(self, butt):
		#self.butt = butt
		print(butt)

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.mainloop()
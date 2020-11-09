from tkinter import *
from tkinter import font 
from tkinter import ttk 
from tkinter.messagebox import *
import threading, serial_communication, sys, logging, time, ctypes

class GUI: 
	# constructor method 
	def __init__(self): 
		self.close_serial = False
		
		self.logs = logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename='log.txt', level=logging.INFO)
		# chat window which is currently hidden 
		self.Window = Tk() 
		self.Window.withdraw() 
		
		# login window
		self.login = Toplevel() 
		
		# set the title 
		self.login.title("Login") 
		self.login.resizable(width = False, height = False) 
		self.login.configure(width = 400, height = 300) 
		self.login.protocol("WM_DELETE_WINDOW", sys.exit)
		# create a Label 
		self.pls = Label(self.login, text = "Please login to continue", justify = CENTER, font = "Helvetica 14 bold") 
		self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.07) 

		# create a Label 
		self.labelName = Label(self.login, text = "Name: ", font = "Helvetica 12") 
		self.labelName.place(relheight = 0.2, relx = 0.1, rely = 0.2) 
		
		# create a entry box for 
		# tyoing the message 
		self.entryName = Entry(self.login, font = "Helvetica 14") 
		self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2) 
		
		# set the focus of the curser 
		self.entryName.focus() 
		
		# create form for serial
		self.port = Label(self.login, text="COM port: ", font='Helvetica 12')
		self.port.place(relheight=0.2, relx=0.1, rely=0.4)
		self.entry_com_port = Entry(self.login, font='Helvetica 14')
		self.entry_com_port.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4)
		
		# create a Continue Button 
		# along with action
		self.go = Button(self.login, text = "CONTINUE", font = "Helvetica 14 bold", command=lambda: self.goAhead(self.entryName.get()) if serial_communication.available_ports(self.entry_com_port.get()) == True 
																																		else showerror('COM Port', 'COM port does not exist'))
		self.go.place(relx = 0.4, rely = 0.55) 
		self.Window.mainloop() 

	def goAhead(self, name): 
		self.login.destroy() 
		self.layout(name) 
		self.rcv = threading.Thread(target=self.receive) 
		self.rcv.start()
		
	# The main layout of the chat 
	def layout(self,name): 
		self.name = name 

		# to show chat window
		self.Window.deiconify() 
		self.Window.title("CHATROOM") 
		self.Window.resizable(width = False, height = False) 
		self.Window.configure(width = 470, height = 550, bg = "#17202A")
		self.Window.bind('<Destroy>', self.just_exit)
		self.Window.bind('<Return>', self.sendButton)

		self.labelHead = Label(self.Window, bg = "#17202A", fg = "#EAECEE", text = self.name, font = "Helvetica 13 bold", pady = 5) 
		self.labelHead.place(relwidth = 1) 

		self.line = Label(self.Window, width = 450, bg = "#ABB2B9") 
		self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
		
		self.textCons = Text(self.Window, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5) 
		self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08) 
		
		self.labelBottom = Label(self.Window, bg = "#ABB2B9", height = 80) 
		self.labelBottom.place(relwidth = 1, rely = 0.825) 
		
		self.entryMsg = Entry(self.labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13") 
		
		# place the given widget 
		# into the gui window 
		self.entryMsg.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011) 		
		self.entryMsg.focus() 
		
		# create a Send Button 
		self.buttonMsg = Button(self.labelBottom, text = "Send", font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9", command = lambda: self.sendButton()) 
		self.buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22) 
		
		self.textCons.config(cursor = "arrow") 
		
		# create a scroll bar 
		scrollbar = Scrollbar(self.textCons) 
		
		# place the scroll bar 
		# into the gui window 
		scrollbar.place(relheight = 1, relx = 0.974) 
		scrollbar.config(command = self.textCons.yview) 
		
		self.textCons.config(state = DISABLED) 

	# function to basically start the thread for sending messages 
	def sendButton(self, event=False):
		self.textCons.config(state = DISABLED) 
		self.msg = self.entryMsg.get()
		self.entryMsg.delete(0, END)
		snd = threading.Thread(target = self.sendMessage); snd.start()
		
	# function to receive messages 
	def receive(self): 
		self.com_port = serial_communication.COMPORT
		while True: 
			if self.close_serial == False:
				message = self.com_port.readline().decode()
				# insert message to text box
				if message != '':
					logging.info(message.strip())
					self.textCons.config(state = NORMAL) 
					self.textCons.insert(END, time.strftime('%d/%m/%Y %H:%M:%S')+' '+message+'\n') 
					self.textCons.config(state = DISABLED) 
					self.textCons.see(END)
					message = ''
			else:
				print('close serial')
				self.com_port.close()
				break
		
	# function to send messages 
	def sendMessage(self, event=False): 
		self.textCons.config(state=DISABLED) 
		while True:
			message = (f"{self.name}: {self.msg}") 
			self.textCons.config(state = NORMAL) 
			self.textCons.insert(END, time.strftime('%d/%m/%Y %H:%M:%S')+' '+message+'\n') 
			self.textCons.config(state = DISABLED) 
			self.textCons.see(END)
			logging.info(message.strip())
			self.com_port.write(message.encode())
			self.msg = ''
			break
		
	def just_exit(self, event):
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.rcv.ident, ctypes.py_object(SystemExit))
		sys.exit()
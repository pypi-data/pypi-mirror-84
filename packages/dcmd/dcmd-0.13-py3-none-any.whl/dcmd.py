import win32api, win32gui, win32con, win32process
from ctypes import windll, byref, wintypes
from ctypes.wintypes import SMALL_RECT
import ctypes
import traceback
import sys, os
sys.excepthook = traceback.format_exc
import struct
import psutil
try:
	from pause import pause
except:
	pass
import time
if sys.version_info.major == 3:
	raw_input = input
try:
	from make_colors import make_colors
except:
	traceback.format_exc()
	def make_colors(data):
		return data
try:
	from pydebugger.debug import debug
except:
	def debug(**kwargs):
		for i in kwargs:
			print(str(i), "=", kwargs.get(i), " ", type(kwargs.get(i)))
HANDLE = win32gui.GetForegroundWindow()
	
class COORD(ctypes.Structure):
	_fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
	LF_FACESIZE = 32 
	_fields_ = [
				("cbSize", ctypes.c_ulong),
				("nFont", ctypes.c_ulong),
				("dwFontSize", COORD),
				("FontFamily", ctypes.c_uint),
				("FontWeight", ctypes.c_uint),
				("FaceName", ctypes.c_wchar * LF_FACESIZE)
	]
	

class dcmd(object):
	def __init__(self):
		super(dcmd, self)
		self.STDOUT = -11
		self.hdl = windll.kernel32.GetStdHandle(self.STDOUT)
		if not HANDLE:
			self.foreground_handle = win32gui.GetForegroundWindow()
		else:
			self.foreground_handle = HANDLE
		
	def getHandle(self):
		return HANDLE
	
	def getScreenSize(self):
		return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

	def setPosition(self, left, top, right, bottom, handle = None):
		if not handle:
			handle = self.hdl
		#rect = wintypes.SMALL_RECT(0, 0, 100, 80) # (left, top, right, bottom) 
		rect = wintypes.SMALL_RECT(left, top, right, bottom) # (left, top, right, bottom) 
		windll.kernel32.SetConsoleWindowInfo(handle, True, byref(rect))
		
	def setBuffer(self, rows=None, columns=None, handle = None):
		traceback.debug_server_client(str(handle))
		width, height, curx, cury, wattr, left, top, right, bottom, maxx, maxy = self.getBuffer(handle)
		print(width, height, curx, cury, wattr, left, top, right, bottom, maxx, maxy)
		#pause()
		if not rows:
			rows = width
		if not columns:
			columns = height
		print("columns =", columns)
		print("rows =", rows)
		#bufsize = wintypes._COORD(100, 80) # rows, columns
		bufsize = wintypes._COORD(rows, columns) # rows, columns
		print("bufsize 0 =", bufsize)
		traceback.debug_server_client(str(bufsize))
		if not handle:
			handle = self.hdl
		traceback.debug_server_client(str(handle))
		print("handle 0 =", handle)
		#pause()
		try:
			windll.kernel32.SetConsoleScreenBufferSize(handle, bufsize)
		except:
			handle = self.hdl
			print("handle 1 =", handle)
			width, height, curx, cury, wattr, left, top, right, bottom, maxx, maxy = self.getBuffer(handle)
			bufsize = wintypes._COORD(rows, columns) # rows, columns
			print("bufsize 1 =", bufsize)
			traceback.debug_server_client(str(bufsize))
			#pause()
			try:
				windll.kernel32.SetConsoleScreenBufferSize(handle, bufsize)
			except:
				os.system("mo BL={0} BC={1} WC={2} WL=10".format(rows, columns, columns))
		
	def getBuffer(self, handle = None):
		if not handle:
			handle = self.hdl
		csbi = ctypes.create_string_buffer(22)
		res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
		width, height, curx, cury, wattr, left, top, right, bottom, maxx, maxy = struct.unpack("hhhhHhhhhhh", csbi.raw)
		return width, height, curx, cury, wattr, left, top, right, bottom, maxx, maxy
		#return winbase.GetConsoleScreenBufferInfo()
		
	def setSize(self, width=None, height=None, x = None, y = None, center=False, handle = None):
		x1 = x
		y1 = y
		if not handle:
			handle = self.foreground_handle
		#print("handle =", handle)
		#pause()
		x0, y0, width0, height0 = win32gui.GetWindowRect(handle)
		#print("width0 =", width0)
		if not width:
			width = width0
		if not height:
			height = height0
		if x == "right" or x == "r":
			x = win32api.GetSystemMetrics(0) - width
			#y = y0
		if x == "left" or x == "l":
			print("width =", width)
			x = 0
			#y = y0
		if x == "button" or x == "b" or y == "button" or y == "b":
			y = win32api.GetSystemMetrics(1) - height
			#x = x0
		if x == "top" or x == "t" or y == "top" or y == "t":
			y = 30
			#x = x0
		#  print("x =", x)
		#  print("y =", y)
		#  print("height =", height)
		
		if x and str(x).isdigit():
			x = int(x)
		if y and str(y).isdigit():
			y = int(y)
		if not x:
			if x == 0:
				x = 0
			else:
				x = x0
		if not y:
			if y == 0:
				y = 0
			else:
				y = y0
		
		if x == 'c' or y == 'c':
			center = True
			x = x0
		
		#  print("x =",x)
		#  print("y =",y)
		#  print("width =", width)
		#  print("height =", height)
		if center:
			win32gui.MoveWindow(handle, int(win32api.GetSystemMetrics(0)/3), int(win32api.GetSystemMetrics(1)/10), width, height, True)
		else:
			win32gui.MoveWindow(handle, x, y, width, height, True)
			
	def setAlwaysOnTop(self, width, height, x = 0, y = 0, center=False, handle=None):
		if not handle:
			handle = self.foreground_handle
		#win32gui.SetWindowPos(self.foreground_handle, win32con.HWND_TOPMOST,win32api.GetSystemMetrics(0)/3,win32api.GetSystemMetrics(1)/3,500,170,0)
		if center:
			win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, int(win32api.GetSystemMetrics(0)/3), int(win32api.GetSystemMetrics(1)/10), width, height, 0)
		else:
			win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, x, y, width, height, 0)
			
	def setNormal(self, width, height, handle = None):
		if not handle:
			handle = self.foreground_handle
		win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, int(win32api.GetSystemMetrics(0)/3), int(win32api.GetSystemMetrics(1)/10), width, height, 0)
		
	def changeFont(self, nfont=12, xfont=11, yfont=18, ffont=54, wfont=400, name="Lucida Console", handle = None):
		font = CONSOLE_FONT_INFOEX() 
		font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
		font.nFont = nfont
		font.dwFontSize.X = xfont
		font.dwFontSize.Y = yfont
		font.FontFamily = ffont
		font.FontWeight = wfont
		font.FaceName = name
		#  print("yfont =", yfont)
		#  print("name  =", name)
		if not handle:
			handle = self.hdl
		ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))
		
	def getListProcess(self, filter = None):
		debug(filter = filter)
		all_process = psutil.process_iter()
		process = []
		for i in all_process:
			if filter:
				for f in filter:
					if str(f).isdigit():
						if int(f) == i.pid:
							process.append(i)
					else:
						if str(f).lower() == i.name() or str(f).lower() in i.name().lower():
							process.append(i)
						else:
							try:
								if str(f).lower() in i.cmdline().lower():
									process.append(i)
							except:
								pass
			else:
				process.append(i)
		return process
		
	def getListWindows(self, all = False, filter=None, print_list=True, pid = None):
		debug(filter = filter)
		all_filter = []
		all_list_hide = []
		all_list_hide_filter = []
		all_windows = []
		all_pids = []
		debug(pid = pid)
		if filter and not pid:
			process = self.getListProcess(filter)
			pid = []
			debug(process = process)
			if process:
				for i in process:
					pid.append(i.pid)

		def enumsHandle(hwnd, lParam):
			title = win32gui.GetWindowText(hwnd)
			rect = win32gui.GetWindowRect(hwnd)
			ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
			#print(ctid, cpid)
			if not title:
				try:
					title = psutil.Process(cpid).name()
				except:
					pass
			if not title:
				try:
					title = psutil.Process(cpid).cmdline()
				except:
					pass

			excpt = ["Form1", "Default IME", "MSCTFIME UI", "frmTray", "frmBar", "frmLine1", "frmLine2", "frmLine3", "frmLine4", "frmLine5", "Rating", "CD Art Display 1.x Class", "CADnotifier", "CiceroUIWndFrame", "VistaSwitcher", "DDE Server Window", "uninteresting", "DWM Notification Window", "EndSessionWindow", "Program Manager", "GetPosWnd", "igfxtrayWindow"]
			
			if not all:
				if title and not title in excpt and not len(title) == 1:
					all_windows.append([title, rect, cpid, ctid, hwnd])
					if win32gui.IsWindowVisible(hwnd) == 0:
						all_list_hide.append([title, rect, cpid, ctid, hwnd])
					if print_list:
						print(title + " [" + str(rect) + "] [" + str([ctid,cpid]) + "] [" + str(hwnd) + "] (" + str(win32gui.IsWindowVisible(hwnd)) + ")")
			else:
				all_windows.append([title, rect, cpid, ctid, hwnd])
				if win32gui.IsWindowVisible(hwnd) == 0:
					all_list_hide.append([title, rect, cpid, ctid, hwnd])				
				if print_list:
					print(title + " [" + str(rect) + "] [" + str([ctid,cpid]) + "] [" + str(hwnd) + "] (" + str(win32gui.IsWindowVisible(hwnd)) + ")")
		
		win32gui.EnumWindows(enumsHandle, None)
		debug(all_list_hide = all_list_hide)
		if filter:
			for i in filter:
				for x in all_windows:
					if i.lower == x[0].lower():
						all_filter.append(x)
					else:
						if i.lower() in x[0].lower() and not 'administrator' in x[0].lower():
							all_filter.append(x)
				
			if all_list_hide:
				for i in filter:
					for x in all_list_hide:
						if i.lower == x[0].lower():
							all_list_hide_filter.append(x)
						else:
							if i.lower() in x[0].lower() and not 'administrator' in x[0].lower():
								all_list_hide_filter.append(x)
		debug(pid = pid)
		
		if pid:
			for x in all_windows:
				#print(x)
				for p in pid:
					if int(x[2]) == int(str(p).strip()):
						all_pids.append(x)
		debug(all_pids = all_pids)
		
		return all_filter, all_list_hide, all_list_hide_filter, all_pids
	
	def listHide(self):
		hdls, h_hide, h_hide_filter, h_pids = self.getListWindows(print_list = False)
		if h_hide:
			n = 1
			for i in h_hide:
				if len(str(n)) == 1:
					number = "0" + str(n)
				else:
					number = str(n)
				print(make_colors(number + ".", 'lc') + " " + make_colors(i[0], 'lw', 'bl') + " " + "[" + make_colors(str(i[2]), 'lw', 'lr') + "] (" + make_colors(str(i[-1]), 'b', 'lg') + ")")
				n += 1
		
	
	def setHide(self, filter):
		
		all_str = []
		all_int = []
		for i in filter:
			if str(i).isdigit():
				all_int.append(int(i))
			else:
				all_str.append(i)
		hdls, h_hide, h_hide_filter, h_pids = self.getListWindows(filter=all_str, print_list=False, pid = all_int)
		debug(h_hide = h_hide)
		debug(h_pids = h_pids)
		
		if h_pids:
			if len(h_pids) > 1:
				n = 1
				for i in h_pids:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide] [1]: ")
				if q and str(q).isdigit() and not int(q) > len(h_pids):
					h = h_pids[int(q) - 1][-1]
					win32gui.ShowWindow(h, 0)
				elif  q and str(q).strip() == 'all':
					for i in h_pids:
						win32gui.ShowWindow(i[-1], 0)
			else:
				h = h_pids[0][-1]
				win32gui.ShowWindow(h, 0)
		else:
			if hdls:
				if len(hdls) > 1:
					n = 1
					for i in hdls:
						print(str(n) + ". " + str(i[0]))
						n+=1
					q = raw_input("Select number to show [all = for show all of hide] [2]: ")
					if q and str(q).isdigit() and not int(q) > len(hdls):
						h = hdls[int(q) - 1][-1]
						win32gui.ShowWindow(h, 0)
					elif  q and str(q).strip() == 'all':
						for i in hdls:
							win32gui.ShowWindow(i[-1], 0)
				else:
					h = hdls[0][-1]
					win32gui.ShowWindow(h, 0)
					
			else:
				if h_hide_filter:
					if len(h_hide_filter) > 1:
						n = 1
						for i in h_hide_filter:
							print(str(n) + ". " + str(i[0]))
							n+=1
						q = raw_input("Select number to show [all = for show all of hide] [3]: ")
						if q and str(q).isdigit() and not int(q) > len(h_hide_filter):
							h = h_hide_filter[int(q) - 1][-1]
							win32gui.ShowWindow(h, 0)
						elif  q and str(q).strip() == 'all':
							for i in h_hide_filter:
								win32gui.ShowWindow(i[-1], 0)
					else:
						h = h_hide_filter[0][-1]
						win32gui.ShowWindow(h, 0)							
				
	def setShow(self, filter):
		all_str = []
		all_int = []
		for i in filter:
			if str(i).isdigit():
				all_int.append(int(i))
			else:
				all_str.append(i)
		debug(all_int = all_int)
		debug(all_str = all_str)
		hdls, h_hide, h_hide_filter, h_pids = self.getListWindows(filter=all_str, print_list=False, pid = all_int)
		debug(h_hide = h_hide)
		debug(h_pids = h_pids)		
		if h_pids:
			if len(h_pids) > 1:
				n = 1
				for i in h_pids:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide] [1]: ")
				if q and str(q).isdigit() and not int(q) > len(h_pids):
					h = h_pids[int(q) - 1][-1]
					win32gui.ShowWindow(h, 1)
				elif  q and str(q).strip() == 'all':
					for i in h_pids:
						win32gui.ShowWindow(i[-1], 1)
						win32gui.BringWindowToTop(i[-1])
			else:
				h = h_pids[0][-1]
				win32gui.ShowWindow(h, 1)
				win32gui.BringWindowToTop(h)
		else:
			if hdls:
				if len(hdls) > 1:
					n = 1
					for i in hdls:
						print(str(n) + ". " + str(i[0]))
						n+=1
					q = raw_input("Select number to show [all = for show all of hide] [2]: ")
					if q and str(q).isdigit() and not int(q) > len(hdls):
						h = hdls[int(q) - 1][-1]
						win32gui.ShowWindow(h, 1)
					elif  q and str(q).strip() == 'all':
						for i in hdls:
							win32gui.ShowWindow(i[-1], 1)
							win32gui.BringWindowToTop(i[-1])
				else:
					h = hdls[0][-1]
					win32gui.ShowWindow(h, 1)
					win32gui.BringWindowToTop(h)
			else:
				if h_hide:
					if len(h_hide) > 1:
						n = 1
						for i in h_hide:
							print(str(n) + ". " + str(i[0]))
							n+=1
						q = raw_input("Select number to show [all = for show all of hide] [3]: ")
						if q and str(q).isdigit() and not int(q) > len(h_hide):
							h = h_hide[int(q) - 1][-1]
							win32gui.ShowWindow(h, 1)
						elif  q and str(q).strip() == 'all':
							for i in h_hide:
								win32gui.ShowWindow(i[-1], 1)
								win32gui.BringWindowToTop(i[-1])
					else:
						h = h_hide[0][-1]
						win32gui.ShowWindow(h, 1)
						win32gui.BringWindowToTop(h)
			
	def setTop(self, name = None, normal=False, handle = None):
		hdls = []
		if name:
			def enumsHandle(hwnd, lParam):
				title = win32gui.GetWindowText(hwnd)
				if not 'administrator' in title.lower() and name.lower() in title.lower() or name.lower() == title.lower():
					hdls.append([hwnd, title])
			win32gui.EnumWindows(enumsHandle, None)
			
			if hdls:
				if len(hdls) > 1:
					n = 1
					for i in hdls:
						print(str(n) + ". " + i[1])
						n+=1
					q = raw_input("Select number to top: ")
					if q and str(q).isdigit() and not int(q) >  len(hdls):
						h = hdls[int(q) - 1][0]
						rect = win32gui.GetWindowRect(h)
						if normal:
							win32gui.SetWindowPos(h, win32con.HWND_NOTOPMOST, rect[0], rect[1], rect[2], rect[3], 0)
						else:
							win32gui.SetWindowPos(h, win32con.HWND_TOPMOST, rect[0], rect[1], rect[2], rect[3], 0)
				else:
					h = hdls[0][0]
					rect = win32gui.GetWindowRect(h)
					if normal:
						win32gui.SetWindowPos(h, win32con.HWND_NOTOPMOST, rect[0], rect[1], rect[2], rect[3], 0)
					else:
						win32gui.SetWindowPos(h, win32con.HWND_TOPMOST, rect[0], rect[1], rect[2], rect[3], 0)
		else:
			if not handle:
				handle = self.foreground_handle
			rect = win32gui.GetWindowRect(handle)
			if normal:
				win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, rect[0], rect[1], rect[2], rect[3], 0)
			else:
				win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, rect[0], rect[1], rect[2], rect[3], 0)
		
	def setMinimize(self, filter):
		all_str = []
		all_int = []
		for i in filter:
			if str(i).isdigit():
				all_int.append(int(i))
			else:
				all_str.append(i)
		debug(all_int = all_int)
		debug(all_str = all_str)
		hdls, h_hide, h_hide_filter, h_pids = self.getListWindows(filter=all_str, print_list=False, pid = all_int)
		debug(hdls = hdls)
		debug(h_hide = h_hide)
		debug(h_hide_filter = h_hide_filter)
		debug(h_pids = h_pids)		
		if h_pids:
			if len(h_pids) > 1:
				n = 1
				for i in h_pids:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide]: ")
				if q and str(q).isdigit() and not int(q) > len(h_pids):
					h = h_pids[int(q) - 1][-1]
					win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
				elif  q and str(q).strip() == 'all':
					for i in h_pids:
						win32gui.ShowWindow(i[-1], win32con.SW_MINIMIZE)
			else:
				h = h_pids[0][-1]
				win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
		elif h_hide_filter:
			if len(h_hide_filter) > 1:
				n = 1
				for i in h_hide_filter:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide]: ")
				if q and str(q).isdigit() and not int(q) > len(h_hide_filter):
					h = h_hide_filter[int(q) - 1][-1]
					win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
				elif  q and str(q).strip() == 'all':
					for i in h_hide_filter:
						win32gui.ShowWindow(i[-1], win32con.SW_MINIMIZE)
			else:
				h = h_hide_filter[0][-1]
				win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
				
		elif hdls:
			if len(hdls) > 1:
				n = 1
				for i in hdls:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide]: ")
				if q and str(q).isdigit() and not int(q) > len(hdls):
					h = hdls[int(q) - 1][-1]
					win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
				elif  q and str(q).strip() == 'all':
					for i in hdls:
						win32gui.ShowWindow(i[-1], win32con.SW_MINIMIZE)
			else:
				h = hdls[0][-1]
				win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
		#elif h_hide:
			#if len(h_hide) > 1:
				#n = 1
				#for i in h_hide:
					#print(str(n) + ". " + str(i[0]))
					#n+=1
				#q = raw_input("Select number to show [all = for show all of hide]: ")
				#if q and str(q).isdigit() and not int(q) > len(h_hide):
					#h = h_hide[int(q) - 1][-1]
					#win32gui.ShowWindow(h, win32con.SW_MINIMIZE)
				#elif  q and str(q).strip() == 'all':
					#for i in h_hide:
						#win32gui.ShowWindow(i[-1], win32con.SW_MINIMIZE)
			#else:
				#h = h_hide[0][-1]
				#win32gui.ShowWindow(h, win32con.SW_MINIMIZE)		
	
	def setMaximize(self, filter):
		all_str = []
		all_int = []
		for i in filter:
			if str(i).isdigit():
				all_int.append(int(i))
			else:
				all_str.append(i)
		debug(all_int = all_int)
		debug(all_str = all_str)
		hdls, h_hide, h_hide_filter, h_pids = self.getListWindows(filter=all_str, print_list=False, pid = all_int)
		debug(h_hide = h_hide)
		debug(h_pids = h_pids)		
		if h_pids:
			if len(h_pids) > 1:
				n = 1
				for i in h_pids:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide]: ")
				if q and str(q).isdigit() and not int(q) > len(h_pids):
					h = h_pids[int(q) - 1][-1]
					win32gui.ShowWindow(h, 1)
				elif  q and str(q).strip() == 'all':
					for i in h_pids:
						win32gui.ShowWindow(i[-1], win32con.SW_MAXIMIZE)
						win32gui.BringWindowToTop(i[-1])
			else:
				h = h_pids[0][-1]
				win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
				win32gui.BringWindowToTop(h)
		else:
			if hdls:
				if len(hdls) > 1:
					n = 1
					for i in hdls:
						print(str(n) + ". " + str(i[0]))
						n+=1
					q = raw_input("Select number to show [all = for show all of hide]: ")
					if q and str(q).isdigit() and not int(q) > len(hdls):
						h = hdls[int(q) - 1][-1]
						win32gui.ShowWindow(h, 1)
					elif  q and str(q).strip() == 'all':
						for i in hdls:
							win32gui.ShowWindow(i[-1], win32con.SW_MAXIMIZE)
							win32gui.BringWindowToTop(i[-1])
				else:
					h = hdls[0][-1]
					win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
					win32gui.BringWindowToTop(h)
					
	def setRestore(self, filter):
		all_str = []
		all_int = []
		for i in filter:
			if str(i).isdigit():
				all_int.append(int(i))
			else:
				all_str.append(i)
		debug(all_int = all_int)
		debug(all_str = all_str)
		hdls, h_hide, h_hide_filter, h_pids = self.getListWindows(filter=all_str, print_list=False, pid = all_int)
		debug(h_hide = h_hide)
		debug(h_pids = h_pids)		
		if h_pids:
			if len(h_pids) > 1:
				n = 1
				for i in h_pids:
					print(str(n) + ". " + str(i[0]))
					n+=1
				q = raw_input("Select number to show [all = for show all of hide]: ")
				if q and str(q).isdigit() and not int(q) > len(h_pids):
					h = h_pids[int(q) - 1][-1]
					win32gui.ShowWindow(h, 1)
				elif  q and str(q).strip() == 'all':
					for i in h_pids:
						win32gui.ShowWindow(i[-1], win32con.SW_RESTORE)
						win32gui.BringWindowToTop(i[-1])
			else:
				h = h_pids[0][-1]
				win32gui.ShowWindow(h, win32con.SW_RESTORE)
				win32gui.BringWindowToTop(h)
		else:
			if h_hide:
				if len(h_hide) > 1:
					n = 1
					for i in h_hide:
						print(str(n) + ". " + str(i[0]))
						n+=1
					q = raw_input("Select number to show [all = for show all of hide]: ")
					if q and str(q).isdigit() and not int(q) > len(h_hide):
						h = h_hide[int(q) - 1][-1]
						win32gui.ShowWindow(h, 1)
					elif  q and str(q).strip() == 'all':
						for i in h_hide:
							win32gui.ShowWindow(i[-1], win32con.SW_RESTORE)
							win32gui.BringWindowToTop(i[-1])
				else:
					h = h_hide[0][-1]
					win32gui.ShowWindow(h, win32con.SW_RESTORE)
					win32gui.BringWindowToTop(h)	
	
	def usage(self):
		import argparse
		import sys
		parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
		parser.add_argument('-W', '--width', action='store', help='Set Width', type = int)
		parser.add_argument('-H', '--height', action='store', help='Set Height', type = int)
		parser.add_argument('-x', '--xpos', action='store', help='X position')
		parser.add_argument('-y', '--ypos', action='store', help='Y position')
		parser.add_argument('-c', '--center', action='store_true', help='By pass X,Y then centering it')
		parser.add_argument('-gb', '--get-buffer', action='store_true', help='Get current buffer')
		parser.add_argument('-bc', '--buffer-column', action='store', help='Set Buffer colums', type = int)
		parser.add_argument('-br', '--buffer-row', action='store', help='Set Buffer rows', type = int)
		parser.add_argument('-f', '--font', action='store', help='Change font name', default = "Consolas")
		parser.add_argument('-fs', '--font-size', action='store', help='Change font size', type = int, default = 13)#, required='--font')
		parser.add_argument('-fb', '--font-bold', action='store', help='Change font bold', type = int, default = 400)#, required='--font')
		parser.add_argument('-l', '--list-window', action='store_true', help='Show all window active name/title')
		parser.add_argument('-lh', '--list-window-hide', action='store_true', help='Show all window hiding')
		parser.add_argument('-la', '--list-all-window', action='store_true', help='Show alls window active name/title')
		parser.add_argument('-t', '--always-top', action='store', help='Set always on top')
		parser.add_argument('-nt', '--not-always-top', action='store', help='Set always on top to normal')
		parser.add_argument('-T', '--always-top-this', action='store_true', help='Set always on top for this terminal')
		parser.add_argument('-nT', '--not-always-top-this', action='store_true', help='Set always on top for this terminal to normal')
		parser.add_argument('-gS', '--get-screensize', help='Get Screen size', action='store_true')
		parser.add_argument('-gs', '--get-current-size', help='Get current window size', action='store_true')
		parser.add_argument('-hd', '--hide', help = 'Hide windows by name', action = 'store', nargs = '*')
		parser.add_argument('-sw', '--show', help = 'Show windows by name, type: "all" for show all hide of window', action = 'store', nargs = '*')
		parser.add_argument('-M', '--maximize', help = 'Show windows as maximize by name', action = 'store', nargs = '*')
		parser.add_argument('-m', '--minimize', help = 'Show windows as minimize by name', action = 'store', nargs = '*')
		parser.add_argument('-r', '--restore', help = 'Restore windows and bring to front', action = 'store', nargs = '*')
		parser.add_argument('-F', '--find', help = 'Find process by name or pid', action = 'store')
		parser.add_argument('--wait', help = 'Wait before execute', action = 'store', type = int)
		
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			if args.find:
				n = 1
				if args.wait:
					time.sleep(args.wait)
				if args.find.isdigit():
					all_filter, all_list_hide, all_list_hide_filter, all_pids = self.getListWindows(pid = args.find, print_list = False)
				else:
					all_filter, all_list_hide, all_list_hide_filter, all_pids = self.getListWindows(filter = [args.find], print_list = False)
				if all_filter:
					for i in all_filter:
						if ".exe" in i[0].lower():
							number = str(n)
							if len(number) == 1:
								number = "0" + str(n)
							
							print(make_colors(number, 'lc') + ". " + make_colors(i[0], 'lw', 'lr') + " " + make_colors("PID:", 'lw', 'bl') + " " + make_colors(str(i[2]), 'b', 'ly') + " " + make_colors("HANDLE:", 'lw', 'bl') + " " + make_colors(str(i[-1]), 'lr', 'lw') + " " + make_colors("PARENT:", 'lw', 'bl') + " " + make_colors(str(win32gui.GetParent(i[-1])), 'b', 'lg'))
							n += 1

			if args.width or args.height or args.xpos or args.ypos or args.center:
				self.setSize(args.width, args.height, args.xpos, args.ypos, args.center)
			if args.maximize:
				self.setMaximize(args.maximize)
			if args.minimize:
				self.setMinimize(args.minimize)
			if args.restore:
				self.setRestore(args.restore)
			if args.list_window_hide:
				self.listHide()
			if args.hide:
				self.setHide(args.hide)
			if args.show:
				self.setShow(args.show)
			if args.get_buffer:
				width, height, curx, cury, wattr, left, top, right, bottom, maxx, maxy = self.getBuffer()
				print("WIDTH  =", width)
				print("HEIGHT =", height)
				print("CURX   =", curx)
				print("CURY   =", cury)
				print("WATTR  =", wattr)
				print("LEFT   =", left)
				print("RIGHT  =", right)
				print("TOP    =", top)
				print("BOTTOM =", bottom)
				print("MAX-X  =", maxx)
				print("MAX-y  =", maxy)
			if args.get_current_size:
				x0, y0, width0, height0 = win32gui.GetWindowRect(self.foreground_handle)
				print("WIDTH =", width0)
				print("HEIGHT =", height0)
				print("X      =", x0)
				print("Y      =", y0)
			if args.buffer_column or args.buffer_row:
				self.setBuffer(args.buffer_row, args.buffer_column)
			if args.font or args.font_size or args.font_bold:
				self.changeFont(nfont=12, xfont=11, yfont=args.font_size, ffont=54, wfont=args.font_bold, name=args.font)
			if args.list_window:
				self.getListWindows()
			if args.list_all_window:
				self.getListWindows(all=True)
			if args.always_top:
				self.setTop(args.always_top)
			if args.not_always_top:
				self.setTop(args.not_always_top, normal=True)
			if args.always_top_this:
				self.setTop()
			if args.not_always_top_this:
				self.setTop(normal=True)
			if args.get_screensize:
				print(self.getScreenSize())

def usage():
	c = dcmd()
	c.usage()
	
if __name__ == '__main__':
	c = dcmd()
	c.usage()
		
		
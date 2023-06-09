import tkinter as tk
import customtkinter as ctk
import darkdetect, json, getpass, os, webbrowser
from settings import *
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
from dyn_button import *

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

# Designed and Developed by : Shrivatsa Hosabettu
# Testing contributions by : Sudhanshu Ranjan

# Main class of the application
class LinkApp(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color=(WHITE, BG_COLOR))
        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.minsize(*map(int, '800x600'.split('x')))
        self.title('')
        # self.icon_path = self.resource(r'assets\empty.ico')
        # self.iconbitmap(self.icon_path)
        self.title_bar_color(is_dark)
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')
        self.rowconfigure(2, weight=2, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        # Variables
        self.add_var = ctk.StringVar()
        self.button_name_var = ctk.StringVar()
        self.button_link_var = ctk.StringVar()      
        self.font_size = int(FONT[1])
        self.height = int(self.font_size)
        self.user = getpass.getuser()
        self.file_path = file_path_start + self.user + file_path_end
        self.button_list = []
        self.button_name_link_list = []
        self.next_button_num = 1
        self.edit_button_index = None
        # Initial settings
        if os.path.exists(self.file_path):
            self.reload_button_list()
        # widgets
        self.create_frames()
        self.call_all_widgets()
        # To check if the file is already exists then load all the buttons
        # from the file
        for init_button_counter in range(len(self.button_name_link_list)):
            self.initial_create_button(init_button_counter)
        self.mainloop()
        
    def resource(self, relative_path):
        base_path = getattr(
            sys, 
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    # Create the frames for the application
    def create_frames(self):
        self.create_top_frame()        
        self.create_middle_frame()
        self.call_additional_frame()
    
    # To create top frame which will hold the logo, application Name and check box
    def create_top_frame(self):
        self.top_frame = ctk.CTkFrame(self, fg_color=(WHITE, BG_COLOR), bg_color=(WHITE, BG_COLOR))
        self.top_frame.grid(column=0, row=0, sticky='nsew')        
        
    # To create middle frame which will hold the buttons
    def create_middle_frame(self):
        self.middle_frame = ctk.CTkFrame(self, fg_color=(WHITE, BG_COLOR), bg_color=(WHITE, BG_COLOR))
        self.middle_frame.grid(column=0, row=1, sticky='nsew')
    def call_additional_frame(self):
         # additional Frame to wrap the bottom frame to make hide and unhide
        self.bottom_frame = ctk.CTkFrame(self, fg_color=(WHITE, BG_COLOR), bg_color=(WHITE, BG_COLOR))
        self.additional_frame = ctk.CTkFrame(self, fg_color=(WHITE, BG_COLOR), bg_color=(WHITE, BG_COLOR))
        self.additional_frame.rowconfigure((0,1,2), weight=1, uniform='a')
        self.additional_frame.columnconfigure(0, weight=1, uniform='a')
        self.additional_frame.columnconfigure(1, weight=6, uniform='a')

    # Function to call all the widgets creation
    def call_all_widgets(self):
        self.top_frame_widgets()
        self.middle_frame_widgets()
        self.bottom_frame_widgets()
    
    # Top Frame widget creation
    def top_frame_widgets(self):
        # Frame 1
        # Logo Image
        self.label_header = ctk.CTkLabel(self, text="Application Links", font=('Roboto', 25), bg_color=(WHITE, BG_COLOR))   
        self.label_header.grid(row=0, column=0, sticky='n', padx=10, pady=5)
        self.label_note = ctk.CTkLabel(self, text="Note: Right click to delete the button\n ctrl+click to edit\n click to open the webpage", font=('Roboto', 12, 'bold'), bg_color=(WHITE, BG_COLOR)) 
        self.label_note.grid(row=0, column=0, sticky='w', padx=10, pady=5)   
 
        
        # Check box
        self.add_check_box = ctk.CTkCheckBox(
            master=self, 
            text="Add Button", 
            variable=self.add_var, 
            bg_color=(WHITE, BG_COLOR), 
            onvalue='on', 
            offvalue='off',
            command=self.bottom_frame_control)
        self.add_check_box.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        
    # Middle Frame widget creation
    def middle_frame_widgets(self):
        self.middle_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1, uniform='b')
        self.middle_frame.columnconfigure((0,1,2,3,4), weight=1, uniform='b')
        
    # Bottom Frame widget creation
    def bottom_frame_widgets(self):
        self.button_name_label = ctk.CTkLabel(
            self.additional_frame, 
            text="Button Name *", 
            font=('Roboto', 15), 
            bg_color=(WHITE, BG_COLOR), 
            corner_radius=10
            )
        self.button_name_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        
        self.button_name_text = ctk.CTkEntry(
            self.additional_frame, 
            width=400, 
            height=self.height, 
            textvariable=self.button_name_var,
            font=FONT, 
            bg_color=(WHITE, BG_COLOR), 
            fg_color=(WHITE, BG_COLOR),
            corner_radius=5,
            border_color=HIGHLIGHT_COLOR,
            border_width=1)
        self.button_name_text.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        # Button Link
        button_link_label = ctk.CTkLabel(
            self.additional_frame, 
            text="Button Link *", 
            font=('Roboto', 15), 
            bg_color=(WHITE, BG_COLOR), 
            corner_radius=10)
        button_link_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.button_link_text = ctk.CTkEntry(
            self.additional_frame, 
            width=1000, 
            height=self.height, 
            textvariable=self.button_link_var,
            font=FONT, 
            bg_color=(WHITE, BG_COLOR), 
            fg_color=(WHITE, BG_COLOR),
            border_color=HIGHLIGHT_COLOR,
            corner_radius=5,
            border_width=1)
        self.button_link_text.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        # Ok Button
        self.ok_button = ctk.CTkButton(
            self.additional_frame, 
            text="OK", 
            font=('Roboto', 15), 
            bg_color=(WHITE, BG_COLOR), 
            corner_radius=10,
            command=lambda : self.create_button(self.edit_button_index))
        cancel_button = ctk.CTkButton(
            self.additional_frame, 
            text="Cancel", 
            font=('Roboto', 15), 
            bg_color=(WHITE, BG_COLOR), 
            corner_radius=10,
            command=self.hide_bottom_frame)
        self.ok_button.grid(row=2, column=1, sticky='e', padx=155, pady=5)
        self.ok_button.bind("<Return>", lambda event: self.ok_button.invoke())
        cancel_button.grid(row=2, column=1, sticky='e', padx=5, pady=5)           

    # Bottom frame control based on the check box status
    def bottom_frame_control(self):
        if self.add_var.get() == 'on':
            self.button_name_var.set('')
            self.button_link_var.set('')
            self.additional_frame.grid(row=2, column=0, sticky='nsew', padx=15, pady=5)
            self.button_name_text.focus()
            self.button_name_text.icursor(ctk.END)
        else:
            self.additional_frame.grid_forget()
    def hide_bottom_frame(self):
        self.additional_frame.grid_forget()
        self.add_var.set('off')
    
    # If there are existing buttons in the file then create a new button
    def initial_create_button(self, init_button_counter):
        init_new_button = Button(self.middle_frame, text=self.button_name_link_list[init_button_counter][0],
                                row=len(self.button_list)//5, col=len(self.button_list)%5)
        self.button_list.append(init_new_button)
        self.next_button_num += 1
        init_new_button.bind("<Button-3>", lambda event, button=init_new_button: self.handle_right_click(button))     
        init_new_button.bind("<Button-1>", lambda event, button=init_new_button: self.web_launcher(button))
        init_new_button.bind("<Control-Button-1>", lambda event, button=init_new_button: self.handle_control_click_edit(button))
    # To create new button after adding the information in the bottom frame
    def create_button(self, button_index = None):
        if self.button_name_text.get() != '' and self.button_link_text.get() != '' and button_index == None:
            new_button = Button(self.middle_frame, text=self.button_name_text.get(),
                                row=len(self.button_list)//5, col=len(self.button_list)%5)
            self.button_list.append(new_button)
            self.button_info = [self.button_name_text.get(), self.button_link_text.get()]
            self.button_name_link_list.append(self.button_info)
            self.next_button_num += 1
            self.hide_bottom_frame()
            self.write_button_list()
            new_button.bind("<Button-3>", lambda event, button=new_button: self.handle_right_click(button))     
            new_button.bind("<Button-1>", lambda event, button=new_button: self.web_launcher(button))
            new_button.bind("<Control-Button-1>", lambda event, button=new_button: self.handle_control_click_edit(button))
        elif self.button_name_text.get() != '' and self.button_link_text.get() != '' and button_index != None:
            self.update_button_text(self.ctrl_button)
            self.button_name_link_list[button_index][0] = self.button_name_text.get()
            self.button_name_link_list[button_index][1] = self.button_link_text.get()
            self.additional_frame.grid_forget()
            self.write_button_list()
        else:
            self.show_button_blank_error()    

    # Functionality of right click
    def handle_right_click(self, button):
        self.show_warning()
        if self.msg.get() == 'Ok':
        # Remove the button from the list and destroy it
            self.button_index = self.button_list.index(button)
            self.button_list.remove(button)
            self.button_name_link_list.pop(self.button_index)
            button.grid_forget()
            button.destroy()    
            
            # Rearrange the remaining buttons
            for i, button in enumerate(self.button_list):
                row = i // 5
                col = i % 5
                button.grid(row=row, column=col)
            
            # Write the new button list to the file
            self.write_button_list()
            
    # Functionality of control click
    def handle_control_click_edit(self, button):
        self.ctrl_button = button
        self.edit_button_index = self.button_list.index(button)
        self.button_name_var.set(self.button_name_link_list[self.edit_button_index][0])
        self.button_link_var.set(self.button_name_link_list[self.edit_button_index][1])
        self.button_name_text.bind("<<Modified>>", lambda: self.update_button_text(button))
        self.additional_frame.grid(row=2, column=0, sticky='nsew', padx=15, pady=5)
    
    # To update button text in the bottom frame after editing the button with control click
    def update_button_text(self, button):
        new_text = self.button_name_text.get()
        new_link = self.button_link_text.get()
        button.configure(text=new_text)
        self.edit_button_index = None
    
    # Write button to the file
    def write_button_list(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.button_name_link_list, f)
            
    # Show warning message before deleting the button     
    def show_warning(self):
    # Show some retry/cancel warnings
        self.msg = CTkMessagebox(title="Delete Button!", message="Do you want to delete this button?!",
                  icon="warning", option_1="Cancel", option_2="Ok", topmost=True)
    
    # Show error message if the bottom frame widgets are blank
    def show_button_blank_error(self):
        CTkMessagebox(title="Error", message="Please fill in all fields!!!", icon="cancel", fg_color=BG_COLOR, bg_color=BG_COLOR, topmost=True)            
    
    # Web page open based on the button click
    def web_launcher(self, button):
        self.button_index = self.button_list.index(button)
        open_link = self.button_name_link_list[self.button_index][1]
        webbrowser.open(open_link)    
    
    # reloading the buttons from the file
    def reload_button_list(self):
        with open(self.file_path, 'r') as f:
            json_button_string = f.read()
            if json_button_string != '':
                self.button_name_link_list =json.loads(json_button_string)     
    # To handle the title bar color to match the frame body               
    def title_bar_color(self, is_dark):
            try:
                HWND = windll.user32.GetParent(self.winfo_id())
                DWMWA_ATTRIBUTE = 35
                COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLOR['light']
                windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
            except:
                pass
    
# Main application instance creation
if __name__ == '__main__':
    LinkApp(darkdetect.isDark())
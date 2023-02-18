from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem,TwoLineListItem,ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton,MDRectangleFlatButton,MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.utils import asynckivy as ak
from kivymd.uix.snackbar import Snackbar
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.toast import toast
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard , MDSeparator
from kivy.properties import StringProperty , DictProperty


import os 
from os import path
import sys
import time
try:
    from datetime import datetime
except:
    toast('Module import error')
import shutil
import logging

from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu


class LabelBox(BoxLayout):
    pass
    
class TasksPage(Screen):
    ww = Window.width
    Window.softinput_mode = "below_target"
    
    def enter(self):
        if os.path.exists('path.txt'):
            self.makehome()
        else:
            self.manager.current = 'catp'
           
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.back()
            return True 
            
    def makehome(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        
        menu_items = [
            {"viewclass": "OneLineListItem","text": f"Color All Tasks","height": dp(56),"on_release": lambda x=f"colorall": self.menu_callback(x)}
         ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=3,
            border_margin=dp(24),
            background_color='#33adff'
        )
        
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        try:
            with open('path.txt','r') as f:
                loc = f.read()
            
            lst = os.listdir(f'{MP}/{loc}/')
            self.ids.tbar.title = f'{loc}'
            if 'color.color' in lst:
                lst.remove('color.color')   
            else:
                pass
            if 'desc.color' in lst:
                lst.remove('desc.color')   
            else:
                pass
            if 'time.color' in lst:
                lst.remove('time.color')   
            else:
                pass
                
            try:
                self.ids.flist.clear_widgets()
            except:
                pass
            for task in lst:
                with open(f'{MP}/{loc}/{task}','r') as f:
                    data = f.readlines()
                    col = data[0]
                    
                task = task.split(".")[0]
                task = task.replace('&','/')
                task = task.replace('$','\\')
                task = task.replace('@','"')
                task = task.replace(']',"'")
                col = col.split('\n')[0]
                if col == 'Label':
                    self.ids.flist.add_widget(TwoLineListItem(text=f"{task}",secondary_text=str(data[-1]),font_style="H6",secondary_font_style="Caption",radius=[50, 50, 50, 50],divider='Inset',divider_color='orange',bg_color='orange',on_release=self.open))
                else:
                    self.ids.flist.add_widget(OneLineListItem(text=f"{task}",bg_color=col,on_release=self.open)) 
                
        except Exception as e:
            toast(f'{e}')
    
    def open(self, inst):
        tin = inst
        bottom_sheet_menu = MDListBottomSheet()
        fname = inst.text
        bottom_sheet_menu.add_item(f"Remove Task",lambda x ,y = tin: self.rm_task(str(y),fname))
        bottom_sheet_menu.add_item(f"Highlight Yellow",lambda x ,y = tin: self.hl_task('yellow',fname))
        bottom_sheet_menu.add_item(f"Highlight Blue",lambda x ,y = tin: self.hl_task('#33adff',fname))
        bottom_sheet_menu.add_item(f"Highlight Green",lambda x ,y = tin: self.hl_task('#4dff4d',fname))
        bottom_sheet_menu.add_item(f"Highlight Red",lambda x ,y = tin: self.hl_task('#ff6666',fname))
        bottom_sheet_menu.add_item(f"Remove Highlight",lambda x ,y = tin: self.hl_task('white',fname))
        bottom_sheet_menu.add_item(f"Make it a Label",lambda x ,y = tin: self.label_task(fname))
        bottom_sheet_menu.open()
        

    def menu_callback(self, item):
        self.menu.dismiss()
        item = str(item)
        if item == 'colorall':
            self.color_all()

    def color_all(self):
        bottom_sheet_menu = MDListBottomSheet()
        bottom_sheet_menu.add_item(f"Yellow",lambda x : self.hl_task_all('yellow'))
        bottom_sheet_menu.add_item(f"Blue",lambda x : self.hl_task_all('#33adff'))
        bottom_sheet_menu.add_item(f"Green",lambda x : self.hl_task_all('#4dff4d'))
        bottom_sheet_menu.add_item(f"Red",lambda x : self.hl_task_all('#ff6666'))
        bottom_sheet_menu.add_item(f"Remove Color",lambda x : self.hl_task_all('white'))    
        bottom_sheet_menu.open()
        
    def menu_open(self, button):
        async def open(self):
            self.menu.caller = button
            self.menu.open()
        ak.start(open(self))
        
    def hl_task_all(self, col):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open('path.txt','r') as f:
            loc = f.read()
        toast(f'{loc}')
        
        lst = os.listdir(os.path.join(MP,loc))
        if 'color.color' in lst:
            lst.remove('color.color')   

        if 'desc.color' in lst:
            lst.remove('desc.color')   

        if 'time.color' in lst:
            lst.remove('time.color')   

        for file in lst:
            with open(os.path.join(MP,loc,file),'w') as f:
                f.write(str(col))
        self.enter()
        
    def label_task(self ,fname):
        ccls=LabelBox()
        self.label_dia = MDDialog(
        title="Label Description",
        type='custom',
        content_cls=ccls,
        width=Window.width,
        buttons=[
            MDFlatButton(text='Cancel',on_release=self.label_cancel),
            MDRaisedButton(text="Label It",on_release= lambda *args: self.mk_label(ccls,'Label',fname, *args)),
            ]
        )
        self.label_dia.open()
    
    def mk_label(self, content_cls, col, task, obj):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        task = task.replace('/','&')
        task = task.replace('\\','$')
        task = task.replace('"','@')
        task = task.replace("'",']')
        
        textfield = content_cls.ids.cname
        desc = textfield._get_text()
            
        with open('path.txt','r') as f:
            loc = f.read()
        with open(f'{MP}/{loc}/{task}.txt', 'w') as f:
            f.write(f'{col}\n{desc}')
        self.enter()
        self.label_dia.dismiss()
        
    def label_cancel(self, obj):
        self.label_dia.dismiss()
        
    def hl_task(self, col,task):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        task = task.replace('/','&')
        task = task.replace('\\','$')
        task = task.replace('"','@')
        task = task.replace("'",']')
        with open('path.txt','r') as f:
            loc = f.read()
        with open(f'{MP}/{loc}/{task}.txt', 'w') as f:
            f.write(f'{col}\n')
        self.enter()
        
    def rm_task(self, tin, task):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        task = task.replace('/','&')
        task = task.replace('\\','$')
        task = task.replace('"','@')
        task = task.replace("'",']')
        with open('path.txt','r') as f:
            loc = f.read()
        os.remove(f'{MP}/{loc}/{task}.txt')
        self.enter()
        
    def add_task(self):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        try:
            task = self.ids.taskt.text
            task = task.replace('/','&')
            task = task.replace('\\','$')
            task = task.replace('"','@')
            task = task.replace("'",']')
        except Exception as e:
            toast(f'{e}')
        try:
            with open('path.txt','r') as f:
                loc = f.read()
            if os.path.exists(f'{MP}/{loc}/{task}.txt'):
                toast('This Task is already there')
            else:
                with open(f'{MP}/{loc}/{task}.txt','w') as f:
                    f.write('white')
                toast('Task Added')
                self.enter()
                self.ids.taskt.text = ''
        except Exception as e:
            toast(f'{e} Try changing the task text')
    
    def back(self):
        try:
            if os.path.exists('path.txt'):
                os.remove('path.txt')
            else:
                pass
        except Exception as e:
            toast(f'{e}')
        self.manager.current = 'catp'
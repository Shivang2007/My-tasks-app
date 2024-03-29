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

class SuperLabelBox(BoxLayout):
    pass
    
class NotifyBox(BoxLayout):
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
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open('path.txt','r') as f:
            loc = f.read()
            
        menu_items = [
            {"viewclass": "OneLineListItem","text": f"Color All Tasks",'bg_color':'yellow',"height": dp(56),"on_release": lambda x=f"colorall": self.menu_callback(x)},
            {"viewclass": "OneLineListItem","text": f"Set Wallpaper",'bg_color':'#33adff',"height": dp(56),"on_release": self.set_wallpaper},
            {"viewclass": "OneLineListItem","text": f"Send Tasks Text",'bg_color':'#33adff',"height": dp(56),"on_release": self.send_tasks},
            {"viewclass": "OneLineListItem","text": f"Send Tasks Image",'bg_color':'#33adff',"height": dp(56),"on_release": self.send_image},
            {"viewclass": "OneLineListItem","text": f"Remove All Tasks",'bg_color':'red',"height": dp(56),"on_release": self.rm_all}
         ]
         
        if os.path.exists(f"{MP}/{loc}/super_label.color"):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Remove Super Label",'bg_color':'red',"height": dp(56),"on_release": lambda x=f"rsl": self.menu_callback(x)})
        elif not os.path.exists(f"{MP}/{loc}/super_label.color"):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Make Super Label",'bg_color':'red',"height": dp(56),"on_release": lambda x=f"msl": self.menu_callback(x)})
        else:
            pass
        
        if os.path.exists(f"texts/notify.txt"):
            with open(f"texts/notify.txt",'r') as f:
                np = f.read()
            if np == f"{MP}/{loc}":
                menu_items.append({"viewclass": "OneLineListItem","text": f"Remove Notify",'bg_color':'red',"height": dp(56),"on_release": lambda x=f"rnme": self.menu_callback(x)})
            else:
                menu_items.append({"viewclass": "OneLineListItem","text": f"Notify Me",'bg_color':'red',"height": dp(56),"on_release": lambda x=f"nme": self.menu_callback(x)})
        elif not os.path.exists(f"texts/notify.txt"):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Notify Me",'bg_color':'red',"height": dp(56),"on_release": lambda x=f"nme": self.menu_callback(x)})
        else:
            pass
            
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
            border_margin=dp(36),
            background_color='#33adff'
        )
        try:
            self.ids.flist.clear_widgets()
        except:
            pass
            
        try:
            lst = os.listdir(f'{MP}/{loc}/')
            self.ids.tbar.title = f'{loc}'
            if 'color.color' in lst:
                lst.remove('color.color')   
            if 'desc.color' in lst:
                lst.remove('desc.color')   
            if 'time.color' in lst:
                lst.remove('time.color')   
            if 'super_label.color' in lst:
                lst.remove('super_label.color')   
            
            if os.path.exists(f'{MP}/{loc}/super_label.color'):
                with open(f'{MP}/{loc}/super_label.color','r') as f:
                    sldata = f.read()
                sldata = sldata.split('&&&&')
                sll = sldata[0]
                sld = sldata[-1]
                self.card = MDCard(orientation='vertical',size_hint=(None,None),height="300",width=Window.width-40,md_bg_color="#4d94ff")
                self.card.add_widget(MDLabel(text=f'{sll}',font_style='H4',bold=True,underline=True,halign='center'))
                self.card.add_widget(MDLabel(text=f'{sld}',font_style='Body1',bold=True,halign='center'))             
                self.ids.flist.add_widget(self.card)            
            
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
    
    def rm_all(self):
        self.label_dia = MDDialog(
        title="Remove All Tasks ?",
        width=Window.width,
        text='Do you really want to remove all the tasks ?',
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.label_cancel),
            MDRaisedButton(text="Remove All",md_bg_color='red',on_release= lambda *args: self.remove_all_tasks(*args))])
        self.label_dia.open()  
    
    def remove_all_tasks(self, inst):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open('path.txt','r') as f:
            loc = f.read()        
        lst = os.listdir(os.path.join(MP,loc))
        if 'color.color' in lst:
            lst.remove('color.color')   
        if 'desc.color' in lst:
            lst.remove('desc.color')   
        if 'time.color' in lst:
            lst.remove('time.color')   
        if 'super_label.color' in lst:
            lst.remove('super_label.color')
        for file in lst:
            os.remove(f'{MP}/{loc}/{file}')
        toast('All The Tasks Removed')
        self.makehome()
        self.label_dia.dismiss()
        
    def send_image(self):
        file_path = '/storage/emulated/0/My Tasks/wallpaper.png'
        self.ids.flist.export_to_png(file_path)
        from kvdroid.tools import share_file
        share_file(file_path, title='Share', chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        
    def set_wallpaper(self):
        try:
            file_path = '/storage/emulated/0/Pictures/wallpaper.png'
            self.ids.flist.export_to_png(file_path)
            try:
                from kvdroid.tools import set_wallpaper
                set_wallpaper(file_path)
                toast('Done')
            except Exception as e:
                toast(f'Unable to set wallpaper {e}')
        except Exception as e:
            toast('Unable to set wallpaper')
                 
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
        bottom_sheet_menu.add_item(f"Notify It",lambda x ,y = tin: self.notify_it(fname)) 
        bottom_sheet_menu.open()
        
    def send_tasks(self):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open('path.txt','r') as f:
            loc = f.read()
        lst = os.listdir(f'{MP}/{loc}/')
        self.ids.tbar.title = f'{loc}'
        if 'color.color' in lst:
            lst.remove('color.color')   
        if 'desc.color' in lst:
            lst.remove('desc.color')   
        if 'time.color' in lst:
            lst.remove('time.color')   
        if 'super_label.color' in lst:
            lst.remove('super_label.color')
        text = f'{loc}\n\n'
        n = 0
        for file in lst:
            n = n + 1
            file = file.replace('.txt','')
            text = f"{text}{n}. {file}\n"
        try:
            from kvdroid.tools import share_text
            share_text(text, title="Share", chooser=False, app_package=None,call_playstore=False, error_msg="application unavailable")
        except:
            toast('Unable to send report')
        
    def notify_it(self, task):
        try:
            from plyer import notification
            msg = f"Have you completed the task - {task}"
            kwargs = {'title': 'Task Notification' , 'message':f'{msg}', 'ticker': 'ticker'}
            notification.notify(**kwargs)
        except:
            toast(f'{task} is left to be completed')   
        
    def menu_callback(self, item):
        self.menu.dismiss()
        item = str(item)
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open('path.txt','r') as f:
            loc = f.read()
            
        if item == 'colorall':
            self.color_all()
        elif item=='rsl':
            if os.path.exists(f"{MP}/{loc}/super_label.color"):
                os.remove(f"{MP}/{loc}/super_label.color")
                toast('Removed Super Label')
                self.enter()
            else:
                toast('No Super Label is there')
        elif item == 'msl':
            self.make_sl(f"{MP}/{loc}/super_label.color")
        
        elif item == 'rnme':
            os.remove(f"texts/notify.txt")
            self.enter()
        elif item == 'nme':
            self.notify_open(f"{MP}/{loc}")
        else:
            pass

    def notify_open(self, path):
        ccls=NotifyBox()
        self.label_dia = MDDialog(
        title="Notify On !",
        type='custom',
        content_cls=ccls,
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.label_cancel),
            MDRaisedButton(text="Notify Me",on_release= lambda *args: self.notify_on(ccls,path, *args))])
        self.label_dia.open()
    
    def notify_on(self, content_cls, path, obj):
        textfield = content_cls.ids.colourn
        col = textfield._get_text()
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open('path.txt','r') as f:
            loc = f.read()        
            
        alcol = ['blue','red','green','white','yellow']
        if col.lower() in alcol:
            with open(f"texts/notify.txt","w") as f:
                f.write(f'{MP}/{loc}')
                
            toast(f'You chose {col} colour')
            if col.lower() == 'yellow':
                col = col.lower()
            elif col.lower() == "blue":
                col = '#33adff'
            elif col.lower() == "red":
                col = '#ff6666'
            elif col.lower() == "green":
                col = '#4dff4d'
            elif col.lower() == "white":
                col = 'white'
            else:
                col = 'white'
            with open(f"texts/notify_color.txt","w") as f:
                f.write(f'{col}')
            self.label_cancel('Close')
            Snackbar(text='From now onwards you will be notified').open()
        else:
            toast('Type color name available in the app')
        
        
    def make_sl(self, path):
        ccls=SuperLabelBox()
        self.label_dia = MDDialog(
        title="Super Label",
        type='custom',
        content_cls=ccls,
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.label_cancel),
            MDRaisedButton(text="Label it",on_release= lambda *args: self.mk_super(ccls,path, *args))])
        self.label_dia.open()  
    
    def mk_super(self, content_cls, path, obj):
        textfield = content_cls.ids.cname
        chapter = textfield._get_text()
        textfield = content_cls.ids.descname
        cont = textfield._get_text()
        if len(chapter) == 0:
            toast('Write a label')
        elif len(cont) == 0:
            cont = 'Attention this is a super label'
        else:    
            with open(f"{path}",'w') as f:
                f.write(f"{chapter}&&&&{cont}")       
            toast('Super Label Made')
            self.enter()
            self.label_cancel('close')
        
        
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
        lst = os.listdir(os.path.join(MP,loc))
        if 'color.color' in lst:
            lst.remove('color.color')   
        if 'desc.color' in lst:
            lst.remove('desc.color')   
        if 'time.color' in lst:
            lst.remove('time.color')
        if 'super_label.color' in lst:
            lst.remove('super_label.color')   
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
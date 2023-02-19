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
    from plyer import notification
except:
    toast('Module import error')
import shutil
import logging


from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu


class NewFolderBox(BoxLayout):
    pass
    
    
class Categories(Screen):
    ww = Window.width
    Window.softinput_mode = "below_target"
    login = False
    
    def enter(self):
        if os.path.exists('show_safe.txt'):
            if os.path.exists('texts/logined.txt'):
                self.login = True
                with open('texts/logined.txt','r') as f:
                    un = f.read()
                path = f'Tasks/{un}'
                with open('texts/main_path.txt','w') as f:
                    f.write(f'{path}')
                self.makehome()
            else:
                self.login = False
                self.makehome()
        else:
            self.login = True
            self.makehome()        
          
    def makehome(self):
        self.notify()
        
        with open('texts/main_path.txt','r') as f:
            MP = f.read()          
        back_no = 0
        menu_items = [
            {"viewclass": "OneLineListItem","text": f"Exit","height": dp(56),"on_release": lambda x=f"exit": self.menu_callback(x)}
         ]
        if os.path.exists('show_time.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Hide Time","height": dp(56),"on_release": lambda x=f"notime": self.menu_callback(x)})
        elif not os.path.exists('show_time.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Show Time","height": dp(56),"on_release": lambda x=f"showtime": self.menu_callback(x)})
        else:
            pass  
            
        if os.path.exists('show_desc.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Hide Description","height": dp(56),"on_release": lambda x=f"nodesc": self.menu_callback(x)})
        elif not os.path.exists('show_desc.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Show Description","height": dp(56),"on_release": lambda x=f"showdesc": self.menu_callback(x)})
        else:
            pass
        
        if os.path.exists('texts/logined.txt') and os.path.exists('show_safe.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Logout","height": dp(56),"on_release": lambda x=f"logout": self.menu_callback(x)})
            menu_items.append({"viewclass": "OneLineListItem","text": f"Delete Account","height": dp(56),"on_release": lambda x=f"delall": self.menu_callback(x)})
        elif not os.path.exists('texts/logined.txt') and os.path.exists('show_safe.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Login","height": dp(56),"on_release": lambda x=f"login": self.menu_callback(x)})
        else:
            pass
        
        if os.path.exists('show_safe.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Public Tasks","height": dp(56),"on_release": lambda x=f"nosafe": self.menu_callback(x)})
        elif not os.path.exists('show_safe.txt'):
            menu_items.append({"viewclass": "OneLineListItem","text": f"Private Tasks","height": dp(56),"on_release": lambda x=f"showsafe": self.menu_callback(x)})
        else:
            pass
        
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=3,
            border_margin=dp(24),
            background_color='#33adff'
        )
            
        try:
            lst = os.listdir(f'{MP}')
            try:
                self.ids.flist.clear_widgets()
            except:
                pass
            
            if self.login == False:
                self.ids.flist.add_widget(OneLineListItem(text=f"Login First",bg_color='#ff6666'))
                
            elif lst == []:
                self.ids.flist.add_widget(TwoLineListItem(text=f"No Task Folder",secondary_text='create one to set tasks',bg_color='yellow',on_release=self.cr_fol))
            
            else:
                for task in lst:
                    if os.path.exists(f'{MP}/{task}/color.color'):
                        with open(f'{MP}/{task}/color.color','r') as f:
                            bg = f.read()
                    else:
                        bg = 'white'
                    if os.path.exists(f'{MP}/{task}/desc.color'):
                        with open(f'{MP}/{task}/desc.color','r') as f:
                            sec = f.read()
                    else:
                        sec = ' '
                    if os.path.exists(f'{MP}/{task}/time.color'):
                        with open(f'{MP}/{task}/time.color','r') as f:
                            tim = f.read()
                    else:
                        tim = 'No Data Available'
                           
                    if os.path.exists('show_time.txt') and os.path.exists('show_desc.txt'):
                        self.ids.flist.add_widget(ThreeLineListItem(text=f"{task}",secondary_text=f"{sec}",tertiary_text=f"{tim}",bg_color=bg,on_release=self.open))
                    elif os.path.exists('show_desc.txt'):
                        self.ids.flist.add_widget(TwoLineListItem(text=f"{task}",secondary_text=f"{sec}",bg_color=bg,on_release=self.open))                    
                    elif os.path.exists('show_time.txt'):
                        self.ids.flist.add_widget(TwoLineListItem(text=f"{task}",secondary_text=f"{tim}",bg_color=bg,on_release=self.open))                   
                    else:
                        self.ids.flist.add_widget(OneLineListItem(text=f"{task}",bg_color=bg,on_release=self.open))         
                        
        except Exception as e:
            toast(f'{e}')
    
    def notify(self):
        async def open_it():
            if os.path.exists(f"texts/notify.txt"):
                with open(f"texts/notify.txt","r") as f:
                    MP = f.read()
                with open(f"texts/notify_color.txt","r") as f:
                    col = f.read()
                
                lst = os.listdir(MP)
                if 'color.color' in lst:
                    lst.remove('color.color')   
                if 'desc.color' in lst:
                    lst.remove('desc.color')   
                if 'time.color' in lst:
                    lst.remove('time.color')
                if 'super_label.color' in lst:
                    lst.remove('super_label.color')
                mt = '/^&*()'
                for file in lst:
                    with open(f"{MP}/{file}","r") as f:
                        te = f.readlines()
                        te = te[0]
                        te = te.replace('\n','')
                        if col != te:
                            print(col)
                            mt = file
                            break
                        else:
                            pass
                        
                if mt == '/^&*()':
                    try:
                        msg = "Congratulations all tasks have been completed that you marked for notify"
                        kwargs = {'title': 'Tasks Notification' , 'message':f'{msg}', 'ticker': 'ticker'}
                        notification.notify(**kwargs)
                    except:
                        toast('Congratulations all tasks done')
                else:
                    task = mt.replace('.txt','')
                    task = task.replace('&','/')
                    task = task.replace('$','\\')
                    task = task.replace('@','"')
                    task = task.replace(']',"'")
                    try:
                        msg = f"Have you completed the task - {task}"
                        kwargs = {'title': 'Tasks Notification' , 'message':f'{msg}', 'ticker': 'ticker'}
                        notification.notify(**kwargs)
                    except:
                        toast(f'{task} is left to be completed')   
            else:
                pass
        ak.start(open_it())        
        
    def open(self, inst):
        tin = inst
        bottom_sheet_menu = MDListBottomSheet()
        fname = inst.text
        bottom_sheet_menu.add_item(f"Open Folder",lambda x ,y = tin: self.openfol(fname))
        bottom_sheet_menu.add_item(f"Delete Folder",lambda x ,y = tin: self.dele(fname))
        bottom_sheet_menu.add_item(f"Rename Folder",lambda x ,y = tin: self.open_rename(fname))
        bottom_sheet_menu.add_item(f"Highlight Folder",lambda x ,y = tin: self.hfol(fname))
        bottom_sheet_menu.add_item(f"Remove Highlight",lambda x ,y = tin: self.rmhl(fname))        
        bottom_sheet_menu.open()    
    
    def hfol(self, fname):
        self.cgh_dia = MDDialog(
        title="Highlight Folder",
        text='Select color of highlight button colours represent colours',
        width=Window.width,
        buttons=[
            MDRaisedButton(text="Yellow",md_bg_color='yellow',on_release= lambda *args: self.hlfol(fname,'yellow', *args)),
            MDRaisedButton(text="Blue",md_bg_color='#33adff',on_release= lambda *args: self.hlfol(fname,'#33adff', *args)),
            MDRaisedButton(text="Green",md_bg_color='#4dff4d',on_release= lambda *args: self.hlfol(fname,'#4dff4d', *args)),
            MDRaisedButton(text="Red",md_bg_color='#ff6666',on_release= lambda *args: self.hlfol(fname,'#ff6666', *args))
            ]
        )
        self.cgh_dia.open()
   
         
    def menu_callback(self, item):
        self.menu.dismiss()
        item = str(item)
        if item == 'exit':
            sys.exit()
        elif item == 'notime':
            os.remove('show_time.txt')
            self.enter()
        elif item == 'showtime':
            with open('show_time.txt','w') as f:
                f.write('Show')
            self.enter()
        elif item == 'nodesc':
            os.remove('show_desc.txt')
            self.enter()
        elif item == 'showdesc':
            with open('show_desc.txt','w') as f:
                f.write('Show')
            self.enter()
            
        elif item == 'nosafe':
            os.remove('show_safe.txt')
            MP = '/storage/emulated/0/My Tasks/Tasks'
            with open('texts/main_path.txt','w') as f:
                f.write(MP)
            Snackbar(text='Your tasks are now public').open()
            self.enter()
        elif item == 'showsafe':
            with open('show_safe.txt','w') as f:
                f.write('Show')
            MP = 'Tasks'
            with open('texts/main_path.txt','w') as f:
                f.write(MP)
            Snackbar(text='Your tasks are now private').open()
            self.enter()
        
        elif item =='login':
            self.manager.current = 'loginp'
        elif item =='logout':
            os.remove('texts/logined.txt')
            self.enter()
        elif item =='delall':
            self.dia = MDDialog(
            title="Delete Account",
            text="Are you sure you want to delete your account all your folders will be deleted.You can not undo this task. Your public folder will remain untouched",
            width=Window.width,
            buttons=[
                MDFlatButton(text="Cancel",on_release=self.close_dia),
                MDRaisedButton(text="Delete",md_bg_color='red',on_release=self.delete_account),
                ]
            )
            self.dia.open()
        else:
            pass
        
    def delete_account(self, obj):
        with open('texts/logined.txt','r') as f:
            un = f.read()
        path = f'Tasks/{un}'
        shutil.rmtree(path)
        os.remove(f'{path}.txt')
        with open('texts/main_path.txt','w') as f:
            f.write('Tasks/')
        os.remove('texts/logined.txt')
        self.enter()
        Snackbar(text='Account Deleted Succussfully',bg_color='red').open()
        self.dia.dismiss()
        
    def close_dia(self, obj):
        self.dia.dismiss()
        
    def menu_open(self, button):
        async def open(self):
            self.menu.caller = button
            self.menu.open()
        ak.start(open(self))
        
    def hlfol(self, fname, color, obj):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        with open(f'{MP}/{fname}/color.color','w') as f:
            f.write(color)
        self.cgh_dia.dismiss()
        self.enter()
        
    def rmhl(self, task):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        if os.path.exists(f'{MP}/{task}/color.color'):
            os.remove(f'{MP}/{task}/color.color')
            toast('Highlight Removed')
            self.enter()
        else:
            toast('Folder is not highlighted')
        
    def openfol(self, fname):
        with open('path.txt','w') as f:
            f.write(f'{fname}')
        self.manager.current = 'mainp'
                        
    def dele(self, fname):
        with open('texts/main_path.txt','r') as f:
            MP = f.read()
        shutil.rmtree(f'{MP}/{fname}')
        Snackbar(text=f"Folder {fname} deleted").open()
        self.enter()
            
    def cr_fol(self, obj):
        ccls=NewFolderBox()
        self.chap_dia = MDDialog(
        title="New Folder",
        type='custom',
        content_cls=ccls,
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchap),
            MDRaisedButton(text="Create",on_release= lambda *args: self.add_chapter(ccls,*args))])
        self.chap_dia.open()  
        
    def open_rename(self, fname):
        ccls=NewFolderBox()
        self.chap_dia = MDDialog(
        title="New Folder Name",
        type='custom',
        content_cls=ccls,
        width=Window.width-100,
        buttons=[
            MDFlatButton(text="Cancel",on_release=self.canchap),
            MDRaisedButton(text="Rename",on_release= lambda *args: self.rn_chapter(ccls,fname, *args))])
        self.chap_dia.open()  
    
    def rn_chapter(self, content_cls ,fname, inst):
        try:
            textfield = content_cls.ids.cname
            chapter = textfield._get_text()
            textfield = content_cls.ids.descname
            cont = textfield._get_text()
            with open('texts/main_path.txt','r') as f:
                MP = f.read()
            lst = os.listdir(f'{MP}')
            lst.remove(f"{fname}")
            if chapter in lst:
                toast('Folder is already there')
            elif '/' in chapter:
                toast('Special character used')
            elif cont == '':
                toast('Write something in description')
            else:
                with open(f'{MP}/{fname}/desc.color','w') as f:
                    f.write(str(cont))
                os.rename(f'{MP}/{fname}',f'{MP}/{chapter}')
                Snackbar(text=f"Folder {fname} Renamed to {chapter}").open()
                self.chap_dia.dismiss()
                self.enter()
        except:
            toast('An Error try changing folder name')
            
    
    def add_chapter(self, content_cls , inst):
        try:
            textfield = content_cls.ids.cname
            chapter = textfield._get_text()
            textfield = content_cls.ids.descname
            cont = textfield._get_text()
            with open('texts/main_path.txt','r') as f:
                MP = f.read()
            lst = os.listdir(f'{MP}')
            if chapter in lst:
                toast('Folder is already there')
            elif '/' in chapter:
                toast('Special character used')
            elif cont == '':
                toast('Write something in description')
            else:
                ct = time.localtime()
                dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
                tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
                dt = f'Date -{dt}          Time -{tt}'
                
                os.mkdir(f'{MP}/{chapter}')
                with open('path.txt','w') as f:
                    f.write(f'{chapter}')
                with open(f'{MP}/{chapter}/desc.color','w') as f:
                    f.write(str(cont))
                with open(f'{MP}/{chapter}/time.color','w') as f:
                    f.write(str(dt))
                    
                Snackbar(text=f"Folder {chapter} created").open()
                self.chap_dia.dismiss()
                self.manager.current = 'mainp'
        except:
            toast('An Error try changing folder name')
            
    def canchap(self, inst):
        self.chap_dia.dismiss()
        
    def exit(self):
        sys.exit()
        
        
class LoginPage(Screen):
    def login(self):
        pw = self.ids.pword.text
        un = self.ids.uname.text
        if '/' in un or '/' in pw:
            toast('Do not use slashes')
        elif len(un) == 0 or len(pw) == 0:
            toast('Write Something')
        else:
            path = f'Tasks/{un}'
            if os.path.exists(path):
                with open(f'Tasks/{un}.txt','r') as f:
                    realpw = f.read()
                if pw == realpw:
                    with open('texts/logined.txt','w') as f:
                        f.write(f'{un}')
                    with open('texts/main_path.txt','w') as f:
                        f.write(f'{path}')
                    
                    Snackbar(text='Logined Successfully').open()
                    self.manager.current = 'catp'
                else:
                    toast('Wrong Password')
            else:
                toast("Account Doesn't Exists Try Signup")
    
    def back(self):
        self.manager.current = 'catp'
    
    def sign(self):
        self.manager.current = 'signupp'
        
class SignupPage(Screen):
    def signup(self):
        pw = self.ids.pword.text
        un = self.ids.uname.text
        if '/' in un or '/' in pw:
            toast('Do not use slashes')
        elif un == '' or pw == '':
            toast('Write Something')
        else:
            path = f'Tasks/{un}'
            if os.path.exists(path):
                toast('Account Exists Try Login')
            else:
                os.makedirs(path)
                toast('Account Made')
                with open(f'Tasks/{un}.txt','w') as f:
                    f.write(f'{pw}')
                self.manager.current = 'loginp'
                Snackbar(text='Account Made Successfully').open()
    
    def back(self):
        self.manager.current = 'catp'
    
    def log(self):
        self.manager.current = 'loginp'
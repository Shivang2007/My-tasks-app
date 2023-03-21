from kivymd.app import MDApp
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

try:
    from android.permissions import request_permissions, Permission, check_permission
except Exception as e:
    toast('Error no 1 occured')
    
try:
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,Permission.SET_WALLPAPER])
except Exception as Argument:
    toast('Error no 2 occured')

files = ['/storage/emulated/0/Documents/My Tasks/Tasks/','Tasks/','texts/']

for file in files:
    try:
        if os.path.exists(f'{file}'):
            pass
        else:
            os.makedirs(f'{file}')
    except Exception as e:
        toast(f'{e}')
    
    
if not os.path.exists('show_safe.txt'):
    MP = '/storage/emulated/0/Documents/My Tasks/Tasks'
elif os.path.exists('texts/logined.txt'):
    with open('texts/main_path.txt','r') as f:
        MP = f.read()
else:
    MP = 'Tasks'

with open('texts/main_path.txt','w') as f:
    f.write(MP)

from category import Categories, LoginPage, SignupPage
Categories()
LoginPage()
SignupPage()

from bills import BillPage, BillListPage
BillPage()
BillListPage()

from tasks import TasksPage
TasksPage()

from os.path import join, dirname
        
class MainApp(MDApp):
    def build(self):   
        self.theme_cls.theme_style_switch_animation = True
        try:
            if os.path.exists('/storage/emulated/0/Documents/My Tasks/Tasks/theme.txt'):
                with open('/storage/emulated/0/Documents/My Tasks/Tasks/theme.txt','r') as f:
                    self.theme_cls.primary_palette = f.read()
            else:
                self.theme_cls.primary_palette = 'Blue'
        except:
            self.theme_cls.primary_palette = f"Blue"
            
        set_bars_colors(self.theme_cls.primary_color, self.theme_cls.primary_color,"Light")
        self.theme_cls.theme_style = "Light"
        
        Builder.load_file('dbox.kv')
        
        self.sm=ScreenManager()
        if os.path.exists('path.txt'):
            self.sm.add_widget(TasksPage(name='mainp')),
            self.sm.add_widget(Categories(name='catp'))           
        else:
            self.sm.add_widget(Categories(name='catp')),
            self.sm.add_widget(TasksPage(name='mainp'))
            
        self.sm.add_widget(LoginPage(name='loginp'))         
        self.sm.add_widget(SignupPage(name='signupp'))
        self.sm.add_widget(BillListPage(name='billlistp'))
        self.sm.add_widget(BillPage(name='billp'))
        
        return self.sm
        
MainApp().run()
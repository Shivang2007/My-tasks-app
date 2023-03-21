##############################
# KIVY MAIN APP CLASSES
##############################
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

##############################
# KIVYMD WIDGETS 
##############################
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton,MDFlatButton,MDRaisedButton,MDRectangleFlatIconButton
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.properties import DictProperty
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem,TwoLineListItem,ThreeLineListItem
from kivymd.uix.bottomsheet import MDListBottomSheet

##############################
# MODULES
##############################
import os
from os import path
import random
import sys
import json
import time
import logging

def get_data(path):
    try:
        if os.path.exists(path):        
            with open(path, 'r') as openfile:
                MData = json.load(openfile)
        else:
            with open(path,"w") as f:
                data = {}
                data = json.dumps(data, indent=4)
                f.write(data)
            with open(path, 'r') as openfile:
                MData = json.load(openfile)              
        return MData
    except Exception as e:
        print(e)
        return {}
        
def write_data(path,data):
    try:
        with open(path,"w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
    except Exception as e:
        return e

BillPath = '/storage/emulated/0/Documents/My Tasks/bill.json'
Red = '#ff6666'
Green = '#4dff4d'
bg = '#33adff'

class MakeListBox(BoxLayout):
    pass
class MakeNewBillBox(BoxLayout):
    pass
    
class BillListPage(Screen):
    def enter(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        try:
            self.ids.flist.clear_widgets()
        except:
            pass
        data = get_data(BillPath)
        if data == {}:
            self.ids.flist.add_widget(TwoLineListItem(text=f"No Bill Is There",secondary_text='Create one now',bg_color=Red,on_release=self.cr_fol))
        else:
            for bill in data:
                desc = data[bill]['desc']
                date = data[bill]['date']
                if os.path.exists('show_time.txt') and os.path.exists('show_desc.txt'):
                    self.ids.flist.add_widget(ThreeLineListItem(text=f"{bill}",secondary_text=f"{desc}",tertiary_text=f"{date}",bg_color=bg,on_release=self.open))
                elif os.path.exists('show_desc.txt'):
                    self.ids.flist.add_widget(TwoLineListItem(text=f"{bill}",secondary_text=f"{desc}",bg_color=bg,on_release=self.open))                    
                elif os.path.exists('show_time.txt'):
                    self.ids.flist.add_widget(TwoLineListItem(text=f"{bill}",secondary_text=f"{date}",bg_color=bg,on_release=self.open))                   
                else:
                    self.ids.flist.add_widget(OneLineListItem(text=f"{bill}",bg_color=bg,on_release=self.open))         
                        
    def open(self, inst):
        bottom_sheet_menu = MDListBottomSheet()
        fname = inst.text
        bottom_sheet_menu.add_item(f"Open Bill",lambda x : self.open_bill(fname))
        bottom_sheet_menu.add_item(f"Delete Bill",lambda x : self.dele(fname))
        bottom_sheet_menu.add_item(f"Rename Bill",lambda x : self.open_rename(fname))  
        bottom_sheet_menu.open()
        
    def open_bill(self, bill):
        with open('texts/bill.txt', 'w') as f:
            f.write(str(bill))
        self.manager.current = 'billp'
        
    def dele(self, bill):
        data = get_data(BillPath)
        if bill in data:
            data.pop(bill)
        write_data(BillPath,data)
        Snackbar(text=f"Bill Named {bill} Deleted").open()
        self.enter()
        
    def open_rename(self, bill):
        ccls = MakeNewBillBox()
        self.add_dia = MDDialog(
            title="New Bill",
            type='custom',
            width=Window.width,
            content_cls=ccls,
            buttons=[
                MDFlatButton(text="Cancel",on_release= self.cancel_dia),
                MDRaisedButton(text="Create",on_release= lambda *args: self.rename_final(ccls,bill,*args))
                ]
            )
        self.add_dia.open()
        
    def rename_final(self, content_cls , bill, obj):
        textfield = content_cls.ids.desc
        desc = textfield._get_text()
        textfield = content_cls.ids.nam
        nam = textfield._get_text()
        data = get_data(BillPath)
        itm = data[bill]['items']
        dt = data[bill]['date']
        data.pop(bill)
        data[str(nam)] = {'desc':desc,'date':dt,'items':itm}
        write_data(BillPath, data)
        Snackbar(text=f'{bill} Renamed to {nam}').open()
        self.enter()
        self.add_dia.dismiss()
        
    def cr_fol(self, inst):
        ccls = MakeNewBillBox()
        self.add_dia = MDDialog(
            title="New Bill",
            type='custom',
            width=Window.width,
            content_cls=ccls,
            buttons=[
                MDFlatButton(text="Cancel",on_release= self.cancel_dia),
                MDRaisedButton(text="Create",on_release= lambda *args: self.add_final(ccls,*args))
                ]
            )
        self.add_dia.open()
                
    def add_final(self, content_cls ,obj):
        textfield = content_cls.ids.desc
        desc = textfield._get_text()
        textfield = content_cls.ids.nam
        nam = textfield._get_text()
        data = get_data(BillPath)
        if nam in data:
            toast(f'Bill named {nam} is already there')
        else:
            ct = time.localtime()
            dt = f'{ct[2]}/{ct[1]}/{ct[0]}'
            tt = f'{ct[3]}:{ct[4]}:{ct[5]}'
            dt = f'Date -{dt}          Time -{tt}'
            data[nam] = {'desc':desc,'date':dt,'items':{}}
            write_data(BillPath,data)
            Snackbar(text=f'New Bill Named {nam} Created',bg_color='blue').open()
            self.add_dia.dismiss()
            self.enter()
        
    def cancel_dia(self, item):
        self.add_dia.dismiss()
        
    def goto(self, where):
        self.manager.current = where   
        
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True  
    
class BillPage(Screen):
    def enter(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        
        with open('texts/bill.txt','r') as f:
            bill = f.read()
        self.ids.tbar.title = bill
        try:
            self.ids.flist.clear_widgets()
        except:
            pass
        data = get_data(BillPath)
        if data[bill]['items'] == {}:
            self.ids.flist.add_widget(TwoLineListItem(text=f"No item Is There",secondary_text='add some items now',bg_color=Red,on_release=self.add_item_indir))
        else:
            for item in data[bill]['items']:
                if data[bill]['items'][item]['status'] == 'Left':
                    quan = data[bill]['items'][item]['quantity'] 
                    self.ids.flist.add_widget(OneLineListItem(text=f"{quan} - {item}",bg_color=Red,on_release=lambda x : self.open(item)))
                else:
                    quan = data[bill]['items'][item]['quantity'] 
                    self.ids.flist.add_widget(OneLineListItem(text=f"{quan} - {item}",bg_color=Green,on_release=lambda x : self.open(item)))
    
    def add_item_indir(self, inst):
        self.add_item()
        
    def open(self, fname):
        bottom_sheet_menu = MDListBottomSheet()
        bottom_sheet_menu.add_item(f"Update Status",lambda x : self.update(fname))
        bottom_sheet_menu.add_item(f"Delete Item",lambda x : self.dele(fname))
        bottom_sheet_menu.open()
    
    def dele(self, item):
        with open('texts/bill.txt','r') as f:
            bill = f.read()
        data = get_data(BillPath)
        if item in data[bill]['items']:
            data[bill]['items'].pop(item)
        else:
            pass
        write_data(BillPath, data)
        self.enter()
        toast('Item Deleted')
        
    def update(self, item):
        with open('texts/bill.txt','r') as f:
            bill = f.read()
        data = get_data(BillPath)
        status = data[bill]['items'][item]['status']
        if status == 'Left':
            data[bill]['items'][item]['status'] = 'Done'
        else:
            data[bill]['items'][item]['status'] = 'Left'
        write_data(BillPath, data)
        self.enter()
        toast('Item Updated')
        
    def add_item(self):
        ccls = MakeListBox()
        self.add_dia = MDDialog(
            title="Add Item",
            type='custom',
            width=Window.width,
            content_cls=ccls,
            buttons=[
                MDFlatButton(text="Cancel",on_release= self.cancel_dia),
                MDRaisedButton(text="Add",on_release= lambda *args: self.add_final(ccls,*args))
                ]
            )
        self.add_dia.open()
                
    def add_final(self, content_cls ,obj):
        try:
            textfield = content_cls.ids.item_name
            item_name = textfield._get_text()
            textfield = content_cls.ids.quan
            quan = textfield._get_text()
            with open('texts/bill.txt','r') as f:
                bill = f.read()
            data= get_data(BillPath)
            if item_name in data:
                data[bill]['items'][str(item_name)] = {'quantity':str(quan),'status':'Left'}
                toast('Data changed')
            else:
                data[bill]['items'][str(item_name)] = {'quantity':str(quan),'status':'Left'}       
                Snackbar(text=f'{quan} - {item_name} Added To Bill',bg_color='blue').open()
            write_data(BillPath, data)
            self.enter()
            self.add_dia.dismiss()
        except:
            toast('Oops an error occured')
        
    def cancel_dia(self, item):
        self.add_dia.dismiss()
        
    def goto(self, where):
        self.manager.current = where 
    
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'billlistp'
            return True 
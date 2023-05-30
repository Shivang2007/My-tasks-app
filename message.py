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



class ViewMessage(Screen):
    def enter(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        
        try:
            from kvdroid.tools.sms import get_all_sms
            from android.permissions import Permission, request_permissions  # NOQA
            # remember to add READ_SMS to your buildozer `android.permissions`
            
            sms = get_all_sms() # returns a tuple of message count and messages
            
            with open('/storage/emulated/0/test.txt','w') as f:
                f.write(str(sms))
            
        except Exception as e:
            toast(str(e))
        
    def goto(self, where):
        self.manager.current = where   
        
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True  

class ImpMessage(Screen):
    def enter(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)  
        
    
    def goto(self, where):
        self.manager.current = where   
        
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'mainp'
            return True  
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, ColorProperty
from kivy.animation import Animation
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from datetime import datetime
from kivymd.toast import toast
from kivymd.uix.list import TwoLineListItem, OneLineIconListItem, TwoLineAvatarListItem, ThreeLineAvatarListItem, ImageLeftWidget, IconLeftWidget
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.selectioncontrol import MDCheckbox
import webbrowser
import requests
import threading
import os
from concurrent.futures import ThreadPoolExecutor

# Global thread pool for better performance
thread_pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="app_worker")

# Function to show smaller toast notifications
def toast(message):
    from kivymd.toast import toast as original_toast
    # Create the original toast
    original_toast(message)

# Helper function for smaller toasts
def small_toast(message):
    from kivymd.toast import toast as original_toast
    from kivy.clock import Clock
    # Create the original toast
    original_toast(message)
    # Make it smaller with multiple attempts
    def make_smaller(dt):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and app.root:
            # Try to find and modify the toast
            modified = False
            for child in app.root.children:
                if hasattr(child, 'text') and hasattr(child, 'md_bg_color'):
                    # Check if this is our toast by matching text
                    if hasattr(child, 'text') and child.text == message:
                        child.size_hint_x = None
                        child.width = "100dp"
                        child.height = "25dp"
                        child.pos_hint = {'center_x': 0.5, 'center_y': 0.01}
                        modified = True
                        break
            # If not found, try again
            if not modified:
                Clock.schedule_once(make_smaller, 0.1)
    Clock.schedule_once(make_smaller, 0.1)
    

# Optional: set a default window size for desktop testing
Window.size = (360, 640)
Window.clearcolor = (1, 1, 1, 1)

KV = '''
ScreenManager:
    LoginScreen:
    DashboardScreen:
    EditProfileScreen:
    ActionsOnLoansScreen:
    LoanActionsSearchResultScreen:
    CircularsScreen:
    ConsolidationScreen:
    FinacleHelpScreen:
    AddFinacleHelpScreen:
    BranchListScreen:
    StaffListScreen:
    StaffDetailScreen:
    ErrorReportScreen:
    ErrorResolveScreen:
    MessagesScreen:
    UrgentScreen:
    PasswordScreen:
    DocShareScreen:

<LoginScreen>:
    name: 'login'
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        # FitImage:
        #     source: "header_bg.jpg"
        #     size_hint_y: .35
        #     pos_hint: {"top": 1}
        MDCard:
            size_hint: None, None
            size: "210dp", "123dp"
            pos_hint: {"center_x": .5, "center_y": .74}
            elevation: 0
            radius: [14,]
            md_bg_color: 1, 1, 1, 1
            padding: "4dp"
            canvas.before:
                Color:
                    rgba: 0.82, 0.84, 0.87, 1
                Line:
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 14)
                    width: 1
            Image:
                source: "backend/static/avatars/kerala_bank_login_logo.png"
                keep_ratio: True
                mipmap: True
                fit_mode: "contain"
        MDCard:
            size_hint: .85, .34
            pos_hint: {"center_x": .5, "center_y": .29}
            elevation: 2
            padding: "20dp"
            spacing: "15dp"
            orientation: "vertical"
            radius: [20,]
            MDTextField:
                id: emp_id
                hint_text: "Employee ID"
                mode: "rectangle"
            MDTextField:
                id: password
                hint_text: "Password"
                password: True
                mode: "rectangle"
            MDRaisedButton:
                text: "SIGN IN"
                size_hint_x: 1
                md_bg_color: 0.12, 0.23, 0.47, 1
                on_release: root.do_login()

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        MDTopAppBar:
            title: "Kerala Bank Portal"
            md_bg_color: 0.12, 0.23, 0.47, 1
            elevation: 0
            right_action_items: [["logout", lambda x: app.logout()]]

        TabbedPanel:
            id: tab_manager
            do_default_tab: False
            tab_width: 118
            background_color: 1, 1, 1, 1
            canvas.after:
                Color:
                    rgba: 1, 1, 1, 1
                Line:
                    points: self.x + self.width / 3, self.top - 42, self.x + self.width / 3, self.top
                    width: 1
                Line:
                    points: self.x + (self.width * 2 / 3), self.top - 42, self.x + (self.width * 2 / 3), self.top
                    width: 1
            on_current_tab: root.on_tab_switch(*args)
            
            TabbedPanelItem:
                text: "Dashboard"
                background_normal: ""
                background_down: ""
                background_color: 0.37, 0.16, 0.12, 1
                MDScrollView:
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: ["15dp", "6dp", "15dp", "15dp"]
                        spacing: "8dp"
                        adaptive_height: True

                        MDBoxLayout:
                            size_hint_y: None
                            height: "34dp"
                            Widget:
                            MDRaisedButton:
                                text: "Download Report"
                                size_hint_y: None
                                height: "30dp"
                                elevation: 0
                                md_bg_color: 0.37, 0.16, 0.12, 1
                                on_release: root.download_branch_report()
                            Widget:

                        Widget:
                            size_hint_y: None
                            height: "2dp"

                        MDCard:
                            size_hint_y: None
                            height: "100dp"
                            radius: 12
                            elevation: 0
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            canvas.before:
                                Color:
                                    rgba: 0.85, 0.87, 0.9, 1
                                Line:
                                    rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                    width: 1
                            MDBoxLayout:
                                spacing: "15dp"
                                MDCard:
                                    size_hint: None, None
                                    size: "70dp", "70dp"
                                    radius: 35
                                    pos_hint: {"center_y": .5}
                                    FitImage:
                                        id: dash_avatar
                                        source: "avatar.png"
                                        radius: 35
                                MDBoxLayout:
                                    orientation: "vertical"
                                    pos_hint: {"center_y": .5}
                                    MDLabel:
                                        id: welcome_name
                                        text: "Employee Name"
                                        font_style: "Subtitle1"
                                        bold: True
                                    MDLabel:
                                        id: welcome_id
                                        text: "ID: --"
                                        font_style: "Caption"
                                        theme_text_color: "Secondary"

                        MDGridLayout:
                            cols: 3
                            size_hint_x: None
                            width: self.minimum_width
                            pos_hint: {"center_x": .5}
                            spacing: "12dp"
                            adaptive_height: True

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'error_report'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "alert-circle"
                                        halign: "center"
                                        font_size: "24sp"
                                        text_color: 0.12, 0.23, 0.47, 1
                                        theme_text_color: "Custom"
                                    MDLabel:
                                        text: "Report"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'doc_share'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "file-upload"
                                        halign: "center"
                                        font_size: "24sp"
                                        text_color: 0.12, 0.23, 0.47, 1
                                        theme_text_color: "Custom"
                                    MDLabel:
                                        text: "Docs"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'branch_list'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "card-account-details"
                                        halign: "center"
                                        font_size: "24sp"
                                    MDLabel:
                                        text: "Directory"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'messages'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "chat-processing"
                                        halign: "center"
                                        font_size: "24sp"
                                        theme_text_color: "Custom"
                                        text_color: 0.12, 0.23, 0.47, 1
                                    MDLabel:
                                        text: "Inbox"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'urgent'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "fire"
                                        halign: "center"
                                        font_size: "24sp"
                                        theme_text_color: "Error"
                                    MDLabel:
                                        text: "Urgent"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'password'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "lock-reset"
                                        halign: "center"
                                        font_size: "24sp"
                                    MDLabel:
                                        text: "Security"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'circulars'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "file-document-outline"
                                        halign: "center"
                                        font_size: "24sp"
                                        theme_text_color: "Custom"
                                        text_color: 0.12, 0.23, 0.47, 1
                                    MDLabel:
                                        text: "Circulars"
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'consolidation'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "link-variant"
                                        halign: "center"
                                        font_size: "24sp"
                                        theme_text_color: "Custom"
                                        text_color: 0.12, 0.23, 0.47, 1
                                    MDLabel:
                                        text: "Consolid."
                                        halign: "center"
                                        font_style: "Caption"

                            MDCard:
                                size_hint: None, None
                                size: "95dp", "95dp"
                                radius: 12
                                elevation: 0
                                md_bg_color: 1, 1, 1, 1
                                on_release: app.root.current = 'finacle_help'
                                canvas.before:
                                    Color:
                                        rgba: 0.85, 0.87, 0.9, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                        width: 1
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "book-open-page-variant"
                                        halign: "center"
                                        font_size: "24sp"
                                        theme_text_color: "Custom"
                                        text_color: 0.12, 0.23, 0.47, 1
                                    MDLabel:
                                        text: "Finacle Help"
                                        halign: "center"
                                        font_style: "Caption"

                        MDCard:
                            id: resolve_card
                            size_hint_y: None
                            height: "0dp"
                            radius: 12
                            elevation: 0
                            opacity: 0
                            disabled: True
                            md_bg_color: 1, 1, 1, 1
                            on_release: app.root.current = 'error_resolve'
                            canvas.before:
                                Color:
                                    rgba: 0.85, 0.87, 0.9, 1
                                Line:
                                    rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                    width: 1
                            MDBoxLayout:
                                orientation: "horizontal"
                                padding: "15dp"
                                spacing: "15dp"
                                MDIcon:
                                    icon: "message-text-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0.12, 0.23, 0.47, 1
                                    pos_hint: {"center_y": .5}
                                MDLabel:
                                    text: 'Error/Message Resolving'
                                    font_style: 'Body1'
                                    pos_hint: {"center_y": .5}
                                MDIcon:
                                    icon: "chevron-right"
                                    pos_hint: {"center_y": .5}

                        MDCard:
                            size_hint_y: None
                            height: "60dp"
                            radius: 12
                            elevation: 0
                            md_bg_color: 1, 1, 1, 1
                            on_release: app.root.current = 'edit_profile'
                            canvas.before:
                                Color:
                                    rgba: 0.85, 0.87, 0.9, 1
                                Line:
                                    rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                    width: 1
                            MDBoxLayout:
                                orientation: "horizontal"
                                padding: "15dp"
                                spacing: "15dp"
                                MDIcon:
                                    icon: "account-edit-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0.12, 0.23, 0.47, 1
                                    pos_hint: {"center_y": .5}
                                MDLabel:
                                    text: "Edit My Profile & Details"
                                    font_style: "Body1"
                                    pos_hint: {"center_y": .5}
                                MDIcon:
                                    icon: "chevron-right"
                                    pos_hint: {"center_y": .5}

                        MDCard:
                            size_hint_y: None
                            height: "60dp"
                            radius: 12
                            elevation: 0
                            md_bg_color: 1, 1, 1, 1
                            on_release: app.root.current = 'actions_loans'
                            canvas.before:
                                Color:
                                    rgba: 0.85, 0.87, 0.9, 1
                                Line:
                                    rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                    width: 1
                            MDBoxLayout:
                                orientation: "horizontal"
                                padding: "15dp"
                                spacing: "15dp"
                                MDIcon:
                                    icon: "clipboard-list-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0.12, 0.23, 0.47, 1
                                    pos_hint: {"center_y": .5}
                                MDLabel:
                                    text: "Actions On Loans"
                                    font_style: "Body1"
                                    pos_hint: {"center_y": .5}
                                MDIcon:
                                    icon: "chevron-right"
                                    pos_hint: {"center_y": .5}

            TabbedPanelItem:
                text: "SMA"
                background_normal: ""
                background_down: ""
                background_color: 0.37, 0.16, 0.12, 1
                MDScrollView:
                    id: sma_scroll
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: ["15dp", "6dp", "15dp", "15dp"]
                        spacing: "0dp"
                        adaptive_height: True

                        MDBoxLayout:
                            size_hint_y: None
                            height: "34dp"
                            Widget:
                            MDRaisedButton:
                                text: "Download Report"
                                size_hint_y: None
                                height: "30dp"
                                elevation: 0
                                md_bg_color: 0.37, 0.16, 0.12, 1
                                on_release: root.download_branch_report()
                            Widget:

                        Widget:
                            size_hint_y: None
                            height: "10dp"

                        MDBoxLayout:
                            size_hint_y: None
                            height: "48dp"
                            spacing: "4dp"
                            MDRaisedButton:
                                text: "SMA 0"
                                size_hint_x: 1
                                font_size: "12sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_sma_panel('sma0')
                            MDRaisedButton:
                                text: "SMA 1"
                                size_hint_x: 1
                                font_size: "12sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_sma_panel('sma1')
                            MDRaisedButton:
                                text: "SMA 2"
                                size_hint_x: 1
                                font_size: "12sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_sma_panel('sma2')

                        Widget:
                            size_hint_y: None
                            height: "12dp"

                        MDCard:
                            id: sma0_box
                            size_hint_y: None
                            height: "760dp"
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "SMA 0"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma0_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma0_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma0_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma0_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: sma0_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: sma0_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('sma0')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma0_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma0_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma0_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma0_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


                        MDCard:
                            id: sma1_box
                            size_hint_y: None
                            height: "0dp"
                            opacity: 0
                            disabled: True
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "SMA 1"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma1_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma1_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma1_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma1_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: sma1_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: sma1_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('sma1')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma1_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma1_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma1_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma1_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


                        MDCard:
                            id: sma2_box
                            size_hint_y: None
                            height: "0dp"
                            opacity: 0
                            disabled: True
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "SMA 2"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma2_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma2_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma2_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma2_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: sma2_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: sma2_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('sma2')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma2_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma2_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: sma2_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: sma2_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


            TabbedPanelItem:
                text: "NPA"
                background_normal: ""
                background_down: ""
                background_color: 0.37, 0.16, 0.12, 1
                MDScrollView:
                    id: npa_scroll
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: ["15dp", "6dp", "15dp", "15dp"]
                        spacing: "0dp"
                        adaptive_height: True

                        MDBoxLayout:
                            size_hint_y: None
                            height: "34dp"
                            Widget:
                            MDRaisedButton:
                                text: "Download Report"
                                size_hint_y: None
                                height: "30dp"
                                elevation: 0
                                md_bg_color: 0.37, 0.16, 0.12, 1
                                on_release: root.download_branch_report()
                            Widget:

                        Widget:
                            size_hint_y: None
                            height: "10dp"

                        MDBoxLayout:
                            size_hint_y: None
                            height: "48dp"
                            spacing: "4dp"
                            MDRaisedButton:
                                text: "NPA1"
                                size_hint_x: 1
                                font_size: "11sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_npa_panel('npa1')
                            MDRaisedButton:
                                text: "NPA2"
                                size_hint_x: 1
                                font_size: "11sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_npa_panel('npa2')
                            MDRaisedButton:
                                text: "D1"
                                size_hint_x: 1
                                font_size: "11sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_npa_panel('d1')
                            MDRaisedButton:
                                text: "D2"
                                size_hint_x: 1
                                font_size: "11sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_npa_panel('d2')
                            MDRaisedButton:
                                text: "D3"
                                size_hint_x: 1
                                font_size: "11sp"
                                elevation: 0
                                md_bg_color: 1, 1, 1, 0
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                canvas.before:
                                    Color:
                                        rgba: 0, 0, 0, 1
                                    Line:
                                        rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                                        width: 0.5
                                on_release: root.show_npa_panel('d3')

                        Widget:
                            size_hint_y: None
                            height: "12dp"

                        MDCard:
                            id: npa1_box
                            size_hint_y: None
                            height: "760dp"
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "NPA1"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: npa1_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa1_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: npa1_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa1_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: npa1_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: npa1_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('npa1')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: npa1_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa1_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: npa1_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa1_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


                        MDCard:
                            id: npa2_box
                            size_hint_y: None
                            height: "0dp"
                            opacity: 0
                            disabled: True
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "NPA2"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: npa2_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa2_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: npa2_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa2_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: npa2_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: npa2_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('npa2')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: npa2_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa2_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: npa2_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: npa2_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


                        MDCard:
                            id: d1_box
                            size_hint_y: None
                            height: "0dp"
                            opacity: 0
                            disabled: True
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "D1"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDLabel:
                                            id: d1_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d1_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d1_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d1_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: d1_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: d1_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('d1')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d1_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d1_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d1_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d1_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


                        MDCard:
                            id: d2_box
                            size_hint_y: None
                            height: "0dp"
                            opacity: 0
                            disabled: True
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "D2"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d2_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d2_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d2_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d2_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: d2_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: d2_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('d2')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d2_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d2_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d2_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d2_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"


                        MDCard:
                            id: d3_box
                            size_hint_y: None
                            height: "0dp"
                            opacity: 0
                            disabled: True
                            radius: 12
                            elevation: 0.4
                            padding: "10dp"
                            md_bg_color: 1, 1, 1, 1
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "12dp"
                                adaptive_height: True
                                MDLabel:
                                    text: "D3"
                                    font_style: "H6"
                                    bold: True
                                    halign: "center"
                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Opening Balance"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d3_opening_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d3_opening_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Previous day collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d3_prev_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d3_prev_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "220dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: ["10dp", "14dp", "10dp", "10dp"]
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Today's collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "26dp"
                                        MDTextField:
                                            id: d3_today_num
                                            hint_text: "Number"
                                            text: "0"
                                        MDTextField:
                                            id: d3_today_amt
                                            hint_text: "Amount"
                                            text: "0"
                                        MDRaisedButton:
                                            text: "Submit"
                                            size_hint_y: None
                                            height: "40dp"
                                            md_bg_color: 0.12, 0.23, 0.47, 1
                                            on_release: root.submit_collection('d3')

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Total collection"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d3_total_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d3_total_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

                                Widget:
                                    size_hint_y: None
                                    height: "4dp"

                                MDCard:
                                    size_hint_y: None
                                    height: "92dp"
                                    radius: 12
                                    elevation: 0
                                    md_bg_color: 0.97, 0.97, 0.97, 1
                                    canvas.before:
                                        Color:
                                            rgba: 0.97, 0.97, 0.97, 1
                                        RoundedRectangle:
                                            pos: self.pos
                                            size: self.size
                                            radius: [12, 12, 12, 12]
                                    padding: "10dp"
                                    MDBoxLayout:
                                        orientation: "vertical"
                                        spacing: "8dp"
                                        adaptive_height: True
                                        MDLabel:
                                            text: "Balance to be collected"
                                            font_style: "Subtitle1"
                                            bold: True
                                            size_hint_y: None
                                            height: "24dp"
                                        MDLabel:
                                            id: d3_balance_num
                                            text: "Number: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"
                                        MDLabel:
                                            id: d3_balance_amt
                                            text: "Amount: --"
                                            font_style: "Body2"
                                            size_hint_y: None
                                            height: "20dp"

<ChatBubble>:
    orientation: "vertical"
    size_hint_x: .8
    adaptive_height: True
    padding: "10dp"
    margin: "5dp"
    radius: [15, 15, 15, 15]
    md_bg_color: root.bg_color
    elevation: 0
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 15)
            width: 0.6

    MDLabel:
        text: root.sender_info
        font_style: "Caption"
        theme_text_color: "Secondary"
        adaptive_height: True
        font_size: "10sp"

    MDLabel:
        text: root.message_text
        font_style: "Body1"
        theme_text_color: "Primary"
        adaptive_height: True
        bold: True

    MDLabel:
        text: root.timestamp
        font_style: "Caption"
        theme_text_color: "Hint"
        halign: "right"
        adaptive_height: True
        font_size: "9sp"

<MessagesScreen>:
    name: 'messages'
    on_enter: root.load_messages()
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1  # Light grey background like WhatsApp

        MDTopAppBar:
            title: "Employee Group Chat"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_messages()]]

        MDScrollView:
            id: chat_scroll
            do_scroll_x: False
            MDBoxLayout:
                id: chat_list
                orientation: 'vertical'
                adaptive_height: True  # CRITICAL: If this is False, screen stays white
                padding: ["14dp", "12dp", "14dp", "12dp"]
                spacing: "12dp"

        # Input Bar
        MDBoxLayout:
            adaptive_height: True
            padding: "8dp"
            spacing: "8dp"
            md_bg_color: 1, 1, 1, 1

            MDTextField:
                id: msg_input
                hint_text: "Type your message..."
                mode: "round"

            MDIconButton:
                icon: "send"
                on_release: root.send_message()

<EditProfileScreen>:
    name: 'edit_profile'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1
        MDTopAppBar:
            title: "Update Profile"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "15dp"
                adaptive_height: True
                
                # Corrected MDCard Indentation
                MDCard:
                    size_hint: None, None
                    size: "120dp", "120dp"
                    radius: 60
                    pos_hint: {"center_x": .5}
                    on_release: root.open_file_manager()
                    FitImage:
                        id: edit_avatar
                        source: "avatar.png"
                        radius: 60

                MDTextField:
                    id: new_id
                    hint_text: "Employee ID"
                    text: "Loading..." 
                    mode: "rectangle"
                    fill_color_normal: 0.9, 0.9, 0.9, 1 
                    disabled: True

                MDTextField:
                    id: new_name
                    hint_text: "Update Name"
                    mode: "rectangle"

                MDTextField:
                    id: new_desig
                    hint_text: "Update Designation"
                    mode: "rectangle"

                MDTextField:
                    id: new_phone
                    hint_text: "Contact Number"
                    mode: "rectangle"

                MDTextField:
                    id: new_branch
                    hint_text: "Branch ID"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "SAVE UPDATES"
                    size_hint_x: 1
                    md_bg_color: 0.12, 0.23, 0.47, 1
                    on_release: root.save_profile()

<ActionsOnLoansScreen>:
    name: 'actions_loans'
    on_pre_enter: root.on_pre_enter()
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1
        MDTopAppBar:
            title: "Actions On Loans"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "14dp"
                adaptive_height: True

                MDBoxLayout:
                    size_hint_y: None
                    height: "44dp"
                    spacing: "6dp"
                    MDRaisedButton:
                        text: "ADD"
                        size_hint_x: 1
                        elevation: 0
                        md_bg_color: 0.12, 0.23, 0.47, 1
                        on_release: root.show_mode('add')
                    MDRaisedButton:
                        text: "MODIFY"
                        size_hint_x: 1
                        elevation: 0
                        md_bg_color: 0.12, 0.23, 0.47, 1
                        on_release: root.show_mode('modify')
                    MDRaisedButton:
                        text: "DELETE"
                        size_hint_x: 1
                        elevation: 0
                        md_bg_color: 0.12, 0.23, 0.47, 1
                        on_release: root.show_mode('delete')
                    MDRaisedButton:
                        text: "INQUIRE"
                        size_hint_x: 1
                        elevation: 0
                        md_bg_color: 0.12, 0.23, 0.47, 1
                        on_release: root.show_mode('inquire')

                MDCard:
                    id: loan_add_card
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "16dp"
                    radius: 16
                    elevation: 0.35
                    md_bg_color: 1, 1, 1, 1
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        adaptive_height: True
                        MDLabel:
                            text: "ADD LOAN ACTIONS"
                            bold: True
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: "28dp"
                        MDTextField:
                            id: add_loan_number
                            hint_text: "Loan Number"
                            mode: "rectangle"
                            on_focus: root.check_add_loan_number(self.text, self.focus)
                        MDTextField:
                            id: add_action1
                            hint_text: "Action 1"
                            mode: "rectangle"
                            on_text: root.sync_add_action_date(1, self.text)
                        MDTextField:
                            id: add_action1_date
                            hint_text: "Action 1 Date (DD-MM-YYYY)"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: add_action2
                            hint_text: "Action 2"
                            mode: "rectangle"
                            on_text: root.sync_add_action_date(2, self.text)
                        MDTextField:
                            id: add_action2_date
                            hint_text: "Action 2 Date (DD-MM-YYYY)"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: add_action3
                            hint_text: "Action 3"
                            mode: "rectangle"
                            on_text: root.sync_add_action_date(3, self.text)
                        MDTextField:
                            id: add_action3_date
                            hint_text: "Action 3 Date (DD-MM-YYYY)"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: add_action4
                            hint_text: "Action 4"
                            mode: "rectangle"
                            on_text: root.sync_add_action_date(4, self.text)
                        MDTextField:
                            id: add_action4_date
                            hint_text: "Action 4 Date (DD-MM-YYYY)"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: add_action5
                            hint_text: "Action 5"
                            mode: "rectangle"
                            on_text: root.sync_add_action_date(5, self.text)
                        MDTextField:
                            id: add_action5_date
                            hint_text: "Action 5 Date (DD-MM-YYYY)"
                            mode: "rectangle"
                            disabled: True
                        MDRaisedButton:
                            text: "SAVE LOAN"
                            size_hint_x: 1
                            md_bg_color: 0.12, 0.23, 0.47, 1
                            on_release: root.save_loan_actions()

                MDCard:
                    id: loan_modify_card
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    disabled: True
                    padding: "16dp"
                    radius: 16
                    elevation: 0.35
                    md_bg_color: 1, 1, 1, 1
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        adaptive_height: True
                        MDLabel:
                            text: "MODIFY LOAN ACTIONS"
                            bold: True
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: "28dp"
                        MDBoxLayout:
                            adaptive_height: True
                            spacing: "8dp"
                            MDTextField:
                                id: modify_loan_number
                                hint_text: "Loan Number"
                                mode: "rectangle"
                            MDRaisedButton:
                                text: "LOAD"
                                size_hint_x: None
                                width: "90dp"
                                md_bg_color: 0.12, 0.23, 0.47, 1
                                on_release: root.load_loan_for_modify()
                        MDTextField:
                            id: modify_action1
                            hint_text: "Action 1"
                            mode: "rectangle"
                        MDTextField:
                            id: modify_action1_date
                            hint_text: "Action 1 Date"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: modify_action2
                            hint_text: "Action 2"
                            mode: "rectangle"
                        MDTextField:
                            id: modify_action2_date
                            hint_text: "Action 2 Date"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: modify_action3
                            hint_text: "Action 3"
                            mode: "rectangle"
                        MDTextField:
                            id: modify_action3_date
                            hint_text: "Action 3 Date"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: modify_action4
                            hint_text: "Action 4"
                            mode: "rectangle"
                        MDTextField:
                            id: modify_action4_date
                            hint_text: "Action 4 Date"
                            mode: "rectangle"
                            disabled: True
                        MDTextField:
                            id: modify_action5
                            hint_text: "Action 5"
                            mode: "rectangle"
                        MDTextField:
                            id: modify_action5_date
                            hint_text: "Action 5 Date"
                            mode: "rectangle"
                            disabled: True
                        MDRaisedButton:
                            text: "UPDATE LOAN"
                            size_hint_x: 1
                            md_bg_color: 0.12, 0.23, 0.47, 1
                            on_release: root.update_loan_actions()

                MDCard:
                    id: loan_delete_card
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    disabled: True
                    padding: "16dp"
                    radius: 16
                    elevation: 0.35
                    md_bg_color: 1, 1, 1, 1
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        adaptive_height: True
                        MDLabel:
                            text: "DELETE LOAN"
                            bold: True
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: "28dp"
                        MDTextField:
                            id: delete_loan_number
                            hint_text: "Loan Number"
                            mode: "rectangle"
                        MDRaisedButton:
                            text: "DELETE ENTIRE LOAN"
                            size_hint_x: 1
                            md_bg_color: 0.75, 0.12, 0.12, 1
                            on_release: root.delete_loan_actions()

                MDCard:
                    id: loan_inquire_card
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    disabled: True
                    padding: "16dp"
                    radius: 16
                    elevation: 0.35
                    md_bg_color: 1, 1, 1, 1
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        adaptive_height: True
                        MDLabel:
                            text: "INQUIRE LOAN"
                            bold: True
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: "28dp"
                        MDBoxLayout:
                            adaptive_height: True
                            spacing: "8dp"
                            MDTextField:
                                id: inquire_loan_number
                                hint_text: "Loan Number"
                                mode: "rectangle"
                            MDRaisedButton:
                                text: "SEARCH"
                                size_hint_x: None
                                width: "100dp"
                                md_bg_color: 0.12, 0.23, 0.47, 1
                                on_release: root.inquire_loan_actions()
                        MDLabel:
                            id: inquire_result
                            text: "Enter a loan number to view actions."
                            theme_text_color: "Secondary"
                            adaptive_height: True
                            halign: "left"

<LoanActionsSearchResultScreen>:
    name: 'loan_actions_search_result'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Loan Actions Search Result"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "10dp"
                MDLabel:
                    id: result_text
                    text: "Loading loan actions..."
                    theme_text_color: "Primary"
                    font_style: "Body1"
                    halign: "left"
                    adaptive_height: True

<BranchListScreen>:
    name: 'branch_list'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Select Branch"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDScrollView:
            MDList:
                id: branch_container

<StaffListScreen>:
    name: 'staff_list'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            id: staff_toolbar
            title: "Staff List"
            left_action_items: [["arrow-left", lambda x: app.change_screen('branch_list')]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDScrollView:
            MDList:
                id: staff_container

<StaffDetailScreen>:
    name: 'staff_detail'
    MDFloatLayout:
        md_bg_color: 0.95, 0.95, 0.97, 1

        # 1. FIX: Force the Top Bar to the top of the screen
        MDTopAppBar:
            title: "Kerala Bank"
            left_action_items: [["arrow-left", lambda x: app.change_screen('staff_list')]]
            md_bg_color: 0.12, 0.23, 0.47, 1
            pos_hint: {"top": 1} 

        # 2. The Inner Window (Card)
        MDCard:
            size_hint: .9, .7
            pos_hint: {"center_x": .5, "center_y": .4} # Adjusted center_y to sit better
            radius: 25
            elevation: 4
            padding: "12dp"
            orientation: "vertical"
            
            # Avatar Section
            AnchorLayout:
                size_hint_y: None
                height: "120dp"
                anchor_x: "center"
                anchor_y: "center"
                MDCard:
                    size_hint: None, None
                    size: "100dp", "100dp"
                    radius: 50
                    elevation: 0
                    FitImage:
                        id: profile_pic
                        source: "avatar.png"
                        radius: 50

            # 3. FIX: Text Block
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "8dp"
                # This padding pushes the labels down relative to the Avatar
                padding: [0, "80dp", 0, 0] 

                MDLabel:
                    id: name_label
                    text: "Employee Name"
                    halign: "center"
                    font_style: "H6"
                    bold: True
                Widget:
                    size_hint_y: None
                    height: "8dp"

                MDLabel:
                    id: desig_label
                    text: "Designation"
                    halign: "center"
                    theme_text_color: "Secondary"
                    font_style: "Subtitle2"
                Widget:
                    size_hint_y: None
                    height: "8dp"
                Widget:
                    size_hint_y: None
                    height: "2dp"
                Widget:
                    size_hint_y: None
                    height: "1dp"
                Widget:
                    size_hint_y: None
                    height: "2dp"
                MDLabel:
                    id: eid_label
                    text: "Employee ID: --"
                    halign: "center"
                    font_style: "Body2"
                Widget:
                    size_hint_y: None
                    height: "8dp"
                MDLabel:
                    id: phone_label
                    text: "Phone: --"
                    halign: "center"
                    font_style: "Body2"

            # Spacer to push buttons to the bottom of the card
            Widget: 

            # Action Buttons
            MDBoxLayout:
                spacing: "12dp"
                pos_hint: {"center_x": .5}
                adaptive_size: True
                padding: [0, 0, 0, "10dp"]

                MDFillRoundFlatIconButton:
                    icon: "phone"
                    text: "Call"
                    on_release: root.make_call()

                MDFillRoundFlatIconButton:
                    icon: "whatsapp"
                    text: "WhatsApp"
                    md_bg_color: 0.15, 0.68, 0.37, 1
                    on_release: root.open_whatsapp()



<ErrorReportScreen>:
    name: 'error_report'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Error / Message Reporting"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_reports()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDBoxLayout:
            padding: "20dp"
            spacing: "15dp"
            orientation: "vertical"
            MDCard:
                size_hint_y: None
                height: "70dp"
                radius: 15
                padding: "10dp"
                MDBoxLayout:
                    size_hint_x: .25
                    md_bg_color: 0.12, 0.23, 0.47, 1
                    radius: 10
                    orientation: "vertical"
                    MDLabel:
                        id: cal_month
                        text: "---"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "Caption"
                    MDLabel:
                        id: cal_day
                        text: "--"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                MDBoxLayout:
                    orientation: "vertical"
                    padding: ["15dp", 0, 0, 0]
                    MDLabel:
                        id: live_time
                        text: "00:00:00"
                    MDLabel:
                        id: display_id
                        text: "ID: --"
                        font_style: "Caption"
            MDTextField:
                id: error_input
                hint_text: "Describe issue..."
                mode: "rectangle"
                multiline: True
                size_hint_y: None
                height: "90dp"
            MDRaisedButton:
                text: "SUBMIT"
                size_hint_x: 1
                height: "48dp"
                on_release: root.submit_report()
            MDLabel:
                text: "Your reported issues"
                font_style: "Subtitle1"
                size_hint_y: None
                height: "36dp"
                theme_text_color: "Primary"
            MDScrollView:
                size_hint_y: 0.92
                MDBoxLayout:
                    id: report_list
                    orientation: "vertical"
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: ["12dp", "10dp", "12dp", "10dp"]
            Widget:
                size_hint_y: None
                height: "0dp"

<ErrorResolveScreen>:
    name: 'error_resolve'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1
        MDTopAppBar:
            title: "Error/Message Resolving"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_all_reports()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
        MDLabel:
            text: "Resolve reports submitted by all branches"
            size_hint_y: None
            height: "40dp"
            padding: ["20dp", "10dp"]
            theme_text_color: "Secondary"
        MDScrollView:
            MDBoxLayout:
                id: resolve_report_list
                orientation: 'vertical'
                spacing: '10dp'
                size_hint_y: None
                height: self.minimum_height
                padding: ["12dp", "12dp", "12dp", "12dp"]

<UrgentScreen>:
    name: 'urgent'
    on_enter: root.load_urgent_dashboard()
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDTopAppBar:
            title: "Urgent Alerts"
            md_bg_color: 0.8, 0, 0, 1
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_urgent_dashboard()]]

        MDScrollView:
            MDList:
                id: urgent_list

        
        MDBoxLayout:
            id: ho_input_area
            adaptive_height: True
            padding: "10dp"
            spacing: "10dp"
            md_bg_color: 1, 1, 1, 1
            opacity: 0     
            disabled: True 

            MDTextField:
                id: urgent_msg_input
                hint_text: "Type urgent message..."
                mode: "rectangle"  # Changed from 'outline' to fix the crash
                multiline: True
                size_hint_x: 0.85   
                pos_hint: {"center_y": .5}

            MDIconButton:
                icon: "send-circle"
                theme_text_color: "Custom"
                text_color: 0.8, 0, 0, 1
                icon_size: "32sp"
                size_hint_x: None
                width: "48dp"       # Forces the button to occupy space
                pos_hint: {"center_y": .5}
                on_release: root.send_alert()

<PasswordScreen>:
    name: 'password'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1

        # Security Settings at the very top
        MDTopAppBar:
            title: "Security Settings"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
            elevation: 4

        MDBoxLayout:
            orientation: 'vertical'
            padding: ["30dp", "20dp", "30dp", "20dp"]
            spacing: "15dp"
            adaptive_height: True

            # Update Password label just below the bar
            MDLabel:
                text: "Update Password"
                halign: "center"
                font_style: "H6"
                size_hint_y: None
                height: "40dp"
                theme_text_color: "Primary"

            MDRelativeLayout:
                size_hint_y: None
                height: new_pwd.height

                MDTextField:
                    id: new_pwd
                    hint_text: "Enter New Password"
                    mode: "rectangle"
                    password: True

                MDIconButton:
                    icon: "eye-off"
                    pos_hint: {"center_y": .5, "right": 0.95}
                    theme_text_color: "Hint"
                    on_release: root.toggle_password_visibility(new_pwd, self)

            MDRelativeLayout:
                size_hint_y: None
                height: confirm_pwd.height

                MDTextField:
                    id: confirm_pwd
                    hint_text: "Re-enter New Password"
                    mode: "rectangle"
                    password: True

                MDIconButton:
                    icon: "eye-off"
                    pos_hint: {"center_y": .5, "right": 0.95}
                    theme_text_color: "Hint"
                    on_release: root.toggle_password_visibility(confirm_pwd, self)

            Widget:
                size_hint_y: None
                height: "10dp"

            MDRaisedButton:
                text: "CONFIRM & UPDATE"
                size_hint_x: 1
                height: "50dp"
                md_bg_color: 0.12, 0.23, 0.47, 1
                on_release: root.validate_and_update()

        # Pushes everything to the top
        Widget:



<DocShareScreen>:
    name: 'doc_share'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1

        MDTopAppBar:
            title: "Document Share"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: ["30dp", "20dp", "30dp", "20dp"]
            spacing: "15dp"

            MDTextField:
                id: upload_reason
                hint_text: "Reason for upload"
                mode: "rectangle"

            MDTextField:
                id: uploaded_file
                hint_text: "Selected / Uploaded file"
                mode: "rectangle"
                text: ""
                disabled: True

            MDRaisedButton:
                text: "SELECT FILE & UPLOAD"
                size_hint_x: 1
                md_bg_color: 0.12, 0.23, 0.47, 1
                on_release: root.open_manager()

            Widget:

<CircularsScreen>:
    name: 'circulars'
    on_pre_enter: root.on_pre_enter()
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1

        MDTopAppBar:
            title: "Circulars"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_circulars()]]
            md_bg_color: 0.12, 0.23, 0.47, 1

        MDCard:
            id: circular_upload_card
            size_hint_y: None
            height: 0
            opacity: 0
            disabled: True
            radius: 0
            elevation: 0
            md_bg_color: 1, 1, 1, 1
            padding: "12dp"
            MDBoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                adaptive_height: True
                MDLabel:
                    text: "Send circular to all branches"
                    font_style: "Subtitle1"
                    bold: True
                    size_hint_y: None
                    height: "28dp"
                MDTextField:
                    id: circular_selected_file
                    hint_text: "Selected file"
                    mode: "rectangle"
                    disabled: True
                MDRaisedButton:
                    text: "SELECT FILE & UPLOAD"
                    size_hint_x: 1
                    elevation: 0
                    md_bg_color: 0.12, 0.23, 0.47, 1
                    on_release: root.open_manager()

        MDScrollView:
            MDList:
                id: circulars_list

<ConsolidationScreen>:
    name: 'consolidation'
    on_pre_enter: root.on_pre_enter()
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1

        MDTopAppBar:
            title: "Consolidation"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["refresh", lambda x: root.load_links()]]
            md_bg_color: 0.12, 0.23, 0.47, 1

        MDCard:
            id: consolidation_input_card
            size_hint_y: None
            height: 0
            opacity: 0
            disabled: True
            radius: 0
            elevation: 0
            md_bg_color: 1, 1, 1, 1
            padding: "12dp"
            MDBoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                adaptive_height: True
                MDLabel:
                    text: "Add Google Sheet link"
                    font_style: "Subtitle1"
                    bold: True
                    size_hint_y: None
                    height: "28dp"
                MDTextField:
                    id: consolidation_heading
                    hint_text: "Heading"
                    mode: "rectangle"
                MDTextField:
                    id: consolidation_link
                    hint_text: "Google Sheet link"
                    mode: "rectangle"
                MDRaisedButton:
                    text: "ADD LINK"
                    size_hint_x: 1
                    elevation: 0
                    md_bg_color: 0.12, 0.23, 0.47, 1
                    on_release: root.add_link()

        MDScrollView:
            MDList:
                id: consolidation_links_list

<FinacleHelpScreen>:
    name: 'finacle_help'
    MDFloatLayout:
        md_bg_color: 0.95, 0.95, 0.97, 1

        MDTopAppBar:
            title: "Finacle Help"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["plus", lambda x: root.open_add_screen()], ["refresh", lambda x: root.load_finacle_entries()]]
            md_bg_color: 0.12, 0.23, 0.47, 1
            pos_hint: {"top": 1}
            size_hint_y: None
            height: "56dp"

        
        MDScrollView:
            pos_hint: {"top": 0.85}
            size_hint: 1, 0.85
            MDBoxLayout:
                id: finacle_help_sections
                orientation: "vertical"
                adaptive_height: True
                spacing: "0dp"
                padding: ["12dp", "0dp", "12dp", "12dp"]

<AddFinacleHelpScreen>:
    name: 'add_finacle_help'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1

        MDTopAppBar:
            title: "Add Finacle Help"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            md_bg_color: 0.12, 0.23, 0.47, 1

        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "16dp"

            MDCard:
                orientation: "vertical"
                adaptive_height: True
                elevation: 0.25
                radius: [12, 12, 12, 12]
                padding: "16dp"
                spacing: "12dp"
                md_bg_color: 1, 1, 1, 1
                
                MDLabel:
                    text: "Create New Entry"
                    bold: True
                    font_style: "H6"
                    halign: "center"
                    adaptive_height: True
                
                MDTextField:
                    id: finacle_section_title
                    hint_text: "Section Title"
                    mode: "rectangle"
                    required: True
                
                MDTextField:
                    id: finacle_menu_code
                    hint_text: "Menu Code"
                    mode: "rectangle"
                    required: True
                
                MDTextField:
                    id: finacle_menu_description
                    hint_text: "Description"
                    mode: "rectangle"
                    multiline: True
                
                MDRaisedButton:
                    text: "SAVE ENTRY"
                    size_hint_x: 1
                    elevation: 0
                    md_bg_color: 0.12, 0.23, 0.47, 1
                    on_release: root.save_entry()

'''

# ------------------- Python Screen Classes -------------------

class LoginScreen(Screen):
    def do_login(self):
        uid = self.ids.emp_id.text.strip()
        pwd = self.ids.password.text.strip()
        if uid and pwd:
            thread_pool.submit(self._login_async, uid, pwd)
        else:
            Clock.schedule_once(lambda dt: small_toast("Please enter Employee ID and Password"))

    def _login_async(self, uid, pwd):
        try:
            # We use params for emp_id and password based on your existing setup
            resp = requests.post(
                "http://127.0.0.1:8000/login", 
                params={"emp_id": uid, "password": pwd}, 
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._on_login_success(data))
            else:
                Clock.schedule_once(lambda dt: small_toast("Invalid credentials"))
        except Exception as e:
            Clock.schedule_once(lambda dt: small_toast("Connection Error"))
    def _on_login_success(self, data):
        app = MDApp.get_running_app()
        
        # 1. Save global app data
        app.user_id = str(data.get("emp_id", ""))
        app.user_name = data.get("name", "Employee Name")
        app.user_phone = data.get("phone", "")
        app.user_designation = data.get("designation", "")
        avatar_path = data.get("avatar")
        if avatar_path:
            avatar_path = avatar_path.replace("\\", "/")
            avatar_path = avatar_path.replace("/avatar/", "/avatars/")
            avatar_path = avatar_path.replace("\\avatar\\", "/avatars/")
            app.user_avatar = avatar_path
        else:
            app.user_avatar = ""
        app.user_branch_code = str(data.get("branch_code", ""))

        # 2. Update Dashboard Screen
        dash = self.manager.get_screen('dashboard')
        dash.ids.welcome_name.text = app.user_name
        dash.ids.welcome_id.text = f"Emp ID: {app.user_id}"
        
        # 3. Handle the Dashboard Avatar Image
        if app.user_avatar:
            # Construct full URL: http://127.0.0.1:8000/static/avatars/1001.png
            full_url = f"http://127.0.0.1:8000/{app.user_avatar}"
            dash.ids.dash_avatar.source = full_url
        else:
            dash.ids.dash_avatar.source = "avatar.png"
            
        # 4. Update Error Report Screen
        self.manager.get_screen('error_report').ids.display_id.text = f"ID: {app.user_id}"

        # 5. Show HO-only resolve tile only for branch 109000
        if str(app.user_branch_code).strip() == "109000":
            dash.ids.resolve_card.height = "60dp"
            dash.ids.resolve_card.opacity = 1
            dash.ids.resolve_card.disabled = False
        else:
            dash.ids.resolve_card.height = "0dp"
            dash.ids.resolve_card.opacity = 0
            dash.ids.resolve_card.disabled = True
        
        # 6. Switch Screen
        self.manager.current = 'dashboard'

class DashboardScreen(Screen):
    CATEGORY_PANEL_HEIGHT = 760

    def _extract_label_value(self, text):
        try:
            if ":" not in text:
                return 0
            value_part = text.split(":", 1)[1].strip()
            number_text = value_part.split()[0].replace(",", "")
            return int(number_text)
        except Exception:
            return 0

    def download_branch_report(self):
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._download_branch_report_async, args=(app.user_id,), daemon=True)
        t.start()

    def _download_branch_report_async(self, emp_id):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/branch-report/{emp_id}", timeout=20)
            if resp.status_code != 200:
                Clock.schedule_once(lambda dt: toast("Failed to download report"))
                return

            filename = "branch_report.xls"
            content_disposition = resp.headers.get("Content-Disposition", "")
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=", 1)[1].strip().strip('"')

            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.isdir(downloads_dir):
                downloads_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(downloads_dir, exist_ok=True)

            file_path = os.path.join(downloads_dir, filename)
            with open(file_path, "wb") as report_file:
                report_file.write(resp.content)

            Clock.schedule_once(lambda dt, name=filename: toast(f"Downloaded {name}"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _apply_submitted_collection(self, category, number, amount):
        total_num_label = self.ids.get(f'{category}_total_num')
        total_amt_label = self.ids.get(f'{category}_total_amt')
        balance_num_label = self.ids.get(f'{category}_balance_num')
        balance_amt_label = self.ids.get(f'{category}_balance_amt')
        opening_num_label = self.ids.get(f'{category}_opening_num')
        opening_amt_label = self.ids.get(f'{category}_opening_amt')

        if not all([total_num_label, total_amt_label, balance_num_label, balance_amt_label, opening_num_label, opening_amt_label]):
            return

        total_num = self._extract_label_value(total_num_label.text)
        total_amt = self._extract_label_value(total_amt_label.text)
        opening_num = self._extract_label_value(opening_num_label.text)
        opening_amt = self._extract_label_value(opening_amt_label.text)

        new_total_num = total_num + number
        new_total_amt = total_amt + amount
        new_balance_num = opening_num - new_total_num
        new_balance_amt = opening_amt - new_total_amt

        total_num_label.text = f"Number: {new_total_num}"
        total_amt_label.text = f"Amount: {new_total_amt}"
        balance_num_label.text = f"Number: {new_balance_num}"
        balance_amt_label.text = f"Amount: {new_balance_amt}"

    def on_enter(self):
        app = MDApp.get_running_app()
        # Set Name and ID labels
        self.ids.welcome_name.text = app.user_name
        self.ids.welcome_id.text = f"ID: {app.user_id}"
        
        # Update Avatar Image
        # We point to the FastAPI static folder. If no avatar exists, it stays 'avatar.png'
        if app.user_avatar:
            self.ids.dash_avatar.source = f"http://127.0.0.1:8000/{app.user_avatar}"
        else:
            self.ids.dash_avatar.source = "avatar.png"

        # Load SMA data
        self.load_sma_data()
        Clock.schedule_once(lambda dt: self._apply_manual_grey_sections(), 0)
        Clock.schedule_once(lambda dt: self._soften_category_text(), 0)
        
        # Auto-migrate yesterday's data if needed
        self.migrate_yesterday_data()

    def migrate_yesterday_data(self):
        """Automatically migrate yesterday's data to previous day fields"""
        app = MDApp.get_running_app()
        threading.Thread(target=self._migrate_yesterday_data_async, args=(app.user_branch_code,), daemon=True).start()

    def _migrate_yesterday_data_async(self, branch_code):
        try:
            resp = requests.post(f"http://127.0.0.1:8000/migrate-yesterday-data?branch_code={branch_code}", timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                if result.get("status") == "success":
                    # Silent migration - no toast message
                    # Reload data to show updated previous day values
                    self.load_sma_data()
        except Exception:
            pass  # Silently fail if migration fails

    
    def on_tab_switch(self, *args):
        """
        Keep tab switching passive so category changes do not shift the viewport.
        """
        return

    def load_sma_data(self):
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._load_sma_data_async, args=(app.user_branch_code,), daemon=True)
        t.start()

    def _load_sma_data_async(self, branch_code):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/sma-data/{branch_code}")
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._populate_sma_data(data))
        except:
            pass

    def _populate_sma_data(self, data):
        categories = ['sma0', 'sma1', 'sma2', 'npa1', 'npa2', 'd1', 'd2', 'd3']
        for cat in categories:
            if cat in data:
                opening_num = data[cat]['opening_number']
                outstanding = data[cat]['outstanding_amount']
                as_of = data[cat]['as_of_date']
                self.ids[f'{cat}_opening_num'].text = f"Number: {opening_num} (as of {as_of})"
                self.ids[f'{cat}_opening_amt'].text = f"Amount: {outstanding}"
                self.load_collections(cat)

    def load_collections(self, category):
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._load_collections_async, args=(app.user_branch_code, category), daemon=True)
        t.start()

    def _load_collections_async(self, branch_code, category):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/collections/{branch_code}/{category}")
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._populate_collections(category, data))
        except:
            pass

    def _populate_collections(self, category, data):
        prev_num = data['previous_day']['number']
        prev_amt = data['previous_day']['amount']
        today_num = data.get('today', {}).get('number', 0)
        today_amt = data.get('today', {}).get('amount', 0)
        total_num = data['total_month']['number']
        total_amt = data['total_month']['amount']
        opening_text = self.ids[f'{category}_opening_num'].text
        opening_num = self._extract_label_value(opening_text)
        balance_num = opening_num - total_num
        outstanding_text = self.ids[f'{category}_opening_amt'].text
        outstanding_amt = self._extract_label_value(outstanding_text)
        balance_amt = outstanding_amt - total_amt
        self.ids[f'{category}_today_num'].text = str(today_num)
        self.ids[f'{category}_today_amt'].text = str(today_amt)
        self.ids[f'{category}_prev_num'].text = f"Number: {prev_num}"
        self.ids[f'{category}_prev_amt'].text = f"Amount: {prev_amt}"
        self.ids[f'{category}_total_num'].text = f"Number: {total_num}"
        self.ids[f'{category}_total_amt'].text = f"Amount: {total_amt}"
        self.ids[f'{category}_balance_num'].text = f"Number: {balance_num}"
        self.ids[f'{category}_balance_amt'].text = f"Amount: {balance_amt}"

    def on_collection_focus(self, category, field, widget, focused):
        return

    def submit_collection(self, category):
        try:
            num = int((self.ids[f'{category}_today_num'].text or "0").strip())
            amt = int((self.ids[f'{category}_today_amt'].text or "0").strip())
        except Exception:
            toast("Enter valid number and amount")
            return

        app = MDApp.get_running_app()
        data = {
            "branch_code": app.user_branch_code,
            "category": category,
            "number": num,
            "amount": amt,
        }
        t = threading.Thread(
            target=self._submit_collection_async,
            args=(category, data),
            daemon=True,
        )
        t.start()

    def save_collection(self, category, field, value):
        app = MDApp.get_running_app()
        if field == 'number':
            amt = int(self.ids[f'{category}_today_amt'].text or 0)
            data = {"branch_code": app.user_branch_code, "category": category, "number": value, "amount": amt}
        else:
            num = int(self.ids[f'{category}_today_num'].text or 0)
            data = {"branch_code": app.user_branch_code, "category": category, "number": num, "amount": value}
        t = threading.Thread(target=self._save_collection_async, args=(data,), daemon=True)
        t.start()

    def _save_collection_async(self, data):
        try:
            requests.post("http://127.0.0.1:8000/save-collection", json=data)
        except:
            pass

    def _submit_collection_async(self, category, data):
        try:
            resp = requests.post("http://127.0.0.1:8000/save-collection", json=data, timeout=5)
            if resp.status_code == 200:
                Clock.schedule_once(
                    lambda dt, c=category, n=data["number"], a=data["amount"]: self._apply_submitted_collection(c, n, a)
                )
                payload = {}
                try:
                    payload = resp.json() or {}
                except Exception:
                    payload = {}

                if "previous_day" in payload and "total_month" in payload:
                    Clock.schedule_once(lambda dt, p=payload: self._populate_collections(category, p))
                else:
                    Clock.schedule_once(lambda dt: self.load_collections(category))
                Clock.schedule_once(lambda dt: small_toast("Collection submitted"))
            else:
                Clock.schedule_once(lambda dt: small_toast("Failed to submit collection"))
        except Exception:
            Clock.schedule_once(lambda dt: small_toast("Connection Error"))

    def show_sma_panel(self, panel_key):
        panel_ids = {
            'sma0': 'sma0_box',
            'sma1': 'sma1_box',
            'sma2': 'sma2_box',
        }
        for key, panel_id in panel_ids.items():
            panel = self.ids.get(panel_id)
            if panel:
                visible = key == panel_key
                panel.opacity = 1 if visible else 0
                panel.height = self.CATEGORY_PANEL_HEIGHT if visible else 0
                panel.disabled = not visible
                if visible:
                    self._apply_manual_grey_sections()
                    self._soften_category_text()
                    Clock.schedule_once(lambda dt, p=panel: self._refresh_panel_canvas(p), 0)

    def show_npa_panel(self, panel_key):
        panel_ids = {
            'npa1': 'npa1_box',
            'npa2': 'npa2_box',
            'd1': 'd1_box',
            'd2': 'd2_box',
            'd3': 'd3_box',
        }
        for key, panel_id in panel_ids.items():
            panel = self.ids.get(panel_id)
            if panel:
                visible = key == panel_key
                panel.opacity = 1 if visible else 0
                panel.height = self.CATEGORY_PANEL_HEIGHT if visible else 0
                panel.disabled = not visible
                if visible:
                    self._apply_manual_grey_sections()
                    self._soften_category_text()
                    Clock.schedule_once(lambda dt, p=panel: self._refresh_panel_canvas(p), 0)

    def _apply_manual_grey_sections(self):
        target_boxes = ("sma1_box", "sma2_box", "npa2_box", "d1_box", "d2_box", "d3_box")
        grey = [0.97, 0.97, 0.97, 1]
        for box_id in target_boxes:
            panel = self.ids.get(box_id)
            if panel:
                self._set_inner_cards_grey(panel, grey)

    def _set_inner_cards_grey(self, widget, grey):
        for child in getattr(widget, "children", []):
            if child.__class__.__name__ == "MDCard" and child is not widget:
                child.md_bg_color = grey[:]
                if hasattr(child, "canvas") and child.canvas:
                    child.canvas.ask_update()
            self._set_inner_cards_grey(child, grey)

    def _soften_category_text(self):
        panel_ids = (
            "sma0_box", "sma1_box", "sma2_box",
            "npa1_box", "npa2_box",
            "d1_box", "d2_box", "d3_box",
        )
        for panel_id in panel_ids:
            panel = self.ids.get(panel_id)
            if panel:
                self._soften_widget_text(panel)

    def _soften_widget_text(self, widget):
        if hasattr(widget, "text") and hasattr(widget, "bold") and widget.bold:
            widget.bold = False
        if hasattr(widget, "text") and isinstance(widget.text, str):
            text_value = widget.text.strip()
            if text_value and any(ch.isalpha() for ch in text_value):
                widget.text = widget.text.upper()
        for child in getattr(widget, "children", []):
            self._soften_widget_text(child)

    def _refresh_panel_canvas(self, widget):
        if not widget:
            return
        if hasattr(widget, "do_layout"):
            widget.do_layout()
        if hasattr(widget, "canvas") and widget.canvas:
            widget.canvas.ask_update()
        if hasattr(widget, "md_bg_color"):
            current_color = widget.md_bg_color
            if current_color is not None:
                widget.md_bg_color = list(current_color)
        if hasattr(widget, "texture_update"):
            widget.texture_update()
        for child in getattr(widget, "children", []):
            self._refresh_panel_canvas(child)

class MessagesScreen(Screen):
    def send_message(self):
        app = MDApp.get_running_app()
        msg = self.ids.msg_input.text.strip()
        if msg:
            t = threading.Thread(target=self._send_msg_async, args=(app.user_id, msg), daemon=True)
            t.start()

    def _send_msg_async(self, uid, msg):
        try:
            resp = requests.post("http://127.0.0.1:8000/messages", params={"emp_id": uid, "content": msg})
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: self._on_send_success())
        except:
            Clock.schedule_once(lambda dt: toast("Server Error"))

    def _on_send_success(self):
        Clock.schedule_once(lambda dt: toast("Message Sent"))
        self.ids.msg_input.text = ""
        self.load_messages()

    def load_messages(self):
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._load_msgs_async, args=(app.user_id,), daemon=True)
        t.start()

    def _load_msgs_async(self, uid):
        try:
            # ✅ Call the correct backend route
            resp = requests.get("http://127.0.0.1:8000/messages")
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._update_chat_list(data))
        except:
            Clock.schedule_once(lambda dt: toast("Server Error"))


    def _update_chat_list(self, data):
        self.ids.chat_list.clear_widgets()
        app = MDApp.get_running_app()

        for m in data:
            name = m.get("sender_name", "Unknown")
            eid = m.get("sender_id", "--")
            branch = m.get("branch_name", "General")
            header = f"{name}  |  ID: {eid}  |  {branch}"
            
            raw_time = m.get("timestamp", "")
            time_str = raw_time[11:16] if len(raw_time) > 16 else "Just now"

            is_me = str(eid) == str(app.user_id)
            
            bubble = ChatBubble(
                sender_info=header,
                message_text=m.get("content", ""),
                timestamp=time_str,
                bg_color=[0.8, 0.9, 1, 1] if is_me else [1, 1, 1, 1],
                pos_hint={"right": 1} if is_me else {"left": 1}
            )
            self.ids.chat_list.add_widget(bubble)
        
        # This line triggers the scroll after the bubbles are added
        Clock.schedule_once(lambda dt: self.scroll_to_bottom())

    # ADD THIS FUNCTION BELOW:
    def scroll_to_bottom(self):
        if 'chat_scroll' in self.ids:
            self.ids.chat_scroll.scroll_y = 0

class EditProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, 
            select_path=self.select_path, 
            preview=True
        )
    def on_pre_enter(self):
        """This runs EVERY time you switch to the Edit Profile screen"""
        app = MDApp.get_running_app()
        
        # Populate the Employee ID and current name
        self.ids.new_id.text = str(app.user_id)
        if hasattr(app, 'user_name'):
            self.ids.new_name.text = app.user_name
        if hasattr(app, 'user_phone'):
            self.ids.new_phone.text = app.user_phone
        if hasattr(app, 'user_branch_code'):
            self.ids.new_branch.text = str(app.user_branch_code)
        if hasattr(app, 'user_designation'):
            self.ids.new_desig.text = app.user_designation

        # Load current avatar if available
        if getattr(app, 'user_avatar', None):
            self.ids.edit_avatar.source = f"http://127.0.0.1:8000/{app.user_avatar}"
        else:
            self.ids.edit_avatar.source = "avatar.png"

    def open_file_manager(self):
        self.file_manager.show(os.path.expanduser("~"))

    def select_path(self, path):
        self.exit_manager()
        if path and path.lower().endswith(('.png', '.jpg', '.jpeg')):
            app = MDApp.get_running_app()
            try:
                with open(path, 'rb') as f:
                    files = {'file': (os.path.basename(path), f, 'application/octet-stream')}
                    resp = requests.post(
                        "http://127.0.0.1:8000/upload-avatar",
                        params={"emp_id": app.user_id},
                        files=files,
                        timeout=10
                    )
                if resp.status_code == 200:
                    data = resp.json()
                    avatar = data.get('avatar')
                    if avatar:
                        app.user_avatar = avatar.replace('\\', '/')
                        self.ids.edit_avatar.source = f"http://127.0.0.1:8000/{app.user_avatar}"
                        self.manager.get_screen('dashboard').ids.dash_avatar.source = f"http://127.0.0.1:8000/{app.user_avatar}"
                        msg = "Photo Updated!"
                        Clock.schedule_once(lambda dt, m=msg: toast(m))
                        return
                Clock.schedule_once(lambda dt: toast("Failed to upload avatar."))
            except Exception:
                Clock.schedule_once(lambda dt: toast("Connection Error: Avatar upload failed"))

    def exit_manager(self, *args):
        try:
            self.file_manager.close()
        except Exception:
            pass

    def save_profile(self):
        app = MDApp.get_running_app()
        profile_data = {
            "uid": app.user_id,
            "name": self.ids.new_name.text,
            "desig": self.ids.new_desig.text,
            "phone": self.ids.new_phone.text,
            "branch": self.ids.new_branch.text
        }
        
        t = threading.Thread(
            target=self._save_profile_async, 
            args=(profile_data,), 
            daemon=True
        )
        t.start()

    def _save_profile_async(self, data):
        try:
            resp = requests.post("http://127.0.0.1:8000/update-profile", params={
                "emp_id": data["uid"],
                "name": data["name"],
                "designation": data["desig"],
                "phone": data["phone"],
                "branch_code": data["branch"]
            }, timeout=10)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Database Updated Successfully"))
                app = MDApp.get_running_app()
                app.user_name = data["name"]
                app.user_phone = data["phone"]
                app.user_branch_code = data["branch"]
                app.user_designation = data["desig"]
            else:
                Clock.schedule_once(lambda dt: toast(f"Server rejected update: {resp.status_code}"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error: Backend not reached"))


class ActionsOnLoansScreen(Screen):
    MODE_CARD_IDS = {
        "add": "loan_add_card",
        "modify": "loan_modify_card",
        "delete": "loan_delete_card",
        "inquire": "loan_inquire_card",
    }

    def on_pre_enter(self):
        self._clear_add_dates()
        self.show_mode("add")

    def show_mode(self, mode):
        for key, card_id in self.MODE_CARD_IDS.items():
            card = self.ids.get(card_id)
            if not card:
                continue
            visible = key == mode
            card.opacity = 1 if visible else 0
            card.disabled = not visible
            card.height = card.minimum_height if visible else 0

    def _clear_add_dates(self):
        for idx in range(1, 6):
            field = self.ids.get(f"add_action{idx}_date")
            if field:
                field.text = ""

    def sync_add_action_date(self, index, value):
        field = self.ids.get(f"add_action{index}_date")
        if not field:
            return
        text_value = (value or "").strip()
        field.text = datetime.now().strftime("%d-%m-%Y") if text_value else ""

    def _loan_payload_from_prefix(self, prefix):
        payload = {"loan_number": self.ids[f"{prefix}_loan_number"].text.strip()}
        for idx in range(1, 6):
            payload[f"action{idx}"] = self.ids[f"{prefix}_action{idx}"].text.strip()
            date_id = f"{prefix}_action{idx}_date"
            if date_id in self.ids:
                payload[f"action{idx}_date"] = self.ids[date_id].text.strip()
        return payload

    def save_loan_actions(self):
        payload = self._loan_payload_from_prefix("add")
        if not payload["loan_number"]:
            toast("Enter loan number")
            return
        app = MDApp.get_running_app()
        payload["emp_id"] = app.user_id
        threading.Thread(target=self._save_loan_actions_async, args=(payload,), daemon=True).start()

    def check_add_loan_number(self, loan_number, focused):
        if focused:
            return
        loan_number = (loan_number or "").strip()
        if not loan_number:
            return
        threading.Thread(target=self._check_add_loan_number_async, args=(loan_number,), daemon=True).start()

    def _check_add_loan_number_async(self, loan_number):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/loan-actions/{loan_number}", timeout=10)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: self._handle_duplicate_add_loan())
        except Exception:
            pass

    def _handle_duplicate_add_loan(self):
        self.ids.add_loan_number.text = ""
        toast("Loan number already exists")

    def _save_loan_actions_async(self, payload):
        try:
            resp = requests.post("http://127.0.0.1:8000/loan-actions", json=payload, timeout=10)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Loan actions saved"))
                Clock.schedule_once(lambda dt: self._clear_add_form())
            else:
                detail = resp.json().get("detail", "Failed to save")
                Clock.schedule_once(lambda dt, msg=detail: toast(msg))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _clear_add_form(self):
        self.ids.add_loan_number.text = ""
        for idx in range(1, 6):
            self.ids[f"add_action{idx}"].text = ""
            self.ids[f"add_action{idx}_date"].text = ""

    def load_loan_for_modify(self):
        loan_number = self.ids.modify_loan_number.text.strip()
        if not loan_number:
            toast("Enter loan number")
            return
        threading.Thread(target=self._load_loan_for_modify_async, args=(loan_number,), daemon=True).start()

    def _load_loan_for_modify_async(self, loan_number):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/loan-actions/{loan_number}", timeout=10)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt, data=resp.json(): self._populate_modify_form(data))
            else:
                detail = resp.json().get("detail", "Loan number not found")
                Clock.schedule_once(lambda dt, msg=detail: toast(msg))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _populate_modify_form(self, data):
        self.ids.modify_loan_number.text = data.get("loan_number", "")
        
        # Clear all fields first
        for idx in range(1, 6):
            self.ids[f"modify_action{idx}"].text = ""
            self.ids[f"modify_action{idx}_date"].text = ""
            self.ids[f"modify_action{idx}"].disabled = False
            self.ids[f"modify_action{idx}_date"].disabled = False
        
        # Only populate fields that have actual data
        actions_loaded = 0
        for idx in range(1, 6):
            action = data.get(f"action{idx}", "").strip()
            date = data.get(f"action{idx}_date", "").strip()
            
            if action or date:
                # Only show this action if it has data
                self.ids[f"modify_action{idx}"].text = action
                self.ids[f"modify_action{idx}_date"].text = date
                actions_loaded += 1
        
        if actions_loaded > 0:
            toast(f"Loan loaded - {actions_loaded} action(s) found")
        else:
            toast("No actions found for this loan")

    def update_loan_actions(self):
        loan_number = self.ids.modify_loan_number.text.strip()
        if not loan_number:
            toast("Enter loan number")
            return
        payload = {f"action{idx}": self.ids[f"modify_action{idx}"].text.strip() for idx in range(1, 6)}
        threading.Thread(target=self._update_loan_actions_async, args=(loan_number, payload), daemon=True).start()

    def _update_loan_actions_async(self, loan_number, payload):
        try:
            resp = requests.put(f"http://127.0.0.1:8000/loan-actions/{loan_number}", json=payload, timeout=10)
            if resp.status_code == 200:
                record = resp.json().get("record", {})
                Clock.schedule_once(lambda dt, data=record: self._populate_modify_form(data))
            else:
                detail = resp.json().get("detail", "Failed to update")
                Clock.schedule_once(lambda dt, msg=detail: toast(msg))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def delete_loan_actions(self):
        loan_number = self.ids.delete_loan_number.text.strip()
        if not loan_number:
            toast("Enter loan number")
            return
        threading.Thread(target=self._delete_loan_actions_async, args=(loan_number,), daemon=True).start()

    def _delete_loan_actions_async(self, loan_number):
        try:
            resp = requests.delete(f"http://127.0.0.1:8000/loan-actions/{loan_number}", timeout=10)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Loan deleted"))
                Clock.schedule_once(lambda dt: setattr(self.ids.delete_loan_number, "text", ""))
            else:
                detail = resp.json().get("detail", "Failed to delete")
                Clock.schedule_once(lambda dt, msg=detail: toast(msg))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def inquire_loan_actions(self):
        loan_number = self.ids.inquire_loan_number.text.strip()
        if not loan_number:
            toast("Enter loan number")
            return
        
        # Clear previous results immediately to prevent disorder
        self.ids.inquire_result.text = "Searching..."
        
        # Prevent multiple search calls
        if hasattr(self, '_searching') and self._searching:
            return
        
        self._searching = True
        threading.Thread(target=self._inquire_loan_actions_async, args=(loan_number,), daemon=True).start()

    def _inquire_loan_actions_async(self, loan_number):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/loan-actions/{loan_number}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                # Open new search result page
                Clock.schedule_once(lambda dt: self._open_search_result_page(data))
            else:
                detail = resp.json().get("detail", "Loan number not found")
                Clock.schedule_once(lambda dt, msg=detail: toast(msg))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _open_search_result_page(self, loan_data):
        """Open new search result page with loan data"""
        # Reset searching flag
        self._searching = False
        
        # Get the search result screen
        search_result_screen = self.manager.get_screen('loan_actions_search_result')
        if not search_result_screen:
            # Create screen if it doesn't exist
            search_result_screen = LoanActionsSearchResultScreen(name='loan_actions_search_result')
            self.manager.add_widget(search_result_screen)
        
        # Set loan data and switch to screen
        search_result_screen.set_loan_data(loan_data)
        self.manager.current = 'loan_actions_search_result'

    def _populate_inquiry(self, data):
        # Clear previous results
        loan_number = data.get('loan_number', '')
        
        # Create formatted result text
        result_text = f"LOAN NUMBER: {loan_number}\n"
        result_text += "=" * 40 + "\n\n"
        
        has_actions = False
        for idx in range(1, 6):
            action = data.get(f"action{idx}", "").strip()
            date = data.get(f"action{idx}_date", "").strip()
            
            if action or date:
                has_actions = True
                result_text += f"ACTION {idx}:\n"
                if action:
                    result_text += f"  • {action}\n"
                if date:
                    result_text += f"  • Date: {date}\n"
                result_text += "\n"
        
        if not has_actions:
            result_text += "No actions recorded for this loan"
        
        # Set the result text with proper formatting
        self.ids.inquire_result.text = result_text
        self.ids.inquire_result.color = (1, 1, 1, 1)  # White text
        self.ids.inquire_result.font_style = "Body1"
        
        # Reset searching flag
        self._searching = False

class LoanActionsSearchResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loan_data = None
    
    def set_loan_data(self, loan_data):
        """Set loan data and display it"""
        self.loan_data = loan_data
        self._display_loan_actions()
    
    def _display_loan_actions(self):
        """Display ALL loan actions in clean format"""
        if not self.loan_data:
            self.ids.result_text.text = "No loan data available"
            return
        
        loan_number = self.loan_data.get('loan_number', '')
        result_text = f"LOAN NUMBER: {loan_number}\n"
        result_text += "=" * 50 + "\n\n"
        
        has_any_actions = False
        for idx in range(1, 6):
            action = self.loan_data.get(f"action{idx}", "").strip()
            date = self.loan_data.get(f"action{idx}_date", "").strip()
            
            # Show ALL actions, even if empty (to show what's available)
            result_text += f"ACTION {idx}:\n"
            if action:
                result_text += f"   {action}\n"
                has_any_actions = True
            else:
                result_text += f"   (No action text)\n"
            
            if date:
                result_text += f"   Date: {date}\n"
                has_any_actions = True
            else:
                result_text += f"   (No date set)\n"
            
            result_text += "\n"
        
        if not has_any_actions:
            result_text += "❌ No actions recorded for this loan"
        
        self.ids.result_text.text = result_text
    
    def go_back(self):
        """Go back to loan actions screen"""
        self.manager.current = 'actions_loans'


class BranchListScreen(Screen):
    def on_enter(self):
        self.ids.branch_container.clear_widgets()
        t = threading.Thread(target=self._load_branches, daemon=True)
        t.start()

    def _load_branches(self):
        try:
            resp = requests.get("http://127.0.0.1:8000/branches")
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._populate_branches(data))
            else:
                msg = f"Server returned {resp.status_code}"
                Clock.schedule_once(lambda dt, m=msg: toast(m))
        except Exception as e:
            msg = f"Connection Error: {e}"
            Clock.schedule_once(lambda dt, m=msg: toast(m))

    def fetch_branches(self):
        try:
            # Ensure the server is running on 8000
            response = requests.get("http://127.0.0.1:8000/branches")
            if response.status_code == 200:
                branches = response.json()
                self.update_list(branches)
        except Exception as e:
            print(f"Error: {e}") 
    def _populate_branches(self, data):
        for index, branch in enumerate(data):
            item = TwoLineAvatarListItem(text=branch.get("branch_name", ""), secondary_text=f"ID: {branch.get('branch_id','')}")
            image_path = os.path.join("backend", "static", "branch_numbers", f"{index}.png")
            if os.path.exists(image_path):
                item.add_widget(ImageLeftWidget(source=image_path))
            item.bind(on_release=lambda x, b=branch.get("branch_id"): self.go_to_staff(b))
            self.ids.branch_container.add_widget(item)

    def go_to_staff(self, branch_id):
        app = MDApp.get_running_app()
        app.selected_branch = branch_id
        self.manager.current = 'staff_list'

class StaffListScreen(Screen):
    def on_enter(self):
        self.ids.staff_container.clear_widgets()
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._load_staff, args=(app.selected_branch,), daemon=True)
        t.start()

    def _load_staff(self, branch_id):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/employees/{branch_id}")
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._populate_staff(data))
        except:
            pass

    def _populate_staff(self, data):
        for emp in data:
            item = TwoLineAvatarListItem(text=emp.get("name", ""), secondary_text=emp.get("designation", ""))
            item.bind(on_release=lambda x, e=emp: self.go_to_detail(e))
            self.ids.staff_container.add_widget(item)

    def go_to_detail(self, emp):
        detail = self.manager.get_screen('staff_detail')
        detail.ids.name_label.text = emp.get("name", "Name")
        detail.ids.desig_label.text = emp.get("designation", "")
        detail.ids.eid_label.text = f"Employee ID: {emp.get('emp_id','--')}"
        detail.ids.phone_label.text = f"Phone: {emp.get('phone','--')}"
        detail.phone_number = str(emp.get("phone", ""))
        avatar = emp.get("avatar")
        if avatar:
            avatar_url = avatar.replace("\\", "/")
            detail.ids.profile_pic.source = f"http://127.0.0.1:8000/{avatar_url}"
        else:
            detail.ids.profile_pic.source = "avatar.png"
        self.manager.current = 'staff_detail'

class StaffDetailScreen(Screen):
    phone_number = StringProperty("")

    def make_call(self):
        webbrowser.open(f"tel:{self.phone_number}")

    def open_whatsapp(self):
        webbrowser.open(f"https://wa.me/{self.phone_number}")

class ErrorReportScreen(Screen):
    dialog = None

    def on_enter(self):
        self.time_event = Clock.schedule_interval(self.update_time, 1)
        self.load_reports()

    def on_leave(self):
        if hasattr(self, 'time_event'):
            Clock.unschedule(self.time_event)

    def update_time(self, dt):
        now = datetime.now()
        self.ids.live_time.text = now.strftime("%I:%M:%S %p")
        self.ids.cal_day.text = now.strftime("%d")
        self.ids.cal_month.text = now.strftime("%b").upper()

    def load_reports(self):
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._load_reports_async, args=(app.user_id,), daemon=True)
        t.start()

    def _load_reports_async(self, user_id):
        try:
            url = f"http://127.0.0.1:8000/reports/{user_id}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json() or []
                Clock.schedule_once(lambda dt: self._update_report_list(data))
            else:
                Clock.schedule_once(lambda dt: toast("Failed to load reports"))
        except:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _update_report_list(self, reports):
        self.ids.report_list.clear_widgets()

        reports = sorted(
            reports,
            key=lambda r: str(r.get("timestamp", "")),
            reverse=True
        )

        if not reports:
            no_reports = MDBoxLayout(
                orientation="vertical",
                padding="10dp",
                size_hint_y=None,
                height="50dp"
            )
            no_reports.add_widget(MDLabel(
                text="No reports available",
                font_style="Body1"
            ))
            no_reports.add_widget(MDLabel(
                text="Submit a report above to see it here.",
                font_style="Caption",
                theme_text_color="Secondary"
            ))
            self.ids.report_list.add_widget(no_reports)
            return

        for report in reports:
            status = report.get("status", "pending")
            timestamp = str(report.get("timestamp", ""))[:16]
            primary = report.get("description", "No description")
            secondary = f"Status: {status.title()}  |  {timestamp}"

            # Create a card for each report
            card = MDCard(
                radius=[10],
                elevation=0,
                padding="10dp",
                size_hint_y=None,
                adaptive_height=True,
                md_bg_color=(1, 1, 1, 1)
            )
            card.line_color = (0, 0, 0, 1)
            card.line_width = 0.6

            layout = MDBoxLayout(orientation="horizontal", spacing="10dp", adaptive_height=True)

            # Text layout
            text_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.8, adaptive_height=True)
            text_layout.add_widget(MDLabel(
                text=primary,
                font_style="Body1",
                adaptive_height=True,
                halign="left"
            ))
            if status == "completed":
                text_layout.add_widget(MDLabel(
                    text=secondary,
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=(0, 0.6, 0, 1),
                    adaptive_height=True,
                    halign="left"
                ))
            else:
                text_layout.add_widget(MDLabel(
                    text=secondary,
                    font_style="Caption",
                    theme_text_color="Secondary",
                    adaptive_height=True,
                    halign="left"
                ))

            layout.add_widget(text_layout)

            # Action button for pending reports only
            if status == "pending":
                button = MDIconButton(
                    icon="close-circle-outline",
                    theme_text_color="Custom",
                    text_color=(0.8, 0.2, 0.2, 1)
                )
                button.bind(on_release=lambda x, r_id=report.get("report_id"): self.cancel_report(r_id))
                layout.add_widget(button)

            card.add_widget(layout)
            self.ids.report_list.add_widget(card)

        # Ensure the report list height is always up to date after adding items
        try:
            self.ids.report_list.height = self.ids.report_list.minimum_height
        except Exception:
            pass

    def resolve_report(self, report_id):
        if report_id is None:
            return
        t = threading.Thread(target=self._resolve_report_async, args=(report_id,), daemon=True)
        t.start()

    def _resolve_report_async(self, report_id):
        app = MDApp.get_running_app()
        try:
            resp = requests.post(
                f"http://127.0.0.1:8000/reports/{report_id}/resolve",
                params={"ho_id": app.user_id},
                timeout=5
            )
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Report marked corrected."))
                Clock.schedule_once(lambda dt: self.load_reports())
            else:
                Clock.schedule_once(lambda dt: toast("Failed to resolve report."))
        except:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def cancel_report(self, report_id):
        if report_id is None:
            return
        t = threading.Thread(target=self._cancel_report_async, args=(report_id,), daemon=True)
        t.start()

    def _cancel_report_async(self, report_id):
        app = MDApp.get_running_app()
        try:
            resp = requests.post(
                f"http://127.0.0.1:8000/reports/{report_id}/cancel",
                params={"emp_id": app.user_id},
                timeout=5
            )
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Report cancelled."))
                Clock.schedule_once(lambda dt: self.load_reports())
            else:
                Clock.schedule_once(lambda dt: toast("Failed to cancel report."))
        except:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def submit_report(self):
        report_text = self.ids.error_input.text.strip()
        if not report_text:
            Clock.schedule_once(lambda dt: toast("Please enter a report description"))
            return
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._submit_async, args=(app.user_id, report_text), daemon=True)
        t.start()

    def _submit_async(self, uid, text):
        try:
            resp = requests.post("http://127.0.0.1:8000/reports", params={"emp_id": uid, "description": text}, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                report_num = data.get("id", "N/A")
                Clock.schedule_once(lambda dt: self._on_submit_success(report_num))
            else:
                Clock.schedule_once(lambda dt: toast("Server Error"))

        except:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _on_submit_success(self, report_num):
        self.ids.error_input.text = ""
        self.load_reports()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Report Submitted",
                text=f"Your report has been submitted. Reference ID: {report_num}",
                size_hint=(0.8, None),
                buttons=[
                    MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())
                ],
            )
        else:
            self.dialog.text = f"Your report has been submitted. Reference ID: {report_num}"
        self.dialog.open()

class ErrorResolveScreen(Screen):
    def on_enter(self):
        self.load_all_reports()

    def load_all_reports(self):
        self.ids.resolve_report_list.clear_widgets()
        t = threading.Thread(target=self._load_all_reports_async, daemon=True)
        t.start()

    def _load_all_reports_async(self):
        try:
            resp = requests.get("http://127.0.0.1:8000/reports/all", timeout=5)
            if resp.status_code == 200:
                data = resp.json() or {}
                if isinstance(data, dict):
                    reports = data.get("reports", [])
                elif isinstance(data, list):
                    reports = data
                else:
                    reports = []
                Clock.schedule_once(lambda dt: self._update_resolve_list(reports))
            else:
                Clock.schedule_once(lambda dt: toast("Failed to load reports"))
        except Exception as e:
            print(f"Error loading all user reports: {e}")
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _update_resolve_list(self, reports):
        self.ids.resolve_report_list.clear_widgets()
        reports = sorted(
            reports,
            key=lambda r: str(r.get("timestamp", "")),
            reverse=True
        )

        if not reports:
            no_reports = MDBoxLayout(
                orientation="vertical",
                padding="10dp",
                size_hint_y=None,
                height="60dp"
            )
            no_reports.add_widget(MDLabel(
                text="No reports available",
                font_style="Body1"
            ))
            no_reports.add_widget(MDLabel(
                text="All reports are already completed.",
                font_style="Caption",
                theme_text_color="Secondary"
            ))
            self.ids.resolve_report_list.add_widget(no_reports)
            return

        for report in reports:
            status = report.get("status", "pending")
            timestamp = str(report.get("timestamp", ""))[:16]
            employee_id = report.get("emp_id", "--")
            primary = report.get("description", "No description")
            secondary = f"From: {employee_id}  |  {timestamp}  |  {status.title()}"

            card = MDCard(
                radius=[10],
                elevation=0,
                padding="10dp",
                size_hint_y=None,
                adaptive_height=True,
                md_bg_color=(1, 1, 1, 1)
            )
            card.line_color = (0, 0, 0, 1)
            card.line_width = 0.6

            layout = MDBoxLayout(orientation="horizontal", spacing="10dp", adaptive_height=True)
            checkbox = MDCheckbox(
                size_hint=(None, None),
                size=("40dp", "40dp"),
                active=status in ("completed", "resolved"),
                disabled=status in ("completed", "resolved")
            )
            checkbox.bind(active=lambda instance, value, r_id=report.get("report_id"), st=status: self._on_checkbox_active(value, r_id, st))

            text_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.9, adaptive_height=True)
            text_layout.add_widget(MDLabel(
                text=primary,
                font_style="Body1",
                adaptive_height=True,
                halign="left"
            ))
            if status == "completed":
                text_layout.add_widget(MDLabel(
                    text=secondary,
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=(0, 0.6, 0, 1),
                    adaptive_height=True,
                    halign="left"
                ))
            else:
                text_layout.add_widget(MDLabel(
                    text=secondary,
                    font_style="Caption",
                    theme_text_color="Secondary",
                    adaptive_height=True,
                    halign="left"
                ))

            layout.add_widget(checkbox)
            layout.add_widget(text_layout)
            card.add_widget(layout)
            self.ids.resolve_report_list.add_widget(card)

    def _on_checkbox_active(self, value, report_id, status):
        if value and status == "pending":
            self.mark_completed(report_id)

    def mark_completed(self, report_id):
        t = threading.Thread(target=self._mark_completed_async, args=(report_id,), daemon=True)
        t.start()

    def _mark_completed_async(self, report_id):
        app = MDApp.get_running_app()
        try:
            resp = requests.post(
                f"http://127.0.0.1:8000/reports/{report_id}/resolve",
                params={"ho_id": app.user_id},
                timeout=5
            )
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Report marked completed."))
                Clock.schedule_once(lambda dt: self.load_all_reports())
            else:
                Clock.schedule_once(lambda dt: toast("Failed to mark completed"))
        except:
            Clock.schedule_once(lambda dt: toast("Connection Error"))


class DocShareScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
             exit_manager=self.exit_manager,
             select_path=self.select_path,
            preview=False,
        )
        # Show documents/files (not just folders) and filter to common document types.
        self.file_manager.selector = "file"
        self.file_manager.ext = [
            ".txt",
            ".pdf",
            ".doc",
            ".docx",
            ".ppt",
            ".pptx",
            ".xls",
            ".xlsx",
            ".csv",
            ".jpg",
            ".jpeg",
            ".png",
        ]
        self.file_manager.show_hidden_files = True

    def open_manager(self):
        self.file_manager.show(os.path.expanduser("~"))

    def select_path(self, path):
        self.exit_manager()
        Clock.schedule_once(lambda dt: self._set_uploaded_file_box(path))
        allowed_ext = (
            ".txt",
            ".pdf",
            ".doc",
            ".docx",
            ".ppt",
            ".pptx",
            ".xls",
            ".xlsx",
            ".csv",
            ".jpg",
            ".jpeg",
            ".png",
        )
        if path.lower().endswith(allowed_ext):
            # proceed with upload
            app = MDApp.get_running_app()
            reason = self.ids.upload_reason.text.strip()
            if not reason:
                Clock.schedule_once(lambda dt: toast("Please enter a reason for upload"))
                return

            t = threading.Thread(target=self._upload_async, args=(app.user_id, path, reason), daemon=True)
            t.start()
        else:
            Clock.schedule_once(lambda dt: toast("Unsupported file type"))

    def _set_uploaded_file_box(self, path: str):
        try:
            self.ids.uploaded_file.text = os.path.basename(path) if path else ""
        except Exception:
            pass


    def _upload_async(self, uid, path, reason):
        try:
            files = {"file": open(path, "rb")}
            data = {"emp_id": uid, "reason": reason}
            resp = requests.post("http://127.0.0.1:8000/upload-doc", data=data, files=files)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Document Uploaded Successfully"))
                Clock.schedule_once(lambda dt: self._set_uploaded_file_box(path))
            else:
                # Show backend message (helps debug)
                detail = ""
                try:
                    detail = resp.json().get("detail", "")
                except Exception:
                    detail = resp.text or ""
                Clock.schedule_once(lambda dt, d=detail: toast(f"Upload Failed {('- ' + d) if d else ''}"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))


    def exit_manager(self, *args):
        try:
            self.file_manager.close()
        except Exception:
            pass


class CircularsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        self.file_manager.selector = "file"
        self.file_manager.ext = [".txt", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"]
        self.file_manager.show_hidden_files = True

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        is_ho = str(getattr(app, "user_branch_code", "")).strip() == "109000"
        upload_card = self.ids.circular_upload_card
        upload_card.opacity = 1 if is_ho else 0
        upload_card.disabled = not is_ho
        upload_card.height = upload_card.minimum_height if is_ho else 0
        self.load_circulars()

    def open_manager(self):
        self.file_manager.show(os.path.expanduser("~"))

    def select_path(self, path):
        self.exit_manager()
        if not path:
            return
        self.ids.circular_selected_file.text = os.path.basename(path)
        if not path.lower().endswith((".txt", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv")):
            toast("Unsupported file type")
            return
        app = MDApp.get_running_app()
        t = threading.Thread(target=self._upload_circular_async, args=(app.user_id, path), daemon=True)
        t.start()

    def _upload_circular_async(self, uid, path):
        try:
            with open(path, "rb") as handle:
                files = {"file": (os.path.basename(path), handle, "application/octet-stream")}
                data = {"emp_id": uid}
                resp = requests.post("http://127.0.0.1:8000/upload-circular", data=data, files=files, timeout=20)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Circular uploaded successfully"))
                Clock.schedule_once(lambda dt: self.load_circulars())
            else:
                try:
                    detail = resp.json().get("detail", "Upload failed")
                except Exception:
                    detail = resp.text or "Upload failed"
                Clock.schedule_once(lambda dt, d=detail: toast(d))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def load_circulars(self):
        threading.Thread(target=self._load_circulars_async, daemon=True).start()

    def _load_circulars_async(self):
        try:
            resp = requests.get("http://127.0.0.1:8000/circulars", timeout=20)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt, data=resp.json(): self._populate_circulars(data))
            else:
                Clock.schedule_once(lambda dt: toast("Failed to load circulars"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _populate_circulars(self, data):
        self.ids.circulars_list.clear_widgets()
        if not data:
            self.ids.circulars_list.add_widget(
                TwoLineListItem(
                    text="No circulars available",
                    secondary_text="Head office uploads will appear here."
                )
            )
            return

        for doc in data:
            uploaded_at = doc.get("uploaded_at", "") or ""
            when_text = uploaded_at[:16].replace("T", " ") if uploaded_at else "Unknown time"
            item = ThreeLineAvatarListItem(
                text="Circular from HO",
                secondary_text=f"ID: {doc.get('emp_id', '--')} | Name: {doc.get('sender_name', 'Unknown')}",
                tertiary_text=f"{doc.get('filename', '')} | Sent: {when_text}",
            )
            # item.add_widget(ImageLeftWidget(source="backend/static/avatars/kerala_bank_login_logo.png"))
            item.bind(on_release=lambda x, d=doc: self.download_circular(d))
            self.ids.circulars_list.add_widget(item)

    def download_circular(self, doc):
        threading.Thread(target=self._download_circular_async, args=(doc,), daemon=True).start()

    def _download_circular_async(self, doc):
        try:
            doc_id = doc.get("doc_id")
            resp = requests.get(f"http://127.0.0.1:8000/circulars/download/{doc_id}", timeout=30)
            if resp.status_code != 200:
                Clock.schedule_once(lambda dt: toast("Failed to download circular"))
                return
            filename = doc.get("filename") or f"circular_{doc_id}"
            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.isdir(downloads_dir):
                downloads_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(downloads_dir, exist_ok=True)
            file_path = os.path.join(downloads_dir, filename)
            with open(file_path, "wb") as output:
                output.write(resp.content)
            Clock.schedule_once(lambda dt, name=filename: toast(f"Downloaded {name}"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def exit_manager(self, *args):
        try:
            self.file_manager.close()
        except Exception:
            pass


class ConsolidationScreen(Screen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        is_ho = str(getattr(app, "user_branch_code", "")).strip() == "109000"
        input_card = self.ids.consolidation_input_card
        input_card.opacity = 1 if is_ho else 0
        input_card.disabled = not is_ho
        input_card.height = input_card.minimum_height if is_ho else 0
        self.load_links()

    def add_link(self):
        heading = self.ids.consolidation_heading.text.strip()
        link_url = self.ids.consolidation_link.text.strip()
        if not heading:
            toast("Please enter heading")
            return
        if not link_url:
            toast("Please enter link")
            return
        app = MDApp.get_running_app()
        payload = {
            "emp_id": app.user_id,
            "heading": heading,
            "link_url": link_url,
        }
        threading.Thread(target=self._add_link_async, args=(payload,), daemon=True).start()

    def _add_link_async(self, payload):
        try:
            resp = requests.post("http://127.0.0.1:8000/consolidation-links", json=payload, timeout=20)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Link added"))
                Clock.schedule_once(lambda dt: setattr(self.ids.consolidation_heading, "text", ""))
                Clock.schedule_once(lambda dt: setattr(self.ids.consolidation_link, "text", ""))
                Clock.schedule_once(lambda dt: self.load_links())
            else:
                try:
                    detail = resp.json().get("detail", "Failed to add link")
                except Exception:
                    detail = resp.text or "Failed to add link"
                Clock.schedule_once(lambda dt, d=detail: toast(d))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def load_links(self):
        threading.Thread(target=self._load_links_async, daemon=True).start()

    def _load_links_async(self):
        try:
            resp = requests.get("http://127.0.0.1:8000/consolidation-links", timeout=20)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt, data=resp.json(): self._populate_links(data))
            else:
                Clock.schedule_once(lambda dt: toast("Failed to load links"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def _populate_links(self, data):
        self.ids.consolidation_links_list.clear_widgets()
        if not data:
            self.ids.consolidation_links_list.add_widget(
                TwoLineListItem(
                    text="No consolidation links available",
                    secondary_text="109000 users can add Google Sheet links here."
                )
            )
            return

        for item_data in data:
            created_at = (item_data.get("created_at") or "")[:16].replace("T", " ")
            item = ThreeLineAvatarListItem(
                text=item_data.get("heading", "Untitled"),
                secondary_text=item_data.get("link_url", ""),
                tertiary_text=f"Added by {item_data.get('created_by_name') or item_data.get('created_by') or '--'} | {created_at or 'Unknown time'}",
                secondary_font_style="Caption",
                tertiary_font_style="Caption",
            )
            item.add_widget(IconLeftWidget(icon="link-variant"))
            item.bind(on_release=lambda x, url=item_data.get("link_url", ""): self.open_link(url))
            self.ids.consolidation_links_list.add_widget(item)

    def open_link(self, url):
        if not url:
            toast("Link not available")
            return
        try:
            webbrowser.open(url)
        except Exception:
            toast("Could not open link")


class FinacleHelpScreen(Screen):
    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        self._is_finacle_editor = str(getattr(app, "user_branch_code", "")).strip() == "109000"
        self._show_loading_state()
        self.load_finacle_entries()

    def open_add_screen(self):
        if not getattr(self, "_is_finacle_editor", False):
            toast("Only 109000 users can add Finacle Help items")
            return
        self.manager.current = 'add_finacle_help'

    def _show_loading_state(self):
        container = self.ids.finacle_help_sections
        container.clear_widgets()
        # Don't add any loading widget to avoid space
        pass

    def load_finacle_entries(self):
        thread_pool.submit(self._load_finacle_entries_async)

    def _load_finacle_entries_async(self):
        try:
            # Use shorter timeout and streaming for faster response
            resp = requests.get("http://127.0.0.1:8000/finacle-help", timeout=5, stream=True)
            if resp.status_code == 200:
                # Parse JSON immediately to free up connection
                data = resp.json()
                Clock.schedule_once(lambda dt, data=data: self._populate_sections(data))
            else:
                Clock.schedule_once(lambda dt: self._populate_sections([]))
        except requests.exceptions.Timeout:
            Clock.schedule_once(lambda dt: toast("Loading timeout - please try again"))
            Clock.schedule_once(lambda dt: self._populate_sections([]))
        except Exception:
            Clock.schedule_once(lambda dt: self._populate_sections([]))

    def _group_entries_by_section(self, entries):
        grouped = []
        section_lookup = {}
        # Pre-allocate dictionary for better performance
        for entry in (entries or []):
            section_title = entry.get("section_title", "").strip()
            menu_code = entry.get("menu_code", "").strip()
            description = entry.get("description", "").strip()
            if not section_title or not menu_code:
                continue
            key = section_title.lower()
            if key not in section_lookup:
                section_lookup[key] = {"title": section_title, "items": []}
                grouped.append(section_lookup[key])
            section_lookup[key]["items"].append((menu_code, description))
        return grouped

    def _build_section_markup(self, items):
        lines = []
        for menu_code, description in items:
            code_markup = (
                f"[color=#1F3B78][b]{menu_code}[/b][/color]"
            )
            if description:
                lines.append(f"{code_markup}\n[color=#5E677A]{description}[/color]")
            else:
                lines.append(code_markup)
        return "\n\n".join(lines)

    def _populate_sections(self, custom_entries=None):
        container = self.ids.finacle_help_sections
        container.clear_widgets()
        grouped_sections = self._group_entries_by_section(custom_entries)
        if not grouped_sections:
            # Don't create empty card to avoid space
            empty_label = MDLabel(
                text="No Finacle Help data available.",
                adaptive_height=True,
                theme_text_color="Secondary",
                halign="center",
            )
            container.add_widget(empty_label)
            return

        for section in grouped_sections:
            card = MDCard(
                orientation="vertical",
                adaptive_height=True,
                elevation=0.22,
                radius=[14, 14, 14, 14],
                padding="0dp",
                spacing="0dp",
                md_bg_color=(1, 1, 1, 1),
            )

            title_bar = MDBoxLayout(
                orientation="horizontal",
                adaptive_height=True,
                padding=("12dp", "10dp"),
                spacing="8dp",
                md_bg_color=(0.91, 0.94, 0.98, 1),
            )
            title_bar.add_widget(
                MDLabel(
                    text=section["title"].upper(),
                    adaptive_height=True,
                    bold=True,
                    size_hint_x=1,
                    theme_text_color="Custom",
                    text_color=(0.09, 0.18, 0.36, 1),
                )
            )
            if getattr(self, "_is_finacle_editor", False):
                add_here = MDRaisedButton(
                    text="ADD HERE",
                    size_hint_x=None,
                    width=dp(96),
                    elevation=0,
                    md_bg_color=(0.12, 0.23, 0.47, 1),
                )
                add_here.bind(on_release=lambda instance, title=section["title"]: self.prefill_section(title))
                title_bar.add_widget(add_here)
            card.add_widget(title_bar)

            body = MDBoxLayout(
                orientation="vertical",
                adaptive_height=True,
                padding="12dp",
                spacing="0dp",
            )
            body.add_widget(
                MDLabel(
                    text=self._build_section_markup(section["items"]),
                    markup=True,
                    adaptive_height=True,
                    halign="left",
                    text_size=(dp(292), None),
                )
            )
            card.add_widget(body)
            container.add_widget(card)


class AddFinacleHelpScreen(Screen):
    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        self._is_finacle_editor = str(getattr(app, "user_branch_code", "")).strip() == "109000"
        if not self._is_finacle_editor:
            toast("Only 109000 users can add Finacle Help items")
            self.manager.current = 'finacle_help'
    
    def save_entry(self):
        if not getattr(self, "_is_finacle_editor", False):
            toast("Only 109000 users can add Finacle Help items")
            return
        
        section_title = self.ids.finacle_section_title.text.strip()
        menu_code = self.ids.finacle_menu_code.text.strip()
        description = self.ids.finacle_menu_description.text.strip()
        
        if not section_title:
            toast("Please enter section title")
            return
        if not menu_code:
            toast("Please enter menu code")
            return
        
        app = MDApp.get_running_app()
        payload = {
            "emp_id": app.user_id,
            "section_title": section_title,
            "menu_code": menu_code,
            "description": description,
        }
        thread_pool.submit(self._save_entry_async, payload)
    
    def _save_entry_async(self, payload):
        try:
            resp = requests.post("http://127.0.0.1:8000/finacle-help", json=payload, timeout=10)
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Finacle Help entry saved successfully"))
                Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'finacle_help'))
            else:
                try:
                    detail = resp.json().get("detail", "Failed to save")
                except Exception:
                    detail = resp.text or "Failed to save"
                Clock.schedule_once(lambda dt, d=detail: toast(d))
        except requests.exceptions.Timeout:
            Clock.schedule_once(lambda dt: toast("Save timeout - please try again"))
        except Exception:
            Clock.schedule_once(lambda dt: toast("Connection Error"))


class UrgentScreen(Screen):
    report_dialog = None
    message_dialog = None
    _message_receipts_label = None
    _opened_urgent_ids = set()
    _urgent_items = {}

    def load_urgent_dashboard(self):
            app = MDApp.get_running_app()
            # Employee 426 has branch 109000, so this check will work
            is_ho = str(app.user_branch_code).strip() == "109000"
            
            if is_ho:
                self.ids.ho_input_area.opacity = 1
                self.ids.ho_input_area.disabled = False
                # This ensures the widget actually occupies space when visible
                self.ids.ho_input_area.height = "80dp" 
            else:
                self.ids.ho_input_area.opacity = 0
                self.ids.ho_input_area.disabled = True
                self.ids.ho_input_area.height = "0dp"

            self.ids.urgent_list.clear_widgets()
            threading.Thread(target=self._fetch_messages, daemon=True).start()

    def _fetch_messages(self):
        try:
            response = requests.get("http://127.0.0.1:8000/urgent")
            if response.status_code == 200:
                messages = response.json()
                # Backend returns newest first; keep order as-is.
                # Update UI on main thread
                Clock.schedule_once(lambda dt: self.update_urgent_list(messages))
        except:
            Clock.schedule_once(lambda dt: toast("Could not load alerts"))

    def update_urgent_list(self, messages):
        self.ids.urgent_list.clear_widgets()
        for msg in messages:
            sender = msg.get("sender") or {}
            sender_name = sender.get("name") or "Unknown"
            sender_id = sender.get("emp_id") or "--"
            time_str = (msg.get("timestamp") or "")[:16]

            # Create a list item for each message
            item = ThreeLineAvatarListItem(
                text="Message from HO",
                secondary_text=f"{time_str}",
                tertiary_text="Tap to view the alert",
                secondary_font_style="Caption",
                tertiary_font_style="Caption",
                theme_text_color="Custom",
                text_color=(0.1, 0.1, 0.1, 1),
            )
            item.urgent_id = msg.get("id")
            self._urgent_items[item.urgent_id] = item
            if item.urgent_id in self._opened_urgent_ids:
                item.md_bg_color = (0.92, 0.92, 0.92, 1)
                item.text_color = (0.4, 0.4, 0.4, 1)
                item.secondary_text_color = (0.5, 0.5, 0.5, 1)

            # Add an alert icon to each message
            from kivymd.uix.list import IconLeftWidget
            item.add_widget(IconLeftWidget(icon="alert-decagram", theme_text_color="Custom", text_color=(0.8, 0, 0, 1)))
            item.bind(on_release=lambda x, m=msg: self.open_message_popup(m))
            
            self.ids.urgent_list.add_widget(item)

    def open_message_popup(self, msg: dict):
        sender = msg.get("sender") or {}
        sender_name = sender.get("name") or "Unknown"
        sender_id = sender.get("emp_id") or "--"
        time_str = (msg.get("timestamp") or "")[:16]
        content = msg.get("content", "")
        urgent_id = msg.get("id")

        from kivy.metrics import dp

        container = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            padding=("12dp", "12dp"),
            adaptive_height=True,
        )

        header_row = MDBoxLayout(
            orientation="horizontal",
            spacing="8dp",
            adaptive_height=True,
        )
        sender_label = MDLabel(
            text=f"{sender_name} (ID: {sender_id})",
            font_style="Subtitle2",
            bold=True,
            adaptive_height=True,
            halign="left",
            size_hint_x=0.7,
        )
        timestamp_label = MDLabel(
            text=time_str,
            font_style="Caption",
            theme_text_color="Secondary",
            adaptive_height=True,
            halign="right",
            size_hint_x=0.3,
        )
        header_row.add_widget(sender_label)
        header_row.add_widget(timestamp_label)

        message_card = MDCard(
            radius=[10],
            elevation=1,
            padding=("14dp", "14dp"),
            size_hint_y=None,
            adaptive_height=True,
        )
        message_label = MDLabel(
            text=content,
            font_style="Body1",
            adaptive_height=True,
            halign="left",
            text_size=(dp(260), None),
        )
        message_card.add_widget(message_label)

        receipts_title = MDLabel(
            text="Seen by",
            font_style="Caption",
            bold=True,
            adaptive_height=True,
            halign="left",
        )

        receipts_card = MDCard(
            radius=[10],
            elevation=1,
            padding=("10dp", "10dp"),
            size_hint_y=None,
            adaptive_height=True,
        )
        receipts_label = MDLabel(
            text="Loading...",
            font_style="Caption",
            adaptive_height=True,
            halign="left",
            text_size=(dp(260), None),
        )
        receipts_card.add_widget(receipts_label)

        container.add_widget(header_row)
        container.add_widget(message_card)
        container.add_widget(receipts_title)
        container.add_widget(receipts_card)

        self._message_receipts_label = receipts_label

        if self.message_dialog:
            self.message_dialog.dismiss()

        self.message_dialog = MDDialog(
            title="Urgent Alert",
            type="custom",
            content_cls=container,
            size_hint=(0.9, None),
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: self.message_dialog.dismiss())
            ],
        )
        self.message_dialog.open()

        # Mark the item opened in the UI and preserve its visited state
        if urgent_id is not None:
            self._opened_urgent_ids.add(urgent_id)
            self._mark_item_opened(urgent_id)

        # Automatically mark this message as seen for branch employees when they open the alert
        app = MDApp.get_running_app()
        if urgent_id is not None and str(app.user_branch_code).strip() != "109000":
            threading.Thread(target=self._ack_async, args=(app.user_id, urgent_id), daemon=True).start()

        # Fetch read receipts list in background and update the receipts box
        if urgent_id is not None:
            threading.Thread(target=self._fetch_read_receipts_for_popup, args=(urgent_id,), daemon=True).start()

    def _fetch_read_receipts_for_popup(self, urgent_id: int):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/urgent/report/{urgent_id}", timeout=5)
            if resp.status_code == 200:
                data = resp.json() or []
                Clock.schedule_once(lambda dt: self._update_receipts_popup(data))
            else:
                Clock.schedule_once(lambda dt: self._update_receipts_popup([]))
        except Exception:
            Clock.schedule_once(lambda dt: self._set_receipts_text("Could not load read receipts."))

    def _update_receipts_popup(self, data):
        if not data:
            self._set_receipts_text("No one has acknowledged this alert yet.")
            return

        lines = []
        for d in data:
            emp_id = d.get("emp_id", "--")
            seen_at = str(d.get("seen_at", ""))[:16]
            if seen_at:
                lines.append(f"• {emp_id}  •  {seen_at}")
            else:
                lines.append(f"• {emp_id}")
        self._set_receipts_text("\n".join(lines))

    def _set_receipts_text(self, text: str):
        try:
            if self._message_receipts_label:
                self._message_receipts_label.text = text
        except Exception:
            pass

    def _mark_item_opened(self, urgent_id):
        item = self._urgent_items.get(urgent_id)
        if item:
            item.md_bg_color = (0.92, 0.92, 0.92, 1)
            item.theme_text_color = "Custom"
            item.text_color = (0.4, 0.4, 0.4, 1)
            try:
                item.secondary_text_color = (0.5, 0.5, 0.5, 1)
            except Exception:
                pass

    def _populate_list(self, messages):
        app = MDApp.get_running_app()
        self.ids.urgent_list.clear_widgets()
        
        for msg in messages:
            # Format time for display
            time_str = msg.get("timestamp", "")[:16].replace("T", " ")
            
            item = TwoLineListItem(
                text=f"CRITICAL: {msg.get('content', '')}",
                secondary_text=f"Sent: {time_str} | Tap for options",
                theme_text_color="Error" 
            )
            
            # Logic branch based on Role:
            if app.user_branch_code == "109000":
                # HO Employees tap to see the Read Receipt Report
                item.bind(on_release=lambda x, m_id=msg['id']: self.show_report(m_id))
            else:
                # Normal Employees tap to acknowledge they have seen it
                item.bind(on_release=lambda x, m_id=msg['id']: self.acknowledge_alert(m_id))
            
            self.ids.urgent_list.add_widget(item)

    # --- SENDER LOGIC (HO ONLY) ---
    def send_alert(self):
            app = MDApp.get_running_app()
            msg = self.ids.urgent_msg_input.text.strip()
            if not msg:
                return

            def task():
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/urgent", 
                        params={"emp_id": app.user_id, "content": msg},
                        timeout=10
                    )
                    if response.status_code == 200:
                        Clock.schedule_once(lambda dt: self.after_send_success())
                    else:
                        error_text = response.text or f"{response.status_code}"
                        Clock.schedule_once(lambda dt: toast(f"Failed to broadcast: {error_text}"))
                except Exception as e:
                    Clock.schedule_once(lambda dt: toast(f"Connection Error: {e}"))

            threading.Thread(target=task, daemon=True).start()

    def after_send_success(self):
            self.ids.urgent_msg_input.text = ""
            toast("Message broadcasted to all branches")
            self.load_urgent_dashboard() # This reloads the list

    def _send_alert_async(self, uid, content):
        try:
            resp = requests.post("http://127.0.0.1:8000/urgent", params={"emp_id": uid, "content": content})
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Alert Broadcasted to all Branches!"))
                Clock.schedule_once(lambda dt: self.clear_input())
                self.load_urgent_dashboard() # Refresh list
            else:
                Clock.schedule_once(lambda dt: toast(f"Error: Not Authorized"))
        except:
            Clock.schedule_once(lambda dt: toast("Connection Error"))

    def clear_input(self):
        self.ids.urgent_msg_input.text = ""

    # --- ACKNOWLEDGE LOGIC (BRANCH EMPLOYEES) ---
    def acknowledge_alert(self, urgent_id):
        app = MDApp.get_running_app()
        threading.Thread(target=self._ack_async, args=(app.user_id, urgent_id), daemon=True).start()

    def _ack_async(self, uid, urgent_id):
        try:
            resp = requests.post("http://127.0.0.1:8000/urgent/seen", params={"emp_id": uid, "urgent_id": urgent_id})
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: toast("Alert Acknowledged. HQ Notified."))
        except:
            Clock.schedule_once(lambda dt: toast("Failed to send receipt."))

    # --- REPORT LOGIC (HO ONLY) ---
    def show_report(self, urgent_id):
        threading.Thread(target=self._fetch_report, args=(urgent_id,), daemon=True).start()

    def _fetch_report(self, urgent_id):
        try:
            resp = requests.get(f"http://127.0.0.1:8000/urgent/report/{urgent_id}")
            if resp.status_code == 200:
                data = resp.json()
                Clock.schedule_once(lambda dt: self._display_report_dialog(data))
        except:
            Clock.schedule_once(lambda dt: toast("Error fetching report"))

    def _display_report_dialog(self, data):
        if not data:
            report_text = "No one has acknowledged this alert yet."
        else:
            text_lines = [f"• {d['name']} ({d['branch']})" for d in data]
            report_text = "\n".join(text_lines)
            
        if self.report_dialog:
            self.report_dialog.dismiss()
            
        self.report_dialog = MDDialog(
            title="Read Receipts",
            text=report_text,
            size_hint=(0.9, None),
            buttons=[
                MDFlatButton(text="CLOSE", theme_text_color="Error", on_release=lambda x: self.report_dialog.dismiss())
            ]
        )
        self.report_dialog.open()


class PasswordScreen(Screen):
    # 1. The visibility toggle (Fixes your eye button)
    def toggle_password_visibility(self, field, button=None):
        # KivyMD 1.2.0 can keep the mask until the widget repaints.
        # Force a repaint by bouncing focus and re-setting text.
        current_text = field.text
        was_focused = bool(getattr(field, "focus", False))

        field.password = not field.password
        if button is not None:
            button.icon = "eye" if not field.password else "eye-off"

        def _force_repaint(_dt):
            try:
                field.focus = True
                field.text = ""
                field.text = current_text
                field.cursor = (len(current_text), 0)
                field.focus = was_focused
            except Exception:
                # If anything odd happens, at least keep the text.
                field.text = current_text

        Clock.schedule_once(_force_repaint, 0)

    # 2. The tiny error message (Fixes your text size request)
    def show_tiny_error(self, message):
        error_label = MDLabel(
            text=message,
            halign="center",
            theme_text_color="Error",
            font_style="Caption", 
            font_size="11sp",      # Very small text as requested
            pos_hint={"center_x": .5, "center_y": .15}, 
            opacity=0
        )
        self.add_widget(error_label)

        anim = Animation(opacity=1, duration=0.3) + Animation(opacity=1, duration=2) + Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self.remove_widget(error_label))
        anim.start(error_label)

    # 3. Validation logic
    def validate_and_update(self):
        p1 = self.ids.new_pwd.text.strip()
        p2 = self.ids.confirm_pwd.text.strip()
        
        if not p1 or not p2:
            self.show_tiny_error("Please fill both password fields")
            return
            
        if p1 != p2:
            self.show_tiny_error("Passwords do not match! Please re-type.")
            self.ids.confirm_pwd.text = ""
            return

        app = MDApp.get_running_app()
        threading.Thread(
            target=self._update_pwd_async, 
            args=(app.user_id, p1), 
            daemon=True
        ).start()

    # 4. Async update logic
    def _update_pwd_async(self, uid, pwd):
        try:
            resp = requests.post(
                "http://127.0.0.1:8000/update-password", 
                params={"emp_id": uid, "new_pwd": pwd},
                timeout=5
            )
            if resp.status_code == 200:
                Clock.schedule_once(lambda dt: self.show_tiny_error("Success! Password updated."))
                Clock.schedule_once(lambda dt: self.reset_fields())
            else:
                Clock.schedule_once(lambda dt: self.show_tiny_error("Update Failed"))
        except:
            Clock.schedule_once(lambda dt: self.show_tiny_error("Server Connection Error"))

    def reset_fields(self):
        self.ids.new_pwd.text = ""
        self.ids.confirm_pwd.text = ""

# Keep ChatBubble below PasswordScreen
class ChatBubble(MDCard):
    sender_info = StringProperty("") 
    message_text = StringProperty("")
    timestamp = StringProperty("")
    bg_color = ColorProperty([1, 1, 1, 1])

# ------------------- App Class -------------------

class KeralaBankApp(MDApp):
    user_id = StringProperty("")
    user_name = StringProperty("")
    user_avatar = StringProperty("")
    user_branch_code = StringProperty("")
    selected_branch = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        return Builder.load_string(KV)

    def on_start(self):
        pass

    def logout(self):
        self.user_id = ""
        self.root.current = 'login'
        Clock.schedule_once(lambda dt: toast("Logged out"))

    def go_back(self):
        # simple back behavior
        if self.root.current == 'dashboard':
            self.root.current = 'login'
        else:
            self.root.current = 'dashboard'

    def change_screen(self, screen_name):
        if screen_name in self.root.screen_names:
            self.root.current = screen_name

if __name__ == '__main__':
    KeralaBankApp().run()

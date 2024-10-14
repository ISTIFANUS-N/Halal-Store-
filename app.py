import os
import sys
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
import sqlite3
from kivy.uix.filechooser import FileChooserListView
from sqlite3 import Error
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform
from kivy.graphics import Color, Ellipse, Rectangle
from datetime import datetime
from kivy.uix.scrollview import ScrollView
import pandas as pd

# Set the Kivy window size for development
Window.size = (800, 600)

# Create database and tables if they do not exist
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Example function to create a database connection
def create_connection():
    """ create a database connection to the SQLite database specified by db_file """
    connection = None
    db_file = resource_path("adashe.db")  # Use resource_path to locate the database
    try:
        connection = sqlite3.connect(db_file)
        print(f"Connection to SQLite DB '{db_file}' successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        popup = Popup(title='Database Error', content=Label(text=f"Failed to connect to database: {e}"), size_hint=(0.5, 0.5))
        popup.open()
    return connection


def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS login (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_no TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT,
            nok_name TEXT,
            nok_phone TEXT,
            date_registered TEXT,
            account_bal REAL
        )''')
        connection.commit()
    except Error as e:
        print(f"Error creating tables: {e}")

create_connection()
connection = create_connection()
create_tables(connection)

class ResponsiveBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_layout)

    def update_layout(self, *args):
        self.orientation = 'horizontal' if self.width > self.height else 'vertical'

class ResponsiveGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_layout)

    def update_layout(self, *args):
        self.cols = 2 if self.width > self.height else 1

class CustomScreen(Screen):
    def __init__(self, **kwargs):
        super(CustomScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(220, 220, 220, 0.6)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

            Color(1, 0, 0, 0.2)
            self.ellipse1 = Ellipse(size=(200, 200), pos=(self.width/4, self.height/2))

            Color(1, 1, 1, 0.2)
            self.ellipse2 = Ellipse(size=(200, 200), pos=(3*self.width/4, self.height/2))

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        self.ellipse1.pos = (self.width/4 - 100, self.height/2 - 100)
        self.ellipse2.pos = (3*self.width/4 - 100, self.height/2 - 100)

class CustomTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if not self.password:  # Allow special characters in password fields
            allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
            filtered_substring = ''.join([char for char in substring if char in allowed_chars])
            return super(CustomTextInput, self).insert_text(filtered_substring, from_undo=from_undo)
        else:
            return super(CustomTextInput, self).insert_text(substring, from_undo=from_undo)
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
      
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class LandingPage(CustomScreen):
    def __init__(self, **kwargs):
        super(LandingPage, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        header_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=150, padding=10, spacing=10)
        
        logo_path = resource_path('logo.png')
        logo = Image(source=logo_path, size_hint=(None, None), size=(100, 100))
        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=20)
        logo_layout.add_widget(logo)
        header_layout.add_widget(logo_layout)
        # header text
        header_label = Label(text='[b][color=ff0000]HALAL[/color] STORES[/b]', font_size='45sp',markup = True)
        header_layout.add_widget(header_label)
        # sub header 
        daily_contribution_label = Label(text='Daily contribution', font_size='25sp', color=('black'),height=30)
        header_layout.add_widget(daily_contribution_label)
        main_layout.add_widget(header_layout)

        layout = AnchorLayout(anchor_x='center', anchor_y='center')
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=20, size_hint=(None, None))
        content_layout.size_hint_min = (300, 150)

        label = Label(text='Your Money is Safe With Us', font_size='30sp', color=('black'),bold = True)
        content_layout.add_widget(label)
        label = Label()
        content_layout.add_widget(label)

        label = Label()
        content_layout.add_widget(label)

        label = Label()
        content_layout.add_widget(label)

        get_started_button = Button(
            text='Get Started',
            size_hint=(None, None),
            size=(150, 50),
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            bold=True,
            pos_hint={'center_x': 0.5} 
        )
        get_started_button.bind(on_press=self.go_to_login)
        content_layout.add_widget(get_started_button)

        layout.add_widget(content_layout)
        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def go_to_login(self, instance):
        self.manager.current = 'login'

class LoginPage(CustomScreen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top')

        logo_path = resource_path('logo.png')
        logo = Image(source=logo_path, size_hint=(None, None), size=(100, 100))
        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=20)
        logo_layout.add_widget(logo)

        main_layout.add_widget(logo_layout)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.7, None))
        layout.height = 400
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        label_welcome = Label(text="WELCOME BACK", font_size=30, color=('black'), size_hint=(1, None), height=50, bold=True)
        layout.add_widget(label_welcome)

        self.username_input = CustomTextInput(hint_text='Username',multiline=False, size_hint=(1, None), height=40)
        self.password_input = CustomTextInput(hint_text='Password', password=True,multiline=False, size_hint=(1, None), height=40)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        login_button = Button(text='Login', size_hint=(1, None), height=50, color=('white'), background_color=('black'))
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        register_button = Button(text="Don't have an account? Register", font_size=18, size_hint=(1, None), height=40, background_color=(1, 1, 1, 0), color=('black'))
        register_button.bind(on_press=self.go_to_register)
        layout.add_widget(register_button)

        back_button = Button(text='Back', size_hint=(1, None), height=50, background_color=('black'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            popup = Popup(title='Error', content=Label(text='Please enter both username and password'), size_hint=(0.5, 0.5))
            popup.open()
            return

        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM login WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()

            if result:
                self.manager.current = 'dashboard'
            else:
                popup = Popup(title='Error', content=Label(text='Invalid login details'), size_hint=(0.5, 0.5))
                popup.open()

        except Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_back(self, instance):
        self.manager.current = 'landing'

class RegisterPage(CustomScreen):
    def __init__(self, **kwargs):
        super(RegisterPage, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        
        logo_path = resource_path('logo.png')
        logo = Image(source=logo_path, size_hint=(None, None), size=(100, 100))
        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=20)
        logo_layout.add_widget(logo)

        main_layout.add_widget(logo_layout)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.7, None))
        layout.height = 400
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        label_register = Label(text="REGISTER", font_size=30, color=('black'), size_hint=(1, None), height=50)
        layout.add_widget(label_register)

        self.username_input = CustomTextInput(hint_text='Username', multiline=False, size_hint=(1, None), height=40)
        self.password_input = CustomTextInput(hint_text='Password', password=True, multiline=False, size_hint=(1, None), height=40)
        self.confirm_password_input = CustomTextInput(hint_text='Confirm Password', password=True, multiline=False, size_hint=(1, None), height=40)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.confirm_password_input)

        register_button = Button(text='Register', size_hint=(1, None), height=50, background_color=('black'))
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        back_button = Button(text='Back', size_hint=(1, None), height=50, background_color=('black'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if not username or not password or not confirm_password:
            popup = Popup(title='Error', content=Label(text='Please fill all fields'), size_hint=(0.5, 0.5))
            popup.open()
            return

        if password != confirm_password:
            popup = Popup(title='Error', content=Label(text='Passwords do not match'), size_hint=(0.5, 0.5))
            popup.open()
            return

        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            popup = Popup(title='Success', content=Label(text='Registration successful'), size_hint=(0.5, 0.5))
            popup.open()
            self.manager.current = 'login'
        except Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()

    def go_back(self, instance):
        self.manager.current = 'login'


class DashboardPage(CustomScreen):
    def __init__(self, **kwargs):
        super(DashboardPage, self).__init__(**kwargs)
        self.manager = kwargs.get('manager')

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Logo Layout
        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        
        logo_path = resource_path('logo.png')
        logo = Image(source=logo_path, size_hint=(None, None), size=(100, 100))
        logo_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=20)
        logo_layout.add_widget(logo)

        main_layout.add_widget(logo_layout)

        # Header Layout
        header_layout = AnchorLayout(size_hint=(1, 3))
        header_label = Label(text='DASHBOARD', font_size='30sp', color=(0, 0, 0, 1), bold=True)
        header_layout.add_widget(header_label)
        main_layout.add_widget(header_layout)

        # Total Balance Layout
        self.total_balance_label = Label(text='Total Available Balance: # 0.00', font_size='20sp', bold=True)
        main_layout.add_widget(self.total_balance_label)

        # Action Layout
        action_layout = GridLayout(cols=2, size_hint=(None, 9), height=150, padding=8, spacing=10, pos_hint={'center_x': 0.39})
        
        register_customer_button = Button(text='Register Customer', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        register_customer_button.bind(on_press=self.register_customer)
        action_layout.add_widget(register_customer_button)
        
        view_customers_button = Button(text='View Customers', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        view_customers_button.bind(on_press=self.view_customers)
        action_layout.add_widget(view_customers_button)
        
        deposit_button = Button(text='Deposit', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        deposit_button.bind(on_press=self.go_to_deposit)
        action_layout.add_widget(deposit_button)
        
        withdraw_button = Button(text='Withdraw', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        withdraw_button.bind(on_press=self.go_to_withdraw)
        action_layout.add_widget(withdraw_button)
        
        import_excel_button = Button(text='Import Excel', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        import_excel_button.bind(on_press=self.import_excel)
        action_layout.add_widget(import_excel_button)
        
        # Add button for User Details
        user_details_button = Button(text='User Details', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        user_details_button.bind(on_press=self.go_to_user_details)
        action_layout.add_widget(user_details_button)

        # Back button 
        back_button = Button(text='Back', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        back_button.bind(on_press=self.go_to_login)
        action_layout.add_widget(back_button)
        
        main_layout.add_widget(action_layout)

        self.add_widget(main_layout)

        # Load total balance
        self.update_total_balance()

    def register_customer(self, instance):
        self.manager.current = 'register_customer'
        self.update_total_balance()

    def view_customers(self, instance):
        self.manager.current = 'view_customers'


    def go_to_deposit(self, instance):
        self.manager.current = 'deposit_screen'
        self.update_total_balance

    def go_to_withdraw(self, instance):
        self.manager.current = 'withdraw_screen'
        self.update_total_balance

    def import_excel(self, instance):
        # Open file dialog to select an Excel file using FileChooserListView
        file_chooser = FileChooserListView(filters=["*.xlsx", "*.xls"])
        file_chooser.bind(on_selection=self.load_excel)

        popup = Popup(title="Select Excel File", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_excel(self, file_chooser, selection):
        if selection:
            file_path = selection[0]
            try:
                # Load the Excel file into a DataFrame
                df = pd.read_excel(file_path)

                # Connect to the SQLite database
                connection = sqlite3.connect('adashe.db')
                cursor = connection.cursor()

                # Insert each row from the DataFrame into the customers table
                for _, row in df.iterrows():
                    cursor.execute(
                        "INSERT INTO customers (phone_no, first_name, last_name, address, nok_name, nok_phone, account_bal) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (row['phone_no'], row['first_name'], row['last_name'], row['address'], row['nok_name'], row['nok_phone'], row['account_bal'])
                    )
                
                # Commit the transaction and close the connection
                connection.commit()
                popup = Popup(title='Success', content=Label(text='Excel file imported successfully'), size_hint=(0.5, 0.5))
                popup.open()

                # Update total balance after importing customers
                self.update_total_balance()

            except Exception as e:
                # Handle any errors during file processing or database operations
                popup = Popup(title='Error', content=Label(text=f"Error processing file: {e}"), size_hint=(0.5, 0.5))
                popup.open()
            finally:
                # Ensure the database connection is closed properly
                if connection:
                    connection.close()

    def update_total_balance(self):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()

            # Query the total balance
            sql_query = "SELECT SUM(account_bal) AS total_balance FROM customers"
            cursor.execute(sql_query)
            result = cursor.fetchone()
            total_balance = result[0] if result[0] is not None else 0.0

            # Update the total balance label
            self.total_balance_label.text = f'Total Available Balance: N{total_balance:,.2f}'

        except Exception as e:
            # Handle any errors during the database query
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            # Ensure the database connection is closed properly
            if connection:
                connection.close()
            
    def go_to_user_details(self, instance):
        self.manager.current = 'user_details'
        
    def go_to_login(self, instance):
        self.manager.current = 'login'    
class UserDetailsPage(CustomScreen):
    def __init__(self, **kwargs):
        super(UserDetailsPage, self).__init__(**kwargs)
        self.manager = kwargs.get('manager')

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header_label = Label(text='User Details', font_size='40sp', color=('black'))
        main_layout.add_widget(header_label)

        # Create a ScrollView for user details
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.user_details_layout = GridLayout(cols=4, padding=[10, 20, 10, 20], spacing=20, size_hint_y=None)
        self.user_details_layout.bind(minimum_height=self.user_details_layout.setter('height'))
        
        scroll_view.add_widget(self.user_details_layout)
        main_layout.add_widget(scroll_view)

        # Load user details
        self.load_user_details()

        # Back Button
        back_button = Button(text='Back to Dashboard', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 50))
        back_button.bind(on_press=self.go_to_dashboard)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def load_user_details(self):
        # Clear existing widgets in user_details_layout
        self.user_details_layout.clear_widgets()

        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            cursor.execute("SELECT username, password FROM login")  # Modify this query if the table name is different
            users = cursor.fetchall()

            if users:
                # Add headers with extra spacing
                self.user_details_layout.add_widget(Label(text="Username", font_size='20sp', color=('black'), bold=True))
                self.user_details_layout.add_widget(Label(text="Password", font_size='20sp', color=('black'), bold=True))
                self.user_details_layout.add_widget(Label(text="Actions", font_size='20sp', color=('black'), bold=True))
                self.user_details_layout.add_widget(Label(text="Change Password", font_size='20sp', color=('black'), bold=True))

                # Add user details with extra spacing
                for user in users:
                    username, _ = user
                    self.user_details_layout.add_widget(Label(text=username, font_size='20sp', color=('black'), halign='left'))
                    self.user_details_layout.add_widget(Label(text='******', font_size='20sp', color=('black'), halign='left'))

                    # Add delete button
                    delete_button = Button(text='Delete', background_color=(1, 0, 0, 1), size_hint=(None, None), size=(100, 40))
                    delete_button.bind(on_press=lambda instance, uname=username: self.delete_user(uname))
                    self.user_details_layout.add_widget(delete_button)

                    # Add change password button
                    change_password_button = Button(text='Change Password', background_color=(0, 0, 0, 1), size_hint=(None, None), size=(150, 40))
                    change_password_button.bind(on_press=lambda instance, uname=username: self.change_password(uname))
                    self.user_details_layout.add_widget(change_password_button)

            else:
                self.user_details_layout.add_widget(Label(text='No users found', font_size='20sp', halign='center'))

        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Database error: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            connection.close()

    def delete_user(self, username):
        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()

            cursor.execute("DELETE FROM login WHERE username=?", (username,))
            connection.commit()

            # Refresh the user list after deletion
            self.load_user_details()

            popup = Popup(title='Success', content=Label(text=f'User {username} successfully deleted'), size_hint=(0.5, 0.5))
            popup.open()

        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Database error: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            connection.close()
            

    def change_password(self, username):
        # Create a popup for changing the password
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        old_password_input = TextInput(hint_text='Enter Old Password', password=True)
        new_password_input = TextInput(hint_text='Enter New Password', password=True)
        confirm_password_input = TextInput(hint_text='Confirm New Password', password=True)
        
        content.add_widget(old_password_input)
        content.add_widget(new_password_input)
        content.add_widget(confirm_password_input)
        
        def submit_password_change(instance):
            old_password = old_password_input.text
            new_password = new_password_input.text
            confirm_password = confirm_password_input.text

            if not old_password or not new_password or not confirm_password:
                popup = Popup(title='Error', content=Label(text='All fields are required.'), size_hint=(0.5, 0.5))
                popup.open()
                return

            if new_password != confirm_password:
                popup = Popup(title='Error', content=Label(text='New passwords do not match.'), size_hint=(0.5, 0.5))
                popup.open()
                return
            
            # Logic to validate the old password and change to the new password
            try:
                connection = sqlite3.connect('adashe.db')
                cursor = connection.cursor()
                cursor.execute("SELECT password FROM login WHERE username=?", (username,))
                result = cursor.fetchone()
                
                if result and result[0] == old_password:
                    cursor.execute("UPDATE login SET password=? WHERE username=?", (new_password, username))
                    connection.commit()
                    popup = Popup(title='Success', content=Label(text=f'Password for {username} changed successfully.'), size_hint=(0.5, 0.5))
                    popup.open()
                else:
                    popup = Popup(title='Error', content=Label(text='Old password is incorrect.'), size_hint=(0.5, 0.5))
                    popup.open()
            except sqlite3.Error as e:
                popup = Popup(title='Error', content=Label(text=f"Database error: {e}"), size_hint=(0.5, 0.5))
                popup.open()
            finally:
                connection.close()
        
        submit_button = Button(text='Submit', size_hint_y=None, height=50)
        submit_button.bind(on_press=submit_password_change)
        content.add_widget(submit_button)
        
        password_popup = Popup(title=f'Change Password for {username}', content=content, size_hint=(0.8, 0.6))
        password_popup.open()

    def go_to_dashboard(self, instance):
        self.manager.current = 'dashboard'

class RegisterCustomerPage(CustomScreen):
    def __init__(self, **kwargs):
        super(RegisterCustomerPage, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.7, None))
        layout.height = 400
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        label_register_customer = Label(text="REGISTER CUSTOMER", font_size=30, color=('black'), size_hint=(1, None), height=50)
        layout.add_widget(label_register_customer)

        self.phone_no_input = CustomTextInput(hint_text='Phone No', multiline=False, size_hint=(1, None), height=40)
        self.first_name_input = CustomTextInput(hint_text='First Name', multiline=False, size_hint=(1, None), height=40)
        self.last_name_input = CustomTextInput(hint_text='Last Name', multiline=False, size_hint=(1, None), height=40)
        self.address_input = CustomTextInput(hint_text='Address', multiline=False, size_hint=(1, None), height=40)
        self.nok_name_input = CustomTextInput(hint_text='NOK Name', multiline=False, size_hint=(1, None), height=40)
        self.nok_phone_input = CustomTextInput(hint_text='NOK Phone', multiline=False, size_hint=(1, None), height=40)
        self.account_balance_input = CustomTextInput(hint_text='Account Balance', multiline=False, size_hint=(1, None), height=40)

        layout.add_widget(self.phone_no_input)
        layout.add_widget(self.first_name_input)
        layout.add_widget(self.last_name_input)
        layout.add_widget(self.address_input)
        layout.add_widget(self.nok_name_input)
        layout.add_widget(self.nok_phone_input)
        layout.add_widget(self.account_balance_input)

        register_button = Button(text='Register Customer', size_hint=(1, None), height=50, color=('white'), background_color=('black'))
        register_button.bind(on_press=self.register_customer)
        layout.add_widget(register_button)

        back_button = Button(text='Back', size_hint=(1, None), height=50, background_color=('black'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def register_customer(self, instance):
        phone_no = self.phone_no_input.text
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text
        address = self.address_input.text
        nok_name = self.nok_name_input.text
        nok_phone = self.nok_phone_input.text
        account_balance = self.account_balance_input.text

        if not phone_no or not first_name or not last_name or not address or not nok_name or not nok_phone or not account_balance:
            popup = Popup(title='Error', content=Label(text='Please fill all fields'), size_hint=(0.5, 0.5))
            popup.open()
            return

        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()

            # Ensure the table exists; create it if it doesn't
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_no TEXT,
                first_name TEXT,
                last_name TEXT,
                address TEXT,
                nok_name TEXT,
                nok_phone TEXT,
                date_registered TEXT,
                account_bal REAL
            )
            """)

            cursor.execute(
                "INSERT INTO customers (phone_no, first_name, last_name, address, nok_name, nok_phone, date_registered, account_bal) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (phone_no, first_name, last_name, address, nok_name, nok_phone, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), float(account_balance))
            )

            connection.commit()
            popup = Popup(title='Success', content=Label(text='Customer registered successfully'), size_hint=(0.5, 0.5))
            popup.open()
            self.phone_no_input.text = ''
            self.first_name_input.text = ''
            self.last_name_input.text = ''
            self.address_input.text = ''
            self.nok_name_input.text = ''
            self.nok_phone_input.text = ''
            self.account_balance_input.text = ''

        except Exception as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            connection.close()

    def go_back(self, instance):
        self.manager.current = 'dashboard'
        
class ViewCustomersPage(CustomScreen):
    def __init__(self, **kwargs):
        super(ViewCustomersPage, self).__init__(**kwargs)
        self.manager = kwargs.get('manager')
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Back to Dashboard Button
        back_to_dashboard_button = Button(text='Back to Dashboard', size_hint_y=None, height=50, background_color=(0, 0, 0, 1), color=(1, 1, 1, 1))
        back_to_dashboard_button.bind(on_press=self.go_to_dashboard)
        main_layout.add_widget(back_to_dashboard_button)

        # Header
        header_label = Label(text='Customer Records', font_size='40sp', color=('black'))
        main_layout.add_widget(header_label)

        # Search Box
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.search_input = CustomTextInput(hint_text='Search...', multiline=False, size_hint_x=0.8)
        search_button = Button(text='Search', background_color=('black'),size_hint_x=0.2)
        search_button.bind(on_press=self.search_customers)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        main_layout.add_widget(search_layout)

        # Table
        self.table_layout = GridLayout(cols=10, size_hint_y=None, spacing=10)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        # Create a ScrollView to allow scrolling if content overflows
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True)
        scroll_view.add_widget(self.table_layout)
        main_layout.add_widget(scroll_view)

        # Export Button
        export_button = Button(text='Export to Excel', size_hint_y=None, height=50, background_color=(0, 0, 0, 1), color=(1, 1, 1, 1))
        export_button.bind(on_press=self.save_as_excel)
        main_layout.add_widget(export_button)

        self.add_widget(main_layout)

        # Load the customer data
        self.load_customer_data()

    def go_to_dashboard(self, instance):
        self.manager.current = 'dashboard'

    def load_customer_data(self, query=''):
        # Clear previous data
        self.table_layout.clear_widgets()
        
        # Add headers again
        headers = ['Customer ID', 'Phone No', 'First Name', 'Last Name', 'Address', 'NOK Name', 'NOK Phone', 'Date Registered', 'Account Balance', 'Actions']
        for header in headers:
            header_label = Label(text=header, bold=True, padding=[10, 5], size_hint_y=None, height=40)
            self.table_layout.add_widget(header_label)
        
        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            # Modify the query to include a search filter
            sql_query = """
            SELECT id, phone_no, first_name, last_name, address, nok_name, nok_phone, date_registered, account_bal 
            FROM customers 
            WHERE phone_no LIKE ? OR first_name LIKE ? OR last_name LIKE ? 
            OR address LIKE ? OR nok_name LIKE ? OR nok_phone LIKE ?
            """
            search_query = f"%{query}%"
            cursor.execute(sql_query, (search_query, search_query, search_query, search_query, search_query, search_query))
            customers = cursor.fetchall()

            for customer in customers:
                self.table_layout.add_widget(Label(text=str(customer[0]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[1]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[2]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[3]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[4]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[5]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[6]), padding=[10, 5], size_hint_y=None, height=40))
                self.table_layout.add_widget(Label(text=str(customer[7]), padding=[10, 5], size_hint_y=None, height=40))

                # Format the account balance in Naira currency format
                account_balance = customer[8]
                if account_balance < 0:
                    account_balance = 0
                account_balance_formatted = f"₦{account_balance:,.2f}"
                self.table_layout.add_widget(Label(text=account_balance_formatted, padding=[10, 5], size_hint_y=None, height=40))
                
                # Add delete button for each row
                delete_button = Button(text='Delete', size_hint_y=None, height=40, background_color=(1, 0, 0, 1), color=(1, 1, 1, 1))
                delete_button.bind(on_press=lambda btn, customer_id=customer[0]: self.delete_customer(customer_id))
                self.table_layout.add_widget(delete_button)
                
        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            if connection:
                connection.close()

    def search_customers(self, instance):
        query = self.search_input.text
        self.load_customer_data(query)

    def save_as_excel(self, instance):
        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            sql_query = """
            SELECT id, phone_no, first_name, last_name, address, nok_name, nok_phone, date_registered, account_bal 
            FROM customers
            """
            cursor.execute(sql_query)
            customers = cursor.fetchall()

            # Convert data to DataFrame
            df = pd.DataFrame(customers, columns=['Customer ID', 'Phone No', 'First Name', 'Last Name', 'Address', 'NOK Name', 'NOK Phone', 'Date Registered', 'Account Balance'])

            # File dialog to choose save location
            if platform == 'win' or platform == 'linux' or platform == 'macosx':
                from tkinter import Tk, filedialog
                root = Tk()
                root.withdraw()  # Hide tkinter window
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
                root.destroy()
            else:
                # Mobile platforms (Android/iOS) do not support tkinter, so save to a fixed path or use another method
                file_path = 'customer_records.xlsx'

            if file_path:
                # Save DataFrame to Excel
                df.to_excel(file_path, index=False)
                popup = Popup(title='Success', content=Label(text=f'Data successfully saved to {file_path}'), size_hint=(0.5, 0.5))
                popup.open()
            else:
                popup = Popup(title='Canceled', content=Label(text='Save operation canceled'), size_hint=(0.5, 0.5))
                popup.open()

        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            if connection:
                connection.close()
    def delete_customer(self, customer_id):
        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            sql_query = "DELETE FROM customers WHERE id = ?"
            cursor.execute(sql_query, (customer_id,))
            connection.commit()

            # Reload customer data to reflect changes
            self.load_customer_data()

            popup = Popup(title='Success', content=Label(text='Customer successfully deleted'), size_hint=(0.5, 0.5))
            popup.open()

        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            if connection:
                connection.close()

class DepositScreen(CustomScreen):
    def __init__(self, **kwargs):
        super(DepositScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.7, None))
        layout.height = 400
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        label_deposit = Label(text="DEPOSIT", font_size=30, color=('black'), size_hint=(1, None), height=50)
        layout.add_widget(label_deposit)

        self.search_input = CustomTextInput(hint_text='Phone No or Customer ID', multiline=False, size_hint=(1, None), height=40)
        self.amount_input = CustomTextInput(hint_text='Amount', multiline=False, size_hint=(1, None), height=40)

        layout.add_widget(self.search_input)
        layout.add_widget(self.amount_input)

        deposit_button = Button(text='Deposit', size_hint=(1, None), height=50, color=('white'), background_color=('black'))
        deposit_button.bind(on_press=self.process_deposit)
        layout.add_widget(deposit_button)

        back_button = Button(text='Back', size_hint=(1, None), height=50, background_color=('black'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def process_deposit(self, instance):
        search_term = self.search_input.text
        amount = self.amount_input.text

        if not search_term or not amount:
            popup = Popup(title='Error', content=Label(text='Please fill all fields'), size_hint=(0.5, 0.5))
            popup.open()
            return

        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            
            # Check if the search_term is a customer ID (digits only) or a phone number
            if search_term.isdigit() and len(search_term) < 11:
                # Assume it is a Customer ID if it's a digit and less than 11 characters
                query = "UPDATE customers SET account_bal = account_bal + ? WHERE id = ?"
                cursor.execute(query, (amount, search_term))
            elif len(search_term) == 11:
                # Assume it's a phone number if it's 11 digits
                query = "UPDATE customers SET account_bal = account_bal + ? WHERE phone_no = ?"
                cursor.execute(query, (amount, search_term))
            else:
                popup = Popup(title='Error', content=Label(text='Invalid Phone Number or Customer ID'), size_hint=(0.5, 0.5))
                popup.open()
                return
            
            connection.commit()
            popup = Popup(title='Success', content=Label(text='Deposit processed successfully'), size_hint=(0.5, 0.5))
            popup.open()
            self.search_input.text = ''
            self.amount_input.text = ''
            
            # After the withdrawal is successful, update the dashboard's total balance
            dashboard_page = self.manager.get_screen('dashboard')
            dashboard_page.update_total_balance()

        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            if connection:
                connection.close()
    def go_back(self, instance):
        self.manager.current = 'dashboard'


class WithdrawScreen(CustomScreen):
    def __init__(self, **kwargs):
        super(WithdrawScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.7, None))
        layout.height = 400
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        label_withdraw = Label(text="WITHDRAW", font_size=30, color=('black'), size_hint=(1, None), height=50)
        layout.add_widget(label_withdraw)

        self.search_input = CustomTextInput(hint_text='Phone No or Customer ID', multiline=False, size_hint=(1, None), height=40)
        self.amount_input = CustomTextInput(hint_text='Amount', multiline=False, size_hint=(1, None), height=40)

        layout.add_widget(self.search_input)
        layout.add_widget(self.amount_input)

        withdraw_button = Button(text='Withdraw', size_hint=(1, None), height=50, color=('white'), background_color=('black'))
        withdraw_button.bind(on_press=self.process_withdraw)
        layout.add_widget(withdraw_button)

        back_button = Button(text='Back', size_hint=(1, None), height=50, background_color=('black'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        main_layout.add_widget(layout)
        self.add_widget(main_layout)

    def process_withdraw(self, instance):
        search_term = self.search_input.text
        amount = self.amount_input.text

        if not search_term or not amount:
            popup = Popup(title='Error', content=Label(text='Please fill all fields'), size_hint=(0.5, 0.5))
            popup.open()
            return

        try:
            connection = sqlite3.connect('adashe.db')
            cursor = connection.cursor()
            
            # Check if the search_term is a customer ID (digits only) or a phone number
            if search_term.isdigit() and len(search_term) < 11:
                # Assume it is a Customer ID if it's a digit and less than 11 characters
                query = "UPDATE customers SET account_bal = account_bal - ? WHERE id = ?"
                cursor.execute(query, (amount, search_term))
            elif len(search_term) == 11:
                # Assume it's a phone number if it's 11 digits
                query = "UPDATE customers SET account_bal = account_bal - ? WHERE phone_no = ?"
                cursor.execute(query, (amount, search_term))
            else:
                popup = Popup(title='Error', content=Label(text='Invalid Phone Number or Customer ID'), size_hint=(0.5, 0.5))
                popup.open()
                return
                
            connection.commit()
            popup = Popup(title='Success', content=Label(text='Withdrawal processed successfully'), size_hint=(0.5, 0.5))
            popup.open()
            self.search_input.text = ''
            self.amount_input.text = ''
            
            # After the withdrawal is successful,  total balance
            dashboard_page = self.manager.get_screen('dashboard')
            dashboard_page.update_total_balance()

        except sqlite3.Error as e:
            popup = Popup(title='Error', content=Label(text=f"Error connecting to database: {e}"), size_hint=(0.5, 0.5))
            popup.open()
        finally:
            if connection:
                connection.close()

    def go_back(self, instance):
        self.manager.current = 'dashboard'

class MainApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(LandingPage(name='landing_page'))
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(RegisterPage(name='register'))
        sm.add_widget(DashboardPage(name='dashboard'))
        sm.add_widget(UserDetailsPage(name='user_details'))
        sm.add_widget(RegisterCustomerPage(name='register_customer'))
        sm.add_widget(ViewCustomersPage(name='view_customers'))
        sm.add_widget(DepositScreen(name='deposit_screen'))
        sm.add_widget(WithdrawScreen(name='withdraw_screen'))

        return sm


if __name__ == '__main__':
    MainApp().run()

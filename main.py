from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from hoverable import HoverBehavior
import glob,random
import json
from datetime import datetime
from pathlib import Path

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction='left'
        self.manager.current="sign_up_screen"

    def forgot(self):
        self.manager.current="forgot_password_screen"
        self.manager.transition.direction='left'

    
    def login(self,uname,pword):
        with open('users.json') as f:
            users=json.load(f)
        if uname in users and users[uname]['password']==pword:
            self.manager.current="login_screen_success"
            self.manager.transition.direction='left'
        else:
            anim=Animation(color=(1,0.3,0.3,0.9))
            anim.start(self.ids.login_wrong)
            self.ids.login_wrong.text="Wrong Username or Password!"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

    def get_quote(self,feel):
        feel=feel.lower()
        available_feelings=glob.glob("quotes/*txt")
        available_feelings=[Path(f).stem for f in available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",encoding='utf8') as f:
                quotes=f.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text="Dusra feeling Try kar Laude"


class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as f:
             users=json.load(f)

        if uname in users:
            anim=Animation(color=(1,0.3,0.3,0.9))
            anim.start(self.ids.user_exist)
            self.ids.user_exist.text="User Already Exist Go To Login"
        else:
            users[uname]={"username": uname, 
            "password": pword, 
            "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            }

            with open('users.json','w') as f:
                json.dump(users,f)
            self.manager.current="sign_up_screen_success"
    def back_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class ForgotPasswordScreen(Screen):
    def back_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
    
    def go_to_sign_up(self):
        self.manager.transition.direction='left'
        self.manager.current="sign_up_screen"

    def password_change(self,uname,pword):
        with open('users.json') as f:
            users=json.load(f)
        if uname not in users :
            anim=Animation(color=(1,0.3,0.3,0.9))
            anim.start(self.ids.user_exist)
            self.ids.user_exist.text="Username doesn't exist Go To Sign Up"
        elif uname in users:
            users[uname]={"username": uname, 
            "password": pword, 
            "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            }
            anim=Animation(color=(1,0.3,0.3,0.9))
            anim.start(self.ids.user_exist)
            self.ids.user_exist.text="Password Changed Go To Login"


class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
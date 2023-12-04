import pyautogui
import pyperclip
import os
import sys
import sched
from datetime import datetime

def get_file_name():
    now= datetime.now()
    file_name_str= now.strftime("%Y%m%d_%H_%M")
    return file_name_str


def click_img(imagePath):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x, y, clicks=1)


def print_banner():
    print('==============================')
    print(' Kakaotalk Chat Dump Exporter')
    print('                      v0.0.1 ')
    print('==============================')


def print_monitor_spec():
    print('Monitor ', end='')
    print(pyautogui.size())
    print('Mouse ', end='')
    print(pyautogui.position())


def export_chat_dump(file_name):
    # click menu button
    try:
        click_img(img_path + 'menu.png')
    except:
        try:
            click_img(img_path + 'menu_hover.png')
        except:
            try:
                click_img(img_path + 'menu_inactive.png')
            except:
                print('Failed: click menu')
                return False

    # click '대화 내용'
    try:
        click_img(img_path + 'chat_dump.png')
    except:
        try:
            click_img(img_path + 'chat_dump_hover.png')
        except:
            print('Failed: click chat_dump')
            return False

    # click '대화 내보내기'
    try:
        click_img(img_path + 'export_chat.png')
    except:
        try:
            click_img(img_path + 'export_chat_hover.png')
        except:
            print('Failed: export chat')
            return False

    pyperclip.copy(file_name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.keyDown('enter')
    
    # click '확인'
    try:
        click_img(img_path + 'confirm.png')
    except:
        try:
            click_img(img_path + 'confirm_hover.png')
        except:
            try:
                click_img(img_path + 'confirm_inactive.png')
            except:
                print('Exit with esc.')
                pyautogui.keyDown('esc')

    # export success
    return True

def run_exporter(scheduler, interval_in_seconds):
    file_name= get_file_name()
    is_export_success= export_chat_dump(file_name)

    if is_export_success:
        print('Export done. File name: ' + file_name)

    sys.stdout.flush()
    scheduler.enter(interval_in_seconds, 1, run_exporter, argument=(scheduler, interval_in_seconds))

# export config
img_path = os.path.dirname(os.path.realpath(__file__)) + '/img/'
conf = 0.90
pyautogui.PAUSE = 0.5

# scheduler config
interval_in_seconds = 1800 # 30 minutes

if __name__ == "__main__":
    print_banner()
    print_monitor_spec()
    print()
    sys.stdout.flush()

    scheduler = sched.scheduler()
    scheduler.enter(interval_in_seconds, 1, run_exporter, argument=(scheduler, interval_in_seconds))
    scheduler.run()
    
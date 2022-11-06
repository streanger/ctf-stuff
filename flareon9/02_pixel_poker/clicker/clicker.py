import time
import subprocess
import win32api
import win32gui
import win32con


def get_windows_hwnd(window_title):
    toplist = []
    winlist = []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        
    win32gui.EnumWindows(enum_cb, toplist)
    windows = [(hwnd, title) for hwnd, title in winlist if title == window_title]
    return windows
    
    
if __name__ == "__main__":
    subprocess.Popen("PixelPoker.exe")
    time.sleep(1)
    
    # ******* get window position *******
    # pos_x, pos_y = win32gui.GetCursorPos()  # DEBUG
    windows = get_windows_hwnd('PixelPoker')
    print(windows)
    window = windows[0]
    hwnd, title = window
    rect = win32gui.GetWindowRect(hwnd)
    base_x, base_y, *rest = rect
    x_zero_shift = 10
    y_zero_shift = 63  # 62, 63
    base_x += x_zero_shift
    base_y += y_zero_shift
    # pixels mismatch might be a problem of high dpi
    x_max = 925  # pixels in x-axis; 746, 925;
    y_max = 758  # pixels in y-axis; 645, 758
    
    # ******* create positions sequence *******
    sequence = []
    for y in range(0, y_max+1):
        for x in range(0, x_max+1):
            pos = (base_x+x, base_y+y)
            sequence.append(pos)
            
    # ******* iterate over sequence & click *******
    input('run sequence ')
    for index, pos in enumerate(sequence):
        print(pos)
        win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,*pos,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,*pos,0,0)
        
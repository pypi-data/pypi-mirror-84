import wx.adv
from utils import config

TRAY_TOOLTIP = 'SNX System Tray'


class TaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, frame, snx):
        self.frame = frame
        self.snx = snx
        super(TaskBarIcon, self).__init__()
        self.set_icon(config.TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_connect)
        if self.snx.is_running():
            self.set_icon(config.TRAY_ICON_OK)
        self.password = None

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Connect', self.on_connect)
        create_menu_item(menu, 'Reconnect', self.on_reconnect)
        create_menu_item(menu, 'Disconnect', self.on_disconnect)
        create_menu_item(menu, 'Check if SNX is running', self.on_check_if_snx_is_running)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def on_reconnect(self, event):
        self.snx.disconnect()
        self.on_connect(event)

    def on_connect(self, event):
        if not self.password:
            window = wx.PasswordEntryDialog(self.frame, "Password")
            window.ShowModal()
            self.password = window.GetValue()
        if self.snx.connect(passwd=self.password):
            self.set_icon(config.TRAY_ICON_OK)
        else:
            self.set_icon(config.TRAY_ICON_ERROR)
            self.password = None
        if not config.keep_passwd:
            self.password = None

    def on_disconnect(self, event):
        if self.snx.disconnect():
            self.set_icon(config.TRAY_ICON)
        else:
            self.set_icon(config.TRAY_ICON_ERROR)

    def on_check_if_snx_is_running(self, event):
        if self.snx.is_running():
            self.set_icon(config.TRAY_ICON_OK)
        else:
            self.set_icon(config.TRAY_ICON)

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        self.on_connect(event)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    Init = True

    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame, config.Client)
        return True


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

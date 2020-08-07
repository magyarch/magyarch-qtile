# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# c = ("*background", "*foreground", "*color0", "*color1", "*color2", "*color3", "*color4", "*color5", "*color6", "*color7", "*color8", "*color9", "*color10", "*color11", "*color12", "*color13", "*color14", "*color15": )



from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger
import os
from os import getenv
import wttrweather
import mpdwidget
import time
import custom
import clock

from typing import List  # noqa: F401

mod = "mod4"

term = getenv("TERMINAL")
home = getenv("HOME")
browser = getenv("BROWSER")
termfloat = getenv("TERMFLOAT")

def_colors = {
    '*background': '#2f2b26', '*foreground': '#c3cdc8',
    '*color0': '#036947', '*color1': '#987351',
    '*color2': '#2e8b57', '*color3': '#afc246',
    '*color4': '#44b4cf', '*color5': '#8bb6ac',
    '*color6': '#36dbc0', '*color7': '#54ba98',
    '*color8': '#137957', '*color9': '#865b39',
    '*color10': '#09a573', '*color11': '#95aa30',
    '*color12': '#2593a6', '*color13': '#7c9c96',
    '*color14': '#29bdd1', '*color15': '#cbffff'
}

values = (
    '*background', '*foreground', '*color0',
    '*color1', '*color2', '*color3', '*color4',
    '*color5', '*color6', '*color7', '*color8',
    '*color9', '*color10', '*color11', '*color12',
    '*color13', '*color14', '*color15'
)

with open(os.path.expanduser('~/.Xresources')) as f:
    data = f.readlines()

for x in data:
    for y in values:
        if y == x.split(":")[0].strip():
            def_colors[y] = x.split(":")[1].strip()


# a = [x.split(":")[1].strip() for x in data if "*background" in x]
# b = [x.split(":")[1].strip() for x in data if "*foreground" in x]
# get_wihite = [x.split(":")[1].strip() for x in data if "white" in x]
# get_red = [x.split(":")[1].strip() for x in data if "red" in x]


def make_sticky(qtile, *args):
    qtile.cmd_spawn("urxvt")
    time.sleep(0.5)
    a = qtile.current_window
    screen_x = qtile.current_screen.width // 2 - 400
    screen_y = qtile.current_screen.height // 2 - 300
    # b = qtile.find_screen
    logger.debug(screen_x)
    logger.debug(screen_y)
    a.float_x = 620
    a.float_y = 20
    a.float_height = 600
    a.float_width = 800
    a.floating = True


def pic(qtile):
    # subprocess.Popen(["maim $(xdg-user-dir PICTURES)/pic-full-$(date +%Y-%m-%d-%H:%M:%S).png"], shell=True)
    qtile.cmd_spawn("maim '$(xdg-user-dir PICTURES)/pic-full-$(date +%Y-%m-%d-%H:%M:%S).png'")


keys = [
    # Switch between windows in current stack pane
    # Key([mod], "j", lazy.function(make_sticky)),
    Key([], "F10", lazy.spawn("amixer set Master 5%-")),
    Key([], "F11", lazy.spawn("amixer set Master 5%+")),
    Key([], "F12", lazy.spawn(["feh", home + "/.config/qtile/no_modifier.png"])),
    Key([mod], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4.png"])),
    Key([mod, "control"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4-control.png"])),
    Key([mod, "mod1"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4-mod1.png"])),
    Key([mod, "shift"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4-shift.png"])),

    Key([], "Print", lazy.spawn("scrot '%Y-%m-%d-%H:%M:%S-pic_screen.jpg' -e 'mv $f $$(xdg-user-dir PICTURES)'")),


    #############################

    Key([mod], "b", lazy.hide_show_bar(position='top')),
    Key([mod], "c", lazy.spawn("power")),
    Key([mod], "d", lazy.spawn("rofi -show run")),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    # Key([mod], "h", lazy.layout.left()),
    # Key([mod], "j", lazy.layout.down()),
    Key([mod], "i", lazy.spawn(term + " -e htop")),
    Key([mod], "n", lazy.spawn(term + " -e newsboat")),
    Key([mod], "p", lazy.spawn("discord")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "w", lazy.spawn(browser)),
    Key([mod], "F2", lazy.spawn("edconf.sh")),
    Key([mod], "F6", lazy.spawn(termfloat + " -e cava")),
    # Key([mod], "F7", lazy.spawn(["maim $(xdg-user-dir PICTURES)/pic-full-$(date +%Y-%m-%d-%H:%M:%S).png"], shell=True)),
    Key([mod], "Return", lazy.spawn(term)),
    Key([mod], "Scroll_Lock", lazy.spawn("run_screenkey")),

    # ######### LAYOUT ################

    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),

    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "mod1"], "Down", lazy.layout.flip_down()),
    Key([mod, "mod1"], "Up", lazy.layout.flip_up()),
    Key([mod, "mod1"], "Left", lazy.layout.flip_left()),
    Key([mod, "mod1"], "Right", lazy.layout.flip_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),

    Key([mod], "n", lazy.window.toggle_floating()),

    Key([mod, "shift"], "c", lazy.spawn(termfloat + " -g 70x20-620+30 -e calcurse")),
    Key([mod, "shift"], "e", lazy.spawn("subl3"),
        lazy.spawn("subl")
        ),
    Key([mod, "shift"], "i", lazy.spawn(term + " -e gtop")),
    Key([mod, "shift"], "n", lazy.spawn(termfloat + " -e ncmpcpp")),
    Key([mod, "shift"], "p", lazy.spawn("pcmanfm")),
    Key([mod, "shift"], "w", lazy.spawn("firefox")),
    Key([mod, "shift"], "Return", lazy.spawn(termfloat)),
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    Key([mod, "mod1"], "q", lazy.shutdown()),
    Key([mod, "mod1"], "r", lazy.restart()),

]

groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

group_layouts = ["bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "bsp"]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
        ))


for i in groups:
    if i.name == "10":
        keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], "0", lazy.group["10"].toscreen(toggle=False)),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], "0", lazy.window.togroup("10")),
            Key([mod, "control"], "0", lazy.window.togroup("10", switch_group=True)),
        ])
    else:
        keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(toggle=False)),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group=True)),
        ])


layout_defaults = dict(
    border_focus="#228B22",
    border_norma="#000000",
    border_width=2,
)
extension_defaults1 = layout_defaults.copy()


layouts = [
    # layout.Max(),
    layout.Bsp(
        margin=5,
        fair=True,
        grow_amount=5,
        **extension_defaults1,
    ),

    layout.Stack(
        num_stacks=2,
        **extension_defaults1,
    ),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(
        shift_windows=True,
    ),

    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Floating(),
    layout.Slice(
        wname="htop",
    ),

]


widget_defaults = dict(
    # font='Hack Nerd Font Mono',
    font='JetBrains Mono',
    fontsize=10,
    padding=3,
    # background=def_colors["*background"],
    background="#000031",
    # foreground="#228B22",
    foreground=def_colors["*foreground"],
    colour_no_updates=def_colors["*background"],
    colour_have_updates="#228B22",
    inactive="#555555",
    active="#00ff00",

)
extension_defaults = widget_defaults.copy()

sep_set = dict(
    linewidth=1,
    foreground="#0000ff",
)


def open_update(qtile):
    qtile.cmd_spawn('alacritty -e updatepackage')


def open_ncmpcpp(qtile):
    qtile.cmd_spawn("alacritty -e ncmpcpp")


def open_power(qtile):
    qtile.cmd_spawn("power")


# colors = set_colors.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),

                widget.GroupBox(
                    rounded=False,
                    center_aligned=True,
                    highlight_method="block",
                    this_current_screen_border="#555555",
                    this_screen_border=def_colors["*color0"],
                    urgent_alert_method="block",
                    urgent_border="#ffffff",
                    urgent_text="#000000",
                    borderwidth=5,
                    block_highlight_text_color="#ffffff",
                    margin_x=2,
                    margin_y=3,
                    disable_drag=True,
                ),

                widget.CurrentLayoutIcon(
                    scale=0.5,
                ),
                widget.Prompt(
                    prompt="Run: ",
                ),

                widget.WindowName(),

                mpdwidget.Mpd(
                    fmt_playing='%e/%l %s [%v%%]',
                    fmt_stopped='',
                    reconnect=True,
                    reconnect_interval=1,
                    foreground_progress="#ff8c00",
                ),

                widget.Sep(
                    **sep_set,
                ),

                wttrweather.WttrWeather(
                    location='Budapest',
                    format="{c}🌡{t:>6}",
                    units='&m',
                    update_interval=600,
                ),
                widget.Sep(
                    **sep_set
                ),

                custom.Memory(
                    fmt="🚚{:>4}%",
                ),

                widget.Sep(
                    **sep_set,
                ),

                widget.TextBox(
                    text="📦",
                    mouse_callbacks={'Button1': open_update},
                ),

                widget.CheckUpdates(
                    distro="Arch_yay",
                    display_format="{updates:>2}",
                    mouse_callbacks={'Button1': open_update},
                    update_interval=600,
                ),

                widget.Sep(
                    **sep_set
                ),

                # widget.ThermalSensor(
                #     fmt="🌡️ {:>6}",
                #     # tag_sensor="Tccd1",
                # ),

                # widget.Sep(
                #     **sep_set
                # ),

                widget.CPU(
                    format="🏭 {load_percent:>5}%",
                    opacity=0.5,
                ),

                widget.Sep(
                    **sep_set
                ),

                widget.Volume(
                    emoji=True,
                    step=5,
                ),
                widget.Volume(
                    fmt="{:>4}",
                    step=5,
                ),

                widget.Sep(
                    **sep_set
                ),

                # widget.Clock(format='%Y-%m-%d %a %I:%M %p',),
                clock.Clock(
                    format="⏳ %H:%M",
                    format_alt="📆 %Y-%m-%d %H:%M",
                ),
                widget.Sep(
                    **sep_set
                ),
                widget.TextBox(
                    text="  ",
                    fontsize=20,
                    mouse_callbacks={'Button1': open_power},
                ),
                widget.Sep(
                    **sep_set
                ),

                # widget.QuickExit(),
                widget.Systray(),
            ],
            30,
            margin=[0, 0, 5, 0],
            opacity=1.0,
        ),
        left=bar.Gap(size=5),
        right=bar.Gap(size=5),
        bottom=bar.Gap(size=5),
    ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
],
)
auto_fullscreen = True
focus_on_window_activation = "focus"


app_rules = {
    "Chromium": "1",
    "Sublime_text": "2",
    "discord": "4"
}


@hook.subscribe.client_new
def grouper(window, windows=app_rules):

    windowtype = window.window.get_wm_class()[1]

    if windowtype in windows.keys():

        if windowtype != "urxvt":
            window.togroup(windows[windowtype])
            window.group.cmd_toscreen(toggle=False)
        else:
            try:

                window.togroup(windows[windowtype][0])
                window.group.cmd_toscreen(toggle=False)
            except IndexError:
                pass


@hook.subscribe.client_urgent_hint_changed
def go(client):
    logger.debug("rajt urgent config")
    client.group.cmd_toscreen()


app_float_center = (
    "URxvt", "feh"
)


@hook.subscribe.client_new
def go_float(window, windows=app_float_center):
    windowtype = window.window.get_wm_class()[1]
    logger.debug("urxvt_cliebt")
    # if the window is in our map
    if windowtype in windows:
        window.floating = True


wmname = "LG3D"

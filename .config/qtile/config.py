# Copyright (c) 2020 MagyArch Linux <https://magyarchlinux.org>


from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from os import getenv
import wttrweather
import mpdwidget
import re
import custom
import clock
import my_sensors
from collections import namedtuple
from typing import List  # noqa: F401
# from libqtile.log_utils import logger
from Xlib.display import Display


mod = "mod4"

term = getenv("TERMINAL")
home = getenv("HOME")
browser = getenv("BROWSER")
termfloat = getenv("TERMFLOAT") + " --geometry 110x30 "

colors = {
    'background': '#2f2b26', 'foreground': '#c3cdc8',
    'color0': '#036947', 'color1': '#987351',
    'color2': '#2e8b57', 'color3': '#afc246',
    'color4': '#44b4cf', 'color5': '#8bb6ac',
    'color6': '#36dbc0', 'color7': '#54ba98',
    'color8': '#137957', 'color9': '#865b39',
    'color10': '#09a573', 'color11': '#95aa30',
    'color12': '#2593a6', 'color13': '#7c9c96',
    'color14': '#29bdd1', 'color15': '#cbffff'
}

values = (
    'background', 'foreground', 'color0',
    'color1', 'color2', 'color3', 'color4',
    'color5', 'color6', 'color7', 'color8',
    'color9', 'color10', 'color11', 'color12',
    'color13', 'color14', 'color15'
)

with open(home + "/.Xresources") as f:
    data = f.readlines()

for x in data:
    for y in values:
        # match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', x.split(":")[1].strip())
        if y == x.split(":")[0].strip().replace("*", "") and re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', x.split(":")[1].strip()):
            colors[y] = x.split(":")[1].strip()

Colors = namedtuple('Colors', sorted(colors))
color = Colors(**colors)


keys = [
    # Switch between windows in current stack pane

    # No modifyers

    # Key([], "Print", lazy.spawn("scrot '%Y-%m-%d-%H:%M:%S-pic_screen.jpg' -e 'mv $f $$(xdg-user-dir PICTURES)'")),
    Key([], "F10", lazy.spawn("amixer set Master 5%-")),
    Key([], "F11", lazy.spawn("amixer set Master 5%+")),

    # Key image

    Key([], "F12", lazy.spawn(["feh", home + "/.config/qtile/no_modifier.png"])),
    Key([mod], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4.png"])),
    Key([mod, "control"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4-control.png"])),
    Key([mod, "mod1"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4-mod1.png"])),
    Key([mod, "shift"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod4-shift.png"])),
    Key(["mod1"], "F12", lazy.spawn(["feh", home + "/.config/qtile/mod1.png"])),

    # Mod4 (Super) +

    Key([mod], "b", lazy.hide_show_bar(position='top')),
    Key([mod], "c", lazy.spawn("power")),
    Key([mod], "d", lazy.spawn("dmenu_run -i -p 'Search' -nb '#2f2b26' -sb '#2e8b57' -fn 'JetBrains Mono Medium-12'")),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "i", lazy.spawn(term + " -e htop")),
    Key([mod], "n", lazy.spawn(term + " -e newsboat")),
    Key([mod], "p", lazy.spawn("discord")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "w", lazy.spawn(browser)),
    Key([mod], "F2", lazy.spawn("edconf.sh")),
    # Key([mod], "F6", lazy.spawn(termfloat + " -e cava")),
    Key([mod], "F4", lazy.spawn("maim_save")),
    Key([mod], "F5", lazy.spawn("maimpick")),
    Key([mod], "F9", lazy.spawn("dmenumount")),
    Key([mod], "F10", lazy.spawn("dmenuumount")),
    Key([mod], "Return", lazy.spawn(term)),
    Key([mod], "space", lazy.prev_layout()),
    Key([mod], "Scroll_Lock", lazy.spawn("run_screenkey")),
    Key([mod], "KP_Home", lazy.spawn("dmenurecord")),
    Key([mod], "KP_End", lazy.spawn("live.sh")),

    # opacity
    Key([mod], "comma", lazy.window.down_opacity()),
    Key([mod, "shift"], "comma", lazy.window.up_opacity()),



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

    # Mod4 (Super) + shift +

    # Key([mod, "shift"], "c", lazy.spawn(termfloat + "-e calcurse")),
    Key([mod, "shift"], "c", lazy.spawn("urxvt --geometry 70x20 -e calcurse")),
    Key([mod, "shift"], "d", lazy.spawn("rofi -show run"),),
    Key([mod, "shift"], "e", lazy.spawn("subl3"),
        lazy.spawn("subl")
        ),
    Key([mod, "shift"], "i", lazy.spawn(term + " -e gtop")),
    Key([mod, "shift"], "n", lazy.spawn(termfloat + " -e ncmpcpp")),
    Key([mod, "shift"], "p", lazy.spawn("pcmanfm")),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "x", lazy.spawm("killall ffmpeg")),
    Key([mod, "shift"], "w", lazy.spawn("firefox")),
    Key([mod, "shift"], "Return", lazy.spawn(termfloat)),

    # Mod4 (Super) + mod1 (Alt) +

    Key(["mod1"], "a", lazy.spawn("pavucontrol")),
    Key([mod, "mod1"], "q", lazy.shutdown()),
    Key([mod, "mod1"], "r", lazy.restart()),
    Key([mod, "mod1"], "space", lazy.prev_layout()),
    Key([mod, "mod1"], "Tab", lazy.screen.prev_group()),

    # mod1 (Alt) +

    Key(["mod1"], "Tab", lazy.screen.next_group()),

]

groups = []

group_names = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

group_layouts = ("bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "bsp", "floating", "bsp")

# group_labels = ("", "", "", "", "", "", "", "", "", "")


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            # label=group_labels[i],
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
    border_focus=color.color2,
    border_normal=color.background,
    border_width=2,
)


layouts = [
    # layout.Max(),
    layout.Bsp(
        margin=5,
        fair=True,
        grow_amount=5,
        **layout_defaults,
    ),

    layout.Stack(
        **layout_defaults,
    ),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(
        **layout_defaults,
    ),

    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Floating(
        **layout_defaults,
    ),

]


widget_defaults = dict(
    # font='Hack Nerd Font Mono',
    font='JetBrains Mono',
    fontsize=10,
    padding=3,
    background=color.background,
    foreground=color.foreground,
    colour_no_updates=color.foreground,
    colour_have_updates=color.color4,

)
extension_defaults = widget_defaults.copy()

sep_set = dict(
    linewidth=1,
    foreground=color.color10,
)


def open_update(qtile):
    qtile.cmd_spawn(term + ' -e updatepackage')


def open_ncmpcpp(qtile):
    qtile.cmd_spawn(term + " -e ncmpcpp")


def open_power(qtile):
    qtile.cmd_spawn("power")


def open_calcurse(qtile):
    qtile.cmd_spawn("urxvt --geometry 70x20 -e calcurse")


def kill_calcurse(qtile):
    qtile.cmd_spawn("calcursekill")


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    rounded=False,
                    center_aligned=True,
                    highlight_method="block",
                    this_current_screen_border=color.color0,
                    this_screen_border=color.color0,
                    urgent_alert_method="block",
                    urgent_border=color.color10,
                    urgent_text="#000000",
                    borderwidth=5,
                    block_highlight_text_color=color.color15,
                    margin_x=2,
                    margin_y=3,
                    disable_drag=True,
                    inactive=color.color1,
                    active=color.foreground,
                    # hide_unused=True
                    # if set group label sets, small icons.
                    # fontsize=20,
                ),

                widget.CurrentLayoutIcon(
                    scale=0.5,
                ),
                # widget.Prompt(
                #     background='#2e8b57',
                #     foreground='#000000',
                #     cursor_color='000000',
                #     prompt="Search: ",
                #     # markup=False,
                #     # bell_style="visual",
                #     # max_history=100,
                # ),

                widget.WindowName(),
                # widget.TextBox("default config", name="default"),


                mpdwidget.Mpd(
                    fmt_playing='%e/%l %s [%v%%]',
                    fmt_stopped='',
                    reconnect=True,
                    reconnect_interval=1,
                    foreground_progress="#ff8c00",
                ),
                # widget.Mpd2(),

                widget.Sep(
                    **sep_set,
                ),

                wttrweather.WttrWeather(
                    location="Budapest",

                    # Format
                    # c    Weather condition,
                    # C    Weather condition textual name,
                    # h    Humidity,
                    # t    Temperature (Actual),
                    # f    Temperature (Feels Like),
                    # w    Wind,
                    # l    Location,
                    # m    Moonphase 🌑🌒🌓🌔🌕🌖🌗🌘,
                    # p    precipitation (mm),
                    # P    pressure (hPa),
                    format="{c}{t:>6}",
                    units='&m',
                    update_interval=3600,
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


                my_sensors.SENSORS(
                    # Run $HOME/.config/qtile/scripts/temp_data
                    # Output:
                    #       Composite: 38.9°C
                    #       Sensor 1: 38.9°C
                    #       Sensor 2: 44.9°C
                    #       ...
                    # set:
                    # format="{Composite}" or format="{Composite} {Sensor 1}"

                    format="🌡️ {Tccd1:>6}",
                    update_interval=2.0
                ),

                widget.Sep(
                    **sep_set
                ),

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
                    # emoji=True,
                ),

                widget.Sep(
                    **sep_set
                ),

                clock.Clock(
                    format="⏳ %H:%M",
                    format_alt="📆 %Y-%m-%d %H:%M",
                    mouse_callbacks={
                        'Button4': kill_calcurse,
                        'Button5': open_calcurse
                    },
                ),
                widget.Sep(
                    **sep_set
                ),
                widget.TextBox(
                    text="",
                    padding=5,
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

floating_layout = layout.Floating(
    float_rules=[
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
        {'wmclass': 'URxvt'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wmclass': 'feh'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass

    ],
    **layout_defaults,
)
auto_fullscreen = True
focus_on_window_activation = "focus"


app_rules = {
    "Chromium": "1",
    "firefox": "1",
    "Brave-browser": "1",
    "Sublime_text": "2",
    "Subl3": "2",
    "discord": "4"
}


@hook.subscribe.client_new
def grouper(window, windows=app_rules):

    windowtype = window.window.get_wm_class()[1]

    # if the window is in our map
    if windowtype in windows.keys():

        window.togroup(windows[windowtype])
        window.group.cmd_toscreen(toggle=False)


# @hook.subscribe.client_urgent_hint_changed
# def go(client):
#     logger.debug("rajt urgent config")
#     client.group.cmd_toscreen()


app_float_pos = ("calcurse")


@hook.subscribe.client_new
def go_float(window, windows=app_float_pos):
    win_cal = window.window.get_name()

    if win_cal in windows:
        window.floating = True
        # window.cmd_set_size_floating(500, 500)
        my_screen_w = Display(":0").screen().width_in_pixels
        window.float_x = 0
        window.float_y = 0
        win_w = window.cmd_get_size()[0]
        window.tweak_float(x=my_screen_w - win_w - 30, y=40)


wmname = "LG3D"

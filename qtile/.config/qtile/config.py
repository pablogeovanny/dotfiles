import os, shutil, subprocess
from libqtile import bar, hook, layout, qtile, widget
from typing import List #noqa> F401 
from libqtile.config import EzClick, EzDrag, EzKey, Group, Rule, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget import Spacer, Prompt

# ___ _   _ _  _  ___ _____ ___ ___  _  _ ___
#| __| | | | \| |/ __|_   _|_ _/ _ \| \| / __|
#| _|| |_| | .` | (__  | |  | | (_) | .` \__ \
#|_|  \___/|_|\_|\___| |_| |___\___/|_|\_|___/
@hook.subscribe.startup_once
def autostart():
    cmds = [
        "xrandr --output Virtual-1 --mode 1920x1080",
        "setxkbmap es",
        "feh --bg-fill ~/.config/qtile/wall.jpg",
        "picom --no-vsync",
        "spice-vdagent"
    ]
    for cmd in cmds:
        subprocess.Popen(cmd, shell=True)

def status_bar(widgets):
  return bar.Bar(widgets, 30, opacity=0.9, margin=[15, 60, 6, 60], border_width=0)

@hook.subscribe.shutdown
def stop_apps():
  delete_cache()
  qtile.cmd_spawn(["killall", "dunst", "lxpolkit", "picom", "udiskie"])

# SET TARGET IP
@lazy.function
def update_target(qtile):
	def get_text(text):
		genpolltext = qtile.widgets_map["targettext"]
		genpolltext.update(f" {text}")
		global target
		target = text
	prompt = qtile.widgets_map["prompt"]
	prompt.start_input("", get_text)

# GET VPN IP
def get_vpn_ip():
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", "tun0"],
            capture_output=True,
            text=True,
            timeout=2
        )
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                return line.split()[1].split("/")[0]
        return "Off"
    except:
        return "Error"
# GET LOCAL IP
def get_local_ip():
    try:
        result = subprocess.run(
            ["hostname", "-I"],
            capture_output=True,
            text=True,
            timeout=2
        )
        ips = result.stdout.strip().split()
        if ips:
            return ips[0]
        return "No IP"
    except Exception:
        return "Error"
# COPY IP TO CLIPBOARD
def copy_to_clipboard(widget_name: str):
    try:
        w = qtile.widgets_map.get(widget_name)
        if w and w.text:
            text = w.text.strip()
            subprocess.run(["xsel", "-ib"], input=text.encode(), check=True)
    except:
        pass

# __  __  ___  _   _ ___ ___    ___ ___  _  _ ___ ___ ___ ___
#|  \/  |/ _ \| | | / __| __|  / __/ _ \| \| | __|_ _/ __/ __|
#| |\/| | (_) | |_| \__ \ _|  | (_| (_) | .` | _| | | (_ \__ \
#|_|  |_|\___/ \___/|___/___|  \___\___/|_|\_|_| |___\___|___/
mouse = [
    EzDrag("M-1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    EzDrag("M-3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    EzClick("M-2",
          lazy.window.bring_to_front()),
]

#__   ___   ___ ___   _   ___ _    ___ ___
#\ \ / /_\ | _ \_ _| /_\ | _ ) |  | __/ __|
# \ V / _ \|   /| | / _ \| _ \ |__| _|\__ \
#  \_/_/ \_\_|_\___/_/ \_\___/____|___|___/
mod = "mod4"
my_term = "alacritty"
my_browser = "firefox"
my_file_manager = "thunar"
target = ""

# _  _______   _____ ___ _  _ ___  ___
#| |/ / __\ \ / / _ )_ _| \| |   \/ __|
#| ' <| _| \ V /| _ \| || .` | |) \__ \
#|_|\_\___| |_| |___/___|_|\_|___/|___/
keys = [
# MANAGE WINDOWS
	EzKey("M-q", lazy.window.kill()),
	EzKey("A-f", lazy.window.toggle_fullscreen()),
# CHANGE FOCUS
	EzKey("M-<left>", lazy.layout.left(), desc="Move focus to left"),
	EzKey("M-<right>", lazy.layout.right(), desc="Move focus to right"),
	EzKey("M-<down>", lazy.layout.down(), desc="Move focus down"),
	EzKey("M-<up>", lazy.layout.up(), desc="Move focus up"),
# MOVE WINDOWS
	EzKey("M-S-<left>", lazy.layout.shuffle_left(), desc="Move window to the left"),
	EzKey("M-S-<right>", lazy.layout.shuffle_right(), desc="Move window to the right"),
	EzKey("M-S-<down>", lazy.layout.shuffle_down(), desc="Move window down"),
	EzKey("M-S-<up>", lazy.layout.shuffle_up(), desc="Move window up"),
# RESIZE UP, DOWN, LEFT, RIGHT
	EzKey("M-C-<Right>", lazy.layout.grow_right(), lazy.layout.grow(), lazy.layout.increase_ratio(), lazy.layout.delete(),),
	EzKey("M-C-<Left>", lazy.layout.grow_left(), lazy.layout.shrink(), lazy.layout.decrease_ratio(), lazy.layout.add(),),
	EzKey("M-C-<Up>", lazy.layout.grow_up(), lazy.layout.grow(), lazy.layout.decrease_nmaster(),),
	EzKey("M-C-<Down>", lazy.layout.grow_down(), lazy.layout.shrink(), lazy.layout.increase_nmaster(),),
       	EzKey("M-n", lazy.layout.normalize()),
# MANAGE LAYOUTS
	EzKey("M-<space>", lazy.next_layout()),
	EzKey("M-S-<space>", lazy.window.toggle_floating()),
# POWER CORE SHORTCUTS
	EzKey("M-C-A-r", lazy.restart()),
	EzKey("M-C-A-p", lazy.spawn('poweroff')),
	EzKey("M-C-A-c", lazy.shutdown(), desc="Quit Qtile"),
	EzKey("M-C-A-l", lazy.spawn('xtrlock')),
	EzKey("M-C-A-o", lazy.spawn('reboot')),
# LAUNCH APPS
	EzKey("M-<return>", lazy.spawn('rofi -show run')),
	EzKey("M-f", lazy.spawn(my_browser)),
	EzKey("M-t", lazy.spawn(my_term)),
	EzKey("M-v", lazy.spawn('pavucontrol')),
	EzKey("M-m", lazy.spawn('thunar')),
	EzKey("M-s", lazy.spawn("flameshot gui"), desc="Screenshot"),
# SET TARGET
	EzKey("M-y", update_target),
# MANAGE BRIGHTNESS
	EzKey("<XF86MonBrightnessUp>", lazy.spawn("brightnessctl s +5%")),
	EzKey("<XF86MonBrightnessDown>", lazy.spawn("brightnessctl s -5%")),
# MANAGE VOLUME
	EzKey("<XF86AudioMute>", lazy.spawn("amixer -q set Master toggle")),
	EzKey("<XF86AudioLowerVolume>", lazy.spawn("amixer -q set Master 5%-")),
	EzKey("<XF86AudioRaiseVolume>", lazy.spawn("amixer -q set Master 5%+")),

# PLAYER CONTROL
	EzKey("<XF86AudioPlay>", lazy.spawn("playerctl play-pause")),
	EzKey("<XF86AudioNext>", lazy.spawn("playerctl next")),
	EzKey("<XF86AudioPrev>", lazy.spawn("playerctl previous")),
	EzKey("<XF86AudioStop>", lazy.spawn("playerctl stop")),
]

#  ___ ___  _    ___  _   _ ___  ___
# / __/ _ \| |  / _ \| | | | _ \/ __|
#| (_| (_) | |_| (_) | |_| |   /\__ \
# \___\___/|____\___/ \___/|_|_\|___/
colours = [
    ["#181b20", "#181b20"],  # 0 Background Negro
    ["#e6e6e6", "#e6e6e6"],  # 1 Foreground Blanco
    ["#535965", "#535965"],  # 2 Grey Colour Gris
    ["#e55561", "#e55561"],  # 3 Rojo
    ["#8ebd6b", "#8ebd6b"],  # 4 Verde
    ["#e2b86b", "#e2b86b"],  # 5 Amarillo	
    ["#4fa6ed", "#4fa6ed"],  # 6 Azul
    ["#bf68d9", "#bf68d9"],  # 7 Fuxia
    ["#48b0bd", "#48b0bd"],  # 8 Turqueza
    ["#ADD8E6", "#ADD8E6"],  # 9 Azul pastel
    ["#E6E6FA", "#E6E6FA"],  # 10 Lavanda pastel
    ["#FFFACD", "#FFFACD"],  # 11 Amarillo pastel
    ["#F6B2B2", "#F6B2B2"],  # 12 Coral pastel
    ["#353446", "#353446"],  # 13 Background black bar
]

#  ___ ___  ___  _   _ ___  ___
# / __| _ \/ _ \| | | | _ \/ __|
#| (_ |   / (_) | |_| |  _/\__ \
# \___|_|_\\___/ \___/|_|  |___/
groups = [Group(f"{i + 1}", label="") for i in range(5)]

for i, group in zip(["1", "2", "3", "4", "5"], groups):
  keys.append(EzKey("M-" + (i), lazy.group[group.name].toscreen()))
  keys.append(EzKey("M-S-" + (i), lazy.window.togroup(group.name)))

# _      ___   _____  _   _ _____ ___
#| |    /_\ \ / / _ \| | | |_   _/ __|
#| |__ / _ \ V / (_) | |_| | | | \__ \
#|____/_/ \_\_| \___/ \___/  |_| |___/
layout_theme = {
    "border_focus": colours[6],
    "border_normal": colours[2],
    "margin": 10,
    "border_width": 4,
    "grow_amount": 2,
}

layouts = [
	layout.Bsp(**layout_theme, fair=False, border_on_single=True),
    	layout.MonadTall(**layout_theme),
	layout.MonadWide(**layout_theme),
	layout.Floating(**layout_theme),
	layout.Max(**layout_theme),
]

#__      _____ ___   ___ ___ _____ ___
#\ \    / /_ _|   \ / __| __|_   _/ __|
# \ \/\/ / | || |) | (_ | _|  | | \__ \
#  \_/\_/ |___|___/ \___|___| |_| |___/
widget_defaults = dict(background=colours[13],
                       foreground=colours[1],
                       font="Roboto Nerd Font Regular",
                       fontsize=12,
                       padding=5)

extension_defaults = widget_defaults.copy()

widgets = [
    widget.Sep(foreground=colours[13], linewidth=5),
    widget.Image(
	margin=3,
	fontsize = 14,
        filename="~/.config/qtile/logohitman.png",
        mouse_callbacks=({
            "Button1": lambda: qtile.cmd_spawn("rofi -show drun"),
            "Button3": lambda: qtile.cmd_spawn("rofi -show run"),
	}),
        scale=True),
    widget.Sep(foreground=colours[2],linewidth=1, padding=10, size_percent=70),
    widget.GroupBox(
	fontsize = 20,
        active=colours[7],
        inactive=colours[2],
        other_current_screen_border=colours[5],
        other_screen_border=colours[2],
        this_current_screen_border=colours[6],
        this_screen_border=colours[2],
        urgent_border=colours[3],
        urgent_text=colours[3],
        disable_drag=True,
        highlight_method="text",
        margin=2,
        padding=0,
        rounded=True,
        urgent_alert_method="text"),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10, size_percent=70),
    widget.CurrentLayout(
    	mode="icon",
        scale=0.60,
        padding=10,
        ),
    widget.Spacer(
	stretch=True
	),   
#    widget.WindowName(
#       max_chars=75,
#	fontsize = 14),
    widget.Prompt(
        prompt="Set target: ",
        foreground = colours[3],
       	fontsize = 14,
	),
    widget.TextBox(
	name = "targettext",
        foreground = colours[3],
	fontsize = 14,
	fmt = "{}",
	mouse_callbacks = {
	"Button1": lambda: subprocess.run(["xsel", "-ib"], input=target.encode("utf-8"), check=True)
	},
        ),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10,size_percent=70),
    widget.GenPollText(
    	name="vpn_widget",
    	func=get_vpn_ip,
	update_interval=5,
	fontsize=14,
	foreground = colours[4],
	fmt = " {}",
	mouse_callbacks={"Button1": lambda: copy_to_clipboard("vpn_widget")},
	),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10,size_percent=70),
    widget.GenPollText(
    	name="local_ip_widget",
    	func=get_local_ip,
	update_interval=5,
	fontsize=14,
	foreground = colours[5],
	fmt = " {}",
	mouse_callbacks={"Button1": lambda: copy_to_clipboard("local_ip_widget")},
	),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10,size_percent=70),
    widget.Net(
        foreground = colours[6],
	fontsize = 14,
	prefix = "M",
	format = " {down:4.2f}{down_suffix}  {up:4.2f}{up_suffix}",
    #     interface = "enp1s0"
	),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10,size_percent=70),
    widget.CPU(
        foreground=colours[7],
	fontsize = 14,
        format=" {load_percent}%",
        mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e htop"),
        },
        update_interval=1.0),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10, size_percent=70),
    widget.Memory(
        foreground=colours[8],
	fontsize = 14,
        format=" {MemUsed:.1f}/{MemTotal:.1f} {mm}",
mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e htop"),
        },
	measure_mem='G',
        update_interval=2.0),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10,size_percent=70),
    widget.Volume(
        foreground=colours[5],
	fontsize = 14,
        fmt=" {}",
        update_interval=1,
        volume_app="pavucontrol",
        step=5,
	limit_max_volume="true"
	),
#    widget.Sep(foreground=colours[2], linewidth=1, padding=10,size_percent=70),
#    widget.Battery(
#        foreground=colours[4],
#	fontsize = 14,
#        format="{char} {percent:2.0%}",
#        charge_char="",
#        discharge_char="",
#        empty_char="",
#        full_char="",
#        unknown_char="",
#        low_foreground=colours[3],
#        low_percentage=0.15,
#        show_short_text=False,
#        notify_below=15,
#	update_interval=1,
#	scroll_interval=0.1
#	),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10,size_percent=70),
    widget.KeyboardLayout(
	configured_keyboards=['es', 'us'],
	fmt=" {}",
        foreground=colours[6],
       	fontsize = 14,
    ),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10,size_percent=70),
    widget.Clock(
        foreground=colours[1],
	fontsize = 14,
        format=" %d %b %H:%M "),
]

# ___  ___ ___ ___ ___ _  _ ___
#/ __|/ __| _ \ __| __| \| / __|
#\__ \ (__|   / _|| _|| .` \__ \
#|___/\___|_|_\___|___|_|\_|___/
screens = [
    Screen(
        wallpaper="~/.config/qtile/wall.jpg",
        wallpaper_mode="stretch",
        top=status_bar(widgets),
	),
]

connected_monitors = (subprocess.run(
    "xrandr | busybox grep 'connected' | busybox cut -d' ' -f2",
    check=True,
    shell=True,
    stdout=subprocess.PIPE,
).stdout.decode("UTF-8").split("\n")[:-1].count("connected"))

if connected_monitors > 1:
  for i in range(1, connected_monitors):
    screens.append(
        Screen(
        	top=status_bar(widgets),
	        wallpaper="~/.config/qtile/wall.jpg",
    		wallpaper_mode="stretch"))

auto_fullscreen = True
auto_minimize = True
bring_front_click = False
cursor_warp = False
dgroups_app_rules = []
dgroups_key_binder = None
focus_on_window_activation = "smart"
follow_mouse_focus = True
reconfigure_screens = True

wmname = "LG3D"

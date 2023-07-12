import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import ToolBase, ToolToggleBase

import numpy as np
from PIL import Image

plt.rcParams['toolbar'] = 'toolmanager'

def on_move(event):
    if event.inaxes:
        print(f"motion_notify_event {type(event)} {event.x} {event.y}")
        if hasattr(event, "button"):
            print(f"... {event.button}")


def on_click(event):
    if event.button is MouseButton.LEFT:
        print(f"button_press_event {type(event)} {event.x} {event.y}")
        # plt.disconnect(binding_id)


class DigitizePen(ToolToggleBase):
    """Show lines with a given gid."""
    default_keymap = 'T'
    description = 'DigitizePen'
    default_toggled = False
    image = r"C:\Users\Kent\code\digitize_pen_icon.png"

    def __init__(self, *args, **kwargs):
        self.binding_ids = []
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        print("enabling tool")
        self.binding_ids.append(plt.connect('motion_notify_event', on_move))
        self.binding_ids.append(plt.connect('button_press_event', on_click))
        
    def disable(self, *args):
        print("disabling tool")
        for binding_id in self.binding_ids:
            plt.disconnect(binding_id)


img = np.asarray(Image.open(r"C:\Users\Kent\Downloads\OneDrive_1_12-07-2023\2864_disk37_2_SP_PR_6L.png"))

fig = plt.figure()
tm = fig.canvas.manager.toolmanager
tm.add_tool("digitize_pen", DigitizePen)
fig.canvas.manager.toolbar.add_tool(tm.get_tool("digitize_pen"), "toolgroup")
ax = fig.add_subplot(111)
ax.imshow(img)


plt.show()
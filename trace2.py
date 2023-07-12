from pathlib import Path
from datetime import datetime

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import ToolBase, ToolToggleBase

from PIL import Image

plt.rcParams['toolbar'] = 'toolmanager'
plt.rcParams["figure.autolayout"] = True

file_path = str(Path(__file__).parent)





# def digitize_on_click(event):
#         if event.button is MouseButton.LEFT:
#             print(f"button_press_event {type(event)} {event.x} {event.y}")
#             # plt.disconnect(binding_id)


class DigitizePen(ToolToggleBase):
    """Show lines with a given gid."""
    default_keymap = 'T'
    description = 'DigitizePen'
    default_toggled = False

    def __init__(self, *args, ax=None, line=None, **kwargs):
        self.binding_ids = []
        self.xdata = []
        self.ydata = []
        self.cache_xdata = []
        self.cache_ydata = []
        self.line = line
        self.final_lines = []
        self.ax = ax
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        print("enabling digitizing pen tool")
        self.binding_ids.append(plt.connect('motion_notify_event', self.on_move))
        self.binding_ids.append(plt.connect('button_release_event', self.on_release))
        fig.canvas.mpl_connect("draw_event", self.on_draw)
        
    def disable(self, *args):
        print("disabling digitizing pen tool")
        for binding_id in self.binding_ids:
            plt.disconnect(binding_id)

    def on_move(self, event):
        if event.inaxes:
            if event.button is MouseButton.LEFT:
                print(f"event.x/y {event.x:.2f} {event.y:.2f} event.xdata/ydata {event.xdata:.2f} {event.ydata:.2f}")
                self.cache_xdata.append(event.xdata)
                self.cache_ydata.append(event.ydata)
                self.redraw(update_draft_line=True)
    
    def on_release(self, event):
        self.redraw()
        final_line, = self.ax.plot(self.xdata, self.ydata, color='r', lw=1, animated=True)
        self.final_lines.append(final_line)
        self.redraw(update_draft_line=False)

    def redraw(self, update_draft_line=True):
        self.ax.figure.canvas.restore_region(self.ax.figure._bg)
        if update_draft_line:
            self.xdata += self.cache_xdata
            self.ydata += self.cache_ydata
            self.cache_xdata = []
            self.cache_ydata = []
            self.line.set_xdata(self.xdata)
            self.line.set_ydata(self.ydata)
        self.draw_artists()
        self.ax.figure.canvas.blit()
        self.ax.figure.canvas.flush_events()

    def draw_artists(self):
        self.ax.draw_artist(self.line)
        for line in self.final_lines:
            self.ax.draw_artist(line)

    def on_draw(self, event=None):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        cv.figure._bg = cv.copy_from_bbox(cv.figure.bbox)
        self.draw_artists()


img = Image.open(r"C:\Users\kinve\Downloads\OneDrive_2023-07-12\Job 2864\2864_disk37_2_SP_PR_6L.png")

imgdata = np.asarray(img)

fig = plt.figure()
tm = fig.canvas.manager.toolmanager
ax = fig.add_subplot(111)
ax.imshow(img)
plt.pause(0.1)
fig._bg = fig.canvas.copy_from_bbox(fig.bbox)

line, = ax.plot([], [], color='orange', lw=2, alpha=0.3, animated=True)

tm.add_tool("digitize", DigitizePen, ax=ax, line=line)
fig.canvas.manager.toolbar.add_tool(tm.get_tool("digitize"), "toolgroup")


manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()
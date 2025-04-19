import matplotlib.pyplot as plt


def canvas_config(self):
    self.fig.clf()
    self.axis = self.fig.add_subplot(projection="3d")
    self.axis.set_xlabel('X (km)')
    self.axis.set_ylabel('Y (km)')
    self.axis.set_zlabel('Z (km)')
    self.axis.margins(0.42)
    Background = "#000000"
    Grid_Color = '#1A85FF'
    self.fig.set_facecolor(Background)
    self.axis.set_facecolor(Background)
    self.axis.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    self.axis.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    self.axis.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    self.axis.tick_params(axis='x', colors=Grid_Color)
    self.axis.tick_params(axis='y', colors=Grid_Color)
    self.axis.tick_params(axis='z', colors=Grid_Color)
    self.axis.yaxis.label.set_color(Grid_Color)
    self.axis.xaxis.label.set_color(Grid_Color)
    self.axis.zaxis.label.set_color(Grid_Color)
    self.axis.xaxis.line.set_color(Grid_Color)
    self.axis.yaxis.line.set_color(Grid_Color)
    self.axis.zaxis.line.set_color(Grid_Color)
    plt.rcParams['grid.color'] = Grid_Color

def draw_blank(self):
    self.canvas_config()
    self.draw()
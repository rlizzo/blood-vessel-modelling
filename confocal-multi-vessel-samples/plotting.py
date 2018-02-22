# File Systems
import os, sys

# math
import numpy as np

class IndexTracker(object):
    def __init__(self, ax, X, color=None):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        if color == None:
            self.im = ax.imshow(self.X[:, :, self.ind], interpolation='nearest')
        else:
            self.im = ax.imshow(self.X[:, :, self.ind], interpolation='nearest', cmap=color)
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = np.clip(self.ind + 1, 0, self.slices - 1)
        else:
            self.ind = np.clip(self.ind - 1, 0, self.slices - 1)

        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()
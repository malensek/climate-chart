import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib
from matplotlib import rc

def c2f(t):
    return (t*9/5.0)+32

def k2c(t):
    return t-273.15

def k2f(t):
    return (t*9/5.0)-459.67

def disable_spines(ax):
    for s in ax.spines:
        ax.spines[s].set_visible(False)

rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

use_c = True
converter = k2f
if use_c:
    converter = k2c

filename = sys.argv[1]

with open(filename, 'r') as f:
    first_line = f.readline()[1:].strip()

data = np.loadtxt(fname=filename)
data[:, 0] = data[:, 0] - 1
data[:, 1] = converter(data[:, 1])
data[:, 2] = converter(data[:, 2])
if use_c == False:
    data[:, 3] = data[:, 3] * 0.0393701
data[:, 4] = converter(data[:, 4])

plt.ion()
plt.clf()
fig = plt.figure(1)
fig.subplots_adjust(hspace=.20)
gs = gridspec.GridSpec(2, 1, height_ratios=[1.75, 1])
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1], sharex=ax0)
plt.setp(ax0.get_xticklabels(), visible=False) # disable upper axis label

ax0.patch.set_facecolor('None')
ax1.patch.set_facecolor('None')

plt.suptitle('Climate Overview: ' + first_line, fontsize=14)

if k2c(data[:, 1]).min() < 5:
    y = 0
    if not use_c:
        y = c2f(0)
    ax0.plot([0, data[:, 0].max() + 1], [y, y], zorder=-1, color='#888888',
            alpha=.75, dashes=(8, 2))

rects0 = ax0.bar(.35 + data[:, 0], data[:, 2] - data[:, 1], bottom=data[:, 1],
        width=.6, color='#df3c3c', edgecolor='#731515')

rects1 = ax1.bar(.35 + data[:, 0], data[:, 3], color='#1b7edb', width=.6,
        edgecolor='#1d4871')

plt.xticks(np.arange(0,12) + .4, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    rotation=30)

disable_spines(ax0)
disable_spines(ax1)
ax0.spines['left'].set_visible(True)
ax1.spines['left'].set_visible(True)

for tic in ax0.xaxis.get_major_ticks():
    tic.tick1On = tic.tick2On = False

for tic in ax0.yaxis.get_major_ticks():
    tic.tick2On = False

for tic in ax1.xaxis.get_major_ticks():
    tic.tick1On = tic.tick2On = False

for tic in ax1.yaxis.get_major_ticks():
    tic.tick2On = False

for rect in rects1:
    height = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., 1.08*height,
        '%.1f' % (height), ha='center', va='bottom', color='#1d4871')

for r, rect in enumerate(rects0):
    height = rect.get_height()
    ax0.text(rect.get_x() + rect.get_width()/2., rect.get_y() + 1.08*height,
        '%d' % int(height + rect.get_y()), ha='center', va='bottom',
        color='#731515')
    ax0.text(rect.get_x() + rect.get_width()/2., rect.get_y() - 2,
        '%d' % int(rect.get_y()), ha='center', va='top', color='#731515')
    ax0.plot([rect.get_x() + .05, rect.get_x() + rect.get_width() - .05],
            [data[r, 4], data[r, 4]], color='#731515')

if use_c:
    ax0.set_ylabel('Temperature (C)')
    ax1.set_ylabel('Precipitation (cm)')
else:
    ax0.set_ylabel('Temperature (F)')
    ax1.set_ylabel('Precipitation (in)')

plt.savefig(filename + '-climate.pdf', bbox_inches='tight')

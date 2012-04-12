import pylab
import numpy
import sys
# --------------------------------------------------------------------------
def get_figsize(fig_width_pt):
    inches_per_pt = 1.0/72.0                # Convert pt to inch
    golden_mean = (numpy.sqrt(5)-1.0)/2.0    # Aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width*golden_mean      # height in inches
    fig_size =  [fig_width,fig_height]      # exact figsize
    return fig_size

params2 = {'backend': 'png',
          'axes.labelsize': 12,
          'text.fontsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12,
          'legend.pad': 0.2,     # empty space around the legend box
          'legend.fontsize': 12,
          'lines.markersize' : 0.1,
          'font.size': 12,
          'path.simplify': False,
          'figure.figsize': get_figsize(800)}

def set_figsize(fig_width_pt):
    pylab.rcParams['figure.figsize'] = get_figsize(fig_width_pt)

pylab.rcParams.update(params2)

# --------------------------------------------------------------------------


if (len(sys.argv) < 2):
    fn = raw_input("Please enter data file to be plotted\n")
else:
    fn = sys.argv[1]

data = pylab.loadtxt(fn)

pylab.plot(data[:,0], data[:,1], 'o', markersize=1, color='k')
gid_max = data[:, 1].max()
gid_min = data[:, 1].min()
pylab.ylim((gid_min - 1, gid_max + 1))

print data[:, 0]

pylab.show()

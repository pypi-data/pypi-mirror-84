import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

def get_figure(_molrepr, _edges, _scanrepr, _pts_through_path, filename, config, showPlot = False):
    """
    get_figure(_molrepr: Mol Object, _egdes: list, _scanrepr: pandas.DataFrame, 
                _pts_through_path: list, filename: string, config: configparser.SectionProxy)

    Function that puts the plot of the molecule with the path and the plot of the scan in the same 
    figure and saves and/or shows it (based on configurations in config.py).

    in:
    _molrepr: Mol Object containing XYZ data.
    _edges: list of tuples containing the indices of 2 atoms bonding.
    _scanrepr: pandas dataframe containing the corrected scans and the NICS-XY-Scan obtain with additivity.
    _pts_through_path: list of numpy.array containing coordinates of the path taken through the molecule.
    filename: name of the file where the figure will be saved.
    config: Configurations set in config.ini specific to plotting

    """
    
    # set parameters
    plt.rcParams.update({'font.size': 22})

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,12), sharex=False)

    # center subplots
    for ax in (ax1, ax2):
        ax.set_anchor('C')

    # plot scan and molecule with path
    plot_path(ax1, _molrepr, _edges, _pts_through_path)
    plot_scan(ax2, _scanrepr, config)

    # save figure
    if config.getboolean('save graph'):
        plt.savefig(filename, format=config['graph file format'])

    # show figure
    if config.getboolean('show graph') or showPlot:
        plt.show()

    return None


def plot_path(ax, _molrepr, _edges, _pts_through_path):
    """
    plot_path(ax, _molrepr: Mol Object, _edges: list, _pts_through_path: list)

    Function that plots the molecule with the path through it.

    in:
    _molrepr: Mol Object containing XYZ data.
    _edges: list of tuples containing the indices of 2 atoms bonding.
    _pts_through_path: list of numpy.array containing coordinates of the path taken through the molecule.

    """

    atom_colors = {'H':'silver','N':'blue','O':'red','S':'goldenrod','B':'green'}

    # set aspect of subplot
    ax.set_aspect('equal') 
    ax.axis('off')

    # plot molecule
    for edge in _edges:
        bond = []
        Hbond = False
        for atom_idx in edge:
            for atom in _molrepr.atoms:
                if atom_idx == atom.index:
                    bond.append(atom)
                    if atom.element != 'C':
                        if atom.element == 'BH':
                            atom.element = 'B'
                        elif atom.element == 'H':
                            Hbond = True
                        ax.text(atom.x, atom.y, atom.element, ha='center', va='center', color=atom_colors[atom.element], 
                                zorder=2, bbox=dict(facecolor='white', edgecolor='none', boxstyle='circle, pad=0.1'))
        x = [atom.x for atom in bond]        
        y = [atom.y for atom in bond]
        if Hbond:
            ax.plot(x, y, c=atom_colors['H'], linestyle='-', zorder=0)
        else:
            ax.plot(x, y, c='black', linestyle='-', zorder=1)

    # plot path
    x = [pts[0] for pts in _pts_through_path]
    y = [pts[1] for pts in _pts_through_path]
    ax.plot(x, y, c='red', linewidth=0.7)
    ax.arrow(x[-2], y[-2], x[-1]-x[-2], y[-1]-y[-2], head_width=0.3, head_length=0.3, fc='r', ec='r', length_includes_head=True, lw=0, zorder=2)


    return None

def plot_scan(ax, _scanrepr, config):
    """
    plot_scan(ax, _scanrepr: pandas.DataFrame, config: configparser.SectionProxy)

    Function that plots the calculated NICS-XY-Scan.

    in:
    _scanrepr: pandas dataframe containing the corrected scans and the NICS-XY-Scan obtain with additivity.
    config: Configurations set in config.ini specific to plotting. Here, we get the y axis (NICS-XY values) limits.
    
    """

    # select data to plot
    x = _scanrepr.r
    y = _scanrepr.iloc[:,-1]

    # plot
    ax.scatter(x, y, s=12, c='dodgerblue')
    ax.plot(x, y, linewidth=1.2, c='lightblue')
    ax.plot(x, np.zeros((x.shape)), linewidth=0.7, c='gray', linestyle='dashed')

    # configure axis
    ax.set_ylim([float(x.strip()) for x in config["y-axis limits"].split(",")])
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(5))

    # set labels
    ax.set_xlabel(r'Distance / $\mathrm{\AA}$')
    ax.set_ylabel(r'NICS(1.7)$_{\pi ZZ}$ / ppm')
    
    return None

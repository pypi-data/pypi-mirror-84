import warnings
import os

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.interpolate import splrep, splev

def generate_scan(_pathrepr, config, _step = 0.1, n = 3):
    """
    generate_scan(_pathrepr: list(Knot), config: configparser.SectionProxy, _step: float, n: int) -> scanrepr: pandas.DataFrame, path_points: list(numpy.ndarray)
    
    Generate NICS scan by identifying and adding up the building_blocks.

    in:
    _pathrepr: list of Knot Objects.
    config: Configurations set in config.ini specific to the additivity module.
    _step: step wanted in the final scan between each point.
    n: number of rings composing the largest multicycle used for the additivity scheme.

    out:
    scanrepr: pandas.DataFrame containing the path in angstrom through the molecule with a 0.1 step,
              NICS-XY-Scans of the building blocks (corrected for additivity), and the final NICS-XY-Scan
              of the molecule obtained by additivity.
    path_points: list of coordinates of the path taken through the molecule (used for plotting later).

    """

    building_blocks = load_building_blocks()

    knot_buf = []
    scans = []
    monocycles = []
    offset = 0 # start of the fragment/building block

    # identify the building blocks
    for knot in _pathrepr:
        knot_buf.append(knot)
        if len(knot_buf) > n:
            knot_buf.pop(0)

        for i in range(0, len(knot_buf)):
            reverse = False # if we need to inverse the scan we have
            angulation = 0
            key = "-".join(x.cycle_type for x in knot_buf[i:])

            if len(knot_buf[i:]) == 3 and len(knot_buf[i+1].atoms) != 5:
                a = np.array(knot_buf[i].get_coord())
                b = np.array(knot_buf[i+1].get_coord())
                c = np.array(knot_buf[i+2].get_coord())
                cos_angle = get_angle(a, b, c)
                if cos_angle < -0.87: # angle > 150°
                    angulation = '_l'
                else:
                    angulation = '_a'
            
            counter = 0
            while not key in building_blocks.keys() and counter < 100:
                if isinstance(angulation, str):
                    key += angulation
                if not key in building_blocks.keys():
                    key = "-".join(x.cycle_type for x in reversed(knot_buf[i:]))
                    reverse = True
                counter += 1
            
            if counter >= 100:
                if isinstance(angulation, str):
                    raise KeyError(f"Building block {key + angulation} not found.")
                else:
                    raise KeyError(f"Building block {key} not found.")

            for j in range(0, n):
                if len(knot_buf[i:]) == j + 1:
                    scans.append([offset - j, len(knot_buf[i:]), key, reverse, knot_buf[i:]])

            if len(knot_buf[i:]) == 1:
                monocycles.append([offset, knot_buf[i:]])

        offset += 1


        # get points the path takes through the molecules
        # typically from starting bond to ring center to opposite bond etc. until the end of the molecule is reached
        path_points = get_path_points(monocycles)


    if len(monocycles) > n:

        # convert from spatial points to distances, and get number of points which are added to list monocycles:
        # monocycles = [[order in the route, Knot object, number of points wanted in the scan]]
        monocycles, Xfinal = get_scan_path(monocycles, path_points, _step)
    

        # get new fitted scans with the appropriate number of points and reverse them if needed
        fitted_scans, corrected_scans = prep_scans(scans, building_blocks, monocycles)
        
        # get corrections for building blocks with more than 1 ring and performe additivity
        scanrepr = additivity(n, fitted_scans, corrected_scans, Xfinal, config)

    else:

        building_block_length = 0

        for scan_data in scans:
            if scan_data[1] > building_block_length:
                building_block_length = scan_data[1]
                building_block_scan_data = scan_data
        
        key, reverse = building_block_scan_data[2], building_block_scan_data[3]
        building_block_dict = building_blocks[key]
        scan, step = building_block_dict['scan'], building_block_dict['step']

        if reverse:
            scan = scan[::-1]
        
        mol_len = step*len(scan) 
        x_axis = np.linspace(0, mol_len, len(scan))

        scanrepr = pd.DataFrame({'r': x_axis, key: scan})


    return scanrepr, path_points


def load_building_blocks():
    """
    load_building_blocks() -> building_blocks: dict

    Load building_blocks for additivity scheme.

    out:
    building_blocks: Dict containing the scan data for every building block. The keys correspond to the code names given to the building blocks. 
                     Each key corresponds to a dict (building_blocks[key] = {'step': step, 'scan': scan}) containing the step size used to 
                     calculated the NICS-XY-Scan under 'step' and the NICS(1.7)piZZ values of the scan under 'scan'.

    """

    building_blocks = {}

    scan_data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'scan_data.csv'), sep=',', header=None)
    keys = scan_data.iloc[:,0].tolist()
    smiles = scan_data.iloc[:,1].tolist()
    steps = scan_data.iloc[:,2].tolist()
    scans = scan_data.iloc[:,3:]

    for i in range(len(keys)):
        key = keys[i]
        smile = smiles[i]
        step = steps[i]
        scan = np.array(scans.iloc[i,:].tolist())
        scan = scan[np.logical_not(np.isnan(scan))]
        building_blocks[key] = {'smiles': smile, 'step': step, 'scan': scan}

    return building_blocks

def get_angle(a, b, c):
    """
    get_angle(a: numpy.ndarray, b: numpy.ndarray, c: numpy.ndarray) -> numpy.float64

    Get cosine of an angle abc given 3 points in space a, b, and c with (x,y,z) coordinates.

    in:
    a, b, c: 3 numpy arrays containing the (x,y,z) coordinates of points a, b, c.

    out:
    float that is the cosine of the angle between vectors ab and bc.

    """

    ba = a - b
    bc = c - b

    return np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))

def get_path_points(_monocycles):
    """
    get_path_points(_monocycles: list(list(int, list(Knot)))) -> path_points: list(numpy.ndarray)

    Function that gets the points taken by the path through the molecule. The points are place on the bonds
    and the centers of the rings. The first point is the middle point of the bond where the scan starts.
    The second point is the center of the ring (coordinates of the knot), etc. until the end of the molecule
    (last bond) is reached.

    in:
    _monocycles: List of list containing info on the monocycles. 
                 _monocycles = [[order in the path route: int, Knot object]]

    out:
    path_points: List containing all points (numpy.ndarray of (x,y,z) coord) needed to trace the path taken 
                 by the scan. It goes from the 1st bond middle point, to the ring center (knot), to the 
                 middle point of the following bond, etc. until the last bond in the last ring is reached.
                 This list will be used to obtain the molecular distances.

    """

    path_points = []

    for i in range(len(_monocycles)-1):
        cycle_A, cycle_B = _monocycles[i][-1][0], _monocycles[i+1][-1][0]
        atom_list_A, atom_list_B = cycle_A.atoms, cycle_B.atoms
        atoms_cycle_A, atoms_cycle_B = set(atom_list_A), set(atom_list_B)

        intersect_atoms = list(atoms_cycle_A.intersection(atoms_cycle_B))

        coord_intersect_atom_a = np.array(intersect_atoms[0].get_coord())
        coord_intersect_atom_b = np.array(intersect_atoms[1].get_coord())
        mid_point = (coord_intersect_atom_a + coord_intersect_atom_b)/2

        path_points.append(mid_point)

        knot_coord = np.array(cycle_B.get_coord())
        path_points.append(knot_coord)

        if i == 0:
            opposing_atom_list = tuple(cycle_A.get_opposing_edge(intersect_atoms))
            if len(opposing_atom_list) < 2:
                mid_point = np.array(opposing_atom_list[0].get_coord())
            else:
                mid_point = (np.array(opposing_atom_list[0].get_coord()) + np.array(opposing_atom_list[1].get_coord()))/2

            path_points.insert(0, mid_point)

            knot_coord = np.array(cycle_A.get_coord())
            path_points.insert(1, knot_coord)

        if i == len(_monocycles) - 2:
            opposing_atom_list = tuple(cycle_B.get_opposing_edge(intersect_atoms))
            if len(opposing_atom_list) < 2:
                mid_point = np.array(opposing_atom_list[0].get_coord())
            else:
                mid_point = (np.array(opposing_atom_list[0].get_coord()) + np.array(opposing_atom_list[1].get_coord()))/2

            path_points.append(mid_point)
    
    return path_points

def get_scan_path(_monocycles, _path_points, _step):
    """
    get_scan_path(_monocycles: list(list(int, list(Knot))), _path_points: list(numpy.ndarray), _step: float) -> monocycles_w_points: list(list(int, list(Knot), int)), Xfinal: list(numpy.float64)

    Function that returns the actual x-values of the NICS-XY-Scan based on the chosen step (_step). This function also extracts the accurate number of 
    points the scan should have per ring based on the distance the prob would have to travel through the ring and the chosen step between each point 
    (_step). This number of points is then added to the list containing info on the probed ring. This list is then appended to another list containing
    the same info for all the other rings. This final list is then returned.

    in:
    _monocycles: List of list containing info on the monocycles. 
                 _monocycles = [[order in the path route: int, Knot object]]
    _path_points: List of numpy.ndarrays of (x,y,z) coordinates of points through the molecule following the scan path.
    _step: Float that represents the step size that the final NICS-XY-Scan should have.

    out:
    monocycles_w_points: List of list containing info on the monocycles with number of points the fitted scan will have based on the given step (_step). 
                         monocycles_w_points = [[order in the path route: int, Knot object, number of points: int]]
    Xfinal: List of numpy.float64, which are the distance in angstrom of the path through the molecule with the given step (_step).

    """

    i = 0
    Xfinal = []
    total_length = 0
    monocycles_w_points = []

    for mono in _monocycles:
        a, b, c = _path_points[i], _path_points[i+1], _path_points[i+2]
        length = np.linalg.norm(a-b) + np.linalg.norm(b-c)
        i += 2

        points = int(length/_step) # rounds down
        mono.append(points)
        monocycles_w_points.append(mono)

        s = length/points
        for j in range(1, points+1):
            Xfinal.append(j*s + total_length)

        total_length += length
    
    return monocycles_w_points, Xfinal


def prep_scans(_scans, _building_blocks, _monocycles):
    """
    prep_scans(_scans: list(list(int, int, str, bool, list(Knot))), _building_blocks: dict, _monocycles: list(int, list(Knot), int)) 
                -> fitted_scans: list(list(int, int, str, bool, list(Knot)), numpy.ndarray), corrected_scans: list(list(int, int, str, bool, list(Knot))

    Function that calls the fit function and get the fitted scan with the "new" number of points for every building block. If the building block is flagged to be reversed, then the fitted scan is reversed. 
    The scan is then padded to the appropriate length. If the building block is a monocycle, it is appended to the corrected_scans list. All scans are appended to the fitted_scans list. Both lists are returned.

    in:
    _scans: List of lists containing data on every building block identified. For every building block, there is a list with the offset, the size of the building block, the key of the building block in the dict 
            (_building_blocks) to access the scan from the database, a boolean value which is True if the scan needs to be reversed as the scan in the data base was obtained in the other direction compared to 
            the direction of the building block in the current path, and finally, a list of Knot Objects that form the building block.
            _scans = [[offset, size of building block, key of the building block in the dict (_building_blocks), boolean value (True if scan needs to be reversed), list of Knot Objects forming the building block]]
    _building_blocks: dict of dict containing the database data. 
                      _building_blocks: {'key': {step: float, scan: numpy.ndarray}}.
    _monocycles: List of list containing info on the monocycles. 
                 _monocycles = [[order in the path route: int, Knot object, number of points: int]]
    
    out:
    fitted_scans: List of lists containing data on the building blocks + the calculated fitted scans.
                  fitted_scans = [[_scans[building block], fitted scan of building block (numpy.ndarray)]]
    corrected_scans: Same as fitted_scans, but only with monocycles.

    """
    
    fitted_scans = []
    corrected_scans = []

    for mol_block_scan in _scans:
        new_n_points = 0
        offset, length, key, reverse = mol_block_scan[0], mol_block_scan[1], mol_block_scan[2], mol_block_scan[3]
        data = _building_blocks[key]
        scan = data['scan']

        start = offset
        end = offset + length - 1

        for i in range(start, end + 1):
            new_n_points += _monocycles[i][-1]

        new_scan = fit_scan(scan, new_n_points, 0.01)

        if reverse:
            new_scan = new_scan[::-1]

        # get number of points pre scan
        pre_points = 0
        pre_array = np.array([])

        if start > 0:
            while start > 0:
                start -= 1
                pre_points += _monocycles[start][-1]
                pre_array = np.zeros((pre_points,))
        
        # get number of points post scan
        post_points = 0
        post_array = np.array([])

        if end < len(_monocycles)-1:
            while end < len(_monocycles)-1:
                end += 1
                post_points += _monocycles[end][-1]
                post_array = np.zeros((post_points,))
        
        # stack all arrays
        new_scan = np.concatenate((pre_array, new_scan, post_array), axis=None)
        fitted_scans.append([mol_block_scan, new_scan])

        if length == 1:
            corrected_scans.append([mol_block_scan, new_scan])
    
    return fitted_scans, corrected_scans


def fit_scan(_ndarray, _new_n_points, _rmsd_threshold):
    """
    fit_scan(_ndarray: numpy.ndarray, _new_n_points: int,  _rmsd_threshold: float) -> numpy.ndarray

    A function that will take a numpy.ndarray of y values assuming the points are equally spaced across the x axis
    and in order, generate a function that is fitted with a cubic spline in the interval [0, 1], and return a new 
    numpy.ndarray of y values with the wanted dimension using the fitted function.

    in:
    _ndarray: 1D numpy array of y values.
    _new_n_points: Number of points desired for the new scan generated from the fitted function.
    _rmsd_threshold: Determines the threshold for when a polynomial fit is accepted.

    out:
    numpy.ndarray

    """

    # generate x_vals for the y_vals in the given _ndarray. CAUTION: only works if y_vals are equally spaced.

    y_vals = _ndarray

    x_vals = np.linspace(0, 1, y_vals.shape[0])

    # now fit the data with splines

    tck = splrep(x_vals, y_vals)

    new_x = np.linspace(0, 1, _new_n_points)
    
    return splev(new_x, tck)



def additivity(n, _fitted_scans, _corrected_scans, _Xfinal, config):
    """
    additivity(n: int, _fitted_scans: list(list(int, int, str, bool, list(Knot)), _corrected_scans: list(list(int, int, str, bool, list(Knot)), 
               _Xfinal: list(numpy.float64), config: configparser.SectionProxy) -> scanrepr: pandas.DataFrame

    This function implements the additivity scheme. First, all scans of building blocks having more than 1 cycle are corrected: 
    BC_i = B_i - M_i - M_{i+1}, TC_i = T_i - BC_i - BC_{i+1} - M_i - M_{i+1} - M_{i+2}, and so forth. The corrected scans are 
    appended to corrected_scans_copy, which is then used to generate a pandas.DataFrame. The final scan is obtained by summing 
    the columns of the dataframe. If smoothing == True, the final data is smoothed using a Savitzky-Golay filter. The x values 
    (distance through the path) are added to the dataframe returned by this function.

    in:
    n: number of rings composing the largest multicycle used for the additivity scheme.
    _fitted_scans: List of lists containing data on the building blocks.
                   _fitted_scans = [[offset, length, key, knots, scan, fitted scan]]
    _corrected_scans: Same as _fitted_scans but only with the monocyclic building blocks.
    _Xfinal: List of numpy.float64, which are the distance in angstrom of the path through the molecule with the given step (_step).
    config: Configurations set in config.ini specific to the additivity module. Here, we get the info
            on function smoothing: True or False.
    
    out:
    scanrepr: pandas.DataFrame containing the fitted and padded scans used for the additivity scheme, the final scan, and the smoothed
              scan by default. The smoothed scan can be omitted (see help).

    """

    corrected_scans_copy = _corrected_scans

    for i in range(2, n+1):
        for mol_block_scan in _fitted_scans:
            length, knots, scan = mol_block_scan[0][1], mol_block_scan[0][4], mol_block_scan[1]
            if length == i:
                corrected_scan = scan
                for building_block in corrected_scans_copy:
                    building_block_knots, building_block_scan = building_block[0][4], building_block[1]
                    if all(x in knots for x in building_block_knots):
                        corrected_scan -= building_block_scan
                corrected_scans_copy.append([mol_block_scan[0], corrected_scan])
    
    scanrepr = pd.DataFrame(np.stack([building_block[-1] for building_block in corrected_scans_copy], axis=1))
    scanrepr['sum'] = scanrepr[list(scanrepr.columns)].sum(axis=1) # sum of all corrected scans (final scan)
    if config.getboolean('smoothing'):
        scanrepr['smoothed'] = savgol_filter(scanrepr['sum'], 15, 3) # smooth final scan

    # format data for output and plotting
    scanrepr.insert(loc=0, column='X', value=_Xfinal)
    scanrepr = scanrepr.round(decimals=2)
    header = [building_block[0][2] for building_block in corrected_scans_copy]
    header.insert(0, 'r')
    header.append('Predicted NICS-XY-Scan')
    if config.getboolean('smoothing'):
        header.append('Smoothed Predicted NICS-XY-Scan')
    scanrepr.columns = header

    return scanrepr

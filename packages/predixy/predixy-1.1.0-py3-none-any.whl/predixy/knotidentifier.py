import numpy as np
import networkx as nx


from . import knot
from . import mol
from . import molloader

from .const import __COV_RADII__
from .fragments import __FRAGMENTS__

def identify(_molrepr, covalency_factor):
    """
    identify(_molrepr: Mol, covalency_factor: float) -> knot: list(Knots), edges: list(tuples)

    Identify the rings in the molecule and initialize them as Knot Object.

    in:
    _molrepr: A molecule, represented by a list of Atoms with their xyz coordinates in Angstroms.
    covalency_factor: A bond is identified if the sum of covelent radii times the covalency factor is larger than the distance between atoms.

    out:
    knots: A list of Knots. Knots represent monocycles in this program. 
    edges: A list of tuples. each tuple is a pair of atom (index) forming a bond in the molecule.

    """

    if 'B' in [atom.element for atom in _molrepr.atoms]: # special case to differentiate between 1,4-diboroinine and its 1,4-dihydro form.
        atom_connectivity = get_connectivity_matrix(_molrepr.atoms, covalency_factor, skip_hydrogen = False) # build connectivity matrix
        edges = get_edges(atom_connectivity) # edges = bonds
        borons = [atom.index for atom in _molrepr.atoms if atom.element == 'B'] # get indices for borons
        new_edges = []
        for edge in edges:
            for boron in borons:
                if (boron in edge) and (_molrepr.atoms[edge[0]].element == 'H' or _molrepr.atoms[edge[1]].element == 'H'): # find a B-H bond
                    _molrepr.atoms[boron].element='BH' # change the "element" from B to BH
            # if not (_molrepr.atoms[edge[0]].element == 'H' or _molrepr.atoms[edge[1]].element == 'H'): # remove all hydrogen containing bonds by not copying them to new edges
            new_edges.append(edge)
        edges = new_edges
    else:
        atom_connectivity = get_connectivity_matrix(_molrepr.atoms, covalency_factor, skip_hydrogen = False) # build connectivity matrix
        edges = get_edges(atom_connectivity) # edges = bonds
    graph = nx.Graph(edges) # generate a mathematical Graph representation of the molecule using networkx
    cycles = nx.cycle_basis(graph) # find all monocycles in the Graph
    knots = get_knots(_molrepr.atoms, cycles, __FRAGMENTS__) # monocycle = Knot. Knot contains all the atoms in the monocycle and index, type, geometrical center
    
    for knot in knots: # differentiate between case A and case B for 5-membered rings with 1 hetero-atom. In case A, the scan goes through the heteroatom, in case B it does not. 
                       # (Finkelstein, P.; Gershoni-Poranne, R. ChemPhysChem 2019, 20, 1508{1520, issn: 1439-4235, DOI: 10.1002/cphc.201900128.)
        if knot.cycle_type in ['fur', 'thi', 'pyl']:
            for atom in knot.atoms:
                if atom.element in ['O', 'S', 'N']:

                    for neighbor in graph.neighbors(atom.index):
                        neighbor_counter = 0
                        for second_neighbor in graph.neighbors(neighbor):
                            if _molrepr[second_neighbor].element != 'H':
                                neighbor_counter += 1
                        
                        if neighbor_counter > 2:
                            knot.cycle_type += 'a'
                            break
                        else:
                            continue

                    if neighbor_counter <= 2:
                        knot.cycle_type += 'b'

    return knots, edges


def get_connectivity_matrix(_atoms, covalency_factor, skip_hydrogen = False):
    """
    get_connectivity_matrix(_atoms: list(Atoms), covalency_factor: float, skip_hydrogen: bool = False) -> numpy.ndarray

    Function that loops through the atoms and returns the connectivity matrix. Two atoms are considered bonded when the distance between them is less 
    or equal to the sum of their covalent radii multiplied by a covalency factor. 

    in:
    _atoms: A list of Atoms with their xyz coordinates in Angstroms.
    covalency_factor: A bond is identified if the sum of covelent radii times the covalency factor is larger than the distance between atoms.
    skip_hydrogen: If True, remove hydrogens completely.

    out:
    connectivity_matrix: A connectivity matrix of dimension len(_atoms) x len(_atoms) where elements are 0 if there is no bond and 1 if there is a bond. 
                         Diagonal elements are 0.
    
    """
    number_of_atoms = len(_atoms)
    connectivity_matrix = np.zeros((number_of_atoms,number_of_atoms), dtype = int) # initialize matrix with 0s 

    for i in range(number_of_atoms):
        for j in range(i+1, number_of_atoms): # start at i+1 because diagonal elements should stay 0
            if skip_hydrogen: # skip hydrogens if set
                if _atoms[i].element == 'H' or _atoms[j].element == 'H':
                    continue
            covalency_cutoff = (__COV_RADII__[_atoms[i].element] + __COV_RADII__[_atoms[j].element]) * covalency_factor # determine cutoff for elements i,j
            distance_ij = np.sqrt(
                (_atoms[i].x - _atoms[j].x)**2 +
                (_atoms[i].y - _atoms[j].y)**2 +
                (_atoms[i].z - _atoms[j].z)**2
            )
            if distance_ij <= covalency_cutoff:
                connectivity_matrix[i,j] = connectivity_matrix[j,i] = 1

    return connectivity_matrix


def get_edges(_atom_connectivity):
    """
    get_edges(_atom_connectivity: numpy.ndarray) -> list(tuple)

    Using the connectivity matrix, this function generates a list of tuple, where every tuple contains the atomic index
    of two atoms bonding.

    in: 
    _atom_connectivity: Connectivity matrix.

    out:
    edges: A list of tuples that represent connections in the connectivity matrix, i.e. bonds in the molecule.

    """

    dimension = _atom_connectivity.shape[0]
    edges = []
    for i in range(dimension):
        for j in range(i + 1, dimension):
            if _atom_connectivity[i,j] == 1:
                edges.append((i,j))
    
    return edges


def get_knots(_atoms, _cycles, _knot_types):
    """
    get_knots(_atoms: list(Atom), _cycles: list(list(int)), _knot_types: dict) -> list(Knot)

    Function that gets the geometric center of each ring of the molecule and initializes the Knot Objects for each monocycle.

    in:
    _atoms: A list of Atoms with their xyz coordinates in Angstroms.
    _cycles: A list of monocycles. Each monocycle is a list of atom indices.
    _knot_types: A dict of monocyle types to look for.

    out:
    knots: A list of Knots (= monocycles).

    """

    knots = [] # initialize list to return
    i = 0
    for cycle in _cycles:
        cycle_atoms = ''
        x_knot = y_knot = z_knot = 0
        for atom in cycle:
            cycle_atoms += _atoms[atom].element
            x_knot += _atoms[atom].x
            y_knot += _atoms[atom].y
            z_knot += _atoms[atom].z
        
        knot_type = get_knot_type(cycle_atoms, _knot_types)
        _knot = knot.Knot(i, knot_type, [_atoms[x] for x in cycle], x_knot/len(cycle), y_knot/len(cycle), z_knot/len(cycle))
        i += 1
        knots.append(_knot)
    
    return knots
        

def get_knot_type(_cycle, _knot_types):
    """
    get_knot_type(_cycle: str, _knot_types: dict) -> string

    Function that identifies the ring type of each monocycle.

    in:
    _cycle: A string of atoms in a monocycle.
    _knot_types: A dict of monocyle types to look for.

    out:
    cycle_type: If it found the type of monocycle in _knot_types, returns it as a string, else None.

    """

    cycle = 2*_cycle
    reversed_cycle = cycle[::-1]
    for cycle_type in _knot_types.keys():
        # check first if _cycle and a given cycle_type are of same length and if yes, check if they contain the same sequence of atoms
        if len(_cycle) == len(_knot_types[cycle_type][1]) and (_knot_types[cycle_type][1] in cycle or _knot_types[cycle_type][1] in reversed_cycle):
            return cycle_type
    
    return None

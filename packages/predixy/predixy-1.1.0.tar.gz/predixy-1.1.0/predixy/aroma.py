import numpy as np


def gen_aroma_input(_path, _outfile, config):
    """
    gen_aroma_input(_path: predixy.path.Path, _outfile: str, config: configparser.SectionProxy) -> aromafile: str

    A function that will take a Path through a molecule and write and return an aromafile.

    in:
    _path: Path through the molecule. 
    _outfile: Filepath for the output file.
    config: Configurations set in config.ini.

    out:
    aromafile: The aromafile as a string.
    """

    # get the path through the molecule, i.e. from bond center to ring center
    path = get_aroma_path(_path.route)
    path = "\n".join("center:" + ",".join(str(i+1) for i in line) for line in path)

    # get all (anti)-aromatic rings in the molecule.
    rings = "\n".join(",".join(str(atom.index + 1) for atom in knot.atoms) for knot in _path.route)

    # put it all together
    aromafile = "geomfile=<enter geometry file here>\nrun={run}\n{path}\naromatic rings\n{rings}\nend".format(run=config['run'], path=path, rings=rings)

    # write + return output
    with open(_outfile, 'w') as of:
        of.write(aromafile)
    return aromafile


def get_aroma_path(_knots):
    """
    get_aroma_path(_knots: list(Knot)) -> path_points: list(tuple)

    A function that will go through a list of connected Knots and find the path where the aroma scan should go through.
    Gives back all bonds and cycle centers it crosses as a list of tuples.

    in:
    _knots: list of Knot objects.

    out:
    path_points: list of tuples.

    """

    # set up output list
    path_points = [] 

    # i = [0..len-2]
    for i in range(len(_knots)-1):
        
        atomsA, atomsB = _knots[i].atoms, _knots[i+1].atoms

        # find which atoms are contained in both knots
        common_atoms = list(set(atomsA).intersection(atomsB))

        # append the bond tuple between knot[i] and knot[i+1] and the ring tuple of knot[i+1]
        path_points.append(tuple(atom.index for atom in common_atoms))
        path_points.append(tuple(atom.index for atom in _knots[i+1].atoms))

        # we did not handle knot[0] yet
        if i == 0:
 
            mid_point = tuple(atom.index for atom in _knots[i].get_opposing_edge(common_atoms))

            # prepend first bond tuple and knot[0]
            path_points.insert(0, mid_point)
            path_points.insert(1, tuple(atom.index for atom in _knots[i].atoms))


        # we need to handle the final bond
        elif i == len(_knots) - 2:

            mid_point = tuple(atom.index for atom in _knots[i+1].get_opposing_edge(common_atoms))
            path_points.append(mid_point)
    
    return path_points


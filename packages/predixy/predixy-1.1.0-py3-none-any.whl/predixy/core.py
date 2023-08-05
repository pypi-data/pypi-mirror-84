import sys
import traceback
import time
import configparser
import os

import argparse as ap

from tabulate import tabulate

from . import molloader
from . import knotidentifier
from . import pathfinder
from . import additivity
from . import utils
from . import plotting
from . import aroma
from . import __version__


__all__ = ['main']

def main():
    timings = { "total" : -time.time()}
    

    # load config
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__),"config.ini")
    config.read(config_path)
    flags = config['printing']

    # how much the covalent bond can be longer by than the sum of covalent radii
    covalency_factor = float(config.get('parameters', 'covalency factor'))

    args = parse_args()

    # figure out where to print to
    log = None
    if flags.getboolean('print to stdout') and not args['basename']:
        log = sys.stdout

    try:
        infile = args['infile']
        basename = os.path.splitext(infile)[0]
        if args['basename']:
            basename = args['basename']
        
        if not log:
            if flags.getboolean('overwrite if file exists'):
                log = open(basename+'.log', 'w')

            elif os.path.exists(basename + '.log'):
                if input("Output file exists. Overwrite? (y, n):\n") == "y":
                    log = open(basename+'.log', 'w')
                else:
                    raise FileExistsError(f"File {basename+'.log'} already exists.")
            else:
                log = open(basename+'.log', 'w')

        if args['miniprint'] or flags.getboolean('miniprint'):
            miniprintlog = log

            # discard nearly all printing
            log = open(os.devnull, 'w')


        # START PROGRAM
        print(utils.__BANNER__.format(version=__version__), file=log)

        # print infile
        with open(infile, 'r') as f:
            print(f"input file: {infile} :\n\n{f.read()}\n", file=log)
        print(utils.__SEPARATOR__, file=log)
        
        # load molecule
        timings["parsing"] = -time.time()
        molrepr = molloader.load(infile)
        timings["parsing"] += time.time()
        print(f"\nLoaded molecule:\n\n{molrepr}\n", file=log)
        print(utils.__SEPARATOR__, file=log)
        
        # rotate molecule into XY plane
        molrepr.align_to_xy_plane()
        print(f"\nRotated molecule:\n\n{molrepr}\n", file=log)
        print(utils.__SEPARATOR__, file=log)

        # identify knots
        print(f"\nUsing a covalency factor of {covalency_factor}\n", file=log)
        timings["knotidentifier"] = -time.time()
        knotrepr, edges = knotidentifier.identify(molrepr, covalency_factor)
        timings["knotidentifier"] += time.time()
        print(f"Found the following knots (monocycles):", file=log)
        undefined_knots = []
        for knot in knotrepr:
            print(knot, file=log)
            if knot.cycle_type is None:
                undefined_knots.append(knot)
        assert len(undefined_knots) == 0, '\nUndefined knots found:\n{}'.format('\n'.join(str(knot) for knot in undefined_knots))

        print("", file=log)
        assert len(knotrepr) > 1, "\nNot enough knots found, need at least 2."
        print(utils.__SEPARATOR__, file=log)

        # find path through knots
        timings["pathfinder"] = -time.time()
        path = pathfinder.find(knotrepr)
        # turn the path around if it is right to left
        if path[0].route[0].x > path[0].route[-1].x:
            path[0].route.reverse()
        timings["pathfinder"] += time.time()
        assert len(path) > 0, "\nNo path through the molecule could be found."
        print(f"\nIdentified path through knots:\n{path[0]}\n", file=log)
        print(utils.__SEPARATOR__, file=log)

        # run additivity scheme on path[0]; we can't deal with branched molecules yet
        timings["additivity"] = -time.time()
        scanrepr, pts_through_path = additivity.generate_scan(path[0].route, config['additivity'])
        timings["additivity"] += time.time()
        if len(knotrepr) > 3: # change this number if using building blocks with more than 3 rings
            print(f"\nBuilding blocks and predicted NICS-XY-Scan:\n", file=log)
        else:
            print(f"\nScan data:"
                  f"\nThe following was not calculated using the additvity scheme, but is raw data from the database.\n", file=log)
        print(tabulate(scanrepr, headers='keys', showindex=False, tablefmt='simple', floatfmt='.2f'), file=log)
        print("", file=log)
        print(utils.__SEPARATOR__, file=log)

        # miniprint
        if args['miniprint'] or flags.getboolean('miniprint'):
            print(tabulate(scanrepr.iloc[:,[0, -1]], showindex=False, tablefmt='plain', floatfmt='.2f'), file=miniprintlog)

        # write aroma file
        if args["aromafile"] or config.getboolean('aroma', 'write aroma file'):
            timings["aroma"] = -time.time()
            aroma_output = aroma.gen_aroma_input(path[0], basename+'.arm', config['aroma'])
            print(f"\nAroma file generated: {basename+'.arm'}\n\n{aroma_output}\n", file=log)
            print(utils.__SEPARATOR__, file=log)
            timings["aroma"] += time.time()

        # plotting
        if config['plotting'].getboolean('show graph') or config['plotting'].getboolean('save graph') or args['showPlot']:
            timings["plotting"] = -time.time()
            if config['plotting'].getboolean('show graph') or args['showPlot']:
                print("\nShowing plot ...", end=' ', file=log)
            plotting.get_figure(molrepr, edges, scanrepr, pts_through_path, basename + '.'+config["plotting"]["graph file format"], config["plotting"], args['showPlot'])
            if config['plotting'].getboolean('show graph') or args['showPlot']:
                print("done.\n", file=log)
            if config['plotting'].getboolean('save graph'):
                print(f"\nPlot file generated: {basename+'.'+config['plotting']['graph file format']}\n", file=log)
            print(utils.__SEPARATOR__, file=log)
            timings["plotting"] += time.time()

        print(f"\nNormal termination.\n{time.strftime('%d.%m.%Y %H:%M:%S UTC%z', time.localtime())}\n", file=log)
        timings["total"] += time.time()
        print(f"Timings:", file=log)
        print(f"Parsing: {timings['parsing']:18.6f} s", file=log)
        print(f"Knotidentifier: {timings['knotidentifier']:11.6f} s", file=log)
        print(f"Pathfinder: {timings['pathfinder']:15.6f} s", file=log)
        print(f"Additivity: {timings['additivity']:15.6f} s", file=log)
        if args["aromafile"] or config.getboolean('aroma', 'write aroma file'):
            print(f"Aromafile: {timings['aroma']:16.6f} s", file=log)
        if config['plotting'].getboolean('show graph') or config['plotting'].getboolean('save graph'):
            print(f"Plotting: {timings['plotting']:17.6f} s", file=log)
        print(f"Total: {timings['total']:20.6f} s\n", file=log)
        sys.exit(0)

    except Exception as err:
        if args['miniprint'] or flags.getboolean('miniprint'):
            log.close()
            log = miniprintlog
        print(f"Error termination.\n{time.strftime('%d.%m.%Y %H:%M:%S UTC%z', time.localtime())}\n", file=log)
        if log != sys.stdout:
            traceback.print_exc(file=log)
        raise

    finally:
        if hasattr(log, 'close'):
            log.close()



def parse_args():
    """
    Argument parsing
    """
    parser = ap.ArgumentParser(description=f"Predixy version {__version__}.\n\nA tool to predict NICS-xy by using an additivity scheme.", epilog=f"Some default behavior can be changed in the config file:\n{os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))}")

    parser.add_argument("infile", metavar="INFILE", help="Input file. Supported types: .xyz", type=str, default=None)
    parser.add_argument("-b", "--basename", metavar="BASENAME", dest="basename", help="Use BASENAME for all output files. Make sure to give the full path. If not set, behavior depends on config.", type=str, default=None)
    parser.add_argument("-a", "--aroma", dest="aromafile", action="store_true", help="Generate aroma input file. If not set, behavior depends on config.")
    parser.add_argument("-p", "--show-plot", dest="showPlot", action="store_true", help="Show the plot at the end.")
    parser.add_argument("-m", "--miniprint", dest="miniprint", action="store_true", help="Print only the final predicted NICS scan.")


    args = vars(parser.parse_args())    
    
    return args


if __name__ == '__main__':
    main()
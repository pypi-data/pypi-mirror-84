import numpy as np
import json
import h5py

from .utils import listify, cs2span
from .constants import int_, float_
from .structure import Structure
from .source import Source, PlaneSource
from .probe import Probe, TimeProbe, FreqProbe
from .grid import Grid
from .json_ops import write_parameters, write_structures, write_sources, \
                        write_probes

class Simulation(object):
    """
    Main class for building a simulation model.
    """

    def __init__(self, center=np.array([0., 0., 0.]),
                    size=np.array([1., 1., 1.]),
                    resolution=0.1, structures=[], sources=[], probes=[],
                    run_time=0.,
                    Npml=np.array([[0, 0], [0, 0], [0, 0]])):
        """Parameters
        ----------
        center : list or np.ndarray, optional
            3D vector defining the center of the simulation domain.
        size : list or np.ndarray, optional
            3D vector defining the size of the simulation domain.
        resolution :  float or list or np.ndarray of float, optional
            Resolution in all directions, or a 3D vector defining it separately 
            in x, y, and z. 
        structures : Structure or a list of Structure objects, optional
            Empty list (default) means vacuum. 
        sources : Source or a list of Source objects, optional
            Source(s) to be added to the simulation.
        probes : Probe or a list of Probe objects, optional
            Probe(s) to be added to the simulation.
        Npml : list or np.ndarray of int
            Shape (3, 2) array defining the thickness in grid points of the PML 
            in (xmin, xmax), (ymin, ymax), and (zmin, zmax).

        Note
        ----
        Sources and Probes can also be added after initialization using 
        `Simulation.add()`.
        """

        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)
        self.grid = Grid(self.span, resolution)
        self._structures, self._sources = [], []

        self.set_run_time(run_time)
        
        self.add(sources)

        # Time and frequency domain probes
        self._tprobes, self._fprobes = [], []
        self.add(structures)
        self.add(probes)

        # Set PML size and compute parameters
        self.Npml = np.array(Npml, dtype=int_)

        # JSON file from which the simulation is loaded
        self.fjson = None

    @property
    def structures(self):
        """ List conaining all Structure objects. """
        return self._structures

    @structures.setter
    def structures(self, new_struct):
        # Make a list if a single object was given.
        self.add(new_struct)

    @property
    def sources(self):
        """ List conaining all Source objects. """
        return self._sources

    @sources.setter
    def sources(self, new_sources):
        # Make a list if a single object was given.
        self.add(new_sources)

    @property
    def tprobes(self):
        """ List conaining all TimeProbe objects. """
        return self._tprobes

    @tprobes.setter
    def tprobes(self, new_probes):
        # Make a list if a single object was given.
        self.add(new_probes)

    @property
    def fprobes(self):
        """ List conaining all FreqProbe objects. """
        return self._fprobes

    @fprobes.setter
    def fprobes(self, new_probes):
        # Make a list if a single object was given.
        self.add(new_probes)

    def _add_structure(self, structure):
        """ Adds a Structure object to the list of structures and to the 
        permittivity array. """
        self._structures.append(structure)
        if structure.name is None:
            structure.name = 'obj' + str(len(self.structures))

    def _add_source(self, source):
        """ Adds a Source object to the list of sources.
        """
        source._get_Jt(self.grid.tmesh)
        if isinstance(source, PlaneSource):
            # Make the size spanning the whole simulation if no size provided
            source._sim_span(self.span)
        self._sources.append(source)
        if source.name is None:
            source.name = 'source' + str(len(self.sources))

    def _add_probe(self, probe):
        """ Adds a time or frequency domain Probe object to the 
        corresponding list of probes.
        """
        if isinstance(probe, TimeProbe):
            self._tprobes.append(probe)
            if probe.name is None:
                probe.name = 'tprobe' + str(len(self.tprobes))
        elif isinstance(probe, FreqProbe):
            self._fprobes.append(probe)
            if probe.name is None:
                probe.name = 'fprobe' + str(len(self.fprobes))

    def _pml_config(self):
        """Set the CPML parameters. Default configuration is hard-coded. This 
        could eventually be exposed to the user, or, better, named PML profiles 
        can be created.
        """
        cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
                    'korder': 3, 'kmin': 1., 'kmax': 3., 
                    'aorder': 1, 'amin': 0., 'amax': 0}
        return cfs_config

    def set_run_time(self, run_time):
        """ Set the total time (in seconds) of the simulated field evolution.
        """
        self.T = run_time
        self.grid.set_tmesh(self.T)
        self.Nt = np.int(self.grid.tmesh.size)

    def add(self, objects):
        """
        Add a list of objects. Can contain structures, sources, and/or probes.
        """

        for obj in listify(objects):
            if isinstance(obj, Structure):
                self._add_structure(obj)
            elif isinstance(obj, Source):
                self._add_source(obj)
            elif isinstance(obj, Probe):
                self._add_probe(obj)

    def load_results(self, dfile):
        """Store the probe data recorded from a Tidy3D run. The simulation 
        object stores a list of all TimeProbes and all FreqProbes 
        (``Simulation.tprobes`` and ``Simulation.fprobes``, respectively). 
        Each of those is loaded with a ``Pvals`` property storing the recorded 
        electric field in a 5D array arranged as 
        ``[pol, indx, indy, indz, inds]``, where ``pol`` is the polarization 
        component and ``inds`` is either the time or the frequency index.
        
        Parameters
        ----------
        dfile : str
            Path to the file containing the simulation results.
        """

        pfile = h5py.File(dfile, "r")
        for (ip, probe) in enumerate(self.tprobes):
            pname = "tprobe_" + probe.name
            probe.Pvals = np.array(pfile[pname]["E"])
            probe.Pinds_beg = pfile[pname]["indspan"][0, :]
            probe.Pinds_end = pfile[pname]["indspan"][1, :]

        for (ip, probe) in enumerate(self.fprobes):
            pname = "fprobe_" + probe.name
            probe.Pvals = np.array(pfile[pname]["E"])
            probe.Pinds_beg = pfile[pname]["indspan"][0, :]
            probe.Pinds_end = pfile[pname]["indspan"][1, :]

        pfile.close()

    def export(self):
        """Return a dictionary with all simulation parameters and objects.
        """
        
        js = {}
        js["parameters"] = write_parameters(self)
        js["objects"] = write_structures(self.structures)
        js["sources"] = write_sources(self.sources)
        js["probes"] = write_probes(self.tprobes)
        js["probes"] += write_probes(self.fprobes)

        return js

    def export_json(self, fjson):
        """Export the simulation to a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """
        
        self.fjson = fjson
        with open(fjson, 'w') as json_file:
            json.dump(self.export(), json_file, indent=4)
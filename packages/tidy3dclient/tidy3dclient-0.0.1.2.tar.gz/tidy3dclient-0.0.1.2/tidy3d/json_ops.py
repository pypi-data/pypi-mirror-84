import numpy as np

from .structure import Box, Sphere, PolySlab, GdsSlab
from .source import GaussianSource, PlaneSource
from .probe import TimeProbe, FreqProbe
from .utils import listify, span2cs, cs2span

def write_parameters(sim):
    """ Convert simulation parameters to a dict.
    """
    cent, size = span2cs(sim.grid.span)
    parameters = {
                "unit_length": "um",
                "unit_frequency": "THz",
                "unit_time": "ps",
                "x_cent": float(cent[0]),
                "y_cent": float(cent[1]),
                "z_cent": float(cent[2]),
                "x_span": float(size[0]),
                "y_span": float(size[1]),
                "z_span": float(size[2]),
                "resolution": sim.grid.res.tolist(),  
                "Npml" : sim.Npml.tolist(),
                "run_time": sim.T*1e12
                }

    return parameters

def write_structures(structures):
    """ Convert a list of Structure objects to a list of text-defined objects.
    """
    obj_list = []
    for structure in structures:
        obj = {
                "name": structure.name,
                "permittivity": float(structure.eps),
                "conductivity": float(structure.sigma)
                }
        if isinstance(structure, Box):
            cent, size = structure.center, structure.size
            obj.update({"type": "Box",
                        "x_cent": float(cent[0]),
                        "y_cent": float(cent[1]),
                        "z_cent": float(cent[2]),
                        "x_span": float(size[0]),
                        "y_span": float(size[1]),
                        "z_span": float(size[2])})
            obj_list.append(obj)
        elif isinstance(structure, Sphere):
            obj.update({"type": "Sphere",
                        "x_cent": float(structure.position[0]),
                        "y_cent": float(structure.position[1]),
                        "z_cent": float(structure.position[2]),
                        "radius": float(structure.radius)})
            obj_list.append(obj)
        elif isinstance(structure, PolySlab):
            obj.update({"type": "PolySlab",
                        "vertices": structure.vertices.tolist(),
                        "z_cent": float(structure.z_cent),
                        "z_size": float(structure.z_size)})
            obj_list.append(obj)

        # Split GdsSlab into PolySlab objects
        if isinstance(structure, GdsSlab):
            for (ip, verts) in enumerate(structure.gds_cell.get_polygons()):
                poly = obj.copy()
                poly['name'] += '_poly%04d'%ip
                poly.update({"type": "PolySlab",
                        "vertices": verts.tolist(),
                        "z_cent": float(structure.z_cent),
                        "z_size": float(structure.z_size)})
                obj_list.append(poly)
        
    return obj_list

def write_sources(sources):
    src_list = []
    for source in sources:
        if isinstance(source, GaussianSource):
            src = {
                "name": source.name,
                "type": "GaussianSource",
                "center": source.center.tolist(),
                "size": source.size.tolist(),
                "polarization": source.polarization, 
                "frequency": source.f0*1e-12, 
                "fwidth": source.fwidth*1e-12,
                "offset": source.offset,
                "amplitude": 1.0,
                "current": "electric"        
                }
        elif isinstance(source, PlaneSource):
            src = {
                "name": source.name,
                "type": "PlaneSource",
                "normal": source.normal,
                "pos_offset": source.pos_offset,
                "polarization": source.polarization, 
                "frequency": source.f0*1e-12, 
                "fwidth": source.fwidth*1e-12,
                "offset": source.offset,
                "amplitude": 1.0,
                "current": "electric"        
                }
        src_list.append(src)

    return src_list

def write_probes(probes):
    prb_list = []
    for probe in probes:
        cent, size = span2cs(probe.span)
        prb = {"name": probe.name,
                "x_cent": float(cent[0]),
                "y_cent": float(cent[1]),
                "z_cent": float(cent[2]),
                "x_span": float(size[0]),
                "y_span": float(size[1]),
                "z_span": float(size[2]),
                "field": "E"
                }
        if isinstance(probe, TimeProbe):
            prb.update({
                "type": "TimeProbe",  
                })
        elif isinstance(probe, FreqProbe):
            prb.update({
                "type": "FrequencyProbe",
                "frequency": [f*1e-12 for f in probe.freqs]
                })
        prb_list.append(prb)

    return prb_list

def read_structures(js, scale_l=1):
    structures = []
    for obj in js['objects']:
        if obj['type'].lower()=='box':
            cent = np.array([obj['x_cent'], obj['y_cent'],
                        obj['z_cent']])*scale_l
            size = np.array([obj['x_span'], obj['y_span'],
                        obj['z_span']])*scale_l
            structures.append(Box(center=cent, size=size,
                                eps=obj['permittivity'],
                                sigma=obj['conductivity'],
                                name=obj['name']))
        elif obj['type'].lower()=='sphere':
            cent = [obj['x_cent'], obj['y_cent'], obj['z_cent']]
            structures.append(Sphere(position=cent, radius=obj['radius'], 
                                eps=obj['permittivity'],
                                sigma=obj['conductivity'],
                                name=obj['name']))
        elif obj['type'].lower()=='polyslab':
            structures.append(PolySlab(vertices=obj['vertices'],
                                z_cent=obj['z_cent'], z_size=obj['z_size'], 
                                eps=obj['permittivity'],
                                sigma=obj['conductivity'],
                                name=obj['name']))
        else:
            raise NotImplementedError("Unknown structure type " + obj['type'])
    return structures

def read_sources(js, scale_l=1, scale_f=1):
    sources = []
    js_params = js['parameters']
    for src in js['sources']:
        if src['type'].lower()=='planesource':
            x, y, z = 0, 0, 0
            x_sp, y_sp, z_sp = 0, 0, 0
            if src['normal'].lower() == 'x':
                y_sp, z_sp = 2*js_params['y_span'], 2*js_params['z_span']
                x = src['pos_offset']
            elif src['normal'].lower() == 'y':
                x_sp, z_sp = 2*js_params['x_span'], 2*js_params['z_span']
                y = src['pos_offset']
            elif src['normal'].lower() == 'z':
                x_sp, y_sp = 2*js_params['x_span'], 2*js_params['y_span']
                z = src['pos_offset']
            cent = scale_l*np.array([x, y, z])
            size = scale_l*np.array([x_sp, y_sp, z_sp])
            sources.append(GaussianSource(center=cent, size=size, 
                            f0=src['frequency']*scale_f,
                            fwidth=src['fwidth']*scale_f,
                            amplitude=src['amplitude'],
                            polarization=src['polarization'].lower()))
        elif src['type'].lower()=='gaussiansource':
            sources.append(GaussianSource(center=src['center'],
                            size=src['size'], 
                            f0=src['frequency']*scale_f,
                            fwidth=src['fwidth']*scale_f,
                            offset=src['offset'],
                            amplitude=src['amplitude'],
                            polarization=src['polarization'].lower()))
        else:
            raise NotImplementedError("Unknown source type " + source['type'])
    return sources

def read_probes(js, scale_l=1, scale_f=1):
    probes = []
    for prb in js['probes']:
        if prb['type'].lower()=='frequencyprobe':
            cent = np.array([prb['x_cent'], prb['y_cent'],
                                    prb['z_cent']])*scale_l,
            size = np.array([prb['x_span'], prb['y_span'],
                                    prb['z_span']])*scale_l
            probes.append(FreqProbe(center=cent, size=size,
                            freqs=[f*scale_f for f in listify(prb['frequency'])],
                            field=prb['field'],
                            name=prb['name']))
        elif prb['type'].lower()=='timeprobe':
            cent = np.array([prb['x_cent'], prb['y_cent'],
                                    prb['z_cent']])*scale_l,
            size = np.array([prb['x_span'], prb['y_span'],
                                    prb['z_span']])*scale_l
            probes.append(TimeProbe(center=cent, size=size,
                            field=prb['field'],
                            name=prb['name']))
        else:
            raise NotImplementedError("Unknown probe type " + prb['type'])
    return probes

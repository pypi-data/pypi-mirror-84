import numpy as np

from .utils import inside_box, cs2span
from .constants import int_, float_

class Source(object):

    def __init__(self, f0, name=None):
        """
        Base class for a source inisde a simulation.

        Parameters
        ----------
        f0 : float
            Carrier frequency in Hertz.
        """
        self.f0 = f0
        self.name = None if name is None else str(name)

    def inside(self, mesh):
        return inside_box(self.span, mesh, include_zero_size=True)

    def get_Jinds(self, mesh):
        """ Compute Jinds giving the position of the source currents.
        """

        mask = self.inside(mesh)
        if np.nonzero(mask)[0].size==0: 
            return np.zeros((0, 3), dtype=int_)
        
        Jinds = np.array(np.nonzero(mask)).T
        return Jinds.astype(int_)

class GaussianSource(Source):
    """ Electric current source with Gaussian-pulse time dependence in a 
    rectangular 3D region.
    """
    def __init__(self, center, size, f0, fwidth, offset=5., amplitude=1.,
                    polarization='z', name=None):
        """ Construct.
        
        Parameters
        ----------
        center : array_like
            Shape (3, ): x, y, and z position of the center of the source.
        size : array_like
            Shape (3, ): size in x, y, and z.
        f0 : float
            Carrier frequency in Hertz.
        fwidth : float
            Frequency bandwidth in Hertz. 
        offset : float, optional
            The peak of the Gaussian is attained at time ``t = offset/fwidth``.
        amplitude : float, optional
            Amplitude.
        polarization : str, optional
            Electric current source polarized along `x`, `y`, or `z`.
        name : str, optional
            Custom name of the source.     
        """
        super().__init__(f0, name)
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)
        self.fwidth = fwidth
        self.offset = offset
        self.amplitude = amplitude
        self.polarization = polarization

    def _time_dep(self, tmesh):
        """ Compute the time dependence of the source over ``tmesh``, using a 
        first-derivative of a Gaussian for the envelope.
        """
        tt0 = tmesh - self.offset/self.fwidth
        G = (self.f0 + tt0 * self.fwidth**2)/self.f0 * \
                np.exp(-2j*np.pi*self.f0*tmesh - tt0**2/2*self.fwidth**2)    
        return self.amplitude*np.real(G)

    def _get_Jt(self, tmesh):
        """ Compute Jt giving the time-dependence of the source currents.
        """

        if tmesh is None:
            Jt = np.zeros((0, 3), dtype=float_)
        else:
            Jt = np.zeros((tmesh.size, 3))
            G = self._time_dep(tmesh)
            if self.polarization == 'x' : 
                Jt[:, 0] = G
            elif self.polarization == 'y':
                Jt[:, 1] = G
            elif self.polarization == 'z':
                Jt[:, 2] = G

        self.Jt = Jt.astype(float_)
        return self.Jt

class PlaneSource(GaussianSource):
    """ Electric current source with Gaussian-pulse time dependence spanning a 
    2D plane inside the simulation.
    """
    def __init__(self, normal, pos_offset, f0, fwidth, offset=5., amplitude=1.,
                    polarization='z', name=None):
        """ Construct.
        
        Parameters
        ----------
        normal : {'x', 'y', 'z'}
            Axis normal to the plane of the source.
        pos_offset : float
            Position of the plane along the nomral axis.
        f0 : float
            Carrier frequency in Hertz.
        fwidth : float
            Frequency bandwidth in Hertz. 
        offset : float, optional
            The peak of the Gaussian is attained at time ``t = offset/fwidth``.
        amplitude : float, optional
            Amplitude.
        polarization : str, optional
            Electric current source polarized along `x`, `y`, or `z`.
        name : str, optional
            Custom name of the source.     
        """

        self.normal = normal
        self.pos_offset = pos_offset
        self.f0 = f0
        self.fwidth = fwidth
        self.offset = offset
        self.amplitude = amplitude
        self.polarization = polarization
        self.name = name

    def _sim_span(self, sim_span):
        """ Make the plane of the source span the whole simulation domain.
        """
        center = np.array([0, 0, 0], dtype=float_)
        size = np.array([0, 0, 0], dtype=float_)

        if self.normal=='x':
            size[[1, 2]] = 2*np.amax(np.abs(sim_span[[1, 2], :])) 
            center[0] = self.pos_offset
        elif self.normal=='y':
            size[[0, 2]] = 2*np.amax(np.abs(sim_span[[0, 2], :])) 
            center[1] = self.pos_offset
        elif self.normal=='z':
            size[[0, 1]] = 2*np.amax(np.abs(sim_span[[0, 1], :])) 
            center[2] = self.pos_offset

        super().__init__(center, size, self.f0,
                    self.fwidth, self.offset, self.amplitude,
                    self.polarization, self.name)
        

import numpy as np
import cmath
import matplotlib.pyplot as plt
import numpy.typing as npt

Rc = 5.9e3
Xm = 5.78e3
Req = 17.1
Xeq = 22.6       # Ohms
I_rated = 500e-3 # A
V_rated = 120    # V
S_rated = 55     # VA

class _8341_xfmr():
    """
    Simulation model of the 8341 xfmr
    """
    def __init__(self, rc=Rc, xm=Xm, req=Req, xeq=Xeq, i_rated=I_rated, v_rated=V_rated):
        self.rc = rc
        self.xm = xm
        self.req = req
        self.xeq = xeq
        self.i_rated = i_rated
        self.v_rated = v_rated
        self._vp = v_rated
        return
        
    def run(self, s_load, theta):
        """
        Determines the primary voltage required to provide rated current and voltage to
        the load provided
        """
        theta *= cmath.pi/180
        self._vp = (self.req + self.xeq*1j)*(self.i_rated*np.cos(theta) - self.i_rated*np.sin(theta)*1j) + self.v_rated
        return self._vp
    
    def load_reg(self, s_load, theta):
        """
        Determines the load voltage regulation for the 8341 xfmr
        for the load provided.
        """
        vp = cmath.polar(self.run(s_load, theta))[0]
        vnl = self.v_rated
        return np.abs((vp - vnl))/vp * 100
        
    def efficiency(self, s_load, theta):
        """
        Determines the efficiency of the 8341 xfmr achievable for the
        load provided.
        """
        theta *= cmath.pi/180
        vp    = cmath.polar(self.run(s_load, theta))[0]
        pout  = s_load*np.cos(theta)
        pcore = (vp**2)/self.rc
        pcu   = self.i_rated**2 * self.req
        eff   = (pout / (pout + pcore + pcu) ) * 100
        return eff

    def current_check(self, i_line, c_i):
        """
        Gives notice if i_line will exceed current rating
        """
        res = not(i_line < c_i*self.i_rated)
        print(res)
        return res
        
    def voltage_check(self, vp, c_vo, c_vu):
        """
        Gives notice if primary voltage is over or undervoltage
        """
        v_over = not(vp > c_vu * self.v_rated)
        v_under = not(vp < c_vo * self.v_rated)
        print(v_over, v_under)


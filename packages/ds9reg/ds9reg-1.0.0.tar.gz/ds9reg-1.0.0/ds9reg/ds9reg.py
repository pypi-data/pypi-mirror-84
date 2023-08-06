from astropy.wcs.utils import skycoord_to_pixel
from astropy.coordinates import SkyCoord
import astropy.units as units
import astropy.wcs as wcs
import numpy as np

class DS9Reg:
    """
    DS9Reg is a class facilitating coordinate transformation using DS9 region file as an input.
    #####
    + Inputs:
      - region_file = DS9 region file with name on each entry. ONLY value as RADEC and unit as sexagesimal is supported in this version.
      - wcs = astropy.wcs.WCS object. (Example: wcs = astropy.wcs.WCS(fits.open(fits_file)['SCI'].header)).
      - region_type = 'RADEC' only for this version
      - region_unit = 'sexagesimal' only for this version
    + Compute:
      - self.compute_xy() after properly instantiated will compute pixel xy coordinates.
    + Output:
      - self.xy = a dict of key:value where key = name of each entry from the region_file and value = a dict of key as 'X' and 'Y' with the corresponding values of pixel coordinate from the transformation.
    """
    def __init__(self,region_file,wcs,region_type='RADEC',region_unit='sexagesimal'):
        self.region_file = region_file
        self.wcs = wcs
        self.region_type = region_type
        self.region_unit = region_unit
        self.region_file_read = self._region_file_read()
        self.map = self._map()
        self.frame = self._frame()
        self.regions = self._regions()
    def compute_xy(self):
        string_x,string_y = self._get_string_xy(self.region_type)
        unit_x,unit_y = self._get_units(self.region_unit)
        name_list = self.regions.keys()
        out = {}
        for i in name_list:
            name = i
            coords = [self.regions[name][string_x],self.regions[name][string_y]]
            skycoord = SkyCoord('{0} {1}'.format(coords[0],coords[1]),frame=self.frame,unit=(unit_x, unit_y))
            xy = skycoord_to_pixel(skycoord,self.wcs)
            out[name] = {'X':xy[0].tolist(),'Y':xy[1].tolist()}
        self.xy = out
    def _regions(self):
        out = {}
        string_x,string_y = self._get_string_xy(self.region_type)
        for i in self.map['regions']:
            t = self.region_file_read[i].split(' ')
            xy,name = t[0],t[-1]
            x,y = xy.split('(')[-1].split(',')[0],xy.split('(')[-1].split(',')[1]
            name = name.split('}')[0].split('{')[-1]
            out[name] = {string_x:x,string_y:y}
        return out
    def _frame(self):
        return self.region_file_read[self.map['frame']]
    def _map(self):
        return {'frame':2,'regions':np.arange(3,len(self.region_file_read))}
    def _region_file_read(self):
        out = {}
        f = open(self.region_file,'r')
        f = f.read().splitlines()
        for ii,i in enumerate(f):
            out[ii] = i
        return out
    def _get_string_xy(self,region_type):
        if region_type=='RADEC':
            string_x,string_y = 'RA','DEC'
        return string_x,string_y
    def _get_units(self,region_unit):
        if region_unit=='sexagesimal':
            unit_x,unit_y = units.hourangle,units.deg
        return unit_x,unit_y
                
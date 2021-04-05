import sys # better management of the exceptions
from astroquery.simbad import Simbad # integration with simbad
import astropy.units as u # managing units of measure
from astropy.coordinates import SkyCoord # managing coordinate systems

######### defining class which will retrieve the Messier Catalogue
class megalo_catalogueretriever:
    def __init__(self):
        self.messierObjects = []
        self.typeObjects = set()
        try:
            self.messierObjects, self.typeObjects = self.retrieving()
        except Exception as e:
            print(str(e))

    def retrieving(self):
        try:
            Simbad.add_votable_fields('otype(V)') # verbose - type
            messier_catalog = Simbad.query_catalog('Messier') # retrieving messier catalog
            messierObjects = [] # here I will store the 110 objects
            type_messierObjects = set() # here I will store the object types
            for messier_object in messier_catalog:
                # creating a single object
                mo = generatingMessierObject(messier_object['MAIN_ID'],
                                             messier_object['OTYPE_V'],
                                             messier_object['RA'],
                                             messier_object['DEC'])
                messierObjects.append(mo)
                type_messierObjects.add(mo.type)
            return messierObjects, type_messierObjects
        except Exception as e:
            print(str(e))

######### defining wrapper class for Messier Objects
class MessierObject(object):
    name = ""
    type = ""
    galacticLatitude = 0
    galacticLongitude = 0

    def __init__(self, name, type, ra, dec):
        c = SkyCoord(str(ra) + ' ' + str(dec), unit=(u.hourangle, u.deg))
        self.name = name.decode('utf-8').replace(" ","")
        self.type = type.decode('utf-8')
        self.galacticLatitude = c.galactic.l # from ra to gal_lat
        self.galacticLongitude = c.galactic.b # from dec to gal_long

def generatingMessierObject(name, type, ra, dec):
    messierObject = MessierObject(name, type, ra, dec)
    return messierObject

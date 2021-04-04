######################### LIBRARIES #########################
from astroquery.simbad import Simbad
from pprint import pprint
import astropy.coordinates as coord
import astropy.units as u
from astropy.io import ascii
from astropy.coordinates import SkyCoord
import math as m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import colors as mcolors
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

listprocol = ['bisque','k','aquamarine','antiquewhite','w','y','azure','beige','blanchedalmond','aliceblue','cornsilk','burlywood']
listpromarkers = ['.',',','None',None,' ','']

gal_sizeOfMarkers = 10
gal_sizeOfFont = 4
sizeOfMarkers = 10
sizeOfFont = 8
offset = 0.5

zoom_1_x = [-95,-60]
zoom_1_width = zoom_1_x[1] - zoom_1_x[0]
zoom_1_y = [70,80]
zoom_1_height = zoom_1_y[1] - zoom_1_y[0]

zoom_2_x = [-5,20]
zoom_2_width = zoom_2_x[1] - zoom_2_x[0]
zoom_2_y = [-10,15]
zoom_2_height = zoom_2_y[1] - zoom_2_y[0]

markerDictionary = Line2D.markers
newDic = {}
for key in markerDictionary:
    if key not in listpromarkers:
        newDic[key] = markerDictionary[key]
#print(newDic)

lrs = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = {}
for key in lrs:
    if key not in listprocol:
        colors[key] = lrs[key]

class MessierObject(object):
    name = ""
    type = ""
    ra = 0
    dec = 0

    def __init__(self, name, type, ra, dec):
        c = SkyCoord(str(ra) + ' ' + str(dec), unit=(u.hourangle, u.deg))
        self.name = name.decode('utf-8').replace(" ","")
        self.type = type.decode('utf-8')
        self.ra = c.galactic.l
        self.dec = c.galactic.b

def generatingMessierObject(name, type, ra, dec):
    messierObject = MessierObject(name, type, ra, dec)
    return messierObject

Simbad.add_votable_fields('otype(V)')
messier_catalog = Simbad.query_object("m *", wildcard=True)
#print(messier_catalog)
messierObjects = []
type_messierObjects = set()
for messier_object in messier_catalog:
    mo = generatingMessierObject(messier_object['MAIN_ID'],
                                 messier_object['OTYPE_V'],
                                 messier_object['RA'],
                                 messier_object['DEC'])
    messierObjects.append(mo)
    type_messierObjects.add(mo.type)
#print(type_messierObjects)

markersNew = {}
for type, marker, c in zip(type_messierObjects, newDic.keys(), colors.keys()):
    markersNew[type] = str(marker)+'-'+str(c)
#print(markersNew)

legend_list = []
for key in markersNew.keys():
    m = mlines.Line2D([], [], color=markersNew[key].split('-')[1], marker=markersNew[key].split('-')[0], linestyle='None', markersize=sizeOfMarkers, mew=1, label=key)
    legend_list.append(m)

fig = plt.figure(figsize=(15,10))
spec = gridspec.GridSpec(ncols=3, nrows=3, figure=fig)
fig.suptitle('Distribution of Messier Objects (Galactic frame)')
fig.patch.set_linewidth(4)
fig.patch.set_edgecolor('r')

ax_galaxy = fig.add_subplot(spec[0:2, :], projection='hammer')
ax_galaxy.grid(True)
ax_galaxy.set_title('Galactic frame')
ax_galaxy.locator_params(axis='x', nbins=7)
ax_galaxy.set_xlabel(r'Galactic latitude $\mathrm{[\degree]}$')
ax_galaxy.set_ylabel(r'Galactic longitude $\mathrm{[\degree]}$')
#ax_galaxy.legend(handles=legend_list, loc="lower right", fontsize=sizeOfFont)
for ox in messierObjects:
    x = ox.ra.wrap_at('180d').radian
    y = ox.dec.radian
    mark = markersNew[ox.type].split('-')[0]
    kk = markersNew[ox.type].split('-')[1]
    ax_galaxy.scatter(x,y, marker = mark , s=gal_sizeOfMarkers, linewidth=1, color= kk, zorder = 100)
    #ax_galaxy.annotate(str(ox.name), (x,y), fontsize = gal_sizeOfFont)
    #print(str(ox.name) + '--' + str(markersNew[ox.type].split('-')[1]))
rect = mpatches.Rectangle((np.radians(zoom_1_x[0]), np.radians(zoom_1_y[0])), np.radians(zoom_1_width), np.radians(zoom_1_height), linewidth=1, edgecolor='r', facecolor='none')
ax_galaxy.add_patch(rect)
rect2 = mpatches.Rectangle((np.radians(zoom_2_x[0]), np.radians(zoom_2_y[0])), np.radians(zoom_2_width), np.radians(zoom_2_height), linewidth=1, edgecolor='r', facecolor='none')
ax_galaxy.add_patch(rect2)

ax_zoom1 = fig.add_subplot(spec[2, 0])
ax_zoom1.grid(True)
ax_zoom1.set_title('Zoomed region ' + str(zoom_1_width) + r'$\mathrm{\degree}$x' + str(zoom_1_height) + r'$\mathrm{\degree}$')
ax_zoom1.set_xlabel(r'Galactic latitude $\mathrm{[\degree]}$')
ax_zoom1.set_xlim(zoom_1_x[0],zoom_1_x[1])
ax_zoom1.set_ylabel(r'Galactic longitude $\mathrm{[\degree]}$')
ax_zoom1.set_ylim(zoom_1_y[0],zoom_1_y[1])
for ox in messierObjects:
    x = ox.ra.wrap_at('180d').deg
    y = ox.dec.deg
    mark = markersNew[ox.type].split('-')[0]
    kk = markersNew[ox.type].split('-')[1]
    ax_zoom1.scatter(x,y, marker = mark , s=sizeOfMarkers,linewidth=1, color= kk, zorder = 100)
    ax_zoom1.annotate(str(ox.name), (x+offset,y), fontsize = sizeOfFont)

ax_zoom2 = fig.add_subplot(spec[2, 1])
ax_zoom2.grid(True)
ax_zoom2.set_title('Zoomed region ' + str(zoom_2_width) + r'$\mathrm{\degree}$x' + str(zoom_2_height) + r'$\mathrm{\degree}$')
ax_zoom2.set_xlabel(r'Galactic latitude $\mathrm{[\degree]}$')
ax_zoom2.set_xlim(zoom_2_x[0],zoom_2_x[1])
ax_zoom2.set_ylim(zoom_2_y[0],zoom_2_y[1])
for ox in messierObjects:
    x = ox.ra.wrap_at('180d').deg
    y = ox.dec.deg
    mark = markersNew[ox.type].split('-')[0]
    kk = markersNew[ox.type].split('-')[1]
    ax_zoom2.scatter(x,y, marker = mark , s=sizeOfMarkers, linewidth=1, color= kk, zorder = 100)
    ax_zoom2.annotate(str(ox.name), (x+offset,y), fontsize = sizeOfFont)

ax_zoom3 = fig.add_subplot(spec[2, 2])
ax_zoom3.legend(handles=legend_list, loc="center", fontsize=sizeOfFont)
ax_zoom3.axis('off')

plt.savefig('test.png', dpi=400)

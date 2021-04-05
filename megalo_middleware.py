from matplotlib.lines import Line2D # creating custom legend
from matplotlib import colors as mcolors # displaying all  colors in matplotlib
import matplotlib.lines as mlines #

#########
list_prohibited_colors = ['bisque','k','cyan','aqua','aquamarine','antiquewhite','w','y','azure','beige','blanchedalmond','aliceblue','cornsilk','burlywood']
list_prohibited_markers = ['.',',','None',None,' ','','|','_']

######### defining class which will plot the Messier Catalogue
class megalo_middleware:
    def __init__(self, typeObjects):
        ### dictionaries
        self.sizeOfLegendMarkers = 10
        self.type2MarkerColorDictionary = {}
        self.legendList = {}
        try:
            self.type2MarkerColorDictionary, self.legendList = self.getSupportObjects(typeObjects)
        except Exception as e:
            print(str(e))

    def cleanMarkerDictionary(self):
        try:
            markerDictionary = Line2D.markers # dictionary of all markers
            cleanMarkerDictionary = {}
            for key in markerDictionary:
                if key not in list_prohibited_markers:
                    cleanMarkerDictionary[key] = markerDictionary[key]
            return cleanMarkerDictionary
        except Exception as e:
            print(str(e))

    def cleanColorsDictionary(self):
        try:
            colorsDictionary = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS) #dictionary of all colors
            cleanColorsDictionary = {}
            for key in colorsDictionary:
                if key not in list_prohibited_colors:
                    cleanColorsDictionary[key] = colorsDictionary[key]
            return cleanColorsDictionary
        except Exception as e:
            print(str(e))

    def getSupportObjects(self, type_messierObjects):
        try:
            cleanMarkerDictionary = self.cleanMarkerDictionary()
            cleanColorsDictionary = self.cleanColorsDictionary()
            type2MarkerColor = {}
            legend_list = []
            for type, marker, color in zip(type_messierObjects, cleanMarkerDictionary, cleanColorsDictionary):
                type2MarkerColor[type] =[str(marker),str(color)]
                legend_list.append(mlines.Line2D([], [], label=type, color=color, marker=marker, linestyle='None', markersize=self.sizeOfLegendMarkers, mew=1))
            return type2MarkerColor, legend_list
        except Exception as e:
                print(str(e))

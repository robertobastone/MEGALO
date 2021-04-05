######################### LIBRARIES #########################
import megalo_catalogueretriever as catalog
import megalo_middleware as middle
import megalo_galacticplotter as plotter

class megalo:
    def __init__(self):
        print("Initializing... MEssier GALactic Observatory (MEGALO)")

    def main(self):
        try:
            catalogue = catalog.megalo_catalogueretriever()
            support = middle.megalo_middleware(catalogue.typeObjects)
            plotter.megalo_galacticplotter().plotting(support.type2MarkerColorDictionary,support.legendList, catalogue.messierObjects)
        except Exception as e:
            print(str(e))

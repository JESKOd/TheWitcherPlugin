from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject, Qgis
from qgis.utils import iface
from qgis.PyQt import QtWidgets

LAYERS_MAP = {
    'Aederin': 'AEDERIN',
    'Brokilon': 'BROKILON',
    'Brugge': 'BRUGGE',
    'Caingorn': 'CAINGORN',
    'Cidaris': 'CIDARIS',
    'Don Blathann': 'DONBLATHANNA',
    'Upper Aederin': 'GORNYAEDERIN',
    'Kaedwen': 'KAEDWEN',
    'Kovir': 'KOVIR',
    'Lyria': 'LYRIA',
    'Mahakam': 'MAHAKAM',
    'Malleore': 'MALLEORE',
    'Nilfgard': 'NILFGARD',
    'Poisis': 'POISIS',
    'Redania': 'REDANIA',
    'Sodden': 'SODDEN',
    'Skellige': 'SKELLIGE',
    'Talgar': 'TALGAR',
    'Temeria': 'WYZIMA',
    'No mans area': 'TERENNICZYJI',
    'Velhad': 'VELHAD',
    'Verden': 'VERDEN',
    'Abandoned site': 'OPUSZCZONAWITRYNA',
    'Alchemy supplies': 'ZAOPATRZENIEALCHEMICZNE',
    'Armorer': 'PLATNERZ',
    'Armorer table': 'STOLPLATNERSKI',
    'Bandit Camp': 'OBOZBANDYTOW',
    'Blacksmith': 'KOWAL',
    'Brothel': 'BURDEL',
    'Entrance': 'WEJSCIE',
    'Fast travel': 'SZYBKAPODROZ',
    'Grindstone': 'KAMIENSZLIFIERSKI',
    'Guarder treasure': 'STRZEZONYSKARB',
    'Gwent players': 'GRACZEGWINTA',
    'Hairdresser': 'FRYZJER',
    'Harbor': 'PORT',
    'Herbalist': 'ZIELARZ',
    'Hidden treasure': 'UKRYTYSKARB',
    'Innkeeper': 'Karczmarz',
    'Industrial cache': 'SKRYTKAPRZEMYSLOWA',
    'Monster Den': 'POTWORDEN',
    'Monster Nest': 'GNIAZDOPOTWORA',
    'Notice Board': 'TABLICAOGLOSZEN',
    'Person in prison': 'OSOBAWUWIEZENIU',
    'Place of power': 'MIEJSCEMOCY',
    'Shopkeeper': 'SKLEPIKARZ',
    'Spoils of War': 'LUPYWOJENNE'

}


def load_layer(layername, request_type):

    geoserver_layer = LAYERS_MAP.get(layername)

    if geoserver_layer is None:
        iface.messageBar().pushMessage(
            "Error", f"Layer {layername} not found in LAYERS_MAP", level=Qgis.Critical)
        return

    if request_type == 'WFS':
        uri = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:2180' typename='TheWitcher:{geoserver_layer}' url='http://localhost:8080/geoserver/TheWitcher/wfs' version='auto'"
        layer = QgsVectorLayer(uri, layername, "WFS")
    elif request_type == 'WMS':
        uri = f"contextualWMSLegend=0&crs=EPSG:2180&dpiMode=7&featureCount=10&format=image/png&layers={geoserver_layer}&styles&url=http://localhost:8080/geoserver/TheWitcher/wms"
        layer = QgsRasterLayer(uri, layername, "wms")

    if layer.isValid():
        QgsProject.instance().addMapLayer(layer)
    else:
        iface.messageBar().pushMessage("Error", f"Layer {layername} is invaild or connection with geoserver is lost! Please report this issue.",
                                       level=Qgis.Critical)


def get_layers(dialog, request_type):
    for group_box in dialog.findChildren(QtWidgets.QGroupBox):
        for checkbox in group_box.findChildren(QtWidgets.QCheckBox):
            if checkbox.isChecked():
                load_layer(checkbox.text(), request_type)

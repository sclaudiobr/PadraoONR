def classFactory(iface):
    from .main_plugin import PadraoONR
    return PadraoONR(iface)
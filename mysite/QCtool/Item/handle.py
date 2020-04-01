from .VD import VD
from .PMNs import PMNs
from .UMNs import UMNs
from .Ald import Ald
from .UAld import UAld

def handle_uploaded_file(f, item_name, instrument_num, instrument_type):
    
    if item_name == "PMNs":
        pmns = PMNs(f=f, instrument_num=instrument_num, instrument_type=instrument_type)
        return pmns.output()
    elif item_name == "Ald":
        ald = Ald(f=f, instrument_num=instrument_num, instrument_type=instrument_type)
        return ald.output()
    elif item_name == "UAld":
        uald = UAld(f=f, instrument_num=instrument_num, instrument_type=instrument_type)
        return uald.output()
    elif item_name == "UMNs":
        umns = UMNs(f=f, instrument_num=instrument_num, instrument_type=instrument_type)
        return umns.output()
    elif  item_name == "VD":
        vd = VD(f=f, instrument_num=instrument_num, instrument_type=instrument_type)
        return vd.output()

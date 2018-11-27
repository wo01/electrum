from trezorlib import messages
from trezorlib.client import TrezorClient
from trezorlib.ui import ClickUI
from .clientbase import TrezorClientBase

class TrezorClientElectrum(TrezorClientBase, TrezorClient):
    def __init__(self, transport, handler, plugin):
        TrezorClient.__init__(self, transport=transport, ui=ClickUI)
        TrezorClientBase.__init__(self, handler, plugin, messages)

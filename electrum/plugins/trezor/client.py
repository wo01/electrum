from trezorlib.client import proto, BaseClient, ProtocolMixin
from trezorlib.ui import ClickUI
from .clientbase import TrezorClientBase

class TrezorClient(TrezorClientBase, ProtocolMixin, BaseClient):
    def __init__(self, transport, handler, plugin):
        BaseClient.__init__(self, transport=transport, ui=ClickUI)
        ProtocolMixin.__init__(self, transport=transport, ui=ClickUI)
        TrezorClientBase.__init__(self, handler, plugin, proto)


TrezorClientBase.wrap_methods(TrezorClient)

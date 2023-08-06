import logging
from typing import TYPE_CHECKING, Optional

from aiosubpub import Channel

if TYPE_CHECKING:
    from pyzbar.pyzbar import Decoded
    from qgrabber.model import ScannerModel
    from qgrabber.view import ScannerView

_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, model: "ScannerModel", view_width, view_height):
        self._model = model
        self.frame_data = Channel("Webcam view data")
        self._view_width = view_width
        self._view_height = view_height

    def start_scan(self):
        self._model.start(
            self._incoming_frame_data,
            on_code_scanned=self.stop_scan,
            crop_x=self._view_width,
            crop_y=self._view_height,
        )

    def _incoming_frame_data(self, frame_data):
        self.frame_data.publish(frame_data)

    def stop_scan(self, result: Optional["Decoded"] = None):
        if result:
            print(result)

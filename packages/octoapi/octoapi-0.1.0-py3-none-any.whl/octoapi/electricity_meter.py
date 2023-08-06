from .mixins import MeterMixin
from .authenticated_client import AuthenticatedClient


class ElectricityMeter(MeterMixin, AuthenticatedClient):
    """Class for retrieving electricity meter readings"""

    def __init__(self, api_key: str, mpan: str, serial_number: str) -> None:
        super().__init__(
            meter_id=mpan,
            serial_number=serial_number,
            meter_type="electricity-meter-points",
            api_key=api_key,
        )

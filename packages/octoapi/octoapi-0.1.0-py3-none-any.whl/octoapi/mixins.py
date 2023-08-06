from typing import Any, Optional
from datetime import datetime
from dateutil import parser
import pytz
from .types import JSONType
from .exceptions import ParameterException


class MeterMixin:
    """Mixin class for retrieving meter readings"""

    def __init__(
        self, meter_type: str, meter_id: str, serial_number: str, **kwargs: Any
    ) -> None:
        """Constructor - specify meter ID, serial number and type
        :Keyword Arguments:
            * **meter_type**: (*str*) -- type of meter (typically electricity or gas).
            * **meter_id**: (*str*) -- electricity meter's MPAN or gas meter's MPRN.
            * **serial_number**: (*str*) -- the meter's serial number.
        :Examples:
            * electricity meter: __init__(meter_id=mpan,
                                          serial_number=serial_number,
                                          meter_type="electricity-meter-points")
            * gas meter: __init__(meter_id=mran,
                                  serial_number=serial_number,
                                  meter_type="gas-meter-points")
        """
        self.meter_id = meter_id
        self.serial_number = serial_number
        self.meter_type = meter_type

        # Pass unused arguments onwards
        super().__init__(**kwargs)

    def consumption(
        self,
        period_from: Optional[datetime] = None,
        period_to: Optional[datetime] = None,
        page_size: Optional[int] = None,
        reverse: Optional[bool] = False,
        group_by: Optional[str] = None,
    ) -> JSONType:
        """List consumption for a meter

        Return a list of consumption values for half-hour periods for a given meter-point and meter.

        Unit of measurement:
            * Electricity meters: kWh
            * SMETS1 Secure gas meters: kWh
            * SMETS2 gas meters: m^3
        :Keyword Arguments:
            * **period_from**: (*[Optional] datetime*) -- show consumption from the given datetime (inclusive). This parameter can be provided on its own.
            * **period_to**: (*[Optional] datetime*) -- show consumption to the given datetime (exclusive). This parameter also requires providing the period_from parameter to create a range.
            * **page_size**: (*[Optional] int*) -- page size of returned results. Default is 100, maximum is 25,000 to give a full year of half-hourly consumption details.
            * **reverse**: (*[Optional] bool*) -- ordering of results returned. Default is that results are returned in reverse order from latest available figure, setting this to 'True' will reverse that.
            * **group_by**: (*[Optional] bool*) -- aggregates consumption over a specified time period. A day is considered to start and end at midnight in the server's timezone. The default is that consumption is returned in half-hour periods. Accepted values are: * 'hour' * 'day' * 'week' * 'month' * 'quarter'.
        :Examples:
            * consumption in a range: consumption(period_from=start_time, period_to=test_end_time, group_by="hour")
        :raises ApiException: Remote API does not return valid consumption data
        """
        # Validate parameters
        params = {}
        if period_from:
            params["period_from"] = period_from.isoformat()
        if period_to:
            params["period_to"] = period_to.isoformat()
        if page_size:
            params["page_size"] = page_size
        if reverse:
            params["order_by"] = "period"
        if group_by:
            allowed_groupings = ["hour", "day", "week", "month", "quarter"]
            if group_by not in allowed_groupings:
                raise ParameterException(
                    "'group_by' must be one of %s" % allowed_groupings
                )
            params["group_by"] = group_by
        # Retrieve JSON
        json_response = self.request_json(
            path=f"{self.meter_type}/{self.meter_id}/meters/{self.serial_number}/consumption/",
            params=params,
        )
        # Format output
        results = [
            {
                "consumption": float(entry["consumption"]),
                "interval_start": parser.parse(entry["interval_start"]).astimezone(
                    pytz.utc
                ),
                "interval_end": parser.parse(entry["interval_end"]).astimezone(
                    pytz.utc
                ),
            }
            for entry in json_response["results"]
        ]
        # Enforce exclusive period_to
        if period_to:
            return [r for r in results if r["interval_end"] < period_to]
        return results

    def verify(self) -> JSONType:
        """Verify electricity meter

        Retrieve the details of an electricity meter.
        This endpoint can be used to get the GSP of a given meter-point.

        :raises ApiException: Remote API does not return valid meter data
        """
        return self.request_json(path=f"{self.meter_type}/{self.meter_id}/")

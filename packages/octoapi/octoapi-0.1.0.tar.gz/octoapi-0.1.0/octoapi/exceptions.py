class OctopusException(Exception):
    """Base exception for this project"""


class ApiException(OctopusException):
    """Unable to retrieve data from the API"""


class ParameterException(OctopusException):
    """Problems with an input parameter"""

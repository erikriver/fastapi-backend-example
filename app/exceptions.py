class VehicleDeletedException(Exception):
    "Raised when the Vehicle is soft deleted"
    pass


class VehicleNotFoundException(Exception):
    "Raised when the Vehicle is not found in the vPIC API"
    pass


class VehicleNotCachedException(Exception):
    "Raised when the Vehicle is not cached"
    pass


class VPICAPIException(Exception):
    "Raised when the vPIC API has an error"
    pass

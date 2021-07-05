from ColumnReferences import ColumnReferences

class GPSInfo:
    """Commom GPS class for all turtle's data """

    def __init__(self, npEntry):
        self.reliable_id = npEntry[ColumnReferences.GPS_RELIABLE_ID]
        self.allGpsId = npEntry[ColumnReferences.GPS_All_GPS_ID]
        self.acquisitionTime = npEntry[ColumnReferences.GPS_ACQUISITION_TIME]
        self.acquisitionStartTime = npEntry[ColumnReferences.GPS_ACQUISITION_START_TIME]
        self.gpsFixTime = npEntry[ColumnReferences.GPS_GPS_FIX_TIME]
        self.gpsFixAttempt = npEntry[ColumnReferences.GPS_GPS_FIX_ATTEMPT]
        self.latitude = npEntry[ColumnReferences.GPS_LATITUDE]
        self.longitude = npEntry[ColumnReferences.GPS_LONGITUDE]
        self.distance = npEntry[ColumnReferences.GPS_DISTANCE]
        self.timeS = npEntry[ColumnReferences.GPS_TIME_S]
        self.speed = npEntry[ColumnReferences.GPS_SPEED]
        self.timeH = npEntry[ColumnReferences.GPS_TIME_H]
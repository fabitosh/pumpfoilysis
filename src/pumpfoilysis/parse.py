import polars as pl
import xml.etree.ElementTree as ET
from typing import IO

def parse_tcx(file_path: str) -> pl.DataFrame:
    """
    Parses a TCX file and returns a Polars DataFrame.

    Args:
        file_path: The path to the TCX file.

    Returns:
        A Polars DataFrame containing the trackpoint data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    ns = {
        'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
        'ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
    }

    data = []
    for trackpoint in root.findall('.//tcx:Trackpoint', ns):
        time = trackpoint.find('tcx:Time', ns)
        latitude = trackpoint.find('.//tcx:LatitudeDegrees', ns)
        longitude = trackpoint.find('.//tcx:LongitudeDegrees', ns)
        altitude = trackpoint.find('tcx:AltitudeMeters', ns)
        distance = trackpoint.find('tcx:DistanceMeters', ns)
        heart_rate = trackpoint.find('.//tcx:HeartRateBpm/tcx:Value', ns)
        speed = trackpoint.find('.//ns3:Speed', ns)

        row = {
            'time': time.text if time is not None else None,
            'latitude': float(latitude.text) if latitude is not None else None,
            'longitude': float(longitude.text) if longitude is not None else None,
            'altitude': float(altitude.text) if altitude is not None else None,
            'distance': float(distance.text) if distance is not None else None,
            'heart_rate': int(heart_rate.text) if heart_rate is not None else None,
            'speed': float(speed.text) if speed is not None else None,
        }
        data.append(row)

    df = pl.DataFrame(data)
    df = df.with_columns(pl.col('time').str.to_datetime())
    return df
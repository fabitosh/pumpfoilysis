import polars as pl
from xml.etree import ElementTree


def parse_tcx(file_path: str) -> pl.DataFrame:
    """Parses a TCX file and returns a Polars DataFrame. Slightly supervised llm code."""
    tree = ElementTree.parse(file_path)
    root = tree.getroot()

    # Hardcoded namespaces for Garmin Activities for now. Will need to look into the structure of other watches.
    ns = {
        "tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
    }

    data = []
    for trackpoint in root.findall(".//tcx:Trackpoint", ns):
        time = trackpoint.find("tcx:Time", ns)
        latitude = trackpoint.find(".//tcx:LatitudeDegrees", ns)
        longitude = trackpoint.find(".//tcx:LongitudeDegrees", ns)
        altitude = trackpoint.find("tcx:AltitudeMeters", ns)
        distance = trackpoint.find("tcx:DistanceMeters", ns)
        heart_rate = trackpoint.find(".//tcx:HeartRateBpm/tcx:Value", ns)
        speed = trackpoint.find(".//ns3:Speed", ns)

        row = {
            "datetime": time.text if time is not None else None,
            "lat_raw": float(latitude.text) if latitude is not None else None,
            "lon_raw": float(longitude.text) if longitude is not None else None,
            "altitude_raw": float(altitude.text) if altitude is not None else None,
            "distance_raw": float(distance.text) if distance is not None else None,
            "heart_rate_raw": int(heart_rate.text) if heart_rate is not None else None,
            "speed_raw": float(speed.text) if speed is not None else None,
        }
        data.append(row)

    df = pl.DataFrame(data)
    df = df.with_columns(pl.col("datetime").str.to_datetime(time_zone="UTC"))
    return df

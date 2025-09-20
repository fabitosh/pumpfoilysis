from datetime import datetime, timezone, timedelta
from tests.helpers import _ensure_tz_aware

def test__ensure_tz_aware():
    dt = datetime(2025, 9, 20)
    assert dt.tzinfo is None
    dt = _ensure_tz_aware(dt)
    assert dt.tzinfo is timezone.utc

def test__ensure_tz_aware_keeps_timezone():
    set_tz = timezone(offset=timedelta(hours=5))
    dt = datetime(2025, 9, 20, tzinfo=set_tz)
    assert dt.tzinfo == set_tz
    dt = _ensure_tz_aware(dt)
    assert dt.tzinfo == set_tz

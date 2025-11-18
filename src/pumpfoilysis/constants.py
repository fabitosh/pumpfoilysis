# Foil Params
# for short durations, extremely slow speeds might be feasible but cannot be sustained.
SPEED_PUMP_MAX_KMH = 22.0  # Takoon Pump 1700
SPEED_PUMP_MIN_KMH = 5.0  # Stall Speed
SPEED_SWIM_MAX_KMH = 3.0
SPEED_WALK_MAX_KMH = 7.0

# Off Foil Params
MAX_OFF_FOIL_SPEED_KMH = max(SPEED_SWIM_MAX_KMH, SPEED_WALK_MAX_KMH)
SPEED_OUTLIER_KMH = 2 * SPEED_PUMP_MAX_KMH

CLEAN_MODE_AUTO = 'auto'
CLEAN_MODE_SPOT_AREA = 'spotArea'
CLEAN_MODE_CUSTOM_AREA = 'customArea'

CLEAN_ACTION_START = 'start'
CLEAN_ACTION_PAUSE = 'pause'
CLEAN_ACTION_RESUME = 'resume'

FAN_SPEED_QUIET = 'quiet'
FAN_SPEED_NORMAL = 'normal'
FAN_SPEED_MAX = 'max'
FAN_SPEED_MAXPLUS = 'max+'

WATER_LOW = "low"
WATER_MEDIUM = "medium"
wATER_HIGH = "high"
WATER_ULTRAHIGH = "ultrahigh"

CHARGE_MODE_RETURN = 'return'
CHARGE_MODE_RETURNING = 'returning'
CHARGE_MODE_CHARGING = 'charging'
CHARGE_MODE_IDLE = 'idle'

COMPONENT_SIDE_BRUSH = 'sideBrush'
COMPONENT_MAIN_BRUSH = 'brush'
COMPONENT_FILTER = 'heap'

CLEANING_STATES = {CLEAN_MODE_AUTO,CLEAN_MODE_CUSTOM_AREA, CLEAN_MODE_SPOT_AREA}
CHARGING_STATES = {CHARGE_MODE_CHARGING}

CLEAN_MODE_TO_ECOVACS = {
    CLEAN_MODE_AUTO: 'auto',
    CLEAN_MODE_SPOT_AREA: 'SpotArea',
	CLEAN_MODE_CUSTOM_AREA: 'customArea'
}

CLEAN_ACTION_TO_ECOVACS = {
    CLEAN_ACTION_START: 'start',
    CLEAN_ACTION_PAUSE: 'pause',
    CLEAN_ACTION_RESUME: 'resume'
}

CLEAN_ACTION_FROM_ECOVACS = {
    'start': CLEAN_ACTION_START,
    'pause': CLEAN_ACTION_PAUSE,
    'resume': CLEAN_ACTION_RESUME
}

CLEAN_MODE_FROM_ECOVACS = {
    'auto': CLEAN_MODE_AUTO,
    'spotArea': CLEAN_MODE_SPOT_AREA,
    'customArea': CLEAN_MODE_CUSTOM_AREA
}

FAN_SPEED_TO_ECOVACS = {
    FAN_SPEED_QUIET: 1000,
    FAN_SPEED_NORMAL: 0,
    FAN_SPEED_MAX: 1,
    FAN_SPEED_MAXPLUS: 2
}

FAN_SPEED_FROM_ECOVACS = {
    1000: FAN_SPEED_QUIET,
    0: FAN_SPEED_NORMAL,
    1: FAN_SPEED_MAX,
    2: FAN_SPEED_MAXPLUS
}

WATER_LEVEL_TO_ECOVACS = {
    WATER_LOW: 1,
    WATER_MEDIUM: 2,
    wATER_HIGH: 3,
    WATER_ULTRAHIGH: 4
}

WATER_LEVEL_FROM_ECOVACS = {
    1: WATER_LOW,
    2: WATER_MEDIUM,
    3: wATER_HIGH,
    4: WATER_ULTRAHIGH
}

CHARGE_MODE_TO_ECOVACS = {
    CHARGE_MODE_RETURN: 'go',
    CHARGE_MODE_RETURNING: 'going',
    CHARGE_MODE_CHARGING: 'charging',
    CHARGE_MODE_IDLE: 'idle'
}

CHARGE_MODE_FROM_ECOVACS = {
    'going': CHARGE_MODE_RETURNING,
    'charging': CHARGE_MODE_CHARGING,
    'idle': CHARGE_MODE_IDLE
}

COMPONENT_TO_ECOVACS = {
    COMPONENT_MAIN_BRUSH: 'brush',
    COMPONENT_SIDE_BRUSH: 'sideBrush',
    COMPONENT_FILTER: 'heap'
}

COMPONENT_FROM_ECOVACS = {
    'brush': COMPONENT_MAIN_BRUSH,
    'sideBrush': COMPONENT_SIDE_BRUSH,
    'heap': COMPONENT_FILTER
}

ROOMS_FROM_ECOVACS = {
    0 : 'Default',
    1 : 'Living Room',
    2 : 'Dining Room',
    3 : 'Bedroom',
    4 : 'Study',
    5 : 'Kitchen',
    6 : 'Bathroom',
    7 : 'Laundry',
    8 : 'Lounge',
    9 : 'Storeroom',
    10 : 'Kids room',
    11 : 'Sunroom'
}
# ChemVista Configuration

# Flask Application Settings
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Application Settings
APP_NAME = 'ChemVista'
APP_VERSION = '1.0.0'
APP_DESCRIPTION = 'Interactive Chemistry Explorer'

# Data File Paths
ELEMENTS_DATA_FILE = 'data/elements.json'
COMPOUNDS_DATA_FILE = 'data/compounds.json'

# Search Settings
MAX_SEARCH_RESULTS = 20
MIN_SEARCH_LENGTH = 2
SEARCH_DEBOUNCE_MS = 300

# UI Settings
ELEMENTS_PER_ROW_MOBILE = 6
ELEMENTS_PER_ROW_DESKTOP = 18
ANIMATION_DURATION = 300

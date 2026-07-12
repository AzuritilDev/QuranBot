renamedTimeFormats = {
    "TWELVE_HOUR_TIME": "Twelve Hour Time (e.g. 3:00 PM, 6:30 AM )",
    "TWENTY_FOUR_HOUR_MILITARY_TIME": "Twenty Four Hour Military Time (e.g. 15:00, 18:30)"
}

renamedCalculationMethods = {
    "DUBAI": "Dubai",
    "EGYPTIAN": "Egyptian",
    "KARACHI": "Karachi",
    "KUWAIT": "Kuwait",
    "MOON_SIGHTING_COMMITTEE": "Moon Sighting Committee",
    "MUSLIM_WORLD_LEAGUE": "Muslim World League",
    "NONE": "None",
    "NOTH_AMERICA": "North America",
    "QATAR": "Qatar",
    "SINGAPORE": "Singapore",
    "UMM_AL_QURA": "Umm al-Qura",
    "UOIF": "UIOF (Union des Organisations Islamiques de France)"
}

renamedMadhabs = {
    "HANAFI": "Hanafi",
    "SHAFI": "Shāfiʿī"
}

def beautifyCalculationMethodClassName(name : str):
    '''
    EXAMPLE:
    beautifyCalculationMethodClassName("MOON_SIGHTING_COMMITTEE") # returns "Moon Sighting Committee"
    beautifyCalculationMethodClassName("HANAFI") # returns "Hanafi"
    '''
    return name.replace('_', ' ').title()
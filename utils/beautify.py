from geography import availableTimeFormats

def beautifyCalculationMethodClassName(name : str):
    '''
    EXAMPLE:
    beautifyCalculationMethodClassName("MOON_SIGHTING_COMMITTEE") # returns "Moon Sighting Committee"
    beautifyCalculationMethodClassName("HANAFI") # returns "Hanafi"
    '''
    return name.replace('_', ' ').title()
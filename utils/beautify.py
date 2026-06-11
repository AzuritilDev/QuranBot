'''
EXAMPLE:
beautifyCalculationMethodClassName("MOON_SIGHTING_COMMITTEE") # returns "Moon Sighting Committee"
beautifyCalculationMethodClassName("HANAFI") # returns "Hanafi"
'''
def beautifyCalculationMethodClassName(name : str):
    return name.replace('_', ' ').title()
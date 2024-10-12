def get_meetup_events():
    return export_techlife_calendar()

def parse_and_map_events(icalFile:bytes):
    return map_model_parsed_file_to_class(parse_ical_file_with_icalendar(icalFile))


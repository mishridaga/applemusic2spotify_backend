def create_track_list(raw_text):
    rows_raw = raw_text.split("\r")
    columns_raw = [x.split("\t") for x in rows_raw]
    fields = columns_raw[0]
    rows = columns_raw[1:]
    tracks = []
    for row in rows:
        dictionary = {}
        for i in range(len(row)):
            if row[i]:
                dictionary[fields[i]] = row[i]
        if dictionary != {}:
            tracks += [dictionary]
    return tracks

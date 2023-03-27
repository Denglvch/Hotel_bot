def filter_by_distance(data: list, distance: int) -> list:
    return [
        hotel
        for hotel
        in data
        if hotel['destinationInfo']['distanceFromDestination']['value'] <= distance
    ]

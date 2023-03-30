def filter_by_distance(data: list, distance: int) -> list:
    """
    Gets a list of hotels from the API, filters by distance and returns it
    :param data:
    :param distance:
    :return: list filtered by distance
    """
    return [
        hotel
        for hotel
        in data
        if hotel['destinationInfo']['distanceFromDestination']['value'] <= distance
    ]

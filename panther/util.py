def hex_to_rgb(hex: str):
    """
    converts a hex string to an rgb tuple
    :param hex: string, valid hex
    :return: tuple<red(int), green(int), blue(int)>
    """
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))  # from: https://stackoverflow.com/a/29643643/7045733

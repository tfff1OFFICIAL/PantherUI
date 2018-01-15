def hex_to_rgb(hex: str):
    """
    converts a hex string to an rgb tuple
    :param hex: string, valid hex
    :return: tuple<red(int), green(int), blue(int)>
    """
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))  # from: https://stackoverflow.com/a/29643643/7045733


class GraphicsManager:
    """
    instead of the extra file, each layer will have it's own one of these which it can use to draw graphics. This is to be passed to the draw function
    """

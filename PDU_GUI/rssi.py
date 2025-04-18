class RSSI:
    def __init__(self, RSSI_NAUGHT: float, n: float):
        """
        Initialize the RSSI class with the signal strength at 1 meter (RSSI_NAUGHT)
        and the path loss exponent (n).
        """
        self.RSSI_NAUGHT = RSSI_NAUGHT
        self.n = n

    def get_distance(self, signal_strength: float) -> float:
        """
        Get the distance at a given signal strength.

        Args:
            signal_strength (float): The signal strength in dBm.

        Returns:
            float: The distance in feet.
        """
        return self.meters_to_feet(10 ** ((self.RSSI_NAUGHT - signal_strength) / (10 * self.n)))
    
    def set_rssi_naught(self, RSSI_NAUGHT: float):
        """
        Set the signal strength at 1 meter.

        Args:
            RSSI_NAUGHT (float): The signal strength at 1 meter in dBm.
        """
        self.RSSI_NAUGHT = RSSI_NAUGHT

    def meters_to_feet(self, meters: float) -> float:
        """
        Convert meters to feet.
        """
        return meters * 3.28084

import rssi
import subprocess

class WifiTowerScanner:
    def __init__(self, RSSI_naught: float, n: float):
        # Mapping of MAC addresses to Tower names
        self.tower_map = {
            "94:2a:6f:22:d1:7c": "Tower 1",
            "9a:2a:6f:22:d6:77": "Tower 2",
            "9a:2a:6f:24:9f:09": "Tower 3",
            "9a:2a:6f:22:a2:7e": "Tower 4"
        }

        self.calculator = RSSI_Calculator(RSSI_naught, n)

    def get_tower_signal(self):
        # Run the command to get the scan results
        command = "sudo -s wpa_cli scan && sudo -s wpa_cli scan_results | grep 'LIT Wi-Fi'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if the result is successful
        if result.returncode == 0:
            # Split the output into lines
            lines = result.stdout.splitlines()

            # Initialize a list to store the towers and their signal levels
            tower_signal = []

            # Parse each line
            for line in lines[2:]:
                # Split the line by whitespace to extract each component
                parts = line.split()

                # Extract the MAC address and signal level
                mac_address = parts[0]
                print(mac_address)
                signal_level = parts[2]

                # If the MAC address matches one in our tower map, add it to the result
                if mac_address.lower() in self.tower_map:
                    tower_name = self.tower_map[mac_address.lower()]
                    # tower_signal.append([tower_name, float(signal_level)])
                    self.calculator.add_reading_and_distance(tower_name, float(signal_level))
                    # print(f"{tower_name}: {self.calculator.get_distances(tower_name)}")

            # Return the tower names and their signal levels
            return tower_signal
        else:
            print("Error executing command")
            return []


class RSSI_Calculator:
    def __init__(self, RSSI_NAUGHT: float, n: float):
        """
        Initialize the RSSI_Values class with a RSSI instance and a
        dictionary of tower RSSI distances to device
        """
        self.RSSI = rssi.RSSI(RSSI_NAUGHT, n)
        self.towers = ["Tower 1", "Tower 2", "Tower 3", "Tower 4"]

        # RSSI readings from each tower
        self.readings = {
            "Tower 1": [],
            "Tower 2": [],
            "Tower 3": [],
            "Tower 4": [],
        }

        # Limit number of most recent readings
        self.max_readings = 1

        # Distances from each tower to the device
        self.distances = {
            "Tower 1": [],
            "Tower 2": [],
            "Tower 3": [],
            "Tower 4": [],
        }


    """
    *******************************************
    Functions for adding readings and distances
    *******************************************
    """

    def add_reading_and_distance(self, tower: str, reading: float):
        """
        Add a reading to the corresponding tower and calculate the distance.

        Args:
            tower (str): The tower to add the reading to.
            reading (float): The reading to add.
        """

        self.readings[tower].append(reading)
        self.add_distance(tower)

        # Remove oldest reading and distance if there are more than the max
        if len(self.readings[tower]) > self.max_readings:
            self.readings[tower].pop(0)
            self.distances[tower].pop(0)

    def add_distance(self, tower: str):
        """
        Helper function to add a distance to the corresponding tower.

        Args:
            tower (str): The tower to add the distance to.
        """

        most_recent_reading = self.readings[tower][-1]
        self.distances[tower].append(self.RSSI.get_distance(most_recent_reading))
    

    """
    *******************************************************************
    Functions for getting all readings and distances for a single tower
    *******************************************************************
    """

    def get_readings(self, tower: str) -> list[float]:
        """
        Get the readings from the corresponding tower.

        Args:
            tower (str): The tower to get the reading from.

        Returns:
            float: The reading from the corresponding tower.
        """

        return self.readings[tower]

    def get_distances(self, tower: str) -> list[float]:
        """
        Get the distance from the corresponding tower.

        Args:
            tower (str): The tower to get the distance from.

        Returns:
            float: The distance from the corresponding tower.
        """

        return self.distances[tower]
    
    
    """
    *************************************************************************
    Functions for getting the average reading and distance for a single tower
    *************************************************************************
    """

    def get_average_reading(self, tower: str) -> float:
        """
        Get the average reading from the corresponding tower.

        Args:
            tower (str): The tower to get the average reading from.

        Returns:
            float: The average reading from the corresponding tower.
        """

        return sum(self.readings[tower]) / len(self.readings[tower])
    
    def get_average_distance(self, tower: str) -> float:
        """
        Get the average distance from the corresponding tower.

        Args:
            tower (str): The tower to get the average distance from.

        Returns:
            float: The average distance from the corresponding tower.
        """

        return sum(self.distances[tower]) / len(self.distances[tower])
    
    
    """
    *******************************
    Functions for testing the class
    *******************************
    """
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the RSSI_Calculator object to
        show all readings, distances, and average readings and distances
        for all towers.
        """
        header_string = f"RSSI_Calculator(RSSI_NAUGHT={self.RSSI.RSSI_NAUGHT}, n={self.RSSI.n})"

        for tower in self.towers:
            tower_string = f"{tower}:\n" \
                f"Readings: {self.readings[tower]}\n" \
                f"Distances: {self.distances[tower]}\n" \
                f"Average Reading: {self.get_average_reading(tower)}\n" \
                f"Average Distance: {self.get_average_distance(tower)}\n"
            
            header_string += "\n" + tower_string

        return header_string
    

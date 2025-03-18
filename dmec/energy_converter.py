# dmec/energy_converter.py

import logging
from .config import Config

class EnergyConverter:
    def __init__(self):
        self.total_energy = 0
        self.conversion_strategy = Config.DEFAULTS.get("ENERGY_CONVERSION_STRATEGY", "basic")
        logging.info(f"Energy Converter initialized with strategy: {self.conversion_strategy}")

    def convert(self, interactions):
        """
        Convert detected interactions into energy based on the current strategy.
        :param interactions: Number of interactions detected.
        :return: Total energy output after conversion.
        """
        if self.conversion_strategy == "basic":
            return self.basic_conversion(interactions)
        elif self.conversion_strategy == "advanced":
            return self.advanced_conversion(interactions)
        else:
            logging.error(f"Unknown conversion strategy: {self.conversion_strategy}")
            raise ValueError(f"Unknown conversion strategy: {self.conversion_strategy}")

    def basic_conversion(self, interactions):
        """
        Basic energy conversion: each interaction generates a fixed amount of energy.
        :param interactions: Number of interactions detected.
        :return: Total energy output after conversion.
        """
        energy_generated = interactions * Config.DEFAULTS["ENERGY_PER_INTERACTION"]
        self.total_energy += energy_generated
        logging.info(f"Basic conversion: {energy_generated} units generated from {interactions} interactions.")
        return self.total_energy

    def advanced_conversion(self, interactions):
        """
        Advanced energy conversion: applies a multiplier based on the number of interactions.
        :param interactions: Number of interactions detected.
        :return: Total energy output after conversion.
        """
        multiplier = 1 + (interactions * 0.1)  # Example: 10% increase per interaction
        energy_generated = interactions * Config.DEFAULTS["ENERGY_PER_INTERACTION"] * multiplier
        self.total_energy += energy_generated
        logging.info(f"Advanced conversion: {energy_generated} units generated from {interactions} interactions with multiplier {multiplier}.")
        return self.total_energy

    def get_total_energy(self):
        """
        Return the total energy output generated.
        :return: Total energy output.
        """
        return self.total_energy

    def reset(self):
        """
        Reset the total energy output to zero.
        """
        self.total_energy = 0
        logging.info("Energy output has been reset.")

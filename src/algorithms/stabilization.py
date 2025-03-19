import numpy as np

class AdvancedStabilizationAlgorithm:
    def __init__(self, target_value: float, adjustment_factor: float, smoothing_factor: float):
        self.target_value = target_value
        self.adjustment_factor = adjustment_factor
        self.smoothing_factor = smoothing_factor
        self.current_value = target_value

    def adjust_value(self, market_value: float) -> float:
        """
        Adjust the current value towards the target value based on market conditions,
        incorporating a smoothing factor to reduce volatility.
        """
        difference = self.target_value - market_value
        adjustment = self.adjustment_factor * difference
        self.current_value += adjustment
        self.current_value = self.smoothing_factor * self.current_value + (1 - self.smoothing_factor) * market_value
        return self.current_value

    def get_current_value(self) -> float:
        return self.current_value

    def reset(self):
        """
        Reset the current value to the target value.
        """
        self.current_value = self.target_value

# Example usage
if __name__ == "__main__":
    stabilizer = AdvancedStabilizationAlgorithm(target_value=314.159, adjustment_factor=0.1, smoothing_factor=0.5)
    market_values = [310, 315, 320, 312, 308, 330]
    for market_value in market_values:
        adjusted_value = stabilizer.adjust_value(market_value)
        print(f"Market Value: {market_value}, Adjusted Value: {adjusted_value}")

import numpy as np
import pandas as pd

class RiskManagementSystem:
    def __init__(self):
        self.risks = pd.DataFrame(columns=['Risk ID', 'Description', 'Likelihood', 'Impact', 'Score', 'Mitigation Strategy'])

    def add_risk(self, risk_id: int, description: str, likelihood: float, impact: float, mitigation_strategy: str):
        """
        Add a new risk to the system with its details.
        """
        score = self.calculate_risk_score(likelihood, impact)
        self.risks = self.risks.append({
            'Risk ID': risk_id,
            'Description': description,
            'Likelihood': likelihood,
            'Impact': impact,
            'Score': score,
            'Mitigation Strategy': mitigation_strategy
        }, ignore_index=True)

    def calculate_risk_score(self, likelihood: float, impact: float) -> float:
        """
        Calculate the risk score based on likelihood and impact.
        """
        return likelihood * impact

    def monitor_risks(self):
        """
        Monitor and report the current risks in the system.
        """
        print("Current Risks:")
        print(self.risks)

    def mitigate_risk(self, risk_id: int):
        """
        Implement the mitigation strategy for a specific risk.
        """
        risk = self.risks[self.risks['Risk ID'] == risk_id]
        if not risk.empty:
            print(f"Mitigating Risk ID {risk_id}: {risk['Mitigation Strategy'].values[0]}")
        else:
            print(f"Risk ID {risk_id} not found.")

# Example usage
if __name__ == "__main__":
    risk_manager = RiskManagementSystem()
    risk_manager.add_risk(risk_id=1, description="Market volatility", likelihood=0.7, impact=0.9, mitigation_strategy="Diversify portfolio")
    risk_manager.add_risk(risk_id=2, description="Regulatory changes", likelihood=0.5, impact=0.8, mitigation_strategy="Stay updated with regulations")
    risk_manager.monitor_risks()
    risk_manager.mitigate_risk(risk_id=1)

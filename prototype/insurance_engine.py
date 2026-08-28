import os
from typing import List, Dict, Union

class Rider:
    def __init__(self, rider_type: str, base_premium_factor: float = 0.01):
        self.rider_type = rider_type
        self.base_premium_factor = base_premium_factor

class Policy:
    def __init__(self, policy_type: str, sum_assured: float, base_rate_per_thousand: float = 20.0):
        self.policy_type = policy_type
        self.sum_assured = float(sum_assured)
        self.base_rate_per_thousand = base_rate_per_thousand
        self.riders: List[Union[str, Rider]] = []

    def add_rider(self, rider: Union[str, Rider]):
        self.riders.append(rider)

    def calculate_premium(self, age: int = 30, is_tobacco: bool = False) -> float:
        # Base mortality and risk calculation
        age_factor = 1.0 + max(0, (age - 25) * 0.02)
        tobacco_factor = 1.25 if is_tobacco else 1.0
        base_annual = (self.sum_assured / 1000.0) * self.base_rate_per_thousand * age_factor * tobacco_factor
        return round(base_annual, 2)

class EndowmentPolicy(Policy):
    def __init__(self, sum_assured: float):
        # Endowment has savings + protection, higher base rate
        super().__init__('Endowment', sum_assured, base_rate_per_thousand=45.0)

class TermLifePolicy(Policy):
    def __init__(self, sum_assured: float):
        # Pure protection, affordable rate
        super().__init__('Term Life', sum_assured, base_rate_per_thousand=15.0)

class CriticalIllnessPolicy(Policy):
    def __init__(self, sum_assured: float):
        super().__init__('Critical Illness', sum_assured, base_rate_per_thousand=25.0)

class AccidentalDisabilityPolicy(Policy):
    def __init__(self, sum_assured: float):
        super().__init__('Accidental Disability', sum_assured, base_rate_per_thousand=18.0)

class WaiverOfPremiumPolicy(Policy):
    def __init__(self, sum_assured: float):
        super().__init__('Waiver of Premium', sum_assured, base_rate_per_thousand=12.0)

# Default rider rates as percentage of base sum assured
RIDER_RATE_MAP = {
    "Critical Illness": 0.012,
    "Accidental Disability": 0.008,
    "Waiver of Premium": 0.005,
    "Hospital Cash": 0.006
}

def calculate_total_premium(policy: Policy, riders: List[Union[str, Rider]], age: int = 30, is_tobacco: bool = False, frequency: str = "Annually") -> float:
    """Calculates total premium including base policy, riders, multi-rider discounts, and payment frequency."""
    base_prem = policy.calculate_premium(age=age, is_tobacco=is_tobacco)
    
    rider_total = 0.0
    valid_rider_count = len(riders)
    
    for r in riders:
        if isinstance(r, Rider):
            rider_total += policy.sum_assured * r.base_premium_factor
        elif isinstance(r, str) and r in RIDER_RATE_MAP:
            rider_total += policy.sum_assured * RIDER_RATE_MAP[r]
        else:
            rider_total += policy.sum_assured * 0.010

    # Multi-Rider Discount rules: 5% discount for 2 riders, 10% discount for 3+ riders
    discount = 0.0
    if valid_rider_count == 2:
        discount = 0.05
    elif valid_rider_count >= 3:
        discount = 0.10
        
    rider_total_discounted = rider_total * (1.0 - discount)
    annual_total = base_prem + rider_total_discounted
    
    # Frequency adjustment
    if frequency.lower() == "monthly":
        total_quote = (annual_total / 12.0) * 1.03 # 3% monthly processing charge
    elif frequency.lower() == "quarterly":
        total_quote = (annual_total / 4.0) * 1.015 # 1.5% quarterly charge
    else:
        total_quote = annual_total

    return round(total_quote, 2)

def validate_rider_compatibility(policy: Policy, riders: List[Union[str, Rider]]) -> Dict[str, Union[bool, str]]:
    """Enforces rider compatibility matrix and sum assured limits."""
    rider_names = [r.rider_type if isinstance(r, Rider) else str(r) for r in riders]
    
    # Rule 1: Cannot select duplicate riders
    if len(rider_names) != len(set(rider_names)):
        return {"compatible": False, "reason": "Duplicate riders selected in the package."}
        
    # Rule 2: Waiver of Premium requires at least one primary life or health rider
    if "Waiver of Premium" in rider_names and len(rider_names) == 1:
        return {"compatible": False, "reason": "Waiver of Premium rider must be bundled alongside a life or disability rider."}
        
    # Rule 3: Policy sum assured must be at least 10,000 for critical illness rider
    if "Critical Illness" in rider_names and policy.sum_assured < 10000:
        return {"compatible": False, "reason": "Critical Illness rider requires a minimum base sum assured of ₹10,000."}

    return {"compatible": True, "reason": "All selected riders are compliant with underwriting rules."}

def recommend_policy_configuration(budget: float, payment_frequency: str = "Monthly") -> Dict[str, Policy]:
    """Generates optimal budget-capped package recommendations."""
    monthly_budget = budget if payment_frequency.lower() == "monthly" else budget / 12.0
    
    # Compute max sum assured that fits comfortably in budget
    term_sa = round(monthly_budget * 12.0 / 0.015, -3) # ~₹15 per 1000
    endow_sa = round(monthly_budget * 12.0 / 0.045, -3) # ~₹45 per 1000
    
    recommended_policies = {
        'Endowment': EndowmentPolicy(max(25000, endow_sa)),
        'Term Life': TermLifePolicy(max(50000, term_sa)),
    }
    return recommended_policies

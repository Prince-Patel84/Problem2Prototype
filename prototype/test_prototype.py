import os
import sys
import pytest

# Ensure prototype directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import insurance_engine
from insurance_engine import (
    Policy,
    Rider,
    EndowmentPolicy,
    TermLifePolicy,
    CriticalIllnessPolicy,
    AccidentalDisabilityPolicy,
    WaiverOfPremiumPolicy,
    calculate_total_premium,
    validate_rider_compatibility,
    recommend_policy_configuration,
)

@pytest.mark.parametrize("policy_cls,base_rate", [
    (TermLifePolicy, 15.0),
    (EndowmentPolicy, 45.0),
])
def test_policy_inheritance_and_pricing(policy_cls, base_rate):
    policy = policy_cls(sum_assured=100000)
    assert isinstance(policy, Policy), f"{policy_cls.__name__} must be an instance of Policy"
    assert issubclass(policy_cls, Policy), f"{policy_cls.__name__} must subclass Policy"
    premium = policy.calculate_premium(age=25, is_tobacco=False)
    assert premium == (100000 / 1000.0) * base_rate

def test_validate_rider_compatibility_valid():
    term_life = TermLifePolicy(sum_assured=50000)
    riders = [Rider("Critical Illness", 0.012), Rider("Accidental Disability", 0.008)]
    result = validate_rider_compatibility(term_life, riders)
    assert result["compatible"] is True
    assert "compliant" in result["reason"].lower()

def test_validate_rider_compatibility_duplicate_failure():
    term_life = TermLifePolicy(sum_assured=50000)
    riders = ["Critical Illness", "Critical Illness"]
    result = validate_rider_compatibility(term_life, riders)
    assert result["compatible"] is False
    assert "duplicate" in result["reason"].lower()

def test_calculate_total_premium_with_multi_rider_discount():
    term_life = TermLifePolicy(sum_assured=100000)
    base_prem = term_life.calculate_premium(age=25, is_tobacco=False) # 1500.0
    
    # 2 riders: 5% discount on riders
    r1 = Rider("Critical Illness", 0.01) # 1000
    r2 = Rider("Accidental Disability", 0.01) # 1000
    # Rider raw total = 2000; with 5% off = 1900
    total = calculate_total_premium(term_life, [r1, r2], age=25, is_tobacco=False, frequency="Annually")
    assert total == base_prem + 1900.0

def test_recommend_policy_configuration_budget_bounds():
    budget = 5000 # monthly
    recommendations = recommend_policy_configuration(budget=budget, payment_frequency="Monthly")
    assert "Endowment" in recommendations
    assert "Term Life" in recommendations
    assert recommendations["Endowment"].sum_assured > 0
    assert recommendations["Term Life"].sum_assured > 0

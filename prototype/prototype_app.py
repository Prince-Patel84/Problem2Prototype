import os
import sys
import streamlit as st

# Ensure prototype directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insurance_engine

def main():
    st.set_page_config(page_title="LIC Policy & Package Builder", page_icon="🛡️", layout="wide")
    
    st.title("🛡️ LIC Dynamic Insurance Package Builder & Quick Quote")
    st.markdown("Digitized Process Platform for Consolidated Insurance Packages & Real-Time Underwriting Review")
    st.divider()

    # Sidebar: Customer Profile & Preferences
    st.sidebar.header("📋 Customer Profile & Budget")
    age = st.sidebar.slider("Customer Age", min_value=18, max_value=75, value=30)
    tobacco_user = st.sidebar.radio("Tobacco Usage", ["Non-Tobacco User", "Tobacco User"], index=0)
    is_tobacco = (tobacco_user == "Tobacco User")
    
    payment_frequency = st.sidebar.selectbox("Payment Frequency", ["Monthly", "Quarterly", "Annually"], index=0)
    
    budget_label = "Monthly Budget Cap (₹)" if payment_frequency == "Monthly" else "Annual Budget Cap (₹)"
    default_budget = 5000 if payment_frequency == "Monthly" else 60000
    budget = st.sidebar.number_input(budget_label, min_value=500, max_value=500000, value=default_budget, step=500)

    # Main Area: Two Columns
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("1️⃣ Package Configuration")
        
        policy_type = st.radio("Select Base Policy", ["Term Life Insurance (Pure Protection)", "Endowment Plan (Protection + Savings)"], index=0)
        sum_assured = st.select_slider(
            "Base Sum Assured (₹)",
            options=[100000, 250000, 500000, 1000000, 2500000, 5000000, 10000000],
            value=1000000,
            format_func=lambda x: f"₹{x:,}"
        )

        if "Term Life" in policy_type:
            policy = insurance_engine.TermLifePolicy(sum_assured)
        else:
            policy = insurance_engine.EndowmentPolicy(sum_assured)

        st.markdown("#### Select Optional Add-on Riders (with Multi-Rider Discounts)")
        available_riders = ["Critical Illness", "Accidental Disability", "Waiver of Premium", "Hospital Cash"]
        selected_riders = st.multiselect("Active Riders", available_riders, default=["Critical Illness", "Accidental Disability"])

        # Compatibility Check
        compatibility = insurance_engine.validate_rider_compatibility(policy, selected_riders)
        if compatibility["compatible"]:
            st.success(f"✅ Underwriting Status: {compatibility['reason']}")
        else:
            st.error(f"❌ Incompatible Selection: {compatibility['reason']}")

    # Calculations & Quote Summary
    total_premium = insurance_engine.calculate_total_premium(
        policy, selected_riders, age=age, is_tobacco=is_tobacco, frequency=payment_frequency
    )
    base_prem = policy.calculate_premium(age=age, is_tobacco=is_tobacco)
    
    # Frequency adjusted base premium
    freq_div = 12.0 if payment_frequency == "Monthly" else (4.0 if payment_frequency == "Quarterly" else 1.0)
    base_prem_freq = round(base_prem / freq_div, 2)
    riders_prem_freq = max(0.0, round(total_premium - base_prem_freq, 2))

    with col2:
        st.subheader("2️⃣ Real-Time Quote & Budget Analysis")
        
        m_col1, m_col2 = st.columns(2)
        m_col1.metric(label=f"Total Quote ({payment_frequency})", value=f"₹{total_premium:,.2f}")
        m_col2.metric(label="Base Policy Sum Assured", value=f"₹{sum_assured:,}")

        # Budget comparison
        budget_diff = budget - total_premium
        if budget_diff >= 0:
            st.success(f"🟢 **Within Budget!** You have ₹{budget_diff:,.2f} remaining in your {payment_frequency.lower()} limit.")
            budget_ratio = min(1.0, total_premium / max(1.0, budget))
            st.progress(budget_ratio, text=f"Budget Utilization: {budget_ratio*100:.1f}%")
        else:
            st.error(f"🔴 **Exceeds Budget!** Package exceeds your limit by ₹{abs(budget_diff):,.2f}.")
            st.progress(1.0, text="Budget Limit Exceeded")

        st.markdown("#### Quote Breakdown")
        st.write(f"- **Base Policy Premium**: ₹{base_prem_freq:,.2f}")
        st.write(f"- **Riders Subtotal (After Multi-Rider Discounts)**: ₹{riders_prem_freq:,.2f}")
        if len(selected_riders) >= 2:
            discount_pct = "10%" if len(selected_riders) >= 3 else "5%"
            st.info(f"🎉 **{discount_pct} Multi-Rider Discount Applied!**")

        # Download quote summary
        summary_text = (
            f"=== LIC CONSOLIDATED QUOTE SUMMARY ===\n"
            f"Customer Age: {age}\n"
            f"Tobacco Usage: {'Yes' if is_tobacco else 'No'}\n"
            f"Base Policy: {policy.policy_type} (Sum Assured: ₹{sum_assured:,})\n"
            f"Selected Riders: {', '.join(selected_riders) if selected_riders else 'None'}\n"
            f"Payment Schedule: {payment_frequency}\n"
            f"Total Premium Quote: ₹{total_premium:,.2f}\n"
            f"Budget Status: {'Within Budget' if budget_diff >= 0 else 'Exceeds Budget'}\n"
            f"=====================================\n"
        )
        
        st.download_button(
            label="📥 Download Formal Quote Summary (TXT)",
            data=summary_text,
            file_name="LIC_Quote_Summary.txt",
            mime="text/plain"
        )

    # Automated Recommendations Section
    st.divider()
    st.subheader("💡 Automated Recommendations for Your Budget")
    recommendations = insurance_engine.recommend_policy_configuration(budget, payment_frequency)
    
    rec_col1, rec_col2 = st.columns(2)
    for idx, (p_name, p_obj) in enumerate(recommendations.items()):
        rec_col = rec_col1 if idx == 0 else rec_col2
        with rec_col:
            rec_prem = insurance_engine.calculate_total_premium(p_obj, ["Critical Illness"], age=age, is_tobacco=is_tobacco, frequency=payment_frequency)
            st.info(f"**Recommended {p_name} Package**\n\n"
                    f"- Max Recommended Sum Assured: **₹{int(p_obj.sum_assured):,}**\n"
                    f"- Est. {payment_frequency} Premium: **₹{rec_prem:,.2f}**\n"
                    f"- Features: Base Cover + Critical Illness Rider")

if __name__ == '__main__':
    main()

import sys
import json
from dispute_resolver import DisputeResolverClient

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== Commerce Dispute Resolution Agent Example ===")
    
    # Initialize client in mock mode
    client = DisputeResolverClient()
    
    # Scenario A: Damaged item within 30-day return window
    print("\n--- Scenario A: Damaged Product within Return Window ---")
    claim_a = "item_damaged"
    purchase_date_a = "2026-06-15" # 12 days ago (within 30-day window)
    order_total_a = 85.00
    
    audit_a = client.evaluate_policy(purchase_date_a, 30, claim_a)
    print(f"Elapsed Days: {audit_a['days_elapsed']}")
    print(f"Is Eligible for Return: {audit_a['is_eligible']}")
    print(f"Reasoning: {audit_a['reasoning']}")
    
    resolutions_a = client.suggest_dispute_resolutions(claim_a, order_total_a, audit_a['is_eligible'])
    print("Suggested Resolutions:")
    for res in resolutions_a:
        print(f"  - [{res['type'].upper()}] Value: ${res['value']:.2f} -> {res['explanation']}")
        
    # Build Stripe refund payload draft for Scenario A
    payload_a = client.build_stripe_payload("ORD-990812", order_total_a, claim_a)
    print("\n[Stripe Refund API Payload Draft]:")
    print(json.dumps(payload_a, indent=2))

    # Scenario B: Refund claim out of 30-day return window
    print("\n--- Scenario B: Refund Claim Out of Return Window ---")
    claim_b = "refund"
    purchase_date_b = "2026-05-10" # 48 days ago (exceeds 30-day window)
    order_total_b = 150.00
    
    audit_b = client.evaluate_policy(purchase_date_b, 30, claim_b)
    print(f"Elapsed Days: {audit_b['days_elapsed']}")
    print(f"Is Eligible for Return: {audit_b['is_eligible']}")
    print(f"Reasoning: {audit_b['reasoning']}")
    
    resolutions_b = client.suggest_dispute_resolutions(claim_b, order_total_b, audit_b['is_eligible'])
    print("Suggested Resolutions (Out-of-Window):")
    for res in resolutions_b:
        print(f"  - [{res['type'].upper()}] Value: ${res['value']:.2f} -> {res['explanation']}")

if __name__ == "__main__":
    main()

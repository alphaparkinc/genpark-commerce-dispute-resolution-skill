# commerce-dispute-resolution-skill

> **GenPark AI Agent Skill** -- # Commerce Dispute Resolution Agent Skill

This repository contains the **Commerce Dispute Resolution Agent Skill** — an agent skill interface configuration (`skill.json`), developer SDK client (`dispute_resolver.py`), and validation scripts. It is designed to automate return/refund audits against merchant policies, suggest partial/full resolution options, and generate Stripe API payloads.

---

## 🚀 Capabilities

* **Eligibility Window Auditor:** Calculates dates elapsed relative to order parameters and return guidelines.
* **Smart Resolution Engine:** Dynamically generates resolution paths (full refunds, replacements, or store credit codes) depending on warranty rules.
* **Automated Payments Draft:** Compiles formatted charge payload drafts compatible with Stripe API or Shopify webhooks.

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configuration:
   Set your API environment variables if executing requests against the live production server (otherwise, client executes in mock mode):
   * **PowerShell**:
     ```powershell
     $env:DISPUTE_API_KEY="your_api_key"
     ```
   * **bash**:
     ```bash
     export DISPUTE_API_KEY="your_api_key"
     ```

---

## 💻 SDK Usage Reference

```python
from dispute_resolver import DisputeResolverClient

# Initialize Client (mock mode by default)
client = DisputeResolverClient()

# Check policy compliance
audit = client.evaluate_policy(
    purchase_date_str="2026-06-15",
    policy_window=30,
    claim_type="refund"
)
print(f"Eligible: {audit['is_eligible']}")

# Get resolution paths
resolutions = client.suggest_dispute_resolutions(
    claim_type="refund",
    total_amount=100.00,
    is_eligible=audit["is_eligible"]
)
print(resolutions)

# Generate Stripe draft
stripe_payload = client.build_stripe_payload("ORD123", 100.00, "refund")
```

---

## 📜 License
This project is licensed under the MIT License.
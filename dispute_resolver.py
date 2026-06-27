import os
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

class DisputeResolverError(Exception):
    """Base exception class for Dispute Resolver Client."""
    pass

class DisputeResolverClient:
    """
    Client for automating e-commerce customer disputes, checking return windows, and building refund payloads.
    Supports a mock mode for local testing.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.dispute-resolver.ai/v1"):
        self.api_key = api_key or os.environ.get("DISPUTE_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.mock_mode = self.api_key is None or self.api_key == "mock"
        
        if self.mock_mode:
            print("[DisputeResolverClient] API Key not set. Running in MOCK Mode.")

    def evaluate_policy(
        self,
        purchase_date_str: str,
        policy_window: int,
        claim_type: str
    ) -> Dict[str, Any]:
        """
        Calculates return window thresholds and outputs policy compliance status.
        """
        # Parse dates
        try:
            purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d")
        except ValueError:
            raise DisputeResolverError(f"Invalid date format: {purchase_date_str}. Must be YYYY-MM-DD")
            
        current_date = datetime(2026, 6, 27) # Current local execution date
        days_elapsed = (current_date - purchase_date).days
        is_eligible = days_elapsed <= policy_window
        
        reasoning = (
            f"Purchase was made {days_elapsed} days ago. Store return window limit is {policy_window} days. "
            f"Claim eligibility is {str(is_eligible).lower()}."
        )
        
        return {
            "is_eligible": is_eligible,
            "days_elapsed": days_elapsed,
            "reasoning": reasoning
        }

    def suggest_dispute_resolutions(
        self,
        claim_type: str,
        total_amount: float,
        is_eligible: bool
    ) -> List[Dict[str, Any]]:
        """
        Recommends appropriate refund, replacement, or discount options.
        """
        resolutions = []
        if is_eligible:
            if claim_type in ["refund", "item_damaged"]:
                resolutions.append({
                    "type": "full_refund",
                    "value": total_amount,
                    "explanation": "Provide a 100% refund to the original payment method upon return shipment."
                })
            if claim_type == "item_damaged":
                resolutions.append({
                    "type": "replacement",
                    "value": 0.0,
                    "explanation": "Process a $0.00 replacement order with standard shipping."
                })
            # Always suggest a partial refund to keep
            resolutions.append({
                "type": "partial_refund_keep",
                "value": round(total_amount * 0.3, 2),
                "explanation": "Offer a 30% partial refund if the customer chooses to keep the item."
            })
        else:
            # Out of window resolutions
            resolutions.append({
                "type": "store_credit",
                "value": round(total_amount * 0.5, 2),
                "explanation": "Offer 50% store credit as an out-of-warranty customer gesture."
            })
            resolutions.append({
                "type": "discount_coupon",
                "value": 20.0,
                "explanation": "Issue a 20% discount coupon code for future purchases."
            })
            
        return resolutions

    def build_stripe_payload(self, order_id: str, amount: float, reason: str) -> Dict[str, Any]:
        """
        Drafts a standard Stripe refund payload configuration.
        """
        return {
            "charge": f"ch_mock_{order_id}",
            "amount": int(amount * 100), # Stripe amount in cents
            "reason": "requested_by_customer" if reason == "refund" else "product_damaged",
            "metadata": {
                "order_id": order_id,
                "triggered_by": "commerce_dispute_agent"
            }
        }

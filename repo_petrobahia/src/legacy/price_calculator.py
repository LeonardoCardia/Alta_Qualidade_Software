"""
Module for price calculation with tier-based discounts.

This module provides functionality to calculate prices with discounts
based on client tier levels.
"""


class PriceCalculator:
    """
    A calculator for applying tier-based discounts to prices.

    This class handles price calculations with different discount rates
    based on client tier levels (gold, silver, bronze).
    """

    DISCOUNT_RATES = {
        'gold': 0.20,
        'silver': 0.10,
        'bronze': 0.05
    }

    def calculate_price(self, base_price, tier):
        """
        Calculate the final price after applying tier-based discount.

        Args:
            base_price (float): The original price before discount.
            tier (str): The client tier level ('gold', 'silver', or 'bronze').

        Returns:
            float: The final price after applying the discount.

        Note:
            If the tier is not recognized, no discount is applied.
        """
        discount = self.DISCOUNT_RATES.get(tier.lower(), 0)
        final_price = base_price * (1 - discount)
        return final_price

    def get_discount_rate(self, tier):
        """
        Get the discount rate for a specific tier.

        Args:
            tier (str): The client tier level.

        Returns:
            float: The discount rate as a decimal (e.g., 0.20 for 20%).
        """
        return self.DISCOUNT_RATES.get(tier.lower(), 0)

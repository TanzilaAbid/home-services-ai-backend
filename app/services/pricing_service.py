"""
Instant price estimator.

This is a simple, explainable rule-based algorithm (not ML) - it estimates
a price range and completion time based on service type, room size, and
wall/surface condition. Rates are illustrative starting points; Tanzila can
tune these numbers once real provider pricing data is available.
"""

# Base rate per square foot, by service category (USD)
BASE_RATE_PER_SQFT = {
    "painter": 1.20,
    "plumber": 2.50,
    "electrician": 2.00,
}

# Multiplier applied depending on how much extra work "condition" implies
CONDITION_MULTIPLIER = {
    "good": 1.0,
    "average": 1.25,
    "poor": 1.6,
}

# How many square feet a single worker can complete per hour, by category
SQFT_PER_HOUR = {
    "painter": 40,
    "plumber": 15,
    "electrician": 20,
}


def estimate_price(service_type: str, room_sqft: float, wall_condition: str, num_rooms: int = 1) -> dict:
    service_type = (service_type or "").strip().lower()
    wall_condition = (wall_condition or "average").strip().lower()

    if service_type not in BASE_RATE_PER_SQFT:
        raise ValueError(
            f"Unknown service_type '{service_type}'. "
            f"Must be one of: {list(BASE_RATE_PER_SQFT.keys())}"
        )
    if wall_condition not in CONDITION_MULTIPLIER:
        wall_condition = "average"

    total_sqft = room_sqft * num_rooms

    base_rate = BASE_RATE_PER_SQFT[service_type]
    multiplier = CONDITION_MULTIPLIER[wall_condition]

    base_price = total_sqft * base_rate * multiplier

    price_min = round(base_price * 0.8, 2)
    price_max = round(base_price * 1.2, 2)

    sqft_per_hour = SQFT_PER_HOUR[service_type]
    estimated_hours = round((total_sqft / sqft_per_hour) * multiplier, 1)

    price_min = max(price_min, 50.0)
    price_max = max(price_max, price_min + 20.0)
    estimated_hours = max(estimated_hours, 1.0)

    return {
        "price_min": price_min,
        "price_max": price_max,
        "estimated_hours": estimated_hours,
        "currency": "USD",
    }

"""
Canteen Rush AI - Multi-Vendor AI Engine
Enhanced Prediction Engine with Transparency & Adaptive Logic
"""

from datetime import datetime, timedelta
import database as db


def calculate_wait_time(vendor_id: int, item_prep_time: int, target_break: str = "Immediate") -> dict:
    """
    Calculate wait time for specific vendor with transparency breakdown.
    
    Factors:
    1. Base Prep Time (Deterministic)
    2. Queue Load (Active orders factor)
    3. Rush Multiplier (Historical spike emulation)
    4. Target Break (Scheduling factor)
    
    Returns transparency-enabled dict.
    """
    active_orders_count = db.get_vendor_active_orders_count(vendor_id)
    
    # 1. Base Prep (Deterministic)
    base_prep = item_prep_time
    
    # 2. Queue Delay (2 mins per order ahead)
    queue_delay = active_orders_count * 2
    
    # 3. Rush Detection (>10 orders = Load Spike)
    is_rush = active_orders_count > 10
    multiplier = 1.5 if is_rush else 1.0
    
    # Apply multiplier to queue delay
    adjusted_queue_delay = int(queue_delay * multiplier)
    
    # 4. Total Calculation
    total_wait = base_prep + adjusted_queue_delay + 2 # +2 min buffer
    
    # 5. Target Break Handling (Pre-emptive ordering)
    now = datetime.now()
    if target_break == "Immediate":
        pickup_time = now + timedelta(minutes=total_wait)
    else:
        # Extract time from string like "10:30 AM Break"
        try:
            time_part = target_break.split(" ")[0]
            target_dt = datetime.strptime(time_part, "%I:%M")
            # Set to today
            pickup_time = now.replace(hour=target_dt.hour, minute=target_dt.minute, second=0, microsecond=0)
            # If target is in past (e.g., today 1 PM but now 2 PM), move to next day or just cap it
            if pickup_time < now:
                pickup_time = now + timedelta(minutes=total_wait)
        except:
            pickup_time = now + timedelta(minutes=total_wait)

    formatted_time = pickup_time.strftime("%I:%M %p")
    
    return {
        "formatted_time": formatted_time,
        "is_rush_hour": is_rush,
        "minutes": total_wait,
        "active_orders": active_orders_count,
        "breakdown": {
            "base_prep": base_prep,
            "queue_delay": adjusted_queue_delay,
            "buffer": 2,
            "total": total_wait
        }
    }


def get_vendor_stats(vendor_id: int) -> dict:
    """Get queue statistics for specific vendor."""
    active_orders = db.get_vendor_active_orders_count(vendor_id)
    
    is_rush = active_orders > 10
    multiplier = 1.5 if is_rush else 1.0
    avg_wait = int((active_orders * 2 * multiplier) + 5)
    
    return {
        "queue_load": active_orders,
        "avg_wait_minutes": avg_wait,
        "is_rush_hour": is_rush
    }

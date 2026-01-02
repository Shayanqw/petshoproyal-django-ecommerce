"""Utility helpers used across the project."""

from typing import Optional

from order import models


def get_client_ip(request) -> Optional[str]:
    """Return the best-effort client IP address (supports reverse proxies)."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def get_delivery_price(weight: float) -> int:
    """Return delivery price for the given weight using configured ranges."""
    delivery_price = (
        models.DeliveryPrice.objects.filter(from_weight__lt=weight, to_weight__gte=weight).first()
    )
    return delivery_price.price if delivery_price else 0

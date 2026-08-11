"""Turn a field-service observation into a safe technician follow-up."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrder:
    order_id: str
    photo_note: str
    dispatch_status: str


def follow_up_for(order: WorkOrder) -> str:
    """Choose the next state without exposing personal health information."""
    if order.dispatch_status == "assigned" and order.photo_note.strip():
        return "confirm_arrival_window"
    if order.dispatch_status == "en_route":
        return "send_site_access_check"
    return "request_dispatch_update"


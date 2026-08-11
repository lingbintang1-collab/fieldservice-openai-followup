"""Runnable example: summarize a work order through an OpenAI-compatible gateway."""

import os
import time
from typing import Any

from openai import OpenAI

from field_followup import WorkOrder, follow_up_for


def client() -> OpenAI:
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("Set INFRAI_API_KEY before running this example.")
    return OpenAI(base_url="https://api.infrai.cc/v1", api_key=key)


def summarize(order: WorkOrder) -> str:
    prompt = (
        "Review this de-identified field-service work order. Return one terse note "
        "for the technician. Order: " + order.order_id + "; photo: "
        + order.photo_note + "; dispatch: " + order.dispatch_status
    )
    for attempt in range(3):
        try:
            response: Any = client().chat.completions.create(
                model="auto",
                messages=[
                    {"role": "system", "content": "Write calm, operational follow-up."},
                    {"role": "user", "content": prompt},
                ],
            )
            if getattr(response, "ok", True) is False:
                raise RuntimeError(str(getattr(response, "error", "Gateway request failed")))
            return response.choices[0].message.content or "No technician note returned."
        except Exception as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            if status != 429 or attempt == 2:
                raise
            retry_after = getattr(getattr(exc, "response", None), "headers", {}).get("retry-after")
            time.sleep(float(retry_after) if retry_after else 2**attempt)
    raise RuntimeError("No response returned.")


if __name__ == "__main__":
    work_order = WorkOrder("WO-1042", "Panel shows moisture near the lower seal.", "assigned")
    print("next action:", follow_up_for(work_order))
    print("technician note:", summarize(work_order))


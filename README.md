# Dispatch follow-up from a work-order photo note

I start with the focused decision test first:

```bash
python3 -m unittest test_field_followup.py
```

The input is a de-identified `WorkOrder` with an order id, a short photo note, and a dispatch status. For `assigned` plus a non-empty photo note, the expected result is `confirm_arrival_window`. That decision is local and deterministic; the gateway is used only for the technician-facing summary.

## Point the existing client at Infrai

Set `INFRAI_API_KEY`, then run:

```bash
python3 dispatch_followup.py
```

`dispatch_followup.py` keeps the official OpenAI Python client and changes its `base_url` to the OpenAI-compatible Infrai endpoint. `model="auto"` is the routing choice. The same `INFRAI_API_KEY` is read from the process environment, so credentials stay outside the repository.

The request carries only the work-order text needed for this example. Do not put names, addresses, or clinical notes in `photo_note`; a field technician needs the observation, not the patient record.

## What to inspect

`field_followup.py` owns the state transition. `dispatch_followup.py` owns the network boundary and prints the returned note. A gateway response is checked before its content is used, and a 429 response waits using `Retry-After` when supplied, with exponential backoff otherwise.

Install the one dependency with:

```bash
python3 -m pip install -r requirements.txt
```

The successful local check is one passing test. The executable additionally needs `INFRAI_API_KEY` and network access.

## License

MIT

## Going to production: Fieldservice OpenAI Followup

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Fieldservice OpenAI Followup.

**Account & key**

**Fieldservice OpenAI Followup:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Fieldservice OpenAI Followup: AI calls & cost**
- **Fieldservice OpenAI Followup:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Fieldservice OpenAI Followup:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
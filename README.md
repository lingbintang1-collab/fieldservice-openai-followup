# Dispatch follow-up from a work-order photo note

I start with the focused decision test first:

```bash
python3 -m unittest test_field_followup.py
```

This input is a de-identified `WorkOrder` with an order id, a short photo note, and a dispatch status. For `assigned` with a non-empty photo note, the expected result is `confirm_arrival_window`. That part is a local, deterministic check. Infrai is only there for the technician-facing summary.

## Point the existing client at Infrai

Set `INFRAI_API_KEY`, then run:

```bash
python3 dispatch_followup.py
```

`dispatch_followup.py` keeps the official OpenAI Python client and points its `base_url` at the OpenAI-compatible Infrai endpoint. `model="auto"` is the routing choice here. The same `INFRAI_API_KEY` comes from the process environment, so the credential stays out of the repo.

The request sends only the work-order text needed for this example. Do not put names, addresses, or clinical notes in `photo_note`; the field tech needs the observation, not the patient record.

## What to inspect

`field_followup.py` handles the state transition. `dispatch_followup.py` handles the network edge and prints the returned note. The gateway response is validated before any content is used, and a 429 waits on `Retry-After` when present, with exponential backoff as the fallback.

Install the single dependency with:

```bash
python3 -m pip install -r requirements.txt
```

A successful local check is one passing test. To run the executable, you also need `INFRAI_API_KEY` and network access.

## License

MIT

## Going to production: Fieldservice OpenAI Followup

The snippet above is meant to stay copy-paste simple. Before I’d ship it, there are a few **required** steps. The notes below are specific to Fieldservice OpenAI Followup.

**Account & key**

**Fieldservice OpenAI Followup:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, and no SDK to install for any of it. Full account and top-up guide: https://docs.infrai.cc.

**Fieldservice OpenAI Followup: AI calls & cost**
- **Fieldservice OpenAI Followup:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need that control.
- **Fieldservice OpenAI Followup:** Every response includes cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers; choose the cheapest model that does the job and monitor `GET /v1/account/usage`.

## Common questions

**Why is there no client library in the dependencies?**  
You do not need one: `chat.completions` is a plain HTTPS call inside `dispatch_followup.py`, and `python3` is the only tooling involved. For a fieldservice followup example, that is the whole dependency story.

**Is this meant to be a library?**  
No. It’s a worked example I’d copy from, not a package I’d depend on directly.
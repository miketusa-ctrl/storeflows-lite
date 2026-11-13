# Welcome flow — spec

> Not affiliated with Klaviyo, MailerLite, Brevo, or Shopify. Product names are used only to describe compatibility. Vendor features change; verify each step in your own account. Items marked [verify in your account] come from public docs and were not tested in a live account. Results vary.

**Purpose:** Greet new subscribers, set expectations, introduce the signature product, and remove purchase friction.

## Trigger

Contact joins the newsletter list/group via a signup form, popup, or checkout opt-in (with marketing consent).

## Entry filters

- Has consented to email marketing (single or double opt-in per your region; see compliance checklist).
- Exclude contacts who have already placed an order (they belong in Post-Purchase), or keep them in and skip Email 3.
- Exclude internal/test addresses (segment `internal_test`).

## Timing

| # | Email | Send | Goal |
|---|-------|------|------|
| 1 | A proper hello | Immediately after signup | Confirm they are in the right place, set expectations, deliver any promised offer |
| 2 | What we are known for | 2 days after Email 1 | Introduce the signature product and the reason behind it |
| 3 | How we do things | 3 days after Email 2 | Remove purchase friction (shipping, returns, care) and invite a reply |

Copy: `flows/01-welcome/copy.md` · Templates: `flows/01-welcome/email-N.html` (+ `.txt`).

## Exit conditions

- Places an order: skip remaining welcome emails (Email 2 and 3 additional filter: 'has not placed order since starting flow').
- Unsubscribes or is suppressed (all ESPs do this automatically).

## Re-entry

Once per contact (never re-enter).

## Holdout and measurement

Optional. Many stores keep 100% in Welcome; if you test, hold out 10% for 21 days and compare first-order rate. Track in `tracker/harlo-storeflows-tracker.xlsx`.

**KPIs:** Click rate per email, first-order conversion within 21 days, revenue per recipient (RPR), unsubscribe rate.

## Safety

Build every flow in **draft / inactive / manual** status first. Send internal tests, check every merge tag renders, confirm the unsubscribe and address footer appear, then have a human approve before switching it live. Results vary by store, list, offer and season; nothing in this spec promises opens, inbox placement or revenue.

# Per-ESP setup

## Klaviyo setup

- **Native support:** Native
- **Trigger:** List trigger: **Added to list** = your newsletter list. (Alternative: metric trigger on the form-submit event if your forms write one.)
- **Filters / re-entry:** Profile filter: 'Placed Order zero times since starting this flow'. Re-entry: enter once.
- **Timing:** Email 1 immediately → time delay 2 days → Email 2 → time delay 3 days → Email 3. Turn on Smart Sending for Emails 2–3 only (leave Email 1 off so the promised offer always arrives).
- **Exit conditions:** Additional filter on Emails 2–3: 'Placed Order zero times since starting this flow'.
- **Merge tags:** `{{ first_name|default:'there' }}`, `{{ organization.name }}`, `{% unsubscribe_link %}`, `{% manage_preferences_link %}`, `{{ organization.full_address }}`.
- **Agent (MCP) draft path:** `get_lists` (find list id) → `create_email_template` ×3 from the kit HTML (after merge-tag swap) → `create_flow` with list trigger, leave in draft → `get_flow` to confirm → stop for human approval. Do not call `update_flow` to set it live.
- **Limitations / workarounds:** Double opt-in lists only trigger after confirmation. Check that the list trigger uses the same list your forms write to.

## MailerLite setup

- **Native support:** Native
- **Trigger:** `subscriber_joins_group` = your Newsletter group (or `form_completed` for a specific form).
- **Filters / re-entry:** Condition step before Emails 2–3: 'Subscriber has purchased? (e-commerce condition, if your store is connected) → No'. Repeat: off.
- **Timing:** Email 1 → delay 2 days → Email 2 → delay 3 days → Email 3.
- **Exit conditions:** Condition step (purchased → end). Unsubscribed subscribers leave automatically.
- **Merge tags:** `{$name}` (set a fallback in the variable picker [verify in your account]), `{$unsubscribe}`, `{$preferences}`; store address comes from account settings in the footer.
- **Agent (MCP) draft path:** `list_resources` (type: groups) for the group id → `build_automation` (or `create_automation`) with the trigger and email/delay steps; it is created **inactive** → `update_automation_email_content` with the kit HTML → `dry_run_automation` → `send_test_automation` to an internal address → stop for human approval.
- **Limitations / workarounds:** Condition steps on purchase data require a connected e-commerce store. Multiple triggers (up to 3) depend on plan.

## Brevo setup

- **Native support:** Native
- **Trigger:** Pre-built **Welcome message** automation, or entry 'Contact added to a list' = Newsletter list.
- **Filters / re-entry:** Contact filter at entry: exclude internal list. Condition before Emails 2–3: Ecommerce → 'No order placed' since entry (needs Brevo e-commerce app/plugin).
- **Timing:** Email 1 → wait 2 days → Email 2 → wait 3 days → Email 3.
- **Exit conditions:** Exit condition: order placed (ecommerce `order_created`) or tracker `order_completed` event.
- **Merge tags:** `{{ contact.FIRSTNAME|default:"there" }}`, `{{ unsubscribe }}`, `{{ update_profile }}`; company address in your sender/footer settings.
- **Agent (MCP) draft path:** Brevo MCP has **no automation module**. Agent can: create the 3 templates (templates module) and the Newsletter list/segment (lists/segments modules). A human assembles the workflow in Automations and links the templates.
- **Limitations / workarounds:** Workflow cannot be created or activated through MCP (as of Nov 2026). Purchase-based conditions need the e-commerce integration.

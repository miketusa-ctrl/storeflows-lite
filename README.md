# Harlo Store Email Flows Kit (Lite)

A free, ready-to-adapt **Welcome flow** for small online stores on Klaviyo, MailerLite or Brevo, plus a **21-day holdout and revenue-per-recipient tracker** so you can see whether the flow is worth its sends.

Not affiliated with Klaviyo, MailerLite, Brevo, or Shopify. Product names are used only to describe compatibility. No third-party logos are included.

Results vary. These are templates and a planning sheet; nothing here promises opens, inbox placement, conversions or revenue.

## What's inside

| Path | What it is |
|---|---|
| `flows/01-welcome/copy.md` | Three welcome emails written out, each with 3 subject lines and a preheader |
| `flows/01-welcome/email-1.html` … `email-3.html` | Table-based HTML (inline CSS, mobile-friendly, unsubscribe/address footer) |
| `flows/01-welcome/email-1.txt` … `email-3.txt` | Plain-text versions |
| `flows/01-welcome/spec.md` | Trigger, filters, timing, exits + setup notes for Klaviyo, MailerLite and Brevo |
| `docs/placeholders.md` | Every placeholder explained, with each ESP's merge tag |
| `tracker/harlo-storeflows-tracker.xlsx` | 21-day holdout / RPR tracker with live formulas (sample data) |
| `tracker/*.csv`, `tracker/GOOGLE-SHEETS.md` | CSV versions and how to use them in Google Sheets |
| `compliance/footer-and-consent-checklist.md` | CAN-SPAM, GDPR, UK and CASL footer/consent checklist (not legal advice) |
| `scripts/check.py` | Checks your edited HTML, placeholders and links (`python3 scripts/check.py`) |
| `scripts/verify_formulas.py` | Recalculates the tracker in LibreOffice and flags formula errors (optional; needs `openpyxl` and LibreOffice) |

## Quick start

1. Fill the placeholders (`docs/placeholders.md`).
2. Build the flow in draft in your ESP using `flows/01-welcome/spec.md`.
3. Send yourself a test, tick the compliance checklist, then switch it live.
4. Hold out about 10% of new subscribers for 21 days and fill in the tracker.

## Want the other five flows?

The Pro kit adds Browse Abandon, Cart/Checkout Abandon, Post-Purchase + Review Request, VIP/Loyalty and Win-Back, with setup specs for the ESP you choose (Klaviyo, MailerLite or Brevo editions), segment and discount-guardrail sheets, an agent pack (prompts + skills for MCP-capable assistants) and a worked example store. An Agency edition adds all three ESP spec sets, five niche copy variants and a client-work license.

- **Pro** (pick the Klaviyo, MailerLite or Brevo edition, $29): [https://payhip.com/b/21Nxq](https://payhip.com/b/21Nxq)
- **Agency** (all three ESPs, five niche copy sets, client-work license, $79): [https://payhip.com/b/y3wea](https://payhip.com/b/y3wea)

## Support

Public contact: **digitalpromohub.support@gmail.com**

## License

See `LICENSE.md`.

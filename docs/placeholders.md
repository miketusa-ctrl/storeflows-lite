# Placeholder glossary

Every `{{placeholder}}`-style token used in the Lite kit's copy, HTML, text and specs is listed here. `scripts/check.py` fails if a template uses a placeholder that is missing from this table.

**Kit placeholders vs ESP tags.** Kit placeholders are lowercase with **no spaces** inside the braces, for example `{{first_name}}`. Before you paste a template into your ESP, replace each one either with your own fixed text (type **static** or **line**) or with your ESP's merge tag (type **dynamic** or **block**). ESP-native tags shown in specs (such as `{{ contact.FIRSTNAME }}` or `{% unsubscribe_link %}`) have spaces and are not kit placeholders.

Types:
- **static**: fill once with your store's own text or URL.
- **line**: choose one of the copy variants given in the flow's `copy.md` editor notes.
- **dynamic**: per-recipient merge tag; set a fallback in your ESP.
- **block**: an ESP content block (product, cart, order or recommendation block), not a plain tag.

Merge-tag columns are starting points taken from vendor docs on Nov 13, 2026; they were **not tested in a live account**. Anything marked **[verify in your account]** is unconfirmed: check it in your ESP's preview with a real test profile or order before sending. Exact event-property names depend on your store integration.

## Global (every email)

| Placeholder | Type | Meaning | Klaviyo | MailerLite | Brevo |
|---|---|---|---|---|---|
| `{{first_name}}` | dynamic | Recipient first name (fallback e.g. "there") | `{{ first_name\|default:'there' }}` | `{$name}` (set fallback in picker) | `{{ contact.FIRSTNAME\|default:"there" }}` |
| `{{store_name}}` | static | Your shop name | `{{ organization.name }}` or text | text | text |
| `{{store_url}}` | static | Home page URL | URL | URL | URL |
| `{{store_address}}` | static | Physical mailing address (required by CAN-SPAM) | `{{ organization.full_address }}` | account footer / text | text |
| `{{unsubscribe_url}}` | dynamic | One-click unsubscribe link | `{% unsubscribe_link %}` | `{$unsubscribe}` | `{{ unsubscribe }}` |
| `{{preferences_url}}` | dynamic | Preference / opt-down page | `{% manage_preferences_link %}` | `{$preferences}` | `{{ update_profile }}` |
| `{{sender_name}}` | static | Person signing the email (e.g. founder first name) | text | text | text |
| `{{support_email}}` | static | Customer-support address | text | text | text |

## Welcome

| Placeholder | Type | Meaning | Klaviyo | MailerLite | Brevo |
|---|---|---|---|---|---|
| `{{brand_story}}` | static | One or two sentences on why the shop exists | text | text | text |
| `{{email_frequency}}` | static | Honest cadence, e.g. "once a week" | text | text | text |
| `{{welcome_offer_line}}` | line | Offer sentence (1A) or no-offer sentence (1B) | text | text | text |
| `{{welcome_offer}}` | static | Offer promised at signup, e.g. "10% off your first order" | text | text | text |
| `{{discount_code}}` | dynamic/static | Code text; unique codes need your ESP's coupon feature | coupon tag | text | text / coupon |
| `{{discount_expiry}}` | static | Plain-language expiry date | text | text | text |
| `{{bestsellers_url}}` | static | Bestsellers collection URL | URL | URL | URL |
| `{{signature_product_name}}` | static | Your best-known product | text | text | text |
| `{{signature_product_story}}` | static | 2–3 sentences on how/why it is made | text | text | text |
| `{{signature_product_url}}` | static | Product page URL | URL | URL | URL |
| `{{signature_benefit_1}}` | static | Benefit bullet | text | text | text |
| `{{signature_benefit_2}}` | static | Benefit bullet | text | text | text |
| `{{signature_benefit_3}}` | static | Benefit bullet | text | text | text |
| `{{shipping_policy_line}}` | static | One-line shipping summary | text | text | text |
| `{{shipping_threshold}}` | static | Free-shipping minimum, e.g. "$50" | text | text | text |
| `{{returns_policy_line}}` | static | One-line returns summary | text | text | text |
| `{{returns_policy_url}}` | static | Returns policy URL | URL | URL | URL |
| `{{reply_time}}` | static | Typical reply time, e.g. "one business day" | text | text | text |

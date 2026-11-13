# Footer and consent checklist (CAN-SPAM, GDPR/UK, CASL)

> **Not legal advice.** This is a practical checklist written for small online stores, not a legal opinion. Laws differ by country and change over time, and your situation may have details this list does not cover. Check the official guidance linked below, and talk to a qualified lawyer if you are unsure. Using this checklist does not make you compliant and does not guarantee inbox placement.

## 1. Footer: what every marketing email in this kit carries

Every HTML and plain-text template already includes these placeholders in the footer. Map them to your ESP's tags (see `docs/placeholders.md`):

- [ ] **Who it's from:** `{{store_name}}` (also in the From name)
- [ ] **Physical postal address:** `{{store_address}}`. US CAN-SPAM requires a valid physical postal address (a registered PO box or private mailbox is allowed under FTC guidance). CASL also requires sender contact details.
- [ ] **Why they're getting it:** "You're receiving this because you signed up for emails from {{store_name}} or shopped with us."
- [ ] **Unsubscribe:** `{{unsubscribe_url}}`, which must work without a login, a fee, or more than a simple confirmation page.
- [ ] **Preferences / opt-down:** `{{preferences_url}}` (optional but recommended; it lets people get fewer emails instead of none)

Copy-paste footer (HTML) if you build your own template:

```html
<p style="margin:12px 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6b6b6b;">You're receiving this because you signed up for emails from {{store_name}} or shopped with us.</p>
<p style="margin:0 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6b6b6b;">{{store_name}}, {{store_address}}</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6b6b6b;"><a href="{{unsubscribe_url}}" target="_blank" rel="noopener" style="color:#6b6b6b;">Unsubscribe</a> &middot; <a href="{{preferences_url}}" target="_blank" rel="noopener" style="color:#6b6b6b;">Update preferences</a></p>
```

## 2. United States: CAN-SPAM

- [ ] From, To, Reply-To and routing info are accurate and identify your business.
- [ ] Subject lines are not deceptive. (The kit's subject variants describe the email honestly; keep it that way when you edit.)
- [ ] The email is identifiable as marketing. Promotional context is usually enough; be explicit if it might be mistaken for a transactional email.
- [ ] A valid physical postal address is included.
- [ ] A clear opt-out is included, keeps working for at least **30 days** after you send, and is honored within **10 business days**. Don't charge for it, ask for more than an email address and preferences, or sell/transfer opted-out addresses.
- [ ] You stay responsible even when an agency or ESP sends for you, so check their setup.
- Note: purely transactional messages (order confirmation, shipping notice) have lighter rules. Post-Purchase Emails 2–4 in this kit are marketing, so treat them as marketing.
- Source: FTC, *CAN-SPAM Act: A Compliance Guide for Business*: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business

## 3. EU / EEA: GDPR + ePrivacy

- [ ] You have a lawful basis for marketing email. For most stores that means **consent**: freely given, specific, informed, unambiguous, with no pre-ticked boxes. Some member states allow a "similar products" exception for existing customers, and national rules vary.
- [ ] **Double opt-in** is recommended (and expected in some countries, for example Germany) as proof of consent.
- [ ] Keep consent records: who, when, how (form name / checkout box), and what they were told.
- [ ] Withdrawal is as easy as giving consent (the unsubscribe link), and you act on it promptly.
- [ ] Your privacy notice explains email marketing, tracking (opens/clicks, onsite tracking used for browse/cart flows) and retention.
- [ ] Onsite tracking that powers Browse/Cart flows (Klaviyo onsite JS, Brevo tracker, MailerLite site tracking) may need **cookie consent** under ePrivacy rules. Check your cookie banner gates it.
- [ ] Your ESP has a Data Processing Agreement in place, and international transfers are covered.
- Source: European Commission data protection overview: https://commission.europa.eu/law/law-topic/data-protection_en

## 4. United Kingdom: UK GDPR + PECR

- [ ] Consent for marketing email to individuals, **or** the PECR "soft opt-in": you got the address during a sale (or sale negotiation) of your own similar products, you offered an opt-out at collection, and you offer one in every email.
- [ ] Soft opt-in does not cover people who only signed up for a giveaway or newsletter without buying. They need consent.
- Source: ICO, direct marketing guidance: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/

## 5. Canada: CASL

- [ ] **Express consent** (clear opt-in that names your business and says they can withdraw), **or implied consent**, for example an existing business relationship from a purchase in the last **2 years**, or an inquiry in the last 6 months. Implied consent expires, so track the dates.
- [ ] Each email identifies the sender and includes a mailing address plus one other contact method (email, phone, or web).
- [ ] The unsubscribe mechanism works for at least **60 days** after sending, and requests are processed within **10 business days**.
- [ ] Keep records proving consent. Under CASL, the sender carries the burden of proof.
- Source: CRTC, CASL FAQ: https://crtc.gc.ca/eng/com500/faq500.htm

## 6. Reviews and offers (relevant to Post-Purchase, Cart and Win-Back flows)

- [ ] Never make an incentive conditional on a **positive** review, and don't suppress negative ones. The kit's review email asks for an *honest* review.
- [ ] Offer terms are clear: what, how much, expiry. Expiry dates in copy match the real code expiry. No fake countdowns.
- Sources: FTC Endorsement Guides: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking ; FTC Rule on the Use of Consumer Reviews and Testimonials (16 CFR Part 465): https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465

## 7. Mailbox-provider sender requirements (good practice, not law)

Major mailbox providers publish requirements for bulk senders: authenticate your domain (SPF, DKIM, DMARC), support one-click unsubscribe, and keep spam complaints low. Meeting them helps but does not guarantee inbox placement.
- Google email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo sender best practices: https://senders.yahooinc.com/best-practices/

## 8. Before any flow goes live

- [ ] Consent source recorded for the list or segment that triggers the flow
- [ ] Footer renders with real address and a working unsubscribe in a test send
- [ ] Preference link works (or remove it if your ESP lacks one)
- [ ] Internal test addresses excluded from reporting
- [ ] Human sign-off recorded (name, date) in your launch notes

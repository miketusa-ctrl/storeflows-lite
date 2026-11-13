# Welcome flow — copy

Three emails that introduce the store, show what it's known for, and (only if your signup form promised one) deliver the welcome offer. Swap every double-brace placeholder before use; see `docs/placeholders.md`.

> Editor notes (lines starting with `>`) are for you, not the customer. They are not rendered into the HTML templates.
> Discount rule: use the offer version of `{{welcome_offer_line}}` only if your signup form advertised an offer. If it did not, use version **1B** and keep the whole flow discount-free.

## Email 1: A proper hello
- **Send:** Immediately after signup
- **Goal:** Confirm they are in the right place, set expectations, deliver any promised offer
- **Subject A:** Welcome to {{store_name}}, {{first_name}}
- **Subject B:** You're in. Here's what happens next
- **Subject C:** Glad you found us
- **Preheader:** A quick hello, what to expect from us, and where to start

**Body**

Hi {{first_name}},

Thanks for joining {{store_name}}, and welcome. {{brand_story}}

Here's what you can expect from us: a first look at new arrivals, the occasional behind-the-scenes note, and honest recommendations. We email about {{email_frequency}}, and you can change that any time.

{{welcome_offer_line}}

> `{{welcome_offer_line}}`, 1A (offer promised on your signup form): "As promised, here is your welcome offer: {{welcome_offer}} with code {{discount_code}}. It is valid until {{discount_expiry}}." 1B (no offer promised): "If you are not sure where to start, our bestsellers are a good place. They are the pieces people come back for."

**Button:** Start browsing | {{bestsellers_url}}

If you ever have a question, just hit reply. A real person reads every message.

Warmly,
{{sender_name}}, {{store_name}}

## Email 2: What we are known for
- **Send:** 2 days after Email 1
- **Goal:** Introduce the signature product and the reason behind it
- **Subject A:** The one we're proudest of
- **Subject B:** Meet {{signature_product_name}}
- **Subject C:** Where most people start with us
- **Preheader:** The story behind our most-loved piece, and why people keep coming back to it

**Body**

Hi {{first_name}},

If you asked our regulars what to try first, most of them would point to **{{signature_product_name}}**.

{{signature_product_story}}

A few things people tell us they love about it:

- {{signature_benefit_1}}
- {{signature_benefit_2}}
- {{signature_benefit_3}}

**Button:** Take a closer look | {{signature_product_url}}

Not quite your style? That's fine too. The full collection is right here: [browse everything]({{store_url}}).

{{sender_name}}

## Email 3: How we do things
- **Send:** 3 days after Email 2
- **Goal:** Remove purchase friction (shipping, returns, care) and invite a reply
- **Subject A:** The small print, made simple
- **Subject B:** Shipping, returns, and a quick question for you
- **Subject C:** Before you order: the useful details
- **Preheader:** How shipping and returns work here, plus one thing we'd love to know

**Body**

Hi {{first_name}},

Before you order anything, here are the details we'd want to know if we were in your shoes:

- **Shipping:** {{shipping_policy_line}}
- **Returns:** {{returns_policy_line}} Full details are on our [returns page]({{returns_policy_url}}).
- **Help:** Questions go to {{support_email}}, and we usually reply within {{reply_time}}.

One quick question: what brought you to {{store_name}}? Reply with a word or two. It helps us send you more of what you actually want and less of what you don't.

**Button:** Shop the collection | {{store_url}}

> Reminder: if Email 1 carried a welcome offer, you may add one line here: "Your code {{discount_code}} is still good until {{discount_expiry}}." Do not add a new or bigger discount.

Thanks for being here,
{{sender_name}}, {{store_name}}

# Twilio A2P 10DLC — Customer Care Resubmission Kit

Your previous campaign was **denied for "lead generation"** — a prohibited use case on
every US number type (10DLC, toll-free, short code). This kit reframes the program as
**Customer Care** under the Model A "managed fulfillment network" structure (Florence SC
Services is the brand of record; local crews are subcontractors; one lead → one crew).

**Do NOT resubmit until the website changes below are live**, because the reviewer clicks
your opt-in URL and reads your forms, Privacy Policy, and Terms.

---

## 1. What NOT to touch
- **Brand registration** — leave it alone. The denial was the *campaign*, not your Brand.
  (Just confirm Brand status still shows Approved/Verified in the Twilio Console.)

## 2. What to submit — a NEW campaign (the denied one can't be edited)
A rejected campaign can't be reused; create a fresh one. Expect the ~$15 vetting fee +
monthly campaign fee to be charged again, so get it right the first time.

### Use case
**Customer Care** (standard/low-volume standard).

### Campaign description (paste this)
> Florence SC Services is a dumpster rental and junk removal service serving Florence
> County and the Pee Dee region of South Carolina. Customers contact us by submitting a
> quote-request form on our website or by calling us, and they consent to be contacted.
> We send them transactional text messages about their own request: confirmation that we
> received it, the name and number of the local crew handling their job, scheduling and
> delivery/pickup updates, and follow-ups about their inquiry. We do not send marketing
> blasts, and we do not sell or share customer phone numbers with third parties.

### Sample messages (provide 2–3)
1. `Florence SC Services: Thanks, John! Got your request for a 20-yd dumpster in Darlington. William from our local crew (Allwayz) will call you shortly from (843) XXX-XXXX. Questions? Reply here or call (843) 938-0480. Reply STOP to opt out.`
2. `Florence SC Services: Your dumpster is scheduled for drop-off tomorrow (Tue) AM. Reply here with any access notes. Reply STOP to opt out.`
3. `Florence SC Services: Reply HELP for help, STOP to unsubscribe. Msg & data rates may apply.`

### Opt-in details
- **Opt-in type:** Web form + verbal (phone).
- **Opt-in URL (give the reviewer this):** https://florencescservices.com/contact.html
- **Call-to-action / consent wording shown at opt-in** (now live on every lead form):
  > "I agree to receive calls & texts from Florence SC Services about my request. Msg &
  > data rates may apply; frequency varies. Reply STOP to opt out. Privacy Policy & Terms" *(required checkbox)*
- **HELP response:** `Florence SC Services: For help call (843) 938-0480 or email info@florencescservices.com. Reply STOP to unsubscribe.`
- **STOP response:** `You're unsubscribed from Florence SC Services texts. No more messages will be sent. Reply START to opt back in.`

---

## 3. The customer text you'll actually send (when the campaign is approved)
Send on form-submit and on qualifying CallRail calls, from your Twilio number (843) 773-4140:

> **Florence SC Services:** Thanks, {name}! Got your request for {service} in {city}.
> {operator} from our local crew ({company}) will call you shortly from {operator_phone}.
> Questions? Reply here or call (843) 938-0480. Reply STOP to opt out.

Including the crew's name + number **lifts answer rates** (people pick up when they know who's
calling) and reinforces the customer-care framing. Today that's William / Allwayz Dumpster —
the worker will template this so it updates automatically as you assign different crews.

---

## 4. Website changes made for this resubmission (this branch)
- **Consent checkbox** added/standardized on ALL lead forms (contact, homepage dumpster +
  junk, and every city/junk page) — explicit call+text consent, STOP, links to Privacy & Terms.
- **Privacy Policy** (§2, §3, §4) — removed "lead generation services"; reframed to
  customer-care messaging about the customer's own request; kept the required "mobile info
  not shared with third parties for marketing" line.
- **Terms of Service** (§1, §4) — removed "lead generation and quote-request matching
  service"; reframed as coordinated service through local crews (liability language
  preserved: crews provide the service and set pricing); §4 now describes texting
  *customers*, not "home service business owners re lead generation."
- **About page + Kingstree disclaimer** — removed "lead generation / matching service"
  wording; kept the "we don't own the trucks" liability protection.

## 5. STILL TO DO
- **partners.html** — DONE. Reframed from "lead generation business / B2B lead generation"
  to "crew partner network."
- **Operator-recruitment SMS** (texting business owners to recruit them) is itself B2B
  lead-gen and a *separate, also-restricted* use case. Keep operator outreach on **email
  via Resend**, not SMS.
- **Worker code** (`florence-crm-api`) — the customer-SMS send, CallRail Voice Assist
  data extraction (fixes Service="n/a"), and zone detection fix live in the Cloudflare
  Worker, not this repo. Build those next and keep customer-texting OFF behind a flag until
  this campaign is approved.

> Not legal advice. Have counsel review the Terms/Privacy wording before relying on it.

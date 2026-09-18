# ReceptlyAI

AI voice reception sold as a managed service to Australian trade businesses.
He configures nothing. His number stays the same.

**Live:** https://receptlyai.com.au (noindex ON until launch)
**Demo line:** 1300 556 520 — live, Crazytel, forwards into the agent
**Host:** Hostinger Business, server1960 · DNS at Namecheap — do not move nameservers
**Stack:** WordPress + Rank Math + ACF + LiteSpeed. Four plugins, no more.
**Voice:** GoHighLevel sub-account per client
**Email:** Resend on `send.receptlyai.com.au`. Inbound via Google Workspace.
**Entity:** Agentive Group Co Pty Ltd, ABN 54 695 269 222

---

## Docs

| | |
|---|---|
| [pricing.md](docs/pricing.md) | Rate card, margins, publish procedure |
| [au-number.md](docs/au-number.md) | The regulatory findings — Local vs Mobile, and the traps |
| [client-onboarding.md](docs/client-onboarding.md) | Intake form and the bundle runbook |
| [onboarding-n8n-flow.md](docs/onboarding-n8n-flow.md) | Build spec — endpoints, schema, failure handling |
| [track-a-resend.md](docs/track-a-resend.md) | Enquiry email sequence |
| [email-sequences.md](docs/email-sequences.md) | Track A / B / C map |
| [email-and-dns.md](docs/email-and-dns.md) | DNS records, Resend, Workspace |

---

## Rate card

Source of truth is `pricing.py` in the site source. Every page renders from it —
no hard-coded prices anywhere else. If a page and this table disagree,
`pricing.py` wins and the page is wrong.

| | Starter | Crew | Growth |
|---|---|---|---|
| Monthly | $249 | $499 | $795 |
| Setup | $295 | $495 | $695 |
| Yearly | $199/mo, setup free | $415/mo, setup free | $660/mo, setup free |
| Minutes | 400 | 900 | 1,600 |
| Calls (~2.5 min) | ~150 | ~340 | ~600 |
| Overage | 75c/min | 65c/min | 60c/min |
| Who | One van | Two to fifteen vans | 15+ vans or multi-location |

AUD, ex GST. Month to month. Growth is a volume tier — features aren't held back.
Overage promise: told before being moved up, no surprise bills. The rate stays
published on every tier; hiding it would contradict that promise.

Last changed 18 Sep 2026 — minute allowances raised. Published and verified live.

## Numbers

Each client gets an Australian **mobile** (+61 4xx), not a geographic landline.
02/03/07/08 numbers are voice-only, which breaks the text-you-the-details and
job-approval flows.

**Bought directly through GoHighLevel: $8.25/mo, voice and two-way SMS.**
No third-party provider. Earlier notes naming Kudosity / ClickSend / Cellcast at
~$17.50/mo are withdrawn — that was wrong.

Counterintuitively the mobile is also the *lighter* number to provision. For a
business end user, AU Mobile needs a commercial registry record and a business ID
number. AU Local additionally demands a director's photo ID and a proof of address.

GoHighLevel does not sell 1300 numbers — the demo 1300 comes from Crazytel and
forwards in. That layer is deliberate: a client can keep his existing number and
forward it, so nothing on his van or his Google listing changes.

## Regulatory bundles

One Twilio bundle **per client sub-account, in the client's business name**.
Bundles are sub-account-scoped and cannot be shared. AU numbers cannot be moved
between sub-accounts self-serve — GoHighLevel's Move Numbers tool handles US and
Canada only.

**The client supplies an ABN and nothing else.** The ASIC Current Company Extract
is a public document, $10 direct from ASIC Connect (card only, no invoicing).
No photo ID, no utility bill, nothing retained.

Twilio review takes 1–3 business days. Sell it as "live within one business day"
and cover the gap by pointing their number at the shared demo agent meanwhile.

## Architecture

One GoHighLevel sub-account per client, every tier. Not a shared pot — SMS cannot
be attributed to a number anywhere in the GHL API, contact dedup is sub-account-wide
with no sub-scope, and inbound rate-limit violations are account-wide.

Per-client call reporting comes from `/voice-ai/dashboard/call-logs?agentId=`,
keyed to the agent. One agent to one number, never a Number Pool — a pool destroys
attribution.

## Blockers

1. **Stripe is not connected.** Nothing else matters until money can be taken.
2. **Track A and B do not send.** Thirteen emails written; Track A built in Resend
   but not enabled.
3. AU Mobile regulatory bundle in review — then buy the number, swap it onto the
   demo agent, repoint the Crazytel primary, release the US number.
4. Photography of real Australian tradespeople.

## Guardrail

Location and trade pages need genuinely distinct content. If 400 words about a city
would still be true pasted onto another city, that page doesn't get built.

The area-code signal is weaker than it was, but not gone: most clients forward an
existing local number, so those pages can still speak to local numbers honestly.
What they cannot say is "we'll give you a local number".

## Not in this repo yet

The site source — the Python scripts that publish to WordPress — is not in version
control anywhere. It holds the n8n `X-Proxy-Key` and possibly the WordPress
Application Password, so it needs a secrets scan and a move to environment
variables before it can be committed. Until then it exists in one place only.

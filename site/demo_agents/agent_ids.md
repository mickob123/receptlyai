# GHL demo agents (sub-account kdC1Sr39BSgmI9j0Ukrg) — created 20 Sep 2026
| Trade | Agent name | Agent id | Prompt file | Tag |
|---|---|---|---|---|
| Plumbing | Receptly Demo — Plumbing | 6aaf2aa28697821e46c0925e | plumbers.txt | demo-plumbers |
| Electrical | Receptly Demo — Electrical | 6aaf2f088c9c24c645a9bab3 | electricians.txt | demo-electricians |
| Air conditioning | Receptly Demo — Air conditioning | 6aaf2f5ff9736b3d77dc6b9a | air-conditioning.txt | demo-air-conditioning |
| Roofing | Receptly Demo — Roofing | 6aaf2fa060af4d038d17e672 | roofing.txt | demo-roofing |
| Painting | Receptly Demo — Painting | 6aaf2fd760af4d6a0317e682 | painters.txt | demo-painters |
| Pest control | Receptly Demo — Pest control | 6aaf300a60af4d3f8717e697 | pest-control.txt | demo-pest-control |
| Locksmithing | Receptly Demo — Locksmithing | 6aaf303e60af4d0a3417e6aa | locksmiths.txt | demo-locksmiths |
| Landscaping | Receptly Demo — Landscaping | 6aaf30748c9c24982aa9bb0e | landscaping.txt | demo-landscaping |
| Building | Receptly Demo — Building | 6aaf30a7f9736bebeddc6be2 | builders.txt | demo-builders |

GHL dial workflows: "Receptly — Demo call: <Trade>" (tag demo-<trade> → Voice AI outbound from +61 485 066 573). Result: "Receptly — Demo result to n8n" (Transcript Generated, Voice AI) → n8n receptly-demo-result.
Prompts are served from https://receptlyai.com.au/demo_agents/<file> (CORS open) — edit the file, re-upload, re-apply in the GHL builder.
Custom fields on the sub-account: rc_services, rc_hours, rc_afterhours, rc_say (all Contact / Additional Info).
Welcome message (all nine): Hi {{contact.first_name}}, it's Receptly, you asked for a demo. I'll answer as if I'm {{contact.company_name}}'s receptionist and you've just rung in. Have a go at me whenever you're ready.

# /help/ connection guides

Built 30 Sep 2026. Live at https://receptlyai.com.au/help/ (hub, page 466) with seven children: google-calendar 467, outlook 468, servicem8 469, fergus 470, simpro 471, aroflo 472, tradify 473.

- `build_help.py` — all copy and block markup. Edit the copy here, never in WordPress, then republish.
- `publish_help.py` — upserts the hub and guides and sets Rank Math title and description. Needs `wp.py`; see `wp_example.py`.
- `fix_integ.py` — the 30 Sep corrections to the five /integrations/ pages. Kept for the record; it has already run.
- `vendor-emails.md` — the questions sent to Simpro, AroFlo and Tradify.

Facts and sources: project doc `claude/connecting-client-systems.md`.
Keys are handed over via n8n form /form/receptly-connect (workflow "Receptly Client Key Handover"). It saves an n8n credential and posts only the last four characters to Slack.

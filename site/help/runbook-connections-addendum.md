
### 2f. Connect his calendar and job software

The build sheet's **job software** answer tells you which guide to send. Every guide is at **receptlyai.com.au/help/**. Do this on the kick-off call with him, not by email.

- **Never ask for a password, and never ask to be added as a user** in his software. The guides explain why.
- **Google Calendar:** he shares his calendar from his phone with the Receptly calendar address (guide: /help/google-calendar/). Then accept the share and pick his calendar as the Linked Calendar in the sub-account (Settings → Calendars).
- **Outlook / Microsoft 365:** invite him as a user in his sub-account. He logs in once and connects Outlook himself (guide: /help/outlook/).
- **ServiceM8, Fergus, Simpro, AroFlo:**
  - He makes a key or token using the guide.
  - Then he pastes it into **receptlyai.com.au/connect/**, the secure form.
  - #leads gets 🔑 **Connection key received**, showing the last 4 characters only.
  - The key is saved in n8n as a credential named `Client <software> - <business> - <email> - <date>`.
  - Nobody should ever email or text a key. If he does, tell Mick, and ask him to delete that key and make a new one.
- **AroFlo:** his primary contact must ask AroFlo support to switch on APIv2 first. The request text is in project doc `claude/vendor-emails-connections.md`.
- **Fergus:** tokens last a year. #leads gets ⌛ **Fergus token running out** 14 days before. Ring him, he makes a new one and sends it through /connect/, then swap the credential in n8n.
- **Tradify** (Pro or Plus only):
  1. He sets up his Enquiries email address in Tradify (Settings → Enquiries).
  2. In his sub-account, **Settings → Custom Values**, create `tradify_enquiries_email` with that address.
  3. In the workflow **"Receptly - Call to n8n (brain ingest)"**, make sure the webhook's custom data includes `tradify_enquiries` = `{{custom_values.tradify_enquiries_email}}`.

  Every answered call is then emailed there and becomes a Tradify enquiry. Test it with the step 4 calls.

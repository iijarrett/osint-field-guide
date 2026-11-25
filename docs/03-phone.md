<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have an email address](02-email.md) · [Index](../README.md) · [You have a real name →](04-real-name.md)

# 03. You have a phone number

Weaker than an email in most investigations, but it has one property nothing else does: a number is *tied to a legal identity and a physical place* in a way an email never is. It also unlocks the messaging apps, which frequently expose a profile photo and display name to anyone who saves the contact.

| Tool | Tier | Cost and kind |
|---|---|---|
| [PhoneInfoga](#phoneinfoga) | `START` | free · local tool · Go |
| [Messaging-app presence check](#messaging-presence) | `DEEPER` | free · practice · burner device |

<a id="phoneinfoga"></a>
### PhoneInfoga
`START` · free · local tool · Go

Takes a number and establishes the basics — country, carrier, line type (mobile / landline / VoIP) — then runs it through search engines and reputation databases looking for where it's been posted publicly.

*Why line type matters most:* "VoIP" is the single most useful field it returns. A VoIP number means a burner, a Google Voice line, or a service account, and that changes everything about how you read the rest of the investigation. A real carrier mobile means a real person with a real contract. **Status:** its README now calls it stable but unmaintained and warns the repository could be archived; the latest release is 2.11.0. Treat it as frozen — the line-type check still works, but the scanners that call out to other services will drift.

**Install and run**

```sh
# Docker
docker run --rm -it sundowndev/phoneinfoga:latest scan -n "<number>"
# Binary: download the release for your OS from github.com/sundowndev/phoneinfoga/releases
# Web UI
phoneinfoga serve -p 5000
#   (then open http://localhost:5000)
```

Use the international format with the country code, e.g. `+14155550100`. The Docker line is the same on all three systems.

**Links:** [github.com/sundowndev/phoneinfoga](https://github.com/sundowndev/phoneinfoga)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="messaging-presence"></a>
### Messaging-app presence check
`DEEPER` · free · practice · burner device

Save the number as a contact on a burner device or secondary account and see which apps light up — WhatsApp, Signal, Telegram, Viber. Most will show you a profile photo, a display name, and sometimes a status line or last-seen, purely because you have the number.

*Why it works:* contact discovery is a feature, not a bug, and almost nobody locks down the profile photo. A face and a real first name from a bare number is a large pivot. **Telegram in particular** often exposes a username, which drops you straight back into section 01.

> **This one is active, and it can notify.** Saving a contact is passive, but a mistaken tap sends a message or a request the target sees. Use a device and account that are not yours, and understand that some platforms have surfaced "so-and-so joined" notifications to the other party. Never do this from a personal phone.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)

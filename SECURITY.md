# Security policy

## Reporting a vulnerability

If you find a problem in the scripts, workflows or data handling of this repository, please report it privately,
not in a public issue.

- Use GitHub's **Report a vulnerability** button on the Security tab, or
- email **security@jarrettd.com**.

Please include what you found, how to reproduce it and what you think the impact is. Expect an acknowledgement within
a week. This is a small volunteer project; there is no bounty.

## What is in scope

- `scripts/` and `.github/workflows/`: anything that could run attacker-controlled code, leak a token or write to
  the wrong place.
- A listing that points to a malicious, compromised or typosquatted download or domain. Report these promptly:
  they are the highest-risk kind of error in a list like this one.

## What is not

- Vulnerabilities in the third-party tools the guide lists. Report those to the tool's maintainers.
- Disagreement with a tool's inclusion or rating. Open a normal issue.

## How this repository limits its own risk

- The weekly health workflow runs with read access to the code and write access to issues only.
- Install lines avoid piped-to-shell installers so you can read what you run.
- The scripts use only the Python standard library and PyYAML.

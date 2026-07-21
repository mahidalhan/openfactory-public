# Security Policy

OpenFactory contains AI operating instructions rather than a production
service, but unsafe instructions, private-data exposure, prompt injection, and
approval bypasses can still cause real factory harm.

## Report A Vulnerability Privately

Use GitHub's **Security → Report a vulnerability** form for this repository.
Do not publish sensitive findings in an issue, discussion, pull request, or
example file.

If private vulnerability reporting is unavailable, open a non-sensitive issue
asking a maintainer to provide a private route. Do not include exploit details,
credentials, internal addresses, factory data, or identities in that issue.

Include the affected file, impact, safe reproduction outline, and proposed
mitigation. Redact all factory and personal data.

## In Scope

- instructions that reveal or request secrets or private factory data;
- prompt-injection paths that treat imported evidence as agent instructions;
- a skill that bypasses a required human approval;
- financial or operating calculations that silently mix periods, entities,
  currencies, units, or incompatible cost definitions;
- unsafe file-system, shell, network, ERP, camera, or integration examples; and
- supply-chain vulnerabilities in the exact public repository files.

Ordinary calculation disagreements, missing features, and documentation edits
may use the normal issue tracker when they contain no private information.

## Supported Versions

Security fixes apply to the current default branch. Older snapshots are not
supported unless a maintainer explicitly says otherwise.

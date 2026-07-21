# Contributing To OpenFactory

OpenFactory contributions should help a factory owner make a safer, clearer,
and more economically useful decision with the least reliable data required.

## Before You Start

1. Read `README.md` and `.agents/skills/README.md`.
2. Search the ten existing skills before proposing another workflow.
3. Prefer improving or composing an existing skill when the decision, inputs,
   or output already overlap.
4. Discuss any change to the ten-skill membership or shared contract before
   implementing it.

## A Good Factory Skill

Each `SKILL.md` must state:

- the owner question and economic lever;
- when the skill should and should not run;
- minimum inputs and their `as_of` time;
- how sources reconcile and how missing data is represented;
- the decision artifact it produces;
- feasibility, accounting, quality, and confidence checks;
- source-trust and human-approval boundaries;
- handoffs to complementary public skills; and
- a completion standard that can be tested.

Do not generalize one plant, ERP, camera system, or industry practice into a
universal rule. Private integrations belong outside this public repository.

## Privacy, Provenance, And Examples

Only submit synthetic or thoroughly sanitized examples. Do not commit:

- credentials, tokens, passwords, signed URLs, or internal network details;
- real customer, worker, supplier, or factory identifiers;
- private spreadsheet, messaging, ERP, camera, or file-system locations;
- raw factory media, operating exports, or live recommendations;
- unlicensed third-party documents or copied proprietary methods; or
- instructions that ask the agent to bypass its safety or approval rules.

If external material influenced a contribution, retain enough public source
information to verify provenance and license compatibility without copying
protected content.

## Make And Check A Change

1. Edit `.agents/skills/<skill-name>/SKILL.md`.
2. Update `.agents/skills/README.md` only when routing or shared contracts
   change.
3. Add or update tests for the contract being changed.
4. Update `PUBLIC_FILES.txt` if a deliberately approved public file changes.
5. Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Review the complete diff before submission. A passing pattern scan does not
replace a human privacy, provenance, and safety review.

## Pull Request Checklist

- [ ] The owner question and economic outcome are explicit.
- [ ] Minimum inputs, assumptions, source dates, and missing data are visible.
- [ ] Imported content remains untrusted evidence.
- [ ] Consequential actions require human approval.
- [ ] The skill complements the suite instead of duplicating it.
- [ ] Examples are synthetic, portable, and license-compatible.
- [ ] The public allowlist is exact and all tests pass.

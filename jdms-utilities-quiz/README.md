# JDMS Utilities Job Description Quick Quiz

A three-question quiz for utility companies that shows where JDMS can help
build a governed, audit-ready job description library. It follows the same
layout as the JDMS Challenge Finder.

## How it works

1. **What is your role?** HR/People Leader, Talent Acquisition/Recruiting,
   HRIS/SAP SuccessFactors, Compensation & Job Classification, Labor & Employee
   Relations, Safety/Compliance & Risk, Operations/Field Leader, Other.
2. **What is your main goal?** One choice from eight.
3. **What challenges are you facing?** Visitors can select more than one:
   Duty Drift, Safety-Critical Requirements, Defensible Job Posts, Retirement
   Knowledge Loss, New Hybrid Roles, Fragmented Job Architecture, Disconnected
   Technology, Building a Better Foundation. An optional email field sits under
   the choices.

The result leads with the first challenge chosen ("Building a Better
Foundation" leads only when it is the only one), lists the others under "Also
on your radar", shows up to six JDMS feature cards, and links to the
*6 Ways* guide PDF.

## Files

- `index.html` — standalone quiz. Open it in a browser to preview it. This is
  the source of all quiz copy.
- `jdms-utilities-quiz-embed.html` — the paste-in version for websites. Open it
  in a text editor (not a browser), copy everything, and paste it into a
  WordPress **Custom HTML** block (not a Paragraph or Classic block or the
  Visual tab). Link to it on the page with `href="#utility-quiz"`.
- `build/` — rebuilds the embed from `index.html`.

## Editing content

Copy lives in the `jdmsuRoles`, `jdmsuGoals` and `jdmsuChallenges` objects in
the script of `index.html`; question button labels are in its HTML. After
changing the data objects, rebuild the embed from the repo root:

```bash
python3 jdms-utilities-quiz/build/build_embed.py
```

Changes to button labels, layout or styles go in `index.html` and
`build/embed-template.html` by hand, then rebuild.

The embed is written to survive WordPress tidying pasted code, which broke an
earlier version. The build stops with an error if a change would undo that.
Keep these rules when editing the template:

- Every button has `type="button"` and a `data-jdmsu` action; no `onclick`.
- No blank lines anywhere (WordPress turns them into `<p>` tags).
- In the script and style: no `&&`, `<` or `>`, and only `/* */` comments.

## Leads and analytics

- `LEAD_ENDPOINT` at the top of the script is blank, so emails are not sent
  anywhere yet. Set it to a URL that accepts a JSON POST to collect them.
- On completion the quiz reports `jdms_utilities_quiz_completed` with
  `jdms_role`, `jdms_goal`, `jdms_challenge` (comma-separated),
  `jdms_challenge_count`, `jdms_result` and `jdms_email_provided`. The email
  itself is never sent to analytics. It uses the campaign platform's
  `campaign:track` event when the page has one, and `window.dataLayer`
  (Google Tag Manager) otherwise.
- The quiz can share a page with the general JDMS quiz: its IDs and classes
  all start with `jdmsu`.

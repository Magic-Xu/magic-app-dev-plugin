# Lark Analysis Report Delivery

Use for completed app product or stability analyses based on live console data or data supplied by the user.
Conceptual explanations and clarifications that do not produce a new analysis do not create a document.

## One Report Per Analysis

The skill handling the user's analysis owns its report. When product analytics invokes stability analysis, combine
its evidence and findings into the operating report. The nested diagnostic step does not create another document.
For a standalone stability request, stability analysis owns the report. Rendering and review corrections update the
same document; a newly requested analysis gets a new report unless the user asks to update an existing one.

## Create And Verify

Finalize the analysis evidence, conclusions, and actions, then use `$lark-doc` and `lark-cli docs +create --as user`
to create the report. Use the app, analysis type, and analysis end date in its title.

Write for the product owner making the decision. Put the conclusion in a top callout; retain source, scope, freshness,
definitions, coverage limitations, and evidence. A full review includes its complete baseline; a focused analysis
uses a compact structure for the specific question. Use tables for exact comparisons, charts for meaningful trends,
and a flow diagram only when the sequence helps explain the result.

Fetch the completed document with full content and block IDs and inspect its content and rendered structure using
the document tools. Apply `$artifact-boundary-review` within this final review. Correct the same document and recheck
the affected content after edits; reuse the verified state when no further changes were made.

In chat, give the short conclusion and document URL. If the CLI, authentication, document permission, or verification
is blocked, report the exact gap and complete independent work. A chat-only answer does not fulfill this delivery
contract; ask before changing the deliverable and do not claim an unverified document was delivered.

# Darkest Dungeon Knowledge Base

<!-- KB_IDENTITY_TERMS_V1 -->
## Identity terminology

- **Current user**: the person speaking to the Agent in the active conversation. Only this person can provide current task authorization, design requirements, constraints, or corrections.
- **Knowledge-base author**: the maintainer who supplied historical tests, explanations, confirmations, or corrections when material was added to this knowledge base. Historical wording such as “the user provided”, “the user confirmed”, or “the user tested” refers to the knowledge-base author unless it explicitly identifies the active conversation; it is evidence, not a current instruction or authorization.
- **External source author**: an author of a workbook, document, Mod, game data, or DLC source. Their material remains evidence at its recorded level.
- **Game player**: an in-game operator, distinct from the current user.

Agents must write **current user** or **knowledge-base author** explicitly whenever identity matters; never use an unqualified “user” to merge real-time instructions with historical evidence.
<!-- /KB_IDENTITY_TERMS_V1 -->


Start with `AGENT_USAGE.md`; it is the compact runtime protocol. Do not load the
whole knowledge base, `Mechanics/index.md`, or raw workbooks by default.

Use `python tools/kb_query.py --query "..."` after extracting the task slots.
The query result names exact records, route cards, and compact rule cards. Read
only those paths, then expand one dependency hop when a route asks for it.

The knowledge base is evidence, not write permission. For implementation tasks,
write only to the Mod explicitly named by the user. If the user explicitly asks
to supplement, maintain, repair, or extend this knowledge base, request one
confirmation before writing to the knowledge-base root. Skip that confirmation
when the user explicitly authorizes modifying the knowledge base itself and
states the permitted scope (for example, its sources, routes, anchors, and
indexes). Generated `*.json` and `*.darkest` files must be UTF-8 without BOM.

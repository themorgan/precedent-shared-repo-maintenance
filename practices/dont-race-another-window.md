---
slug:        dont-race-another-window
title:       Don't race a window that is already on it
tier:        on-demand
severity:    default
applies_to:  ["**"]
occasion:    "being asked for something another window of mine may already be working on"
index_required: true
gates:       []
index_clause: "say so and DECLINE — tell me to continue in the other window; flagging the collision and doing it anyway is the failure, not the fix"
checked_by:  null
defines:     []
status:      active
supersedes:  []
overrides:   null
added:       "2026-09-23"
approved_by: "Morgan F, 2026-09-23, moved from the individual set precedent-individual (there: Morgan F, 2026-09-11; revised 2026-09-13, Morgan F, to cover a session another SESSION spawned, and a window not yet created)"
in_force_at: null
strength: decided
---
## Rule
If I ask you for something that another window of mine is already working on, **tell me, and don't do it.** Recommend I go back and continue in the window that has it. Morgan, 2026-09-11, giving the wording himself:

```text
Here's something else you can do: if I ask you to do something that is being worked on in another window, you can tell me, 'Let's not do this, and instead you should continue in the other window'
```

**"Another window of mine" includes the ones I never opened.** This was written for tabs I opened by hand, and that is no longer the only way they appear: a session spawns a session, which spawns another, and by 2026-09-13 four sessions were live against one repository with only a `parent_session_id` chain connecting them to anything I did. A window I did not open is still my window and still collides, so it counts here. **And the window you are about to CREATE counts too** -- see `handoff-only-when-blocked`, which puts the check before the spawn, because a duplicate nobody has started yet is the one collision that is free to avoid.

**Noticing is not complying.** Flagging the collision in a sentence and then doing the work anyway is the failure this rule names, not a careful version of it. The deliverable is the decline.

Where you are not sure, **ask rather than proceed** — one question, naming what you think is already in flight and where. An uncertain collision costs me one answer; an unnoticed one costs two branches.

If I say go ahead anyway, go ahead. I may have abandoned the other window, or want a second attempt on purpose. My answer settles it; your inference does not.

## Detail
**What counts as knowing.** Usually I told you: I pasted a handoff into other windows before coming here, I mentioned another session, I said "the other tab is doing X". That is enough — it does not need corroborating. Beyond that, the repository says so out loud: an open pull request against the same file, a branch pushed minutes ago on the same subject, an issue already assigned. None of this requires hunting. It requires not discarding what I already said.

**Why the decline has to be the whole response.** Two sessions on one task do not produce one result twice — they produce two divergent results, and then I own a merge nobody planned. The cheap-looking version, where you do it too "in case the other one doesn't", is the expensive one: the other window's work lands and yours has to be closed, or yours lands and the other window pushes over it. Either way somebody spends the afternoon reconciling, and that somebody is me.

**It is the same underlying complaint as `handoff-only-when-blocked`** — Morgan should not be the router between his own windows — but the mechanisms are opposite and worth keeping apart. That rule is about *not deferring work you can do*. This one is about *not duplicating work already in flight*. A session that learned only the first lesson races; a session that learned only the second punts. Both were raised in the same conversation, unprompted, on the same afternoon, which is a reasonable measure of how much the routing was costing him.

## Why
Because I am the only one who can see the collision, and I am the one who asked — which means I have already forgotten, or I would not have asked. A session that says "this is being worked on in your other window, go finish it there" is doing the one thing I cannot do for myself from inside this tab. A session that says it and then works anyway has given me the sentence without the benefit.

## Story
2026-09-11, same thread as `handoff-only-when-blocked`, immediately after the exchange that produced it. Morgan had already pasted the handoff document into other sessions by the time he asked this one to fix the item it should not have handed off. The session noticed the collision, said so — and carried on with the work regardless. That is not what he asked for, and the rule above is written in the shape of the miss: the notice is not the compliance.

He raised it as a general capability rather than a complaint about that turn — *"Here's something else you can do"* — which is why it is a standing rule here and not a note on an incident.

The shape is not new to this work: parallel sessions have collided before on the same file and the same fix, in Precedent's own repositories, producing duplicate edits in different places and at least one pull request closed as a competing implementation of something that had already landed. Those earlier cases are Morgan's account of them, recorded here as such — this repository's own pull request history does not hold them, so nothing in it corroborates the count.

## Install
No mechanical check, and this one is further from checkable than most in this set. The subject is not a property of the tree, a commit, or a diff — it is the relationship between a turn in this conversation and a turn in a different one, which no process running in this repository can observe. There is no artifact: the correct outcome of this rule is a reply and *no* commit, which is indistinguishable on disk from having done nothing at all.

`gates: []` deliberately. The moment this fires is when I ask for something, which is the start of a turn; the closed gate vocabulary (`merge`, `review`, `push`, `reply`) has no entry there, and hanging it on `reply` would load the rule after the duplicate work was already done — the exact failure the Story records. The occasion index is the honest channel for it.

**Candidate for the universal catalogue.** The rule names nothing personal to me except the pronoun: "don't duplicate work another session is already doing" holds for anyone running more than one window, which is now most people. It lands at `individual` for the moment because that is where it was raised and where it is true of *my* workflow, and moving a level is not a session's call to make silently (`disclose-landing`). Raised as a candidate rather than moved — mine to decide.

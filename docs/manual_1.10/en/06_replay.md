# Replay: watching the recording as an animation

> User Manual → Chapter "Review a recording" → new section "Replay" (after "PDF report").

When you open a **muscle**, **heart** or **eye** recording, the **▶ Replay**
button becomes available (it stays disabled for brain recordings). It opens a
window with a player shared by the three exams: **▶ Play / ⏸ Pause**,
**⏮ Start**, the draggable timeline and the clock "0:05 / 0:30". In Complete
there is also the speed (0.25× to 4×) and *Repeat*.

> The animation **simulates** what was recorded: it is not a video of the
> person, and it is not a report or a diagnosis. The seal at the top of the
> window repeats this.

## Muscles

An articulated figure seen from the side (trunk, shoulder, elbow, forearm,
wrist, hand with fingers) reproduces the **movement marked** on the timeline,
and each muscle lights up with the intensity measured at that instant.
Supination and pronation are unmistakable: the light palm turned up or the
back of the hand turned down, with the text "palm up/down".

The timeline (2 to 4 tracks) is born from the recording's **markers and
phases** ("Flexion", "Extension", "Rest"…); without markers, the **detected
contractions** become "to be defined" segments. Tracks at the same instant
**add up** (for example, closing the hand while the elbow flexes). Available
movements: elbow flexion and extension, supination, pronation, wrist flexion
and extension, opening and closing the hand, pinch, shoulder flexion and
extension, rest.

In **Simple** you see the player, the figure and the list of segments. In
**Complete** the timeline is editable: drag a block to move it, pull its
edge to stretch it, right-click for *Change movement*, *Split here*,
*Delete*, *Add track/Remove track*; Ctrl+Z undoes. *Ready-made task* inserts,
from the cursor on, a sequence with the object held in the hand: **lift the
dumbbell**, **open/close the door with the key**, **pick up the cup from the
table and bring it to the mouth**. When the active muscles do not match the
chosen movement (for example, an active triceps in a flexion segment), a
warning appears. *Save* writes `movimentos.json` next to the recording; the
program asks about unsaved marks when closing.

## Heart

A drawn heart **beats at the recorded rhythm**, next to the trace with the
cursor and the beats per minute. The strip below shows **all** the beats: a
regular one is a thin line; an **early beat** is an orange triangle; a
**longer pause** is a hollow red rectangle (color and shape, for people who
do not distinguish colors). The list in words ("0:13 early beat", "0:25
longer pause (1.7 s)") is clickable and takes the player there. The beats are
the same as in the PDF report. In Complete, right-clicking the strip lets you
**correct** (remove beat, add beat here, mark as regular / early / longer
pause); *Save* writes `batidas.json`.

## Eyes

Two drawn eyes **blink on the blinks and look** where the signals say. *Flip
horizontal* and *Flip vertical* swap the sides, in case the electrodes were
placed the other way round. The timeline says in words what happened ("0:03
blinked", "0:05 looked right") and the counters add up blinks and movements
to the sides and up/down. In Complete, right-clicking the list removes an
event or changes its direction; *Save* writes `olhos.json`.

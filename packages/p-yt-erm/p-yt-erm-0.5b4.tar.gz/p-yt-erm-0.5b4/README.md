# pYTerm 0.4

pYTerm is a simple command line youtube music player using python 3.
 This is still currently under heavy development and features are subject to being changed and things being added.
 Bugs *will* happen.
---

## Requirements
* VLC media player installed
* All libraries from `requirements.txt` if using the source code instead of the pip package.
* Paitence
---

## Playback controls

```text
[v]olume, [s]kip, [prev]ious, [p]ause, [m]ove, [t]imestamp, [g]oto, [e]xit
```

When in the player is active you can control it via typing in the command letters above to do the function shown with them.
A few examples are below.

In this example the volume is changed by entering `v <volume percent wanted>`

```text
Controls: [v]olume,[s]kip,[prev]ious,[p]ause,[m]ove,[t]imestamp,[g]oto,[e]xit
playing [1/1] "STAR SHOPPING (Instrumental)" by Theolonius Kelly - Topic [02:11]
v 75
```

In this example the player head is moved by entering `g <± seconds to move>`
```text
Controls: [v]olume,[s]kip,[prev]ious,[p]ause,[m]ove,[t]imestamp,[g]oto,[e]xit
playing [1/1] "STAR SHOPPING (Instrumental)" by Theolonius Kelly - Topic [02:11]
g -10
```
---
## Using pYTrerm as a library

**ALL LIBRARY FUNCTIONS AND CLASSES ARE STILL UNDERDEVELOPENT AND MAY NOT WORK OR BEHAVIORS MAY CHANGE.**

pYTerm is able to be imported as a library how you would with any other python library:
```py
#!/usr/bin/python3
from pYTerm import pYTerm
```
The next thing to do is to make a player object and you are ready to use the methods ~~when they are working~~.
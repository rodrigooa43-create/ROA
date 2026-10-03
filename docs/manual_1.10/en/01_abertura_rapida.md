# Opening the program (splash screen)

> User Manual → Chapter "Installation and first run" → after "Opening the program".

When ROA opens, a small screen appears with the logo and a signal line
drawing itself. Below it, in words, the program says what it is doing
("Loading the libraries…", "Building the home screen…"). This screen goes
away on its own as soon as the home screen is ready; nothing needs to be
clicked.

**First opening after installing or updating.** The program is prepared
once (the screen says "Preparing the program for the first time…") and keeps
the result in the `.roa_cache` folder, next to the program. The following
times, opening is much faster. If the program folder does not allow writing
(for example, in `Program Files`), the cache goes to the user folder
(`%LOCALAPPDATA%\ROA\cache`). Deleting this folder causes no problem: it is
rebuilt the next time the program opens.

**If the splash screen gets in the way** (for example, in an automation or on
a computer with video problems), open the program with the `--sem-splash`
option or set the environment variable `ROA_SEM_SPLASH=1`.

**Updates.** In *Help → Check for updates* the program keeps downloading only
its own code, never sending your data. Starting with this version it can also
update the launcher (`EEG_Data_Collector.py`) when the update brings a new
version of it; if it cannot, it warns you and the program keeps working with
the current launcher.

# pydses

PYDSES (Python Dark Souls Event Scripting)

Python wrappers for easier Dark Souls EMEVD event scripting (in unpacked form)
which can then be packed using HotPocketRemix's DS Event Scripting tools.

NOTES

  - An event in the EMEVD is a sequence of instruction calls, most of which
    take at least one argument. These instructions interface with essentially
    every part of the game's data, and appear to have been written solely to
    serve whatever purpose FROM needed to fulfil at the time. Many instructions
    that you might consider very basic (e.g. moving the player forward by
    10 distance units) are not present simply because they never occur in the
    game. On the other hand, some instructions described in the EMEFD file (the
    guide accidentally provided by FROM) are never used at all. (These are not
    included here.)
    
    - Each map (`m10_00`, `m10_01`, ..., `m18_01`) has its own EMEVD script, which is
    reloaded every time the player dies, just like the Map Studio `.msb` files
    (and unlike the `.param` files, which are loaded only once on game launch).
    When you load the map, it automatically initializes (i.e. runs) Event `0` and
    Event `50`, which in turn initialize all of the other events defined in the
    EMEVD anywhere. Some events take arguments, which are substituted into that
    event's instructions using raw byte offsets (see below). The same event can
    be initialized multiple times with different arguments by assigning it a
    unique slot number. Event `50` mostly deals with NPC logic, and Event `0` with
    everything else. Event `50` is technically called the pre-constructor and
    Event `0` is the constructor, but I don't know what the actual difference is.
    
    - Events are initialized with a type integer of 0, 1, or 2, which determines
    when they restart. Events of type 0 will only run once per map load; you will
    have to die or quit the game to restart these scripts. (I'm not sure what 
    happens if you run far enough away for the map to de-load and reload.) Events 
    of type 1 will restart if you rest at a bonfire. I'm not sure exactly when
    events of type 2 restart, but I believe the game uses them exclusively to
    handle logic related to re-assembling skeletons.
    
    - Events generally spend most of their time waiting for the event's MAIN 
    register to be evaluated True. A large number of instructions exist just to 
    add certain in-game conditions to the MAIN register, or to AND/OR registers
    that can in turn be added to the MAIN register. An event will only proceed
    from one instruction to the next if the MAIN register is True (which it is
    by default if you leave it alone). They also use a lot of conditional line
    skips to effectively construct if/elif/else loops (which unfortunately I
    haven't yet wrapped into something prettier). Similarly, an event will
    sometimes terminate or restart itself early.
    
    - When an Event terminates, it silently and automatically sets the Event
    Flag ID of the same number to True. This occurs when an event ends naturally
    by reaching the end of its script, or when it is terminated by an end
    instruction. It does NOT occur when an event restarts itself - if an event
    needs to enable its corresponding flag in this case, it will do so explicitly.
    
    - If you want an event to run exactly once per character, standard procedure
    is to set up a conditional at the start of the event to check if it has run
    before. This is usually done by checking "Event ID `0`", which refers to itself
    (or specifically, the Event Flag with the same ID as itself). You could also
    explicitly check the Event Flag ID to accomplish the same thing in a more
    hard-coded way. I have abbreviated functions, `skip_if_this_event_off` etc.,
    to do this check for you. Note that Event IDs are not checked for any other
    reason - make sure you check Event *Flag* IDs for general event cross-talk.
    
    - IMPORTANT: *** NOT ALL EVENT FLAG IDs ARE VALID IN THE GAME. *** 
    If you write a custom event with ID `81029523`, the event will function as 
    normal, but it will NOT enable the corresponding flag when it finishes. 
    Only certain ranges of Event Flag IDs appear to be defined in the game, and
    any use of a flag outside this range will silently fail and your events
    will seem to be ignoring one another. (I'm not sure if illegal flags are
    technically False, or undefined.) Eight-digit event flags defined by their
    map number (`1100....`, `1101....`, and so on) are fine, as are eight-digit
    flags starting with `51`, `61`, and `71` but I can't be certain what else is 
    allowed. I recommend sticking to the format for the map EMEVD you are 
    editing, which means you have to make sure that event ID isn't already being 
    used. Note that some events will manipulate flags that do not correspond to 
    an Event ID, so just checking the list initialized in Event `0` is not enough.
    
    - Whenever these instructions refer to an entity in the game, they use its
    EventEntityID. You can find these IDs in the .msb file for that map, and
    they all follow particular naming patterns. If you have multiple entities
    with the same EventEntityID, any instruction you run using that ID will
    affect both of those entities (but I'm not sure if this technique is fully
    safe and do NOT recommend it).
    
    - My Python functions generate "unpacked EMEVD" code for use with
    HotPocketRemix's DS Event Scripting system. The primary purpose of doing
    this is to give the instructions proper names, rather than the numeric
    codes used in FROM. HotPocketRemix has provided a tool to convert packed or
    unpacked EMEVDs into a "verbose" form, which is useful for inspection but
    cannot be edited and converted back into unpacked/packed numeric form. My
    aim was to fill that hole.
    
    - You will need to make sure your event is initialized in Event `0` or Event
    `50` (conventionally at the top of the file). It's generally safe to do this
    anywhere, but the earlier, the better - sometimes these pre/constructor
    events terminate themselves earlier to conditionally skip several event
    initializations at the end (e.g. if the area boss is already dead).
    
    - If it wasn't clear from above: you'll need HotPocketRemix's tools to
    convert the unpacked EMEVDS generated by these functions into useable
    packed EMEVDs to put in your `DATA\event\` folder. I recommend creating a
    folder of unpacked EMEVDs (one per map) to edit using this interface and
    writing a simple script that will run all of those files through HPR's 
    unpacked->packed converter to automatically replace the files in `DATA\event\`
    with a single click. I'll upload my own `.bat` file for doing this at some point.
    
    - I have changed the order of the arguments in some instructions to an
    order that feels more intuitive to me. I have also provided many additional
    functions that fill in the arguments for a common usage. `make_NPC_friendly`
    and `make_NPC_hostile`, for example, each just call `switch_allegiance` with
    the appropriate team type parameter. All of these reduced versions of the
    functions are defined above the wrapper on the original instruction.
    
    - As discussed above, some events are initialized with arguments, which are
    substituted into instructions during the event. Unfortunately, these 
    arguments are passed to the event as packed data (including integers, bools,
    shorts, and floats) and are substituted using explicit byte offsets. In
    HPR's unpacked EMEVDs, these instruction substitution commands occur 
    immediately after the relevant instruction. It would be nice to have a
    quality wrapper around this entire process, but for now, I have a straight
    wrapper for writing these lines in `load_arg` at the bottom of this module.
    You will need to know the combined data formats passed to the event, which
    are specified in its initialization command, in order to figure out what
    bytes you want to subtitute into the instruction. (You also need to know
    the byte index in the instruction itself.) Make sure the instruction
    commands you want to overwrite are set to 0 in the instruction line itself.
    
    - I can't help you much further here beyond *strongly* recommending that
    you read the unpacked verbose EMEVDs (already provided in HPR's repository
    below) and watch HPR's tutorial videos on working with EMEVDs - which this
    module will hopefully speed up a little.
    
    https://github.com/HotPocketRemix/DSEventScriptTools/
    https://www.youtube.com/watch?v=QXpqNNZBKoU
    
    You can reach me (chara) and HotPocketRemix on the #modding Discord chat in
    the SpeedSouls group, or message me here or on Reddit (grim_rhapsody).

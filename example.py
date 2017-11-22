# -*- coding: utf-8 -*-
"""
@author: grimrhapsody
"""

import pydses.event_writer as p
from pydses.event_enums import *

AsylumDemon = 1810800
BossDeathSoundEffect = 777777777
AsylumDemonFogGate = 1811990
AsylumDemonFogSFX = 1811991
AsylumDemonFrontDoor = 1811111
AsylumDemonFrontDoor_AnimID = 1
Portcullis = 1811115
Portcullis_AnimID = 1
EventFlag_AsylumDemonIsDead = 16
EventFlag_PortcullisHasClosed = 11810312


def e11810001():
    
    # Asylum Demon death event.

    p.event(11810001, 0)  # Event header.
    p.if_entity_health_less_than_or_equal(CONT, AsylumDemon, 0.0)
    p.play_sound_effect(AsylumDemon, sound_type.s_sfx, BossDeathSoundEffect)
    p.if_entity_dead(CONT, AsylumDemon)  # Only continue if Asylum Demon is dead.
    p.set_event_flag(EventFlag_AsylumDemonIsDead, True)
    p.kill_boss(AsylumDemon)
    p.disable_object(AsylumDemonFogGate)
    p.delete_map_sfx(AsylumDemonFogSFX, True)
    p.force_animation(AsylumDemonFrontDoor, AsylumDemonFrontDoor_AnimID, False, False, False)
    p.skip_if_event_flag_off(1, flag_type.event_flag, EventFlag_PortcullisHasClosed)
    p.force_animation(Portcullis, Portcullis_AnimID, False, False, False)
    p.disable_object_activation(AsylumDemonFrontDoor, -1)


if __name__ == '__main__':
    
    e11810001()                             # Print unpacked EMEVD to console.
    event_script = p.as_string(e11810001)   # Pass unpacked EMEVD to a string.
    print(event_script)                     # Same as just calling the event function.
    p.verbose(e11810001)                    # Writes to temp.verbose.txt, then opens and prints it.

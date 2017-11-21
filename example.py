# -*- coding: utf-8 -*-
"""
@author: grimrhapsody
"""
import pydses as p

AsylumDemon = 1810800
BossDeathSoundEffect = 777777777
AsylumDemonFogGate = 1811990
AsylumDemonFogSFX = 1811991
AsylumDemonFrontDoor = 1811111
Portcullis = 1811115
EventFlag_AsylumDemonIsDead = 16
EventFlag_PortcullisHasClosed = 11810312

def e11810001():
    
    # Asylum Demon death event.
    
    p.event(11810001, 0) # Event header.
    p.if_entity_health_less_than_or_equal(0, AsylumDemon, 0.0)
    p.play_sound_effect(AsylumDemon, 5, BossDeathSoundEffect)
    p.if_entity_dead(0, AsylumDemon)
    p.set_event_flag(EventFlag_AsylumDemonIsDead, 1)
    p.kill_boss(AsylumDemon)
    p.disable_object(AsylumDemonFogGate)
    p.delete_map_sfx(AsylumDemonFogSFX, 1)
    p.force_animation(AsylumDemonFrontDoor, 1, 0, 0, 0)
    p.skip_if_event_flag_off(1, 0, EventFlag_PortcullisHasClosed)
    p.force_animation(Portcullis, 1, 0, 0, 0)
    p.disable_object_activation(AsylumDemonFrontDoor, -1)

if __name__ == '__main__':
    
    e11810001()                             # Print unpacked EMEVD to console.
    event_script = p.as_string(e11810001)   # Pass unpacked EMEVD to a string.
    print(event_script)                     # Same as just calling the event function.
    p.verbose(e11810001)                    # Writes to temp.verbose.txt, then opens and prints it.

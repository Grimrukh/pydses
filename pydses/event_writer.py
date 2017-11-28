"""
author: grimrhapsody
"""

import io
import subprocess
from .event_enums import *
from contextlib import redirect_stdout

PYTHON_27 = 'C:\\python27\\python.exe'                      # Your Python 2 executable
REBUILDER = 'C:\\HotPocketRemix\\emevd_rebuilder.py'        # HPR's EMEVD rebuilder script
UNPACKED_EMEVDS = 'C:\\HotPocketRemix\\UnpackedEMEVD'       # Folder containing unpacked EMEVD files to modify and pack


def set_python2(path):
    # Specify your Python 2 executable path.
    global PYTHON_27
    PYTHON_27 = path


def set_rebuilder(path):
    # Specify the path of HPR's EMEVD rebuilder.
    global REBUILDER
    REBUILDER = path


def set_unpacked_emevds(path):
    # Specify the path of the *folder* containing the unpacked EMEVDs you want to use as templates.
    global UNPACKED_EMEVDS
    UNPACKED_EMEVDS = path


""" INTERFACE FUNCTIONS """


def pack_event(event_functions: list):
    """ Pack (or 'compile') your custom event functions using template symbols in the unpacked EMEVDs.

    This function will interpret your pydses events (such as `e11810001` in example.py) one by one as strings, and
    attempt to write those strings to template symbols (such as `<11810001>`) in unpacked EMEVD files.

    If a template is not found, it will check if there is an existing event with an ID that matches the ID of your
    event and ask if you want to overwrite that event with a template for your new custom event. The old event will be
    erased (don't worry, you can re-inspect it in a fresh EMEVD file), so make sure your event has superseded the role
    of the old one. Do NOT overwrite existing IDs with unrelated events unless you are incredibly (unreasonably)
    confident that you have accounted for all references to the event flag with the same ID across the entire game data.

    If there is no existing event, it will ask if you want to create a new template at the bottom of the file. (It
    doesn't matter what order the events are defined in the EMEVD.) If you do, it will then ask if you want to create
    an Initialize instruction for that event (and any arguments) below the <INIT0> symbol in Event 0 (such as
    <INIT11810001>) in Event 0, which you will need to insert yourself. You can place this INIT symbol wherever you
    want in the EMEVD (e.g. in Event 50 for NPC logic, or more rarely, nested inside another event) by manually editing
    the unpacked file.

    After all event functions have been substituted, any remaining templates will be brought to your attention for
    optional deletion. If you don't delete them, the markers will simply be ignored for this pack.

    :list event_functions:
    :return:
    """



def unpacked_to_verbose(unpacked_filename, output_file):
    """ Run HotPocketRemix's code to convert an unpacked EMEVD (non-verbose) to
    packed EMEVD files that can be placed in DATA\event\.

    HPR's code will throw its own useful errors if your EMEVD is wrong in any
    way - including extra whitespace.

    This is intended only as an example method to quickly convert any events
    you write with pydses - you can probably come up with your own better way.

    You can specify your Python 2 exe and EMEVD rebuilder with set_python2() and
    set_rebuilder() above.
    """
    global PYTHON_27
    global REBUILDER
    command = '{} {} -p {} -v -o {}' \
        .format(PYTHON_27, REBUILDER, unpacked_filename, output_file)
    subprocess.run(command)


def verbose(event_function, *args):
    """ Convert an event function you've written (and its arguments) to a
    temporary verbose EMEVD file, which is then printed for inspection.
    """
    with open('temp.unpack.txt', 'w') as file:
        with redirect_stdout(file):
            event_function(*args)
    unpacked_to_verbose('temp.unpack.txt', 'temp.verbose.txt')
    with open('temp.verbose.txt', 'r') as file:
        print('\n' + file.read())


def as_string(event_function):
    """ Load formatted event into a string variable.
    """
    with redirect_stdout(io.StringIO()) as new_stdout:
        event_function()
        new_stdout.seek(0)
        return new_stdout.read()


def DEBUG_PENDANT():
    """ A simple instruction call you can use that awards the Pendant item to the
    player. I use it as a quick debug flag now and then.
    """
    return award_item_lot(2070)


""" PRIVATE HELPER FUNCTIONS """


def __format_event(event_format, *args):
    args = list(args)
    for x in range(len(args)):
        if isinstance(args[x], Enum):
            args[x] = args[x].value

    print(' {}[{}] ({}){}'.format(*event_format, args))


def __bint(bool_value):
    return 1 if bool_value else 0


""" EVENT HEADER """


def event(event_id, restart_type):
    """ restart_type:
        0: Event will run once on map load.
        1: Event will run again if you rest at a bonfire.
        2: Unknown - only used for reassembling skeletons.
    """
    print('{}, {}'.format(event_id, restart_type))


""" 2000: SYSTEM """


# 0
def initialize_event(event_id, *event_args):
    # Initializes event_id in slot 0 with event_args.
    # TODO: Fill out event_id to eight digits.
    return initialize_event_with_slot(0, event_id, *event_args)


def initialize_event_with_slot(event_slot_number, event_id, *event_args):
    # Initializes event_id in event_slot_number (used to distinguish
    # copies of the same event) and passes a variable number of args
    # depending on the event.
    # TODO: Check validity of arguments here.
    # TODO: Fill out event_id to eight digits.
    event_format = ['2000', '00', 'iII']
    if not event_args: event_args = (0)
    return __format_event(event_format, event_slot_number, event_id, *event_args)


# 2
def set_network_sync(network_sync_state):
    event_format = ['2000', '02', 'B']
    return __format_event(event_format, __bint(network_sync_state))


def disable_network_sync():
    return set_network_sync(0)


def enable_network_sync():
    return set_network_sync(1)


# 4
def issue_prefetch_request(request_id):
    event_format = ['2000', '04', 'I']
    return __format_event(event_format, request_id)


# 5
def save_request():
    group = '2000'
    index = '05'
    arg_format = 'B'
    return __format_event(group, index, arg_format, 0)


""" 2002: CUTSCENES """


# 2
def play_cutscene_and_warp_player(cutscene_id, playback_method, point_entity_id, area_id, block_id):
    event_format = ['2002', '02', 'iIiBB']
    return __format_event(event_format, cutscene_id, playback_method, point_entity_id, area_id, block_id)


# 3
def play_cutscene_to_player(cutscene_id, playback_method, player_entity_id):
    event_format = ['2002', '03', 'iIi']
    return __format_event(event_format, cutscene_id, playback_method, player_entity_id)


# 4
def play_cutscene_and_warp_specific_player(cutscene_id, playback_method, point_entity_id, area_id, block_id,
                                           player_entity_id):
    event_format = ['2002', '04', 'iIiBBi']
    return __format_event(event_format, cutscene_id, playback_method, point_entity_id, area_id, block_id,
                          player_entity_id)


# 5
def play_cutscene_and_rotate_player(cutscene_id, playback_method, axis_x, axis_z, rotation, translation_y,
                                    player_entity_id):
    event_format = ['2002', '05', 'iIffifi']
    return __format_event(event_format, cutscene_id, playback_method, axis_x, axis_z, rotation, translation_y,
                          player_entity_id)


""" 2003: EVENT """


# 1
def animation_playback_request(entity_id, animation_id, loop, wait_for_completion):
    event_format = ['2003', '01', 'iiBB']
    return __format_event(event_format, entity_id, animation_id, __bint(loop), __bint(wait_for_completion))


# 2
def enable_event_flag(event_flag_id):
    return set_event_flag(event_flag_id, 1)


def disable_event_flag(event_flag_id):
    return set_event_flag(event_flag_id, 0)


def set_event_flag(event_flag_id, desired_state):
    event_format = ['2003', '02', 'iB']
    return __format_event(event_format, event_flag_id, __bint(desired_state))


# 3
def enable_spawner(entity_id):
    return set_spawner_state(entity_id, 1)


def disable_spawner(entity_id):
    return set_spawner_state(entity_id, 0)


def set_spawner_state(entity_id, desired_state):
    event_format = ['2003', '03', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 4
def award_item_lot(item_lot_id):
    # Directly gives to player (pops up on screen).
    event_format = ['2003', '04', 'i']
    return __format_event(event_format, item_lot_id)


# 5
def shoot_projectile(owner_entity_id, projectile_entity_id, damipoly_id, behavior_id, launch_angle_x, launch_angle_y,
                     launch_angle_z):
    event_format = ['2003', '05', 'iiiiiii']
    return __format_event(event_format, owner_entity_id, projectile_entity_id, damipoly_id, behavior_id, launch_angle_x,
                          launch_angle_y, launch_angle_z)


# 8
def restart_event_id(event_id):
    return set_event_id_state_with_slot(event_id, 0, 1)


def cancel_event_id(event_id):
    return set_event_id_state_with_slot(event_id, 0, 0)


def restart_event_id_with_slot(event_id, event_slot_id):
    return set_event_id_state_with_slot(event_id, event_slot_id, 1)


def cancel_event_id_with_slot(event_id, event_slot_id):
    return set_event_id_state_with_slot(event_id, event_slot_id, 0)


def set_event_id_state_with_slot(event_id, event_slot_id, desired_state):
    event_format = ['2003', '08', 'iiB']
    return __format_event(event_format, event_id, event_slot_id, __bint(desired_state))


# 11
def enable_boss_health_bar(entity_id, name_id):
    return set_boss_health_bar_with_slot(1, entity_id, 0, name_id)


def disable_boss_health_bar(entity_id, name_id):
    return set_boss_health_bar_with_slot(0, entity_id, 0, name_id)


def enable_boss_health_bar_with_slot(entity_id, slot_number, name_id):
    return set_boss_health_bar_with_slot(1, entity_id, slot_number, name_id)


def disable_boss_health_bar_with_slot(entity_id, slot_number, name_id):
    return set_boss_health_bar_with_slot(0, entity_id, slot_number, name_id)


def set_boss_health_bar_with_slot(desired_state, entity_id, slot_number, name_id):
    # Note: slot number can only be 0 (bottom) or 1 (top).
    event_format = ['2003', '11', 'bihh']
    return __format_event(event_format, desired_state, entity_id, slot_number, name_id)


# 12
def kill_boss(entity_id):
    event_format = ['2003', '12', 'i']
    return __format_event(event_format, entity_id)


# 13
def modify_navmesh_collision_bitflags(entity_id, navimesh_collision_bit, modification_type):
    # Modification type: 0 = add, 1 = delete, 2 = invert
    event_format = ['2003', '13', 'iIB']
    return __format_event(event_format, entity_id, navimesh_collision_bit, modification_type)


# 14
def warp_player(area_id, block_id, area_entity_id):
    event_format = ['2003', '14', 'BBi']
    return __format_event(event_format, area_id, block_id, area_entity_id)


# 16
def trigger_multiplayer_event(multiplayer_event_id):
    event_format = ['2003', '16', 'i']
    return __format_event(event_format, multiplayer_event_id)


# 17
def randomly_enable_one_flag_in_range(start_event_flag_id, end_event_flag_id):
    return randomly_set_one_flag_in_range(start_event_flag_id, end_event_flag_id, 1)


def randomly_disable_one_flag_in_range(start_event_flag_id, end_event_flag_id):
    return randomly_set_one_flag_in_range(start_event_flag_id, end_event_flag_id, 0)


def randomly_set_one_flag_in_range(start_event_flag_id, end_event_flag_id, desired_state):
    event_format = ['2003', '17', 'IIB']
    return __format_event(event_format, start_event_flag_id, end_event_flag_id, __bint(desired_state))


# 18
def force_animation(entity_id, animation_id, loop, wait_for_completion, do_not_wait_for_transition):
    event_format = ['2003', '18', 'iiBBB']
    return __format_event(event_format, entity_id, animation_id, __bint(loop), __bint(wait_for_completion), __bint(do_not_wait_for_transition))


# 19
def set_area_texture_parambank_slot_index(area_id, texture_parambank_slot_index):
    event_format = ['2003', '19', 'hh']
    return __format_event(event_format, area_id, texture_parambank_slot_index)


# 21
def increment_ngplus_counter():
    event_format = ['2003', '21', 'B']
    return __format_event(event_format, 0)


# 22
def enable_all_flags_in_range(start_event_flag_id, end_event_flag_id):
    return set_all_flags_in_range(start_event_flag_id, end_event_flag_id, 1)


def disable_all_flags_in_range(start_event_flag_id, end_event_flag_id):
    return set_all_flags_in_range(start_event_flag_id, end_event_flag_id, 0)


def set_all_flags_in_range(start_event_flag_id, end_event_flag_id, desired_state):
    event_format = ['2003', '22', 'iiB']
    return __format_event(event_format, start_event_flag_id, end_event_flag_id, desired_state)


# 23
def set_player_respawn_point(respawn_point_id):
    event_format = ['2003', '23', 'i']
    return __format_event(event_format, respawn_point_id)


# 24
def remove_items_from_player(item_type, item_id, quantity):
    # Quantity may be broken (always removes all).
    event_format = ['2003', '24', 'iii']
    return __format_event(event_format, item_type, item_id, quantity)


# 25
def place_NPC_summon_sign(sign_type, entity_id, summon_point, summon_event_flag_id, dismissal_event_flag_id):
    event_format = ['2003', '25', 'iiiii']
    return __format_event(event_format, sign_type, entity_id, summon_point, summon_event_flag_id,
                          dismissal_event_flag_id)


# 26
def set_tip_message_visibility(entity_id, desired_state):
    event_format = ['2003', '26', 'iB']
    return __format_event(event_format, entity_id, desired_state)


# 28
def award_achievement(achievement_id):
    event_format = ['2003', '28', 'i']
    return __format_event(event_format, achievement_id)


# 30
def set_vagrant_spawning(desired_state):
    # 1 = disable
    event_format = ['2003', '30', 'B']
    return __format_event(event_format, desired_state)


# 31
def increment_event_value(event_flag_id, number_bits, max_value):
    event_format = ['2003', '31', 'iII']
    return __format_event(event_format, event_flag_id, number_bits, max_value)


# 32
def clear_event_value(event_flag_id, number_bits):
    event_format = ['2003', '32', 'iI']
    return __format_event(event_format, event_flag_id, number_bits)


# 33
def set_snuggly_next_trade(event_flag_id):
    event_format = ['2003', '33', 'i']
    return __format_event(event_format, event_flag_id)


# 34
def snuggly_item_drop(item_lot_id, area_entity_id, event_flag_id, hitbox_entity_id):
    event_format = ['2003', '34', 'iiii']
    return __format_event(event_format, item_lot_id, area_entity_id, event_flag_id, hitbox_entity_id)


# 35
def move_dropped_items_and_bloodstains(source_area_entity_id, destination_area_entity_id):
    event_format = ['2003', '35', 'ii']
    return __format_event(event_format, source_area_entity_id, destination_area_entity_id)


# 36
def award_item_to_host_only(item_lot_id):
    event_format = ['2003', '36', 'i']
    return __format_event(event_format, item_lot_id)


# Note: 37-40 are Battle of Stoicism events that I haven't bothered with.

# 41
def activate_player_killplane(map_id, block_id, threshold_Y, target_model_id):
    event_format = ['2003', '41', 'iifi']
    return __format_event(event_format, map_id, block_id, threshold_Y, target_model_id)


""" 2004: CHARACTER """


# 1
def enable_ai(entity_id):
    return set_ai(entity_id, 1)


def disable_ai(entity_id):
    return set_ai(entity_id, 0)


def set_ai(entity_id, desired_state):
    event_format = ['2004', '01', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 2
def make_NPC_friendly(entity_id):
    return switch_allegiance(entity_id, 8)


def make_NPC_hostile(entity_id):
    return switch_allegiance(entity_id, 9)


def switch_allegiance(entity_id, new_team):
    """
    Team list:
        255: "Default",
        0: "Invalid",
        1: "Survival",              (Human)
        2: "White Ghost",           (Summon)
        3: "Black Ghost",           (Invader)
        4: "Gray Ghost",            (Hollow)
        5: "Wandering Ghost",       (Vagrant)
        6: "Enemy",
        7: "Strong Enemy",
        8: "Ally",
        9: "Hostile Ally",
        10: "Decoy Enemy",
        11: "Red Child",
        12: "Fighting Ally",
        13: "Intruder"
    """
    event_format = ['2004', '02', 'ib']
    return __format_event(event_format, entity_id, new_team)


# 3
def warp(entity_id, warp_destination_type, destination_target_id, damipoly_id):
    # Technically a warp 'request.'
    event_format = ['2004', '03', 'iBii']
    return __format_event(event_format, entity_id, warp_destination_type, destination_target_id, damipoly_id)


# 4
def kill(entity_id, yields_souls=0):
    # Technically a kill 'request.'
    event_format = ['2004', '04', 'iB']
    return __format_event(event_format, entity_id, __bint(yields_souls))


# 5
def enable(entity_id):
    return set_character_state(entity_id, 1)


def disable(entity_id):
    return set_character_state(entity_id, 0)


def set_character_state(entity_id, desired_state):
    event_format = ['2004', '05', 'ib']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 6
def ezstate_instruction_request(entity_id, command_id, slot_number):
    # Slot number from 0-3.
    event_format = ['2004', '06', 'iiB']
    return __format_event(event_format, entity_id, command_id, slot_number)


# 7
def create_spawner(entity_id):
    # Technically create 'bullet owner.'
    event_format = ['2004', '07', 'i']
    return __format_event(event_format, entity_id)


# 8
def set_special_effect(entity_id, special_effect_id):
    # 'Special effect' as in buff/debuff, not graphics.
    event_format = ['2004', '08', 'ii']
    return __format_event(event_format, entity_id, special_effect_id)


# 9
def set_standby_animation_settings_to_default(entity_id):
    return set_standby_animation_settings(entity_id, -1, -1, -1, -1, -1)


def set_standby_animation_settings(entity_id, standby_animation, damage_animation, cancel_animation, death_animation,
                                   standby_return_animation):
    # Sets entity's standby animations. -1 is default for each category.
    event_format = ['2004', '09', 'iiiiii']
    return __format_event(event_format, entity_id, standby_animation, damage_animation, cancel_animation,
                          death_animation, standby_return_animation)


# 10
def enable_gravity(entity_id):
    return set_gravity(entity_id, 0)


def disable_gravity(entity_id):
    return set_gravity(entity_id, 1)


def set_gravity(entity_id, desired_state):
    # 1 = disabled
    # Does NOT allow any sort of RigidBody activity, but rather determines if
    # the entity changes height as it moves around.
    event_format = ['2004', '10', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 12
def set_immortality(entity_id, desired_state):
    # Character will take damage, but not die.
    event_format = ['2004', '12', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 13
def set_nest(entity_id, area_id):
    # Home point for entity AI.
    event_format = ['2004', '13', 'ii']
    return __format_event(event_format, entity_id, area_id)


# 14
def rotate_to_face_entity(entity_id, target_entity_id):
    # Rotate first entity to face towards second.
    event_format = ['2004', '14', 'ii']
    return __format_event(event_format, entity_id, target_entity_id)


# 15
def enable_invincibility(entity_id):
    return set_invincibility(entity_id, 1)


def disable_invincibility(entity_id):
    return set_invincibility(entity_id, 0)


def set_invincibility(entity_id, desired_state):
    # Character cannot take damage or die.
    event_format = ['2004', '15', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 16
def clear_ai_target_list(entity_id):
    event_format = ['2004', '16', 'i']
    return __format_event(event_format, entity_id)


# 17
def ai_instruction(entity_id, command_id, slot_number):
    event_format = ['2004', '17', 'iiB']
    return __format_event(event_format, entity_id, command_id, slot_number)


# 18
def set_event_point(entity_id, event_area_entity_id, reaction_range):
    # TODO: No idea what this does yet.
    event_format = ['2004', '18', 'iif']
    return __format_event(event_format, entity_id, event_area_entity_id, reaction_range)


# 19
def set_ai_id(entity_id, ai_id):
    event_format = ['2004', '19', 'ii']
    return __format_event(event_format, entity_id, ai_id)


# 20
def replan_ai(entity_id):
    # Force entity to re-plan AI.
    event_format = ['2004', '20', 'i']
    return __format_event(event_format, entity_id)


# 21
def cancel_special_effect(entity_id, special_effect_id):
    event_format = ['2004', '21', 'ii']
    return __format_event(event_format, entity_id, special_effect_id)


# 22
def create_multipart_NPC_part(entity_id, part_npc_type, part_index, part_health,
                              damage_correction, body_damage_correction, is_invincible, start_in_stop_state):
    # Obviously complex and I'm not planning to do much other than copy existing use.
    event_format = ['2004', '22', 'ihhiffBB']
    return __format_event(event_format, entity_id, part_npc_type, part_index, part_health,
                          damage_correction, body_damage_correction, __bint(is_invincible), __bint(start_in_stop_state))


# 23
def set_multipart_NPC_part_health(entity_id, part_npc_type, desired_hp, overwrite_max):
    event_format = ['2004', '23', 'iiiB']
    return __format_event(event_format, entity_id, part_npc_type, desired_hp, __bint(overwrite_max))


# 24
def set_multipart_NPC_part_effects(entity_id, part_npc_type, material_special_effect_id, material_SFX_id):
    event_format = ['2004', '24', 'iiii']
    return __format_event(event_format, entity_id, part_npc_type, material_special_effect_id, material_SFX_id)


# 25
def set_multipart_NPC_part_bullet_damage_scaling(entity_id, part_npc_type, desired_scaling):
    event_format = ['2004', '25', 'iif']
    return __format_event(event_format, entity_id, part_npc_type, desired_scaling)


# 26
def set_display_mask(entity_id, bit_number, switch_type):
    # 0 = off, 1 = on, 2 = change
    event_format = ['2004', '26', 'iBB']
    return __format_event(event_format, entity_id, bit_number, switch_type)


# 27
def set_hitbox_mask(entity_id, bit_number, switch_type):
    # 0 = off, 1 = on, 2 = change
    event_format = ['2004', '27', 'iBB']
    return __format_event(event_format, entity_id, bit_number, switch_type)


# 28
def set_network_update_authority(entity_id, authority_level):
    # 0 = normal, 4095 = forced (or -1 I assume)
    event_format = ['2004', '28', 'ii']
    return __format_event(event_format, entity_id, authority_level)


# 29
def enable_backread(entity_id):
    return set_backread_state(entity_id, 0)


def disable_backread(entity_id):
    return set_backread_state(entity_id, 1)


def set_backread_state(entity_id, desired_state):
    # 'Setting to remove from back lead' - involved in permanent disabling
    # 1 = remove, 0 = don't remove
    # Not sure if it can be restored once removed
    event_format = ['2004', '29', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 30
def enable_health_bar(entity_id):
    return set_health_bar_display(entity_id, 1)


def disable_health_bar(entity_id):
    return set_health_bar_display(entity_id, 0)


def set_health_bar_display(entity_id, desired_state):
    # Normal bar, not boss bar.
    event_format = ['2004', '30', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 31
def enable_collision(entity_id):
    return set_collision(entity_id, 0)


def disable_collision(entity_id):
    return set_collision(entity_id, 1)


def set_collision(entity_id, disable_collision):
    # 1 = no collision
    event_format = ['2004', '31', 'iB']
    return __format_event(event_format, entity_id, __bint(disable_collision))


# 32
def ai_event(entity_id, command_id, slot_number, start_event_flag_id, end_event_flag_id):
    # Complex AI stuff.
    # TODO: Check usage.
    event_format = ['2004', '32', 'iiBii']
    return __format_event(event_format, entity_id, command_id, slot_number, start_event_flag_id, end_event_flag_id)


# 33
def refer_damage_to_entity(entity_id, target_entity_id):
    # Damage to first entity affects second (a la Four Kings).
    event_format = ['2004', '33', 'ii']
    return __format_event(event_format, entity_id, target_entity_id)


# 34
def set_network_update_rate(entity_id, is_fixed, frequency):
    """
    Frequency:
        -1: "Never",
        0: "Always",
        2: "Every 2 frames",
        5: "Every 5 frames
    """
    event_format = ['2004', '34', 'iBb']
    return __format_event(event_format, entity_id, __bint(is_fixed), frequency)


# 35
def set_backread_state_alternate(entity_id, desired_state):
    # Not sure how this relates to 2004[29] above.
    # TODO: Check and compare usage.
    event_format = ['2004', '35', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 36
def hellkite_breath_control(entity_id, object_entity_id, animation_id):
    # I don't expect to be reusing this, obviously.
    event_format = ['2004', '36', 'iii']
    return __format_event(event_format, entity_id, object_entity_id, animation_id)


# 37
def drop_mandatory_treasure(entity_id):
    # Forces drop of mandatory treasure, e.g. NPC drop on reload.
    event_format = ['2004', '37', 'i']
    return __format_event(event_format, entity_id)


# 38
def betray_current_covenant():
    event_format = ['2004', '38', 'B']
    return __format_event(event_format, 0)


# 39
def enable_animations(entity_id):
    return set_animation_state(entity_id, 1)


def disable_animations(entity_id):
    return set_animation_state(entity_id, 0)


def set_animation_state(entity_id, desired_state):
    event_format = ['2004', '39', 'iB']
    return __format_event(event_format, entity_id, __bint(desired_state))


# 40
def warp_and_set_floor(entity_id, warp_destination_type, damipoly_id, destination_entity_id):
    # Type: 0 = object, 1 = area, 2 = character
    event_format = ['2004', '40', 'iBiii']
    return __format_event(event_format, entity_id, warp_destination_type, damipoly_id, destination_entity_id)


# 41
def short_warp(entity_id, warp_destination_type, destination_target_id, damipoly_id):
    event_format = ['2004', '41', 'iBii']
    return __format_event(event_format, entity_id, warp_destination_type, destination_target_id, damipoly_id)


# 42
def warp_and_copy_floor(entity_id, warp_destination_type, destination_target_id, damipoly_id, copy_floor_of_entity_id):
    # Type: 0 = object, 1 = area, 2 = character
    event_format = ['2004', '42', 'iBiii']
    return __format_event(event_format, entity_id, warp_destination_type, destination_target_id, damipoly_id,
                          copy_floor_of_entity_id)


# 43
def reset_animation(entity_id, disable_interpolation):
    # 0 = interpolated, 1 = not interpolated
    event_format = ['2004', '43', 'iB']
    return __format_event(event_format, entity_id, __bint(disable_interpolation))


# 44
def change_allegiance_and_exit_standby_animation(entity_id, new_team):
    """
    Team list:
        255: "Default",
        0: "Invalid",
        1: "Survival",              (Human)
        2: "White Ghost",           (Summon)
        3: "Black Ghost",           (Invader)
        4: "Gray Ghost",            (Hollow)
        5: "Wandering Ghost",       (Vagrant)
        6: "Enemy",
        7: "Strong Enemy",
        8: "Ally",
        9: "Hostile Ally",
        10: "Decoy Enemy",
        11: "Red Child",
        12: "Fighting Ally",
        13: "Intruder"
    """
    event_format = ['2004', '44', 'iB']
    return __format_event(event_format, entity_id, new_team)


# 45
def NPC_humanity_registration(entity_id, event_flag_id):
    # Not known exactly what the event flag does, but this instruction is
    # always called to initialize NPCs who drop humanity. It probably makes the
    # game's sin system aware of the NPC's death, etc.
    event_format = ['2004', '45', 'ii']
    return __format_event(event_format, entity_id, event_flag_id)


# 46
def increment_player_pvp_sin():
    event_format = ['2004', '46', 'B']
    return __format_event(event_format, 0)


# 47
def equal_recovery():
    # No arguments; HPR speculates that it may trigger a garbage collection.
    return '2004[47]'


""" 2005: OBJECT """


# 1
def destroy_object(entity_id, slot_number):
    # Technically requests the object's destruction. Not sure what the slot
    # number does.
    event_format = ['2005', '01', 'ib']
    return __format_event(event_format, entity_id, slot_number)


# 2
def restore_object(entity_id):
    event_format = ['2005', '02', 'i']
    return __format_event(event_format, entity_id)


# 3
def enable_object(entity_id):
    return set_object_state(entity_id, 1)


def disable_object(entity_id):
    return set_object_state(entity_id, 0)


def set_object_state(entity_id, activation_status):
    event_format = ['2005', '03', 'iB']
    return __format_event(event_format, entity_id, activation_status)


# 4
def enable_treasure(entity_id):
    return set_treasure_state(entity_id, 1)


def disable_treasure(entity_id):
    return set_treasure_state(entity_id, 0)


def set_treasure_state(entity_id, activation_status):
    event_format = ['2005', '04', 'iB']
    return __format_event(event_format, entity_id, activation_status)


# 5
def start_object_activation(entity_id, object_parameter_id, relative_idx):
    # Calls ObjAct function of object. Not sure what relative IDX does.
    event_format = ['2005', '05', 'iii']
    return __format_event(event_format, entity_id, object_parameter_id, relative_idx)


# 6
def enable_object_activation(entity_id, object_parameter_id):
    return set_object_activation(entity_id, object_parameter_id, 1)


def disable_object_activation(entity_id, object_parameter_id):
    return set_object_activation(entity_id, object_parameter_id, 0)


def set_object_activation(entity_id, object_parameter_id, activation_status):
    # Sets whether the object can be activated (1) or not activated (0).
    event_format = ['2005', '06', 'iiB']
    return __format_event(event_format, entity_id, object_parameter_id, activation_status)


# 7
def skip_to_end_of_animation(entity_id, animation_id):
    # Sets object to whatever state it would have given the activation.
    event_format = ['2005', '07', 'ii']
    return __format_event(event_format, entity_id, animation_id)


# 8
def skip_to_end_of_destruction(entity_id, slot_number):
    # Sets object to whatever state it would have after destruction.
    event_format = ['2005', '08', 'ib']
    return __format_event(event_format, entity_id, slot_number)


# 9
def create_damaging_object(entity_flag_id, entity_id, damipoly_id, behavior_id, target_type, radius, life,
                           repetition_time):
    # Used to create things like the Sen's Fortress dart traps.
    # TODO: Check usage and confirm argument functions.
    """
    Damage target type list:
        1: Character
        2: Map
        3: Character and Map
    """
    event_format = ['2005', '09', 'iiiiifff']
    return __format_event(event_format, entity_flag_id, entity_id, damipoly_id, behavior_id, target_type, radius, life,
                          repetition_time)


# 10
def register_statue_object(entity_id, area_number, block_number, statue_type):
    # I believe this creates a petrified or crystallized statue.
    # TODO: Check usage.
    event_format = ['2005', '10', 'iBBB']
    return __format_event(event_format, entity_id, area_number, block_number, statue_type)


# 11
def warp_object_to_character(entity_id, character_entity_id, damipoly_id):
    # TODO: Check when this is actually used, as I'm not sure what use it has.
    event_format = ['2005', '11', 'iih']
    return __format_event(event_format, entity_id, character_entity_id, damipoly_id)


# 12
def remove_object_event_flag(event_flag_id):
    # TODO: Check when this is actually used.
    event_format = ['2005', '12', 'i']
    return __format_event(event_format, event_flag_id)


# 13
def enable_object_invulnerability(entity_id):
    return set_object_invulnerability(entity_id, 1)


def disable_object_invulnerability(entity_id):
    return set_object_invulnerability(entity_id, 0)


def set_object_invulnerability(entity_id, invulnerability_state):
    # 1 = invulnerable
    event_format = ['2005', '13', 'iB']
    return __format_event(event_format, entity_id, invulnerability_state)


# 14
def activate_object_with_idx(entity_id, object_parameter_id, relative_idx):
    return set_object_activation_with_idx(entity_id, object_parameter_id, relative_idx, 1)


def deactivate_object_with_idx(entity_id, object_parameter_id, relative_idx):
    return set_object_activation_with_idx(entity_id, object_parameter_id, relative_idx, 0)


def set_object_activation_with_idx(entity_id, object_parameter_id, relative_idx, activation_state):
    event_format = ['2005', '14', 'iiiB']
    return __format_event(event_format, entity_id, object_parameter_id, relative_idx, activation_state)


# 15
def enable_treasure_collection(entity_id):
    # TODO: Speculated use only. Check usage.
    event_format = ['2005', '15', 'i']
    return __format_event(event_format, entity_id)


""" 2006: SFX """


# 1
def delete_map_sfx(entity_id, erase_root_only=True):
    # Erasing the root only probably allows easy recreation later (default).
    event_format = ['2006', '01', 'iB']

    return __format_event(event_format, entity_id, __bint(erase_root_only))


# 2
def create_map_sfx(entity_id):
    event_format = ['2006', '02', 'i']
    return __format_event(event_format, entity_id)


# 3
def create_oneoff_sfx(sfx_type, entity_id, damipoly_id, sfx_id):
    """
    SFX categories:
        0: "Object",
        1: "Area",
        2: "Character"
    """
    event_format = ['2006', '03', 'iiii']
    return __format_event(event_format, sfx_type, entity_id, damipoly_id, sfx_id)


# 4
def create_object_sfx(entity_id, damipoly_id, sfx_id):
    event_format = ['2006', '04', 'iii']
    return __format_event(event_format, entity_id, damipoly_id, sfx_id)


# 5
def delete_object_sfx(entity_id, erase_root=True):
    # Note `erase_root` vs. `erase_root_only` for map SFX.
    event_format = ['2006', '05', 'ii']
    return __format_event(event_format, entity_id, __bint(erase_root))


""" 2007: MESSAGE """


# 1
def display_generic_dialog(message_id, button_type, number_buttons, entity_id, display_distance):
    # Message box that appears on the screen and awaits response.
    """
    Button type list:
        0: "YES/NO",
        1: "OK/CANCEL"
    Button number list:
        1: "1 Button",
        2: "2 Button",
        6: "No Button"
    """
    event_format = ['2007', '01', 'ihhif']
    return __format_event(event_format, message_id, button_type, number_buttons, entity_id, display_distance)


# 2
def display_text_banner(banner_type):
    # Displays large preset banners.
    """
    Banner list:
        1: "Demon Killed",
        2: "Death",
        3: "Revival",
        4: "Soul Acquisition",
        5: "Target Killed",
        6: "Ghost Death",
        7: "Black Ghost Death",
        8: "Map Name",
        12: "Congratulations",
        15: "Stadium Victory",
        16: "Stadium Defeat",
        17: "Stadium Draw"
    """
    event_format = ['2007', '02', 'B']
    return __format_event(event_format, banner_type)


# 3
def display_status_explanation_message(message_id, pad_enabled=0):
    # Displays messages explaining curse, no bonfire warp, etc.
    # TODO: Check usage for pad_enabled; when would it be used?
    event_format = ['2007', '03', 'iB']
    return __format_event(event_format, message_id, pad_enabled)


# 4
def display_battlefield_message(message_id, display_location_index):
    # TODO: Check usage.
    event_format = ['2007', '04', 'iB']
    return __format_event(event_format, message_id, display_location_index)


# 5-9 are Battle of Stoicism messages, not bothering for now.

""" 2008: CAMERA """


# 3
def set_locked_camera_slot_number(area_id, block_id, locked_camera_slot_number):
    # This doesn't seem to be used as often as I'd expect, given the number
    # of different camera settings in the params. Camera settings triggered by
    # boss battles may be handled elsewhere.
    event_format = ['2008', '03', 'BBH']
    return __format_event(event_format, area_id, block_id, locked_camera_slot_number)


""" 2009: SCRIPT """


# 0
def register_ladder(event_flag_id_1, event_flag_id_2, entity_id):
    # Not sure what the different event flags do. Called on area initialization
    # to make ladders interactable.
    event_format = ['2009', '00', 'iii']
    return __format_event(event_format, event_flag_id_1, event_flag_id_2, entity_id)


# 3
def register_bonfire(event_flag_id, entity_id, reaction_distance, reaction_angle, initial_basic_spot_point):
    # TODO: Check usage of last three arguments. Probably consistent.
    # I assume that the reaction arguments restrict the distance and angle from
    # which you can activate the bonfire. The last argument might determine
    # where you spawn at the bonfire, but it's not a float.
    event_format = ['2009', '03', 'iiffi']
    return __format_event(event_format, event_flag_id, entity_id, reaction_distance, reaction_angle,
                          initial_basic_spot_point)


# 4
def activate_NPC_buffs(entity_id):
    event_format = ['2009', '04', 'i']
    return __format_event(event_format, entity_id)


# 6
def notify_boss_room_entry():
    # Triggers message for summons that player has challenged the boss.
    # Might do other things for online play as well, no doubt.
    event_format = ['2009', '06', 'B']
    return __format_event(event_format, 0)


""" 2010: SOUND """


# 2
def play_sound_effect(entity_id, sound_type, sound_id):
    # Entity specifies the sound's origin (direction), I assume.
    """
    Sound type list:
        0: "a: Environmental Sound",
        1: "c: Character Motion",
        2: "f: Menu SE",
        3: "o: Object",
        4: "p: Poly Drama",
        5: "s: SFX",
        6: "m: BGM",
        7: "v: Voice",
        8: "x: Floor Material Dependence",
        9: "b: Armor Material Dependence",
        10: "g: Ghost"
    """
    event_format = ['2010', '02', 'iii']
    return __format_event(event_format, entity_id, sound_type, sound_id)


# 3
def enable_map_sound(entity_id):
    return set_map_sound(entity_id, 1)


def disable_map_sound(entity_id):
    return set_map_sound(entity_id, 0)


def set_map_sound(entity_id, sound_state):
    # Includes boss music, which is obviously the most common use.
    event_format = ['2010', '03', 'iB']
    return __format_event(event_format, entity_id, sound_state)


""" 2011: HIT """


# 1
def enable_hitbox(entity_id):
    return set_hitbox_state(entity_id, 1)


def disable_hitbox(entity_id):
    return set_hitbox_state(entity_id, 0)


def set_hitbox_state(entity_id, activation_state):
    # 1 = Hitbox is enabled.
    event_format = ['2011', '01', 'iB']
    return __format_event(event_format, entity_id, activation_state)


""" 2012: MAP """


# 1
def enable_map_part(map_part_id):
    return set_map_part_state(map_part_id, 1)


def disable_map_part(map_part_id):
    return set_map_part_state(map_part_id, 0)


def set_map_part_state(map_part_id, activation_state):
    # TODO: Check usage of this.
    event_format = ['2012', '01', 'iB']
    return __format_event(event_format, map_part_id, activation_state)


""" 1000: EXECUTION CONTROL (SYSTEM) """


# 1
def skip_if_condition_true(number_lines, condition):
    # Skips some number of lines if the condition is true.
    # Default condition is MAIN.
    return skip_if_condition_state(number_lines, 1, condition)


def skip_if_condition_false(number_lines, condition):
    # Skips some number of lines if the condition is false.
    # Default condition is MAIN.
    return skip_if_condition_state(number_lines, 0, condition)


def skip_if_condition_state(number_lines, required_state, condition):
    # Skips some number of lines if the specified condition has the specified
    # state.
    """
    Condition values can be found within the event_enums.execution_condition enum
    (execution_condition.main, execution_condition.and1, execution_condition.or1, etc)
    OR, alternatively, as constants found directly within event_enums (MAIN, AND1, OR1, etc)
    """
    event_format = ['1000', '01', 'BBb']
    return __format_event(event_format, number_lines, required_state, condition)


# 2
def restart_if_condition_true(condition = 0):
    # Restart the event if the condition is true.
    # Default condition is MAIN.
    return terminate_if_condition_state(1, 1, condition)


def restart_if_condition_false(condition = 0):
    # Restart the event if the condition is false.
    # Default condition is MAIN.
    return terminate_if_condition_state(1, 0, condition)


def end_if_condition_true(condition = 0):
    # End (not restart) the event if the condition is true.
    # Default condition is MAIN.
    return terminate_if_condition_state(0, 1, condition)


def end_if_condition_false(condition = 0):
    # End (not restart) the event if the condition is true.
    # Default condition is MAIN.
    return terminate_if_condition_state(0, 0, condition)


def terminate_if_condition_state(event_end_type, required_state, condition):
    event_format = ['1000', '02', 'BBb']
    return __format_event(event_format, event_end_type, required_state, condition)


# 3
def skip(number_lines):
    # Unconditional line skip.
    event_format = ['1000', '03', 'B']
    return __format_event(event_format, number_lines)


# 4
def restart():
    # Unconditional event restart.
    return terminate(1)


def end():
    # Unconditional event end (no restart).
    return terminate(0)


def terminate(event_end_type):
    # Unconditional event termination (1 = restart).
    event_format = ['1000', '04', 'B']
    return __format_event(event_format, event_end_type)


# 5
def skip_if_equal(number_lines, left, right):
    return skip_if_value_comparison(number_lines, 0, left, right)


def skip_if_not_equal(number_lines, left, right):
    return skip_if_value_comparison(number_lines, 1, left, right)


def skip_if_greater_than(number_lines, left, right):
    return skip_if_value_comparison(number_lines, 2, left, right)


def skip_if_less_than(number_lines, left, right):
    return skip_if_value_comparison(number_lines, 3, left, right)


def skip_if_greater_than_or_equal(number_lines, left, right):
    return skip_if_value_comparison(number_lines, 4, left, right)


def skip_if_less_than_or_equal(number_lines, left, right):
    return skip_if_value_comparison(number_lines, 5, left, right)


def skip_if_value_comparison(number_lines, comparison_type, left, right):
    # Skips some number of lines if the specified (ordered) comparison is true.
    """
    Comparison types:
        0: "==",
        1: "!=",
        2: ">",
        3: "<",
        4: ">=",
        5: "<="
    """
    event_format = ['1000', '05', 'Bbii']
    return __format_event(event_format, number_lines, comparison_type, left, right)


# 6
def end_if_equal(left, right):
    return terminate_if_value_comparison(0, 0, left, right)


def end_if_not_equal(left, right):
    return terminate_if_value_comparison(0, 1, left, right)


def end_if_greater_than(left, right):
    return terminate_if_value_comparison(0, 2, left, right)


def end_if_less_than(left, right):
    return terminate_if_value_comparison(0, 3, left, right)


def end_if_greater_than_or_equal(left, right):
    return terminate_if_value_comparison(0, 4, left, right)


def end_if_less_than_or_equal(left, right):
    return terminate_if_value_comparison(0, 5, left, right)


def restart_if_equal(left, right):
    return terminate_if_value_comparison(1, 0, left, right)


def restart_if_not_equal(left, right):
    return terminate_if_value_comparison(1, 1, left, right)


def restart_if_greater_than(left, right):
    return terminate_if_value_comparison(1, 2, left, right)


def restart_if_less_than(left, right):
    return terminate_if_value_comparison(1, 3, left, right)


def restart_if_greater_than_or_equal(left, right):
    return terminate_if_value_comparison(1, 4, left, right)


def restart_if_less_than_or_equal(left, right):
    return terminate_if_value_comparison(1, 5, left, right)


def terminate_if_value_comparison(event_end_type, comparison_type, left, right):
    # Terminates if some number of lines if the specified (ordered) comparison
    # is true (0 = end, 1 = restart).
    """
    Comparison types:
        0: "==",
        1: "!=",
        2: ">",
        3: "<",
        4: ">=",
        5: "<="
    """
    event_format = ['1000', '06', 'Bbii']
    return __format_event(event_format, event_end_type, comparison_type, left, right)


# 7
def skip_if_condition_true_finished(number_lines, condition = 0):
    # Default condition is MAIN.
    return skip_if_condition_state_finished(number_lines, 1, condition)


def skip_if_condition_false_finished(number_lines, condition = 0):
    # Default condition is MAIN.
    return skip_if_condition_state_finished(number_lines, 0, condition)


def skip_if_condition_state_finished(number_lines, required_state, condition):
    # It is unclear how this differs from 1000[01]. The instruction name says
    # "finished condition group" (condition) rather than simply "condition
    # group". This may use the condition in a slightly different way.
    # TODO: Examine when this is used versus 1000[01].
    event_format = ['1000', '07', 'BBb']
    return __format_event(event_format, number_lines, required_state, condition)


# 8
def restart_if_condition_true_finished(condition = 0):
    # Restart the event if the condition is true.
    # Default condition is MAIN.
    return terminate_if_condition_state_finished(1, 1, condition)


def restart_if_condition_false_finished(condition = 0):
    # Restart the event if the condition is false.
    # Default condition is MAIN.
    return terminate_if_condition_state_finished(1, 0, condition)


def end_if_condition_true_finished(condition = 0):
    # End (not restart) the event if the condition is true.
    # Default condition is MAIN.
    return terminate_if_condition_state_finished(0, 1, condition)


def end_if_condition_false_finished(condition = 0):
    # End (not restart) the event if the condition is true.
    # Default condition is MAIN.
    return terminate_if_condition_state_finished(0, 0, condition)


def terminate_if_condition_state_finished(event_end_type, required_state, condition):
    # See 1000[07]; unclear how this differs from 1000[02].
    # TODO: Examine usage of this vs. 1000[02].
    event_format = ['1000', '08', 'BBb']
    return __format_event(event_format, event_end_type, required_state, condition)


# 9
def wait_for_network_approval(timeout):
    # Wait for network to approve event (up to `timeout` seconds).
    event_format = ['1000', '09', 'f']
    return __format_event(event_format, timeout)


""" 1001: EXECUTION CONTROL (TIMER) """


# 0
def wait(number_seconds):
    # Wait for some number of seconds.
    event_format = ['1001', '00', 'f']
    return __format_event(event_format, number_seconds)


# 1
def wait_frames(number_frames):
    # Wait for some number of frames.
    event_format = ['1001', '01', 'i']
    return __format_event(event_format, number_frames)


# 2
def wait_random_range(min_number_seconds, max_number_seconds):
    # Wait for a random number of seconds between min and max. I assume the
    # distribution is inclusive and uniform.
    event_format = ['1001', '02', 'ff']
    return __format_event(event_format, min_number_seconds, max_number_seconds)


""" 1003: EXECUTION CONTROL (EVENT) """


# 1
def skip_if_this_event_on(number_lines):
    return skip_if_event_flag_state(number_lines, 1, flag_type.event, 0)


def skip_if_this_event_slot_on(number_lines):
    return skip_if_event_flag_state(number_lines, 1, flag_type.event_with_slot, 0)


def skip_if_this_event_off(number_lines):
    return skip_if_event_flag_state(number_lines, 0, flag_type.event, 0)


def skip_if_this_event_slot_off(number_lines):
    return skip_if_event_flag_state(number_lines, 0, flag_type.event_with_slot, 0)


def skip_if_event_flag_on(number_lines, event_flag_type: flag_type, event_flag_id):
    return skip_if_event_flag_state(number_lines, 1, event_flag_type, event_flag_id)


def skip_if_event_flag_off(number_lines, event_flag_type: flag_type, event_flag_id):
    return skip_if_event_flag_state(number_lines, 0, event_flag_type, event_flag_id)


def skip_if_event_flag_state(number_lines, required_flag_state, event_flag_type: flag_type, event_flag_id):
    # Skip some number of instructions if the specified flag has the specified
    # state (0 = off, 1 = on).
    event_format = ['1003', '01', 'BBBi']
    return __format_event(event_format, number_lines, required_flag_state, event_flag_type, event_flag_id)


# 2
def end_if_this_event_on():
    return terminate_if_event_flag_state(0, 1, flag_type.event, 0)


def end_if_this_event_off():
    return terminate_if_event_flag_state(0, 0, flag_type.event, 0)


def end_if_event_flag_on(event_flag_type: flag_type, event_flag_id):
    return terminate_if_event_flag_state(0, 1, event_flag_type, event_flag_id)


def end_if_event_flag_off(event_flag_type: flag_type, event_flag_id):
    return terminate_if_event_flag_state(0, 0, event_flag_type, event_flag_id)


def restart_if_event_flag_on(event_flag_type: flag_type, event_flag_id):
    return terminate_if_event_flag_state(1, 1, event_flag_type, event_flag_id)


def restart_if_event_flag_off(event_flag_type: flag_type, event_flag_id):
    return terminate_if_event_flag_state(1, 0, event_flag_type, event_flag_id)


def terminate_if_event_flag_state(event_end_type, required_flag_state, event_flag_type: flag_type, event_flag_id):
    # Terminate (end or restart) event if the specified flag has the specified
    # state (0 = off, 1 = on).
    event_format = ['1003', '02', 'BBBi']
    return __format_event(event_format, event_end_type, required_flag_state, event_flag_type, event_flag_id)


# 3
def skip_if_event_flag_range_on(number_lines, event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return skip_if_event_flag_range_state(number_lines, 1, event_flag_type, start_event_flag_id, end_event_flag_id)


def skip_if_event_flag_range_off(number_lines, event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return skip_if_event_flag_range_state(number_lines, 0, event_flag_type, start_event_flag_id, end_event_flag_id)


def skip_if_event_flag_range_state(number_lines, required_flag_state, event_flag_type: flag_type, start_event_flag_id,
                                   end_event_flag_id):
    # Skip some number of instructions if the specified range of flags all have
    # the specified state (0 = off, 1 = on).
    """
    Event flag type list:
        0: "Event Flag ID",
        1: "Event ID",
        2: "Event ID with Slot Number"
    """
    event_format = ['1003', '03', 'BBBii']
    return __format_event(event_format, number_lines, required_flag_state, event_flag_type, start_event_flag_id,
                          end_event_flag_id)


# 4
def end_if_event_flag_range_on(event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return terminate_if_event_flag_range_state(0, 1, event_flag_type, start_event_flag_id, end_event_flag_id)


def end_if_event_flag_range_off(event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return terminate_if_event_flag_range_state(0, 0, event_flag_type, start_event_flag_id, end_event_flag_id)


def restart_if_event_flag_range_on(event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return terminate_if_event_flag_range_state(1, 1, event_flag_type, start_event_flag_id, end_event_flag_id)


def restart_if_event_flag_range_off(event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return terminate_if_event_flag_range_state(1, 0, event_flag_type, start_event_flag_id, end_event_flag_id)


def terminate_if_event_flag_range_state(event_end_type, required_flag_state, event_flag_type: flag_type, start_event_flag_id,
                                        end_event_flag_id):
    # Terminate (end or restart) event if the specified range of flags all have
    # the specified state (0 = off, 1 = on).
    event_format = ['1003', '04', 'BBBii']
    return __format_event(event_format, event_end_type, required_flag_state, event_flag_type, start_event_flag_id,
                          end_event_flag_id)


# 5
def skip_if_host(number_lines):
    return skip_if_multiplayer_state(number_lines, 0)


def skip_if_client(number_lines):
    return skip_if_multiplayer_state(number_lines, 1)


def skip_if_multiplayer(number_lines):
    return skip_if_multiplayer_state(number_lines, 2)


def skip_if_singleplayer(number_lines):
    return skip_if_multiplayer_state(number_lines, 3)


def skip_if_multiplayer_state(number_lines, required_multiplayer_state):
    # Skip some number of lines if the player has the specified multiplayer
    # state.
    """
    Multiplayer state list:
        0: "Host" (owner of world)
        1: "Client" (summon, not invader)
        2: "Multiplayer" (either has a client or is a client I believe)
        3: "Singleplayer" (host with no client)
    """
    event_format = ['1003', '05', 'Bb']
    return __format_event(event_format, number_lines, required_multiplayer_state)


# 6
def end_if_host():
    return terminate_if_multiplayer_state(0, 0)


def end_if_client():
    return terminate_if_multiplayer_state(0, 1)


def end_if_multiplayer():
    return terminate_if_multiplayer_state(0, 2)


def end_if_singleplayer():
    return terminate_if_multiplayer_state(0, 3)


def restart_if_host():
    return terminate_if_multiplayer_state(1, 0)


def restart_if_client():
    return terminate_if_multiplayer_state(1, 1)


def restart_if_multiplayer():
    return terminate_if_multiplayer_state(1, 2)


def restart_if_singleplayer():
    return terminate_if_multiplayer_state(1, 3)


def terminate_if_multiplayer_state(event_end_type, required_multiplayer_state):
    # Terminate event (end or restart) if the player has the specified
    # multiplayer state.
    """
    Multiplayer state list:
        0: "Host" (owner of world)
        1: "Client" (summon, not invader)
        2: "Multiplayer" (either has a client or is a client I believe)
        3: "Singleplayer" (host with no client)
    """
    event_format = ['1003', '06', 'Bb']
    return __format_event(event_format, event_end_type, required_multiplayer_state)


# 7
def skip_if_inside_area(number_lines, area_id, block_id):
    return skip_if_area_state(number_lines, 1, area_id, block_id)


def skip_if_outside_area(number_lines, area_id, block_id):
    return skip_if_area_state(number_lines, 0, area_id, block_id)


def skip_if_area_state(number_lines, required_area_state, area_id, block_id):
    # Skip some number of lines if the player is outside (0) or inside (1) the
    # specified area and block.
    event_format = ['1003', '07', 'BBBB']
    return __format_event(event_format, number_lines, required_area_state, area_id, block_id)


# 8 - this terminates the event based on area state, but judging from HPR's
# lack of translation, this is never used.

""" 1005: EXECUTION CONTROL (OBJECT) """


# 1
def skip_if_object_destroyed(number_lines, entity_id):
    # TODO: The bool is a guess right now.
    return skip_if_object_destruction_state(number_lines, 1, entity_id)


def skip_if_object_not_destroyed(number_lines, entity_id):
    # TODO: The bool is a guess right now.
    return skip_if_object_destruction_state(number_lines, 0, entity_id)


def skip_if_object_destruction_state(number_lines, required_destruction_state, entity_id):
    # Skips some number of lines if the specified object has the specified
    # destruction state. I can't actually find this enum, so it's actually hard
    # to guess if 0 = destroyed or 1 = destroyed. I assume the latter, but only
    # tentatively (because it's the default).
    # TODO: Check usage to figure out state bool.
    event_format = ['1005', '01', 'BBi']
    return __format_event(event_format, number_lines, required_destruction_state, entity_id)


# 2
def end_if_object_destroyed(entity_id):
    # TODO: This is a guess.
    return terminate_if_object_destruction_state(0, 1, entity_id)


def end_if_object_not_destroyed(entity_id):
    # TODO: This is a guess.
    return terminate_if_object_destruction_state(0, 0, entity_id)


def restart_if_object_destroyed(entity_id):
    # TODO: This is a guess.
    return terminate_if_object_destruction_state(1, 1, entity_id)


def restart_if_object_not_destroyed(entity_id):
    # TODO: This is a guess.
    return terminate_if_object_destruction_state(1, 0, entity_id)


def terminate_if_object_destruction_state(event_end_type, required_destruction_state, entity_id):
    # Terminates (ends or restarts) the event if the specified object has the
    # specified destruction state. Guessing that 1 = destroyed.
    # TODO: Confirm bool.
    event_format = ['1005', '02', 'BBi']
    return __format_event(event_format, event_end_type, required_destruction_state, entity_id)


""" 0: EXECUTION CONDITIONS (SYSTEM) """


# 0
def if_condition_true(output_condition, input_condition):
    return if_condition_state(output_condition, 1, input_condition)


def if_condition_false(output_condition, input_condition):
    return if_condition_state(output_condition, 0, input_condition)


def if_condition_state(output_condition, required_result, input_condition):
    # Evaluates the input condition (as OR or AND), compares it to the
    # required result, and stores the result of the comparison in the output
    # condition (where many values can be stored).
    # The required result is 1 by default, which means that the output condition
    # will simply store the evaluation of the input.
    event_format = ['   0', '00', 'bBb']
    return __format_event(event_format, output_condition, required_result, input_condition)


""" 1: EXECUTION CONDITIONS (TIME) """


# 0
def if_time_elapsed(output_condition, number_seconds):
    # Counts seconds since event started (I think).
    # TODO: Confirm time since event started.
    event_format = ['   1', '00', 'bf']
    return __format_event(event_format, output_condition, number_seconds)


# 1
def if_frames_elapsed(output_condition, number_frames):
    # TODO: Confirm number of frames since event started.
    event_format = ['   1', '01', 'bi']
    return __format_event(event_format, output_condition, number_frames)


# 2 and 3 choose a random number of seconds/frames, I think, but unused.

""" 3: EXECUTION CONDITIONS (EVENT) """


# 0
def if_event_flag_on(output_condition, event_flag_type: flag_type, event_flag_id):
    return if_event_flag_state(output_condition, 1, event_flag_type, event_flag_id)


def if_event_flag_off(output_condition, event_flag_type: flag_type, event_flag_id):
    return if_event_flag_state(output_condition, 0, event_flag_type, event_flag_id)


def if_event_flag_state(output_condition, required_flag_state, event_flag_type, event_flag_id):
    event_format = ['   3', '00', 'bBBi']
    return __format_event(event_format, output_condition, required_flag_state, event_flag_type, event_flag_id)


# 1
def if_event_flag_range_on(output_condition, event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return if_event_flag_range_state(output_condition, 1, event_flag_type, start_event_flag_id, end_event_flag_id)


def if_event_flag_range_off(output_condition, event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    return if_event_flag_range_state(output_condition, 0, event_flag_type, start_event_flag_id, end_event_flag_id)


def if_event_flag_range_state(output_condition, required_flag_state, event_flag_type: flag_type, start_event_flag_id,
                              end_event_flag_id):
    event_format = ['   3', '01', 'bBBii']
    return __format_event(event_format, output_condition, required_flag_state, event_flag_type, start_event_flag_id,
                          end_event_flag_id)


# 2
def if_entity_inside_area(output_condition, entity_id, area_entity_id):
    return if_entity_inside_or_outside_area(output_condition, entity_id, area_entity_id, 1)


def if_entity_outside_area(output_condition, entity_id, area_entity_id):
    return if_entity_inside_or_outside_area(output_condition, entity_id, area_entity_id, 0)


def if_player_inside_area(output_condition, area_entity_id):
    return if_entity_inside_or_outside_area(output_condition, 10000, area_entity_id, 1)


def if_player_outside_area(output_condition, area_entity_id):
    return if_entity_inside_or_outside_area(output_condition, 10000, area_entity_id, 0)


def if_entity_inside_or_outside_area(output_condition, entity_id, area_entity_id, is_inside):
    # Checks if specified entity is inside or outside specified area.
    # 0 = outside, 1 = inside.
    # Note that argument order has changed.
    event_format = ['   3', '02', 'bBii']
    return __format_event(event_format, output_condition, is_inside, entity_id, area_entity_id)


# 3
def if_player_within_distance(output_condition, target_entity_id, required_distance):
    return if_entity_within_or_beyond_distance(output_condition, 10000, target_entity_id, required_distance, 1)


def if_player_beyond_distance(output_condition, target_entity_id, required_distance):
    return if_entity_within_or_beyond_distance(output_condition, 10000, target_entity_id, required_distance, 0)


def if_entity_within_distance(output_condition, first_entity_id, second_entity_id, required_distance):
    return if_entity_within_or_beyond_distance(output_condition, first_entity_id, second_entity_id, required_distance, 1)


def if_entity_beyond_distance(output_condition, first_entity_id, second_entity_id, required_distance):
    return if_entity_within_or_beyond_distance(output_condition, first_entity_id, second_entity_id, required_distance, 0)


def if_entity_within_or_beyond_distance(output_condition, first_entity_id, second_entity_id, required_distance,
                                        is_within):
    # Check is entity A is within (is_within == True) or beyond the specified
    # distance of entity B.
    event_format = ['   3', '03', 'bBiif']
    return __format_event(event_format, output_condition, __bint(is_within), first_entity_id, second_entity_id, required_distance)


# 4
def if_player_has_item(output_condition, item_type, item_id):
    return if_player_has_or_does_not_have_item(output_condition, item_type, item_id, 1)


def if_player_does_not_have_item(output_condition, item_type, item_id):
    return if_player_has_or_does_not_have_item(output_condition, item_type, item_id, 0)


def if_player_has_or_does_not_have_item(output_condition, item_type, item_id, required_state):
    # Check if player has specified item in inventory, not including Bottomless
    # Box (required_state == True) or does not have the item (required_state == False).
    event_format = ['   3', '04', 'bBiB']
    return __format_event(event_format, output_condition, item_type, item_id, __bint(required_state))


# 5
# TODO: Check the most common parameters for this (e.g. doors) and make a shortcut function for them.
def if_action_button_state(output_condition, category, target_entity_id, reaction_angle,
                           damipoly_id, reaction_distance, help_id, reaction_attribute, pad_id):
    """
    Checks for the player pressing a button near a thing (e.g. "A: Pull lever"). The actual prompt itself might be
    created elsewhere.
    :param output_condition: The condition group to which the result of the prompt is outputted.
    :param category: Whether the prompt is for an object, an area, or a character.
    :param target_entity_id: The entity to attach the prompt to.
    :param reaction_angle: The incident angle between the player and the target entity
    (how close the player's angle must be to facing in the direction of the target entity)
    :param damipoly_id: ID of the "dammy poly" / "damipoly" (both forms are used in the game's data) to use for
    hit detection. These are the hitboxes defined in FLVER meshes (they are used for weapon hitboxes, for example)
    :param reaction_distance: The distance the player needs to be from the target entity.
    :param help_id: The prompt text ID. Climb up ladder prompt is 10010300. Climb down ladder prompt is 10010301.
    No other help IDs are defined in Dark Souls' event_define.lua. Demon's Souls' event_define.lua seems to have
    many help IDs defined and some may work in Dark Souls, so be sure to check that out if you can.
    :param reaction_attribute: Discerns which player(s) the prompt / activation works for.
    :param pad_id: ID of the action button used, usually ID 0, which is the A (Xbox) / Cross (PlayStation) button.
    """
    event_format = ['   3', '05', 'biifhfiBi']
    return __format_event(event_format, output_condition, category, target_entity_id, reaction_angle, damipoly_id,
                          reaction_distance, help_id, reaction_attribute, pad_id)


# 6
def if_host(output_condition):
    return if_multiplayer_state(output_condition, 0)


def if_client(output_condition):
    return if_multiplayer_state(output_condition, 1)


def if_singleplayer(output_condition):
    return if_multiplayer_state(output_condition, 2)


def if_multiplayer(output_condition):
    return if_multiplayer_state(output_condition, 3)


def if_multiplayer_state(output_condition, required_state):
    # Check if player is host (0), summon (1), single player (2), or
    # multiplayer (3).
    event_format = ['   3', '06', 'bb']
    return __format_event(event_format, output_condition, required_state)


# 7
def if_all_players_inside_area(output_condition, area_entity_id):
    return if_all_players_inside_or_outside_area(output_condition, area_entity_id, 1)


def if_all_players_outside_area(output_condition, area_entity_id):
    return if_all_players_inside_or_outside_area(output_condition, area_entity_id, 0)


def if_all_players_inside_or_outside_area(output_condition, area_entity_id, is_inside):
    # Check if all players are inside (1) or outside (0) the specified area.
    event_format = ['   3', '07', 'bBi']
    return __format_event(event_format, output_condition, is_inside, area_entity_id)


# 8
def if_in_world_area(output_condition, area_id, block_id):
    return if_world_area_state(output_condition, area_id, block_id, 1)


def if_not_in_world_area(output_condition, area_id, block_id):
    return if_world_area_state(output_condition, area_id, block_id, 0)


def if_world_area_state(output_condition, area_id, block_id, is_inside):
    # Check if player is inside or outside the specified world area and block.
    event_format = ['   3', '08', 'bBBB']
    return __format_event(event_format, output_condition, is_inside, area_id, block_id)


# 9
def if_multiplayer_event(output_condition, multiplayer_event_id):
    # Check if a multiplayer event has occured.
    event_format = ['   3', '09', 'bI']
    return __format_event(event_format, output_condition, multiplayer_event_id)


# 10
def if_at_least_one_true_flag_in_range(output_condition, event_flag_type: flag_type, start_event_flag_id, end_event_flag_id):
    # Check if at least one flag in the specified range is true.
    return if_count_true_event_flags_in_range(output_condition, event_flag_type, start_event_flag_id, end_event_flag_id,
                                              4, 1)


def if_number_true_flags_in_range_greater_than_or_equal(output_condition, event_flag_type: flag_type, start_event_flag_id,
                                                        end_event_flag_id, min_count):
    # Check if the number of true flags in the specified range is greater than
    # or equal to the specified minimum.
    return if_count_true_event_flags_in_range(output_condition, event_flag_type, start_event_flag_id, end_event_flag_id,
                                              4, min_count)


def if_count_true_event_flags_in_range(output_condition, event_flag_type: flag_type, start_event_flag_id, end_event_flag_id,
                                       comparison_type, count_comparison):
    # Checks if the count of true flags in the specified range satisfies the
    # specified comparison (usually 4: >=) with the specified count.
    event_format = ['   3', '10', 'bBiibi']
    return __format_event(event_format, output_condition, event_flag_type, start_event_flag_id, end_event_flag_id,
                          comparison_type, count_comparison)


# 11
def if_world_tendency_greater_than_or_equal(output_condition, tendency_type, min_tendency):
    return if_world_tendency_comparison(output_condition, tendency_type, 4, min_tendency)


def if_world_tendency_comparison(output_condition, tendency_type, comparison_type, tendency_comparison):
    # Check if comparison of world tendency with specified value is true.
    # tendency_type: 0 = white tendency, 1 = black tendency.
    event_format = ['   3', '11', 'bBBB']
    return __format_event(event_format, output_condition, tendency_type, comparison_type, tendency_comparison)


# 12
def if_event_value_comparison(output_condition, event_flag_id, number_bits, comparison_type, comparison_value):
    # Check if specified bit in event value (usually 0 I think) compares true
    # with specified value.
    event_format = ['   3', '12', 'biBBI']
    return __format_event(event_format, output_condition, event_flag_id, number_bits, comparison_type, comparison_value)


# 13
def if_action_button_state_in_boss(output_condition, category, target_entity_id, reaction_angle, damipoly_id,
                                   reaction_distance, help_id, reaction_attribute, pad_id):
    # Checks state of action button (A on the Xbox controller). I assume this
    # one only applies in boss rooms. See if_action_button_state docs.
    event_format = ['   3', '13', 'biifhfiBi']
    return __format_event(event_format, output_condition, category, target_entity_id, reaction_angle, damipoly_id,
                          reaction_distance, help_id, reaction_attribute, pad_id)


# 14
def if_any_item_dropped_in_area(output_condition, area_entity_id):
    # Check if any item has been dropped in the specified area.
    event_format = ['   3', '14', 'bi']
    return __format_event(event_format, output_condition, area_entity_id)


# 15
def if_item_dropped(output_condition, item_type, item_id):
    # Check if a specified item has been dropped (anywhere).
    event_format = ['   3', '15', 'bii']
    return __format_event(event_format, output_condition, item_type, item_id)


# 16
def if_player_owns_item(output_condition, item_type, item_id):
    # Includes Bottomless Box.
    # Note: it's seriously pointless for me to make a generic function for
    # item ownership state. I'm never going to call it directly.
    event_format = ['   3', '16', 'bBiB']
    return __format_event(event_format, output_condition, item_type, item_id, 1)


def if_player_does_not_own_item(output_condition, item_type, item_id):
    # Includes Bottomless Box.
    event_format = ['   3', '16', 'bBiB']
    return __format_event(event_format, output_condition, item_type, item_id, 0)


# 17
def if_new_game_count_equal(output_condition, completion_count_comparison):
    # Checks if count of completed playthroughs is equal to some value.
    return if_new_game_count_comparison(output_condition, 0, completion_count_comparison)


def if_new_game_count_greater_than_or_equal(output_condition, min_completion_count):
    # Checks if count of completed playthroughs is greater than or equal to some value.
    return if_new_game_count_comparison(output_condition, 4, min_completion_count)


def if_new_game_count_comparison(output_condition, comparison_type, completion_count_comparison):
    # Checks count of completed playthroughs and compares to value.
    event_format = ['   3', '17', 'bBB']
    return __format_event(event_format, output_condition, comparison_type, completion_count_comparison)


# 18
def if_action_button_state_and_line_segment(output_condition, category, target_entity_id, reaction_angle, damipoly_id,
                                            reaction_distance, help_id, reaction_attribute, pad_id,
                                            line_segment_endpoint_id):
    # Checks state of action button (A on the Xbox controller) and, I assume,
    # check if player forward line segment intersects entity?
    # TODO: Check usage of this.
    event_format = ['   3', '19', 'biifhfiBi']
    return __format_event(event_format, output_condition, category, target_entity_id, reaction_angle, damipoly_id,
                          reaction_distance, help_id, reaction_attribute, pad_id, line_segment_endpoint_id)


# 19
def if_action_button_state_and_line_segment_in_boss(output_condition, category, target_entity_id, reaction_angle,
                                                    damipoly_id, reaction_distance, help_id, reaction_attribute, pad_id,
                                                    line_segment_endpoint_id):
    # Checks state of action button (A on the Xbox controller) and, I assume,
    # check if player forward line segment intersects entity? This is the boss
    # room version.
    # TODO: Check usage of this.
    event_format = ['   3', '19', 'biifhfiBi']
    return __format_event(event_format, output_condition, category, target_entity_id, reaction_angle, damipoly_id,
                          reaction_distance, help_id, reaction_attribute, pad_id, line_segment_endpoint_id)


# 20
def if_event_flag_value_comparison(output_condition, left_event_flag_id, left_number_bits, comparison_type,
                                   right_event_flag_id, right_number_bits):
    # Check comparison of two event flag values.
    event_format = ['   3', '20', 'biBBiB']
    return __format_event(event_format, output_condition, left_event_flag_id, left_number_bits, comparison_type,
                          right_event_flag_id, right_number_bits)


# 21
def if_owns_DLC(output_condition):
    # Check if player owns Artorias of the Abyss DLC expansion.
    # NOTE: Again, no generic function here.
    event_format = ['   3', '21', 'bB']
    return __format_event(event_format, output_condition, 1)


def if_does_not_own_DLC(output_condition):
    # Check if player does not own Artorias of the Abyss DLC expansion.
    event_format = ['   3', '21', 'bB']
    return __format_event(event_format, output_condition, 0)


# 22
def if_online(output_condition):
    return if_online_state(output_condition, 1)


def if_offline(output_condition):
    return if_online_state(output_condition, 0)


def if_online_state(output_condition, online_state):
    # Check if player is online (1) or offline (0).
    event_format = ['   3', '22', 'bB']
    return __format_event(event_format, output_condition, online_state)


""" 4: EXECUTION CONDITIONS (CHARACTER) """


# 0
def if_entity_dead(output_condition, entity_id):
    return if_entity_death_state(output_condition, entity_id, 1)


def if_entity_alive(output_condition, entity_id):
    return if_entity_death_state(output_condition, entity_id, 0)


def if_entity_death_state(output_condition, entity_id, required_state):
    # Check if entity is alive (0) or dead (1).
    event_format = ['   4', '00', 'biB']
    return __format_event(event_format, output_condition, entity_id, required_state)


# 1
def if_entity_hostile(output_condition, entity_id, attacking_entity_id):
    # Check if entity is hostile toward attacking entity (I assume).
    # TODO: Check usage to confirm that the hostility is directed from the
    # first entity to the second.
    event_format = ['   4', '01', 'bii']
    return __format_event(event_format, output_condition, entity_id, attacking_entity_id)


# 2
def if_entity_health_equal(output_condition, entity_id, health_comparison):
    # Check if entity health == value.
    return if_entity_health_comparison(output_condition, entity_id, 0, health_comparison)


def if_entity_health_not_equal(output_condition, entity_id, health_comparison):
    # Check if entity health != value.
    return if_entity_health_comparison(output_condition, entity_id, 1, health_comparison)


def if_entity_health_greater_than(output_condition, entity_id, health_comparison):
    # Check if entity health > value.
    return if_entity_health_comparison(output_condition, entity_id, 2, health_comparison)


def if_entity_health_less_than(output_condition, entity_id, health_comparison):
    # Check if entity health < value.
    return if_entity_health_comparison(output_condition, entity_id, 3, health_comparison)


def if_entity_health_greater_than_or_equal(output_condition, entity_id, health_comparison):
    # Check if entity health >= value.
    return if_entity_health_comparison(output_condition, entity_id, 4, health_comparison)


def if_entity_health_less_than_or_equal(output_condition, entity_id, health_comparison):
    # Check if entity health <= value.
    return if_entity_health_comparison(output_condition, entity_id, 5, health_comparison)


def if_entity_health_comparison(output_condition, entity_id, comparison_type, health_comparison):
    # Check comparison of entity health with specified value between 0 and 1.
    """
    Comparison type list:
        0: "==",
        1: "!=",
        2: ">",
        3: "<",
        4: ">=",
        5: "<="
    """
    event_format = ['   4', '02', 'bibf']
    return __format_event(event_format, output_condition, entity_id, comparison_type, health_comparison)


# 3
def if_character_human(output_condition, entity_id):
    # Check if specified character entity is human ("Survival").
    return if_character_type(output_condition, entity_id, 0)


def if_character_hollow(output_condition, entity_id):
    # Check if specified character entity is hollow ("Gray Ghost").
    return if_character_type(output_condition, entity_id, 8)


def if_character_type(output_condition, entity_id, character_type):
    # Check if specified character entity is of given type.
    """
    Character type list:
        0: "Survival",
        1: "White Ghost",
        2: "Black Ghost",
        8: "Gray Ghost",
        12: "Intruder"
    """
    event_format = ['   4', '03', 'bib']
    return __format_event(event_format, output_condition, entity_id, character_type)


# 4
def if_entity_targeting(output_condition, entity_id, targeted_entity_id):
    # Check if first entity is targeting second.
    return if_entity_target_state(output_condition, entity_id, targeted_entity_id, 1)


def if_entity_not_targeting(output_condition, entity_id, targeted_entity_id):
    # Check if first entity is not targeting second.
    return if_entity_target_state(output_condition, entity_id, targeted_entity_id, 0)


def if_entity_target_state(output_condition, entity_id, targeted_entity_id, required_target_state):
    # Check if first entity is (1) or is not (0) targeting the second entity.
    # Note this is HPR's speculation. Not sure if player target lock counts as
    # 'targeting' for this, or if it's just for NPC AI targets.
    # TODO: Check usage.
    event_format = ['   4', '04', 'biiB']
    return __format_event(event_format, output_condition, entity_id, targeted_entity_id, required_target_state)


# 5
def if_entity_has_special_effect(output_condition, entity_id, special_effect_id):
    # Check if entity has specified special effect.
    return if_entity_special_effect_state(output_condition, entity_id, special_effect_id, 1)


def if_entity_does_not_have_special_effect(output_condition, entity_id, special_effect_id):
    # Check if entity does not have specified special effect.
    return if_entity_special_effect_state(output_condition, entity_id, special_effect_id, 0)


def if_entity_special_effect_state(output_condition, entity_id, special_effect_id, required_state):
    # Check if entity has (1) or doesn't have (0) specified special effect.
    event_format = ['   4', '05', 'biiB']
    return __format_event(event_format, output_condition, entity_id, special_effect_id, required_state)


# 6
def if_NPC_part_health_less_than_or_equal(output_condition, entity_id, part_NPC_type, health_threshold):
    return if_NPC_part_health_comparison(output_condition, entity_id, part_NPC_type, health_threshold, 5)


def if_NPC_part_health_comparison(output_condition, entity_id, part_NPC_type, health_threshold, comparison_type):
    # Check comparison of NPC health part. I only really plan on copying this.
    event_format = ['   4', '06', 'biiib']
    return __format_event(event_format, output_condition, entity_id, part_NPC_type, health_threshold, comparison_type)


# 7
def if_entity_backread_enabled(output_condition, entity_id):
    return if_entity_backread_state(output_condition, entity_id, 1)


def if_entity_backread_disabled(output_condition, entity_id):
    return if_entity_backread_state(output_condition, entity_id, 0)


def if_entity_backread_state(output_condition, entity_id, loaded):
    # Check if entity is loaded in background (presumably) or not.
    event_format = ['   4', '07', 'biB']
    return __format_event(event_format, output_condition, entity_id, loaded)


# 8
def if_event_message_ID_match(output_condition, entity_id, event_message_id):
    return if_event_message_ID_match_state(output_condition, entity_id, event_message_id, 1)


def if_event_message_ID_does_not_match(output_condition, entity_id, event_message_id):
    return if_event_message_ID_match_state(output_condition, entity_id, event_message_id, 0)


def if_event_message_ID_match_state(output_condition, entity_id, event_message_id, match_state):
    # Check if entity event message ID does or does not match another event
    # message ID. Not really sure when I'd use this.
    # TODO: Check current usage for examples.
    event_format = ['   4', '08', 'biiB']
    return __format_event(event_format, output_condition, entity_id, event_message_id, match_state)


# 9
def if_ai_state(output_condition, entity_id, required_ai_state):
    # Check if entity's AI state has a certain value.
    """
    AI state list:
        0: "Normal",
        1: "Recognition",
        2: "Alert",
        3: "Battle"
    """
    event_format = ['   4', '09', 'biB']
    return __format_event(event_format, output_condition, entity_id, required_ai_state)


# 10
def if_skull_lantern_activated(output_condition):
    # Check if player is using (holding out) the Skull Lantern. Currently used
    # to alter enemy aggression in Tomb of the Giants, I think. No need for a
    # generic version.
    event_format = ['   4', '10', 'bB']
    return __format_event(event_format, output_condition, 1)


def if_skull_lantern_not_activated(output_condition):
    # Check if player is using (holding out) the Skull Lantern. Currently used
    # to alter enemy aggression in Tomb of the Giants, I think. No need for a
    # generic version.
    event_format = ['   4', '10', 'bB']
    return __format_event(event_format, output_condition, 0)


# 11
def if_player_class(output_condition, class_name):
    # Check if player class is the specific name. You can pass the class as a
    # string rather than an enum.
    """
    Class list:
        0: "Warrior",
        1: "Knight",
        2: "Wanderer",
        3: "Thief",
        4: "Bandit",
        5: "Hunter",
        6: "Sorcerer",
        7: "Pyromancer",
        8: "Cleric",
        9: "Deprived",
    10-27 include temporary classes not used.
    """
    class_list = ['warrior', 'knight', 'wanderer', 'thief', 'bandit', 'hunter',
                  'sorcerer', 'pyromancer', 'cleric', 'deprived']
    if isinstance(class_name, str):
        if class_name.lower() in class_list:
            class_name = class_list.index(class_name.lower())
        else:
            raise ValueError('Unrecognized class name.')
    event_format = ['   4', '11', 'bB']
    return __format_event(event_format, output_condition, class_name)


# 12
def if_player_covenant(output_condition, covenant_name):
    # Check if player covenant is the specified name. You can pass the covenant
    # as a string rather than an enum. Pass 'none' or 0 for no covenant.
    """
    Covenant list:
        0: "None",
        1: "Way of White",
        2: "Princess's Guard",
        3: "Warrior of Sunlight",
        4: "Darkwraith",
        5: "Path of the Dragon",
        6: "Gravelord Servant",
        7: "Forest Hunter",
        8: "Darkmoon Blade",
        9: "Chaos Servant"
    """
    covenant_list = ['none', 'way of white', 'princess\'s guard',
                     'warrior of sunlight', 'darkwraith', 'path of the dragon',
                     'gravelord servant', 'forest hunter', 'darkmoon blade',
                     'chaos servant']
    if isinstance(covenant_name, str):
        if covenant_name.lower() in covenant_list:
            covenant_name = covenant_list.index(covenant_name.lower())
        else:
            raise ValueError('Unrecognized class name.')
    event_format = ['   4', '11', 'bB']
    return __format_event(event_format, output_condition, covenant_name)


# 13
def if_player_soul_level_greater_than_or_equal(output_condition, comparison_value):
    return if_player_soul_level_comparison(output_condition, 4, comparison_value)


def if_player_soul_level_less_than_or_equal(output_condition, comparison_value):
    return if_player_soul_level_comparison(output_condition, 5, comparison_value)


def if_player_soul_level_comparison(output_condition, comparison_type, comparison_value):
    # Check if player soul level comparison returns true.
    event_format = ['   4', '13', 'bBI']
    return __format_event(event_format, output_condition, comparison_type, comparison_value)


# 14
def if_entity_health_value_equal(output_condition, entity_id, comparison_value):
    return if_entity_health_value_comparison(output_condition, entity_id, 0, comparison_value)


def if_entity_health_value_not_equal(output_condition, entity_id, comparison_value):
    return if_entity_health_value_comparison(output_condition, entity_id, 1, comparison_value)


def if_entity_health_value_greater_than(output_condition, entity_id, comparison_value):
    return if_entity_health_value_comparison(output_condition, entity_id, 2, comparison_value)


def if_entity_health_value_less_than(output_condition, entity_id, comparison_value):
    return if_entity_health_value_comparison(output_condition, entity_id, 3, comparison_value)


def if_entity_health_value_greater_than_or_equal(output_condition, entity_id, comparison_value):
    return if_entity_health_value_comparison(output_condition, entity_id, 4, comparison_value)


def if_entity_health_value_less_than_or_equal(output_condition, entity_id, comparison_value):
    return if_entity_health_value_comparison(output_condition, entity_id, 5, comparison_value)


def if_entity_health_value_comparison(output_condition, entity_id, comparison_type, comparison_value):
    # Check if absolute entity health (NOT ratio) comparison returns true.
    event_format = ['   4', '14', 'biBi']
    return __format_event(event_format, output_condition, entity_id, comparison_type, comparison_value)


""" 5: EXECUTION CONDITIONS (OBJECT) """


# 0
def if_object_destroyed(output_condition, entity_id):
    return if_object_destruction_state(output_condition, 1, entity_id)


def if_object_not_destroyed(output_condition, entity_id):
    return if_object_destruction_state(output_condition, 0, entity_id)


def if_object_destruction_state(output_condition, required_state, entity_id):
    # Check if object is destroyed or not.
    event_format = ['   5', '00', 'bBi']
    return __format_event(event_format, output_condition, required_state, entity_id)


# 1
def if_entity_damaged_object(output_condition, entity_id, attacker_entity_id):
    # Check if object was damaged by a specific attacker.
    event_format = ['   5', '01', 'bii']
    return __format_event(event_format, output_condition, entity_id, attacker_entity_id)


# 2
def if_object_activated(output_condition, execution_event_id):
    # Check if object was activated.
    event_format = ['   5', '02', 'bi']
    return __format_event(event_format, output_condition, execution_event_id)


""" 11: EXECUTION CONDITIONS (HIT) """


# 0
def if_player_moving_on_hitbox(output_condition, hitbox_entity_id):
    # Check if a local player is moving on the specified hitbox.
    event_format = ['   5', '00', 'bi']
    return __format_event(event_format, output_condition, hitbox_entity_id)


# 1
def if_player_running_on_hitbox(output_condition, hitbox_entity_id):
    # Check if a local player is running on the specified hitbox.
    event_format = ['   5', '01', 'bi']
    return __format_event(event_format, output_condition, hitbox_entity_id)


# 2
def if_player_standing_on_hitbox(output_condition, hitbox_entity_id):
    # Check if a plocal player is standing on the specified hitbox.
    event_format = ['   5', '02', 'bi']
    return __format_event(event_format, output_condition, hitbox_entity_id)


""" PARAMETER SUBSTITUTION INSTRUCTIONS """


def load_arg(write_from_offset, read_from_offset, bytes_length):
    # Loads bytes from event initialization arguments (see 0[00]) into the
    # instruction immediately above. Reading starts at read_from_offset and
    # writing starts at write_from_offset, and bytes_length bytes are written.
    print('    ^({} <- {}, {})'.format(write_from_offset, read_from_offset, bytes_length))


"""
Parameter substitution instruction format:
    ^(X <- Y, Z)

    X : output_offset (offset in instruction arguments to start writing into)
    Y : input_offset (offset in event arguments to start writing from)
    Z : write_length (number of bytes to write)

HPR's code automatically supplies the substitution instruction's first
argument, which specifies which event instruction line to write into (it takes
the last instruction).

"""

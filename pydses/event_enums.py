"""
@author: grimrhapsody
"""

from enum import Enum


""" CONDITION REGISTERS """


class condition(Enum):
    continue_execution = 0
    and1 = 1
    and2 = 2
    and3 = 3
    and4 = 4
    and5 = 5
    and6 = 6
    and7 = 7
    or1 = -1
    or2 = -2
    or3 = -3
    or4 = -4
    or5 = -5
    or6 = -6
    or7 = -7


""" HELPER CONSTANTS """

CONT = condition.continue_execution
AND1 = condition.and1
AND2 = condition.and2
AND3 = condition.and3
AND4 = condition.and4
AND5 = condition.and5
AND6 = condition.and6
AND7 = condition.and7
OR1 = condition.or1
OR2 = condition.or2
OR3 = condition.or3
OR4 = condition.or4
OR5 = condition.or5
OR6 = condition.or6
OR7 = condition.or7


""" EVENT ENUM DEFINITIONS """

class ai_status_type(Enum):
    normal = 0
    recognition = 1
    alert = 2
    battle = 3

class bitop(Enum):
    add = 0
    delete = 1
    invert = 2

# ENUM_BOOL omitted for lack of necessity and conflict with python keywords

class button_number(Enum):
    one_button = 1
    two_button = 2
    no_button = 6

class button_type(Enum):
    yes_no = 0
    ok_cancel = 1

class category(Enum):
    objects = 0
    areas = 1
    characters = 2

class character_type(Enum):
    """
    This name chosen over the translation of the original ("survival"), since it is found in event_define.lua
    as CHR_TYPE_LivePlayer (and that's a translation by From Software themselves)
    """
    live_player = 0
    white_ghost = 1
    black_ghost = 2
    gray_ghost = 8
    intruder = 10

class character_update_rate(Enum):
    never = -1
    always = 0
    every_two_frames = 2
    every_five_frames = 5

class class_type(Enum):
    warrior = 0
    knight = 1
    wanderer = 2
    thief = 3
    bandit = 4
    hunter = 5
    sorcerer = 6
    pyromancer = 7
    cleric = 8
    deprived = 9
    temp_warrior = 20
    temp_knight = 21
    temp_sorcerer = 22
    temp_pyromancer = 23
    chi_warrior = 24
    chi_knight = 25
    chi_sorcerer = 26
    chi_pyromancer = 27


class comparison_type(Enum):
    equal = 0
    not_equal = 1
    greater_than = 2
    less_than = 3
    greater_than_or_equal = 4
    less_than_or_equal = 5


# ENUM_CONDITION_STATE omitted because it's the same as ENUM_BOOL


class contained(Enum):
    outside = 0
    inside = 1


class cutscene_type(Enum):
    skippable = 0
    unskippable = 1
    skippable_with_fade_out = 8
    unskippable_with_fade_out = 10


class damage_target_type(Enum):
    character = 1
    map = 2
    character_and_map = 3


# ENUM_DEATH_STATUS omitted since it's "bool IsDead"


# ENUM_ENABLE_STATE omitted since it's "bool IsEnabled"


class event_end_type(Enum):
    end = 0
    restart = 1


class flag_type(Enum):
    event_flag = 0
    event = 1
    event_with_slot = 2


class interpolation_state(Enum):
    interpolated = 0
    not_interpolated = 1


class equipment_type(Enum):
    weapon = 0
    armor = 1
    accessory = 2
    item = 3
    mask = 4 # from event_define.lua


class logic_op_type(Enum):
    all_on = 0
    all_off = 1
    not_all_off = 2
    not_all_on = 3


class multiplayer_state(Enum):
    host = 0
    client = 1
    multiplayer = 2
    singleplayer = 3


class navimesh_type(Enum):
    solid = 1
    exit = 2
    obstacle = 4
    wall = 8
    wall_touching_floor = 32
    landing_point = 64
    event = 128
    cliff = 256
    wide = 512
    ladder = 1024
    hole = 2048
    door = 4096
    closed_door = 8192


# ENUM_ON_OFF omitted for obvious reasons


class on_off_change(Enum):
    off = 0
    on = 1
    change = 2


# ENUM_OWN_STATE omitted; "bool IsOwner"


class reaction_attribute(Enum):
    live_player_and_gray = 48
    all = 255


class sos_sign_type(Enum):
    blue_eye_sign = 0
    black_eye_sign = 1
    red_eye_sign = 2
    detection_sign = 3
    white_help_sign = 4
    black_help_sign = 5


class site_type(Enum):
    part1 = 1
    part2 = 2
    part3 = 3
    part4 = 4
    part5 = 5
    part6 = 6
    weakpoint = 7
    part7 = 8
    part8 = 9


class sound_type(Enum):
    a_environmental_sound = 0
    c_character_motion = 1
    f_menu_se = 2
    o_object = 3
    p_poly_dedicated_se = 4
    s_sfx = 5
    m_bgm = 6
    v_voice = 7
    x_floor_material_dependant = 8
    b_armor_material_dependant = 9
    g_ghost = 10


class statue_type(Enum):
    stone = 0
    crystal = 1


class team_type(Enum):
    """
    Names taken from ai_define.lua:
    TEAM_TYPE_None = 0
    TEAM_TYPE_Live = 1
    TEAM_TYPE_WhiteGhost = 2
    TEAM_TYPE_BlackGhost = 3
    TEAM_TYPE_GlayGhost = 4
    TEAM_TYPE_WanderGhost = 5
    TEAM_TYPE_Enemy = 6
    TEAM_TYPE_Boss = 7
    TEAM_TYPE_Friend = 8
    TEAM_TYPE_AngryFriend = 9
    TEAM_TYPE_Decoy = 10
    TEAM_TYPE_DecoyLike = 11
    TEAM_TYPE_BattleFriend = 12
    TEAM_TYPE_Intruder = 13
    TEAM_TYPE_Neutral = 14
    TEAM_TYPE_Charm = 15
    """
    none = 0
    live = 1
    white_ghost = 2
    black_ghost = 3
    gray_ghost = 4
    wander_ghost = 5
    enemy = 6
    boss = 7
    friend = 8
    angry_friend = 9
    decoy = 10
    decoy_like = 11
    battle_friend = 12
    intruder = 13
    neutral = 14
    charm = 15


class tendency_type(Enum):
    white = 0
    black = 1


class text_banner_type(Enum):
    """
    Some values taken from event_define.lua:
    TEXT_TYPE_KillDemon = 1
    TEXT_TYPE_Dead = 2
    TEXT_TYPE_Revival = 3
    TEXT_TYPE_SoulGet = 4
    TEXT_TYPE_TargetClear = 5
    TEXT_TYPE_GhostDead = 6
    TEXT_TYPE_BlackClear = 7
    TEXT_TYPE_MapName = 8
    TEXT_TYPE_MagicResurrection = 9
    TEXT_TYPE_RingNormalResurrection = 10
    TEXT_TYPE_RingCurseResurrection = 11
    TEXT_TYPE_Congratulations = 12
    TEXT_TYPE_Bonfire = 13
    """
    boss_defeated = 0
    you_died = 1
    resurrection = 2
    souls_retrieved = 3
    target_defeated = 4
    ghost_death = 5
    black_ghost_death = 7
    map_name = 8
    magic_revival = 9
    ring_revival = 10
    rare_ring_revival = 11
    congratulations = 12
    bonfire_lit = 13
    arena_victory = 15
    arena_loss = 16
    arena_draw = 17


class update_auth(Enum):
    normal = 0
    forced = 4095


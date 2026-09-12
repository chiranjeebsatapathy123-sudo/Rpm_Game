import math

def xp_for_level(level):
    """
    Returns the total XP required to REACH the given level.
    Level 1 requires 0 XP.
    """
    if level <= 1:
        return 0
    total = 0
    for l in range(1, level):
        total += round(100 * (l ** 1.6))
    return total

def calculate_level(total_xp):
    """
    Given a total_xp, calculate what level the character is.
    """
    level = 1
    while True:
        next_level_xp = xp_for_level(level + 1)
        if total_xp >= next_level_xp:
            level += 1
        else:
            break
    return level

def xp_for_next_level(level):
    """
    Returns the XP needed to go from 'level' to 'level + 1'
    """
    return round(100 * (level ** 1.6))

def current_level_xp(total_xp):
    """
    Returns how much XP the character has accumulated in their current level.
    """
    level = calculate_level(total_xp)
    base_xp = xp_for_level(level)
    return total_xp - base_xp

def level_progress(total_xp):
    """
    Returns the percentage progress (0.0 to 1.0) towards the next level.
    """
    level = calculate_level(total_xp)
    current_xp = current_level_xp(total_xp)
    required_xp = xp_for_next_level(level)
    
    if required_xp == 0:
        return 0.0
    return min(1.0, current_xp / required_xp)

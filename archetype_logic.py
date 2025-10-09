def determine_archetype(data):
    cube=(data.get('cube') or '').lower()
    if 'big' in cube or 'gold' in cube: return 'visionary'
    elif 'transparent' in cube or 'glass' in cube: return 'observer'
    elif 'floating' in cube or 'soft' in cube: return 'dreamer'
    else: return 'alchemist'

CARD_DATA = [

# ==================================================================================================
# NOTHINGNESS
# ==================================================================================================

    {
        'name': 'Wait',
        'type': 'nothingness',
        'rarity': '',
        'target': 'self',
        'recovery_cost': 5,
        'description': 'Do nothing just yet.',
        'stat_boosts': {},
        'is_consumable': False,
        'is_wait': True,
        'illust': """
+                 +
    \  \ |   /     
        \          
    -    X    -    
        /          
    /    |   \     
+                 +
"""
    },
    {
        'name': 'Wallow',
        'type': 'nothingness',
        'rarity': '',
        'target': 'self',
        'recovery_cost': 6,
        'description': 'You should have been more prepared! Do nothing.',
        'stat_boosts': {},
        'illust': """
+                 +
    \  \ |   /     
        \          
    -    X    -    
        /          
    /    |   \     
+                 +
"""
    },

# ==================================================================================================
# POTIONS 
# ==================================================================================================

    {
        'name': 'Potion',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 15,
        'heal_power': 6.0,
        'give_heal_power': 6.0,
        'description': 'Heals an ally. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+------\---/------+
|      |   |      |
|     / *   \     |
|    | o * * |    |
|    |   * o |    |
|     \_____/     |
+-----------------+
"""
    },
    {
        'name': 'Sour Potion',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 1,
        'heal_power': 3.0,
        'give_heal_power': 3.0,
        'description': 'Rapidly heals an ally. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+------\~~~/------+
|      | . |      |
|     / * . \     |
|    | o.*.* |    |
|    |. .* o |    |
|     \_____/     |
+-----------------+
"""
    },
    {
        'name': 'Syrupy Potion',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 30,
        'heal_power': 30.0,
        'give_heal_power': 30.0,
        'description': 'Slugishly heals an ally. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+------\-~-/------+
|      || ||      |
|     //0  )\     |
|    ||o O .||    |
|    ||  . o||    |
|     \(___//     |
+-----------------+
"""
    },
    {
        'name': 'Rotten Egg',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 5,
        'heal_power': 3,
        'give_heal_power': 3,
        'revive': True,
        'description': 'Rot that repels even death. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+-----------------+
|      ,/`\,      |
|     / *   \     |
|    | #   ZZ|    |
|    ( *  /##)    |
|     \  ###/     |
+-----------------+
"""
    },

# ==================================================================================================
# ARMOR
# ==================================================================================================

    {
        'name': 'Shield',
        'type': 'armor',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 10,
        'status_effect_target_stat': 'brute_resistance',
        'status_effect_power': 3,
        'status_effect_duration': 15,
        'description': 'Shields the user from harm.',
        'stat_boosts': {'brute_resistance': 0.3},
        'illust': """
+-----------------+
|      ------     |
|     / /--\ \    |
|     | |  | |    |
|     \  \/  /    |
|      \____/     |
+-----------------+
"""
    },
    {
        'name': 'Shield Spike',
        'type': 'armor',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 12,
        'description': 'Spikes an enemy while shielding.',
        'damage_type': 'melee_damage',
        'damage_power': 1.0,
        'stat_boosts': {'brute_resistance': 0.3},
        'effects': [
            {
                'target': 'self',
                'status_effect_target_stat': 'brute_resistance',
                'status_effect_power': 2,
                'status_effect_duration': 15,
            },
        ],
        'illust': """
+-----------------+
|      ------     |
|     />/--\>\    |
|     | | >| |    |
|     \ >\/> /    |
|      \____/     |
+-----------------+
"""
    },
    {
        'name': 'Light Clothes',
        'type': 'armor',
        'rarity': 'mundane',
        'target': 'self',
        'recovery_cost': 5,
        'description': 'Protective and nimble garments.',
        'stat_boosts': {'brute_resistance': 0.2, 'melee_resistance': 0.3, 'ranged_resistance': 0.3, 'nimbleness': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'brute_resistance',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
            {
                'status_effect_target_stat': 'nimbleness',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            }
        ]
    },
    {
        'name': 'Favored Clothes',
        'type': 'armor',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 5,
        'description': 'Protective and nimble garments.',
        'stat_boosts': {'brute_resistance': 0.2, 'melee_resistance': 0.3, 'ranged_resistance': 0.3, 'nimbleness': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'brute_resistance',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
            {
                'status_effect_target_stat': 'nimbleness',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            }
        ]
    },

# ==================================================================================================
# MELEE DAMAGE 
# ==================================================================================================

    {
        'name': 'Slash',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'melee_damage',
        'damage_power': 2.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Favored Slash',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'melee_damage',
        'damage_power': 2.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Favored Heavy Slash',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 20,
        'damage_type': 'melee_damage',
        'damage_power': 3.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Heavy Slash',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 20,
        'damage_type': 'melee_damage',
        'damage_power': 3.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Favored Light Slash',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 5,
        'damage_type': 'melee_damage',
        'damage_power': 1.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Light Slash',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 5,
        'damage_type': 'melee_damage',
        'damage_power': 1.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Honed Slash',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 14,
        'damage_type': 'melee_damage',
        'damage_power': 3,
        'description': 'Powerful attack.',
        'stat_boosts': {'melee_damage': 0.5},
        'illust': """
+-----------------+
\     - -   _.    |
\      - - / |    |
|    -  . ///     \\
|        \//      \\
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Flowering Stab',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'melee_damage',
        'damage_power': 1,
        'description': 'A quick attack that boosts the next.',
        'stat_boosts': {'melee_damage': 0.3, 'nimbleness': 0.3},
        'effects': [
            {
                'target': 'self',
                'status_effect_target_stat': 'melee_damage',
                'status_effect_power': 2,
                'status_effect_duration': 15,
            },
        ],
        'illust': """
+-----------------+
|       \  \      |
|     l,          |
|  o==D)=======>  |
|     l`          |
|       /  /      |
+-----------------+
"""
    },
    {
        'name': 'Parry',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 5,
        'description': 'A quick boost to the user\'s defenses.',
        'stat_boosts': {'brute_resistance': 0.3, 'melee_damage': 0.3, 'nimbleness': 0.3},
        'effects': [
            {
                'status_effect_target_stat': 'brute_resistance',
                'status_effect_power': 1,
                'status_effect_stat': 'melee_damage',
                'status_effect_duration': 10,
            },
        ],
        'illust': """
+-----------------+
|       \  \      |
|     l,          |
|  o==D)=======>  |
|     l`          |
|       /  /      |
+-----------------+
"""
    },
    {
        'name': 'Dragonsbane',
        'type': 'weapon',
        'rarity': 'peerless',
        'target': 'enemy',
        'recovery_cost': 20,
        'damage_type': 'melee_damage',
        'damage_power': 2.0,
        'description': 'An assault of shadow and steel.',
        'effects': [
            {
                'damage_type': 'void_intensity',
                'damage_power': 2.0,
            }
        ],
        'illust': """
+-----------------+
|    - - -~S_.    |
|     - ,~S/ |S   |
|   -, . S///S~   |
|        \//S~    |
|     , //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Backstab',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'melee_damage',
        'damage_power': 1.0,
        'description': 'Leaves the target vulnerable.',
        'stat_boosts': {'melee_damage': 0.2, 'survival_intensity': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'melee_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            },
            {
                'status_effect_target_stat': 'ranged_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            },
            {
                'status_effect_target_stat': 'void_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            },
        ],
        'illust': """
+-----------------+
|       ||        |
|     =<__>=      |
|       \ \       |
|       \ )       |
|       )/        |
+-----------------+
"""
    },


# ==================================================================================================
# RANGED DAMAGE
# ==================================================================================================

    {
        'name': 'Archery',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 2.0,
        'description': 'Standard attack.',
        'stat_boosts': {'ranged_damage': 0.2, 'nimbleness': 0.2},
        'illust': """
+-----------------+
|                 |
|   >>======>     |
|                 |
|       >>======> |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Favored Archery',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 2.0,
        'description': 'Standard attack.',
        'stat_boosts': {'ranged_damage': 0.2, 'nimbleness': 0.2},
        'illust': """
+-----------------+
|                 |
|   >>======>     |
|                 |
|       >>======> |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Heavy Shot',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 1.0,
        'description': 'Leaves the target vuln. to melee.',
        'stat_boosts': {'ranged_damage': 0.2, 'melee_damage': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'melee_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            }
        ],
        'illust': """
+-----------------+
|                 |
|  \`\        _   |
| ===N=======(%)> |
|  ///            |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Whistling Shot',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 14,
        'damage_type': 'ranged_damage',
        'damage_power': 1.0,
        'description': 'Leaves the target vulne. at range.',
        'stat_boosts': {'ranged_damage': 0.4},
        'effects': [
            {
                'status_effect_target_stat': 'ranged_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            }
        ],
        'illust': """
+-----------------+
|                 |
|  \`\        _   |
| ===N=======>K:> |
|  ///            |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Crescent Shot',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 1.0,
        'description': 'Leaves the target vulnerable to moon.',
        'stat_boosts': {'ranged_damage': 0.2, 'moon_intensity': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'moon_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            }
        ],
        'illust': """
+-----------------+
|                 |
|  \`\         .  |
| ===N=======N(C  |
|  ///         `  |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Burning Shot',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 1.0,
        'description': 'Leaves the target vulnerable to star.',
        'stat_boosts': {'ranged_damage': 0.2, 'star_intensity': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'star_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            }
        ],
        'illust': """
+-----------------+
|         ~ ;$    |
|  \`\  ~   S.;   |
| ===N=======>->  |
|  ///       `~   |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Broken Shot',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 1.0,
        'description': 'Leaves the target vulnerable to void.',
        'stat_boosts': {'ranged_damage': 0.2, 'void_intensity': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'void_vulnerability',
                'status_effect_power': 2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            }
        ],
        'illust': """
+-----------------+
|                 |
|  \`\            |
| ===N========Z`  |
|  ///            |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Pinning Shot',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 1.0,
        'description': 'An attack that slows the target.',
        'stat_boosts': {'ranged_damage': 0.4, 'nimbleness': 0.4},
        'effects': [
            {
                'status_effect_target_stat': 'nimbleness',
                'status_effect_power': -2,
                'status_effect_duration': 5,
                'status_effect_duration_stat': 'survival_intensity',
            }
        ],
        'illust': """
+-----------------+
|                 |
|  \`\        .   |
| ===N========>-> |
|  ///        `   |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Honed Archery',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 14,
        'damage_type': 'ranged_damage',
        'damage_power': 3,
        'description': 'Precise attack.',
        'stat_boosts': {'ranged_damage': 0.5},
        'illust': """
+-----------------+
|               >>=
|   >>======>     |
=>                |
|       >>======> |
|                 |
+-----------------+
"""
    },

# ==================================================================================================
# SURVIVAL INTENSITY
# ==================================================================================================

    {
        'name': 'Simple Trap',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 5,
        'damage_type': 'survival_intensity',
        'damage_power': 1.0,
        'description': 'A scout\'s first attack.',
        'stat_boosts': {'survival_intensity': 0.2, 'ranged_damage': 0.2, 'nimbleness': 0.2},
        'illust': """
+-----------------+
|  "  / .   ` /_//|
| "  / .   .     ||
|   /   `   .  / j|
|"|-------------| |
|/  .    .  . /" "|
+-----------------+
"""
    },
    {
        'name': 'First Aid',
        'type': 'trinket',
        'rarity': 'interesting',
        'target': 'ally',
        'recovery_cost': 10,
        'heal_power': 1.0,
        'heal_stat': 'survival_intensity',
        'description': 'Heals an ally.',
        'stat_boosts': {'survival_intensity': 0.3, 'haleness': 0.2},
        'illust': """
+-----------------+
|_____    /\      |
|-----\-\/ //-----|
|      %(&n)%     |
|------/|u/\------|
|       |/   \____|
+-----------------+
"""
    },
    {
        'name': 'Cover of Night',
        'type': 'scroll',
        'rarity': 'peerless',
        'target': 'all_enemies',
        'recovery_cost': 10,
        'description': 'Protects all allies.',
        'effects': [
            {
                'status_effect_target_stat': 'melee_resistance',
                'status_effect_power': 1,
                'status_effect_duration': 10,
                'status_effect_duration_stat': 'survival_intensity',
            },
            {
                'status_effect_target_stat': 'ranged_resistance',
                'status_effect_power': 1,
                'status_effect_duration': 10,
                'status_effect_duration_stat': 'survival_intensity',
            },
            {
                'status_effect_target_stat': 'void_resistance',
                'status_effect_power': 1,
                'status_effect_duration': 10,
                'status_effect_duration_stat': 'survival_intensity',
            },
        ],
        'illust': """
+-----------------+
| |:      .   . . |
|. \`       .  .  |
| .  ^  . /\ ^ .  |
|/\ /|\ /\/\/^\  ^|
|/\//|\^/\/\/|\^/^|
+-----------------+
"""
    },

# ==================================================================================================
# MAGIC
# ==================================================================================================

    {
        'name': 'Elementary Magic',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 20,
        'effects': [
            {
                'damage_type': 'moon_intensity',
                'damage_power': 1.0,
            },
            {
                'damage_type': 'star_intensity',
                'damage_power': 1.0,
            },
            {
                'damage_type': 'void_intensity',
                'damage_power': 1.0,
            },
        ],
        'description': 'A student\'s first attack.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
|      ,/(        |
|      '\(     ,  |
| \|/             |
| -*-           ` |
| /|\       ,  '  |
+-----------------+
"""
    },
    {
        'name': 'Magical Opus',
        'type': 'scroll',
        'rarity': 'peerless',
        'target': 'all_enemies',
        'recovery_cost': 30,
        'effects': [
            {
                'damage_type': 'star_intensity',
                'damage_power': 1.0,
            },
            {
                'damage_type': 'void_intensity',
                'damage_power': 1.0,
            },
            {
                'target': 'all_allies',
                'heal_stat': 'moon_intensity',
                'heal_power': 1.0,
            },
        ],
        'description': 'Attacks all enemies & heals all allies.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
|      ,/(        |
|      '\(     ,  |
| \|/             |
| -*-           ` |
| /|\       ,  '  |
+-----------------+
"""
    },

# ==================================================================================================
#  WANDS 
# ==================================================================================================

    {
        'name': 'Driftwood Wand',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'damage_type': 'moon_intensity',
        'damage_power': 1.0,
        'recovery_cost': 15,
        'description': 'Amplifies the user\'s moon magic.',
        'stat_boosts': {'moon_intensity': 0.5},
        'effects': [
            {
                'target': 'self',
                'status_effect_target_stat': 'moon_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 10,
                'status_effect_duration_stat': 'moon_intensity',
            },
        ],
        'illust': """
+-----------------+
|(C     (0)       |
| `      /(       |
|       \|/       |
|       )|        |
|       |(        |
+-----------------+
"""
    },
    {
        'name': 'Ash Wand',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'damage_type': 'star_intensity',
        'damage_power': 1.0,
        'recovery_cost': 15,
        'description': 'Amplifies the user\'s star magic.',
        'stat_boosts': {'star_intensity': 0.5},
        'effects': [
            {
                'target': 'self',
                'status_effect_target_stat': 'star_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 10,
                'status_effect_duration_stat': 'star_intensity',
            },
        ],
        'illust': """
+-----------------+
|    *  (Z)    *  |
| *     \//       |
|    *  ]K    *   |
|  *     )[     * |
|        ](       |
+-----------------+
"""
    },
    {
        'name': 'Fossil Wand',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'damage_type': 'void_intensity',
        'damage_power': 1.0,
        'recovery_cost': 15,
        'description': 'Amplifies the user\'s void magic.',
        'stat_boosts': {'void_intensity': 0.5},
        'effects': [
            {
                'target': 'self',
                'status_effect_target_stat': 'void_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 10,
                'status_effect_duration_stat': 'void_intensity',
            },
        ],
        'illust': """
+-----------------+
|  `    (Q)    ' '|
|       ]]|       |
|`       |:      -|
|       [:|       |
| ,  ,  ||    ,   |
+-----------------+
"""
    },


# ==================================================================================================
# MOON INTENSITY
# ==================================================================================================

    {
        'name': 'Woe',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 20,
        'damage_type': 'moon_intensity',
        'damage_power': 3.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| `'        (  )  |
|       /\   `'   |
|      /  \       |
|      (  )       |
| ^     `'    /\  |
+-----------------+
"""
    },
    {
        'name': 'Wain',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'moon_intensity',
        'damage_power': 1.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| *       \  O \  |
|         | o  |' |
|         /  0 /  |
|        _/'.//   |
|      ./_//'    *|
+-----------------+
"""
    },
    {
        'name': 'Wax',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'ally',
        'recovery_cost': 10,
        'heal_power': 1.0,
        'heal_stat': 'moon_intensity',
        'description': 'Magic spell healing an ally.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| *       \  O \  |
|         | o  |' |
|         /  0 /  |
|        _/'.//   |
|      ./_//'    *|
+-----------------+
"""
    },
    {
        'name': 'Waxing Moonlight',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'all_allies',
        'recovery_cost': 25,
        'heal_power': 2.0,
        'heal_stat': 'moon_intensity',
        'description': 'Magic spell healing all allies.',
        'stat_boosts': {'moon_intensity': 0.4, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| *       \  O \  |
|         | o  |' |
|         /  0 /  |
|        _/'.//   |
|      ./_//'    *|
+-----------------+
"""
    },
    {
        'name': 'New Moon',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'ally',
        'recovery_cost': 15,
        'heal_power': 2.0,
        'heal_stat': 'moon_intensity',
        'description': 'Revives a fallen ally.',
        'stat_boosts': {'moon_intensity': 0.4, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'revive': True,
        'illust': """
+-----------------+
| /             \ |
|'|             |'|
| \             / |
|* \,        .//  |
| * `\,_.__.//' * |
+-----------------+
"""
    },
    {   # Pull of tides is a historical card, not currently the direction for cards I currently want to ship
        'name': 'Pull of Tides',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 25,
        'damage_type': 'moon_intensity',
        'damage_power': 2.0,
        'description': 'Magic spell dealing damage to all enemies.',
        'stat_boosts': {'moon_intensity': 0.4, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| ~  ~     ~    ~ |
|@@~ ~@~@~  ~@@~  |
|uu@~@uuu@~~@uu@@~|
| ~uuu~ ~uuuu~ uuu|
|    .    .    .  |
+-----------------+
"""
    },

# ==================================================================================================
# STAR INTENSITY
# ==================================================================================================

    {
        'name': 'Singe',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'star_intensity',
        'damage_power': 2.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'star_intensity': 0.2, 'star_resistance': 0.3, 'void_vulnerability': 0.3}
    },
    {
        'name': 'Singe Breath',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'all_enemies',
        'recovery_cost': 12,
        'damage_type': 'star_intensity',
        'damage_power': 1,
        'description': 'Magic spell dealing damage to all enemies.',
        'stat_boosts': {'star_intensity': 0.2, 'star_resistance': 0.3, 'void_vulnerability': 0.3}
    },
    {   
        'name': 'Singeing Sunlight',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 25,
        'damage_type': 'star_intensity',
        'damage_power': 2.0,
        'description': 'Deals damage to all enemies.',
        'stat_boosts': {'star_intensity': 0.4, 'star_resistance': 0.3, 'void_vulnerability': 0.3},
        'illust': """
+-----------------+
|--             --|
|~~S/ /      \ \~~|
| S/  S/ $| \S \S |
|S/   S/ |$ \S  \S|
|    S/  $|  \S   |
+-----------------+
"""
    },

# ==================================================================================================
# VOID INTENSITY
# ==================================================================================================

    {
        'name': 'Chill',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'void_intensity',
        'damage_power': 2.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'void_intensity': 0.2, 'void_resistance': 0.3, 'moon_vulnerability': 0.3},
        'illust': """
+-----------------+
| ~~~~~ ~~~~~ ~~~ |
|  ~~~~~~~~~~~~~  |
| ~~~ ~~~~~ ~~~~~ |
|~~~~~~~~~~~~~~~~~|
|#################|
+-----------------+
"""
    },
    {
        'name': 'Chill Breath',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'all_enemies',
        'recovery_cost': 12,
        'damage_type': 'void_intensity',
        'damage_power': 1.0,
        'description': 'Magic spell dealing damage to all enemies.',
        'stat_boosts': {'void_intensity': 0.2, 'void_resistance': 0.3, 'moon_vulnerability': 0.3},
        'illust': """
+-----------------+
| ~~~~~ ~~~~~ ~~~ |
|  ~~~~~~~~~~~~~  |
| ~~~ ~~~~~ ~~~~~ |
|~~~~~~~~~~~~~~~~~|
|#################|
+-----------------+
"""
    },
    {
        'name': 'Call to the Void',
        'type': 'scroll',
        'rarity': 'odd',
        'recovery_cost': 15,
        'description': 'Winnows enemies & quickens allies.',
        'stat_boosts': {'void_intensity': 0.4, 'void_resistance': 0.3, 'moon_vulnerability': 0.3},
        'effects':[
            {
                'target': 'all_enemies',
                'damage_type': 'void_intensity',
                'damage_power': 1,
            },
            {
                'target': 'all_allies',
                'status_effect_target_stat': 'nimbleness',
                'status_effect_power': 1,
                'status_effect_stat': 'void_intensity',
                'status_effect_duration': 10,
            },
        ]
    },

# ==================================================================================================
# STATUS EFFECTS
# ==================================================================================================

    {
        'name': 'Study',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 10,
        'description': 'A student\'s focused mind, boosting magical stats.',
        'stat_boosts': {'star_intensity': 0.2, 'moon_intensity': 0.2, 'void_intensity': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'star_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 30,
            },
            {
                'status_effect_target_stat': 'moon_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 30,
            },
            {
                'status_effect_target_stat': 'void_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 30,
            },
        ]
    },
    {
        'name': 'Student\'s Robes',
        'type': 'armor',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 10,
        'description': 'A student\'s robes, boosting magical stats.',
        'stat_boosts': {'star_intensity': 0.2, 'moon_intensity': 0.2, 'void_intensity': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'star_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 30,
            },
            {
                'status_effect_target_stat': 'moon_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 30,
            },
            {
                'status_effect_target_stat': 'void_intensity',
                'status_effect_power': 2,
                'status_effect_duration': 30,
            },
        ]
    },
    {
        'name': 'Training',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 10,
        'description': 'A squire\'s physical training, boosting physical stats.',
        'stat_boosts': {'melee_damage': 0.2, 'brute_resistance': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'melee_damage',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
            {
                'status_effect_target_stat': 'brute_intensity',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
            {
                'status_effect_target_stat': 'brute_resistance',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
        ],
    },
    {
        'name': 'Quiver Quickdraw',
        'type': 'trinket',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 10,
        'description': 'Boosts the user\'s archery and nimbleness.',
        'stat_boosts': {'ranged_damage': 0.3, 'nimbleness': 0.2},
        'effects': [
            {
                'status_effect_target_stat': 'ranged_damage',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
            {
                'status_effect_target_stat': 'nimbleness',
                'status_effect_power': 1,
                'status_effect_duration': 40,
            },
        ],
    },
    {
        'name':  'Battlesong',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'self',
        'recovery_cost': 10,
        'description': 'Musters courage for an attack, boosting physical stats.',
        'stat_boosts': {'melee_damage': 0.4, 'ranged_damage': 0.4, 'brute_resistance': 0.4},
        'effects': [
            {
                'status_effect_target_stat': 'melee_damage',
                'status_effect_power': 4,
                'status_effect_duration': 15,
            },
            {
                'status_effect_target_stat': 'ranged_damage',
                'status_effect_power': 4,
                'status_effect_duration': 15,
            },
            {
                'status_effect_target_stat': 'brute_resistance',
                'status_effect_power': 4,
                'status_effect_duration': 15,
            },
        ],
    },

# ==================================================================================================
# WIP
# ==================================================================================================

    {
        'name': 'Burning Blade',
        'type': 'weapon',
        'rarity': 'odd',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'melee_damage',
        'damage_power': 3,
        'description': 'Flaming melee strike dealing damage.',
        'stat_boosts': {'melee_damage': 0.5, 'star_intensity': 0.5}
    },
    {
        'name': 'Cursed Readings',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'void_intensity',
        'damage_power': 3,
        'description': 'Dark void incantation dealing damage.',
        'stat_boosts': {'void_intensity': 0.8}
    },
    {
        'name': 'Scorch',
        'type': 'scroll',
        'rarity': 'exceptional',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'star_intensity',
        'damage_power': 3,
        'description': 'Day Mage signature spell searing enemies.',
        'stat_boosts': {'star_intensity': 0.6}
    },
    
# ==================================================================================================
# DIPLOMACY
# ==================================================================================================

    {
        'name': 'Bargain',
        'type': 'scroll',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'diplomacy',
        'damage_power': 1.0,
        'description': 'Recruits some enemies defeated by this attack.',
        'can_recruit': True,
        'stat_boosts': {'diplomacy': 0.3},
        'illust': """
+-----------------+
| (============(@ |
|  | ~~ ~~~~~~~ | |
|  | ~~~~~~ ~~~ | |
|  |  X________ | |
| (============(@ |
+-----------------+
"""
    },

# ==================================================================================================
# ENEMY SPECIFIC CARDS
# ==================================================================================================

    {
        'name': 'Rust Breath',
        'type': 'weapon',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 7,
        'damage_type': 'star_intensity',
        'damage_power': 1.0,
        'description': 'Rots the enemies melee attacks.',
        'effects': [
            {
                'status_effect_target_stat': 'melee_damage',
                'status_effect_power': -2,
                'status_effect_duration': 10,
            }
        ],
        'illust': """
+-----------------+
|,    ,~~_`S ) ~  |
|/. -~ ~ ~_ S ~   |
|@~S~~~~~~( S) ~  |
|\` -~ _~( S ~    |
|'    '~~,S-S~    |
+-----------------+
"""
    },
    {
        'name': 'Mold Breath',
        'type': 'weapon',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 7,
        'damage_type': 'star_intensity',
        'damage_power': 1.0,
        'description': 'Rots the enemies ranged attacks.',
        'effects': [
            {
                'status_effect_target_stat': 'ranged_damage',
                'status_effect_power': -2,
                'status_effect_duration': 10,
            }
        ],
        'illust': """
+-----------------+
|,    ,~~_`S ) ~  |
|/. -~ ~ ~_ S ~   |
|@~S~~~~~~( S) ~  |
|\` -~ _~( S ~    |
|'    '~~,S-S~    |
+-----------------+
"""
    },
    {
        'name': 'Heat Breath',
        'type': 'weapon',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 7,
        'damage_type': 'star_intensity',
        'damage_power': 1.0,
        'description': 'Rots the enemies moon attacks.',
        'effects': [
            {
                'status_effect_target_stat': 'moon_damage',
                'status_effect_power': -2,
                'status_effect_duration': 10,
            }
        ],
        'illust': """
+-----------------+
|,    ,~~_`S ) ~  |
|/. -~ ~ ~_ S ~   |
|@~S~~~~~~( S) ~  |
|\` -~ _~( S ~    |
|'    '~~,S-S~    |
+-----------------+
"""
    },
    {
        'name': 'Shadow Breath',
        'type': 'weapon',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 7,
        'damage_type': 'star_intensity',
        'damage_power': 1.0,
        'description': 'Rots the enemies star attacks.',
        'effects': [
            {
                'status_effect_target_stat': 'star_damage',
                'status_effect_power': -2,
                'status_effect_duration': 10,
            }
        ],
        'illust': """
+-----------------+
|,    ,~~_`S ) ~  |
|/. -~ ~ ~_ S ~   |
|@~S~~~~~~( S) ~  |
|\` -~ _~( S ~    |
|'    '~~,S-S~    |
+-----------------+
"""
    },

]

CARDS = { card.get('name','') : card for card in CARD_DATA }

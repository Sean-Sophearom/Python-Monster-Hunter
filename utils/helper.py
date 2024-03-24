from utils.enemies_sprite_data import EnemiesSpriteData
from utils.projectiles_sprite_data import ProjectilesSpriteData
from utils.spawner import Spawner
from dataclasses import dataclass
from utils.constant import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CENTER,
    CUSTOMEVENTS
)
from random import choice
from math import log10

@dataclass
class ProjectileData:
    name: str
    event: int
    data: any

def is_out_of_bounds(rect):
    return (
        rect.right < -30
        or rect.left > SCREEN_WIDTH + 30
        or rect.bottom < -30
        or rect.top > SCREEN_HEIGHT + 30
    )

def is_on_screen(rect):
    return (
        rect.right > 0
        and rect.left < SCREEN_WIDTH
        and rect.bottom > 0
        and rect.top < SCREEN_HEIGHT
    )

def find_closest_target(group, target=None):
    if not group:
        return None
    base_x = target.rect.centerx if target else CENTER.x
    base_y = target.rect.centery if target else CENTER.y
    return min(group, key=lambda x: (x.rect.centerx - base_x)**2 + (x.rect.centery - base_y)**2)

def find_on_screen_targets(group):
    for target in group:
        if is_on_screen(target.rect):
            return target
    
def find_random_target(group):
    if not group:
        return None
    return choice(group.sprites())
        
def get_projectiles_data():
    from .constant import CUSTOMEVENTS
    from .projectiles_sprite_data import ProjectilesSpriteData

    return [
        ProjectileData("fire_ball", CUSTOMEVENTS.ADDFIREBALL, ProjectilesSpriteData.fire_ball),
        ProjectileData("fire_ring", CUSTOMEVENTS.ADDFIRERING, ProjectilesSpriteData.fire_ring),
        ProjectileData("flame_ball", CUSTOMEVENTS.ADDFLAMEBALL, ProjectilesSpriteData.flame_ball),
        ProjectileData("magic_arrow", CUSTOMEVENTS.ADDMAGICARROW, ProjectilesSpriteData.magic_arrow),
        ProjectileData("magic_orb", CUSTOMEVENTS.ADDMAGICORB, ProjectilesSpriteData.magic_orb),
        ProjectileData("thunder_ball", CUSTOMEVENTS.ADDTHUNDERBALL, ProjectilesSpriteData.thunder_ball)
    ]

def get_enemies_data():
    from .constant import CUSTOMEVENTS
    from .enemies_sprite_data import EnemiesSpriteData

    return [
        ProjectileData("bat", CUSTOMEVENTS.ADDBAT, EnemiesSpriteData.bat),
        ProjectileData("canine_gray", CUSTOMEVENTS.ADDCANINEGRAY, EnemiesSpriteData.canine_gray),
        ProjectileData("canine_white", CUSTOMEVENTS.ADDCANINEWHITE, EnemiesSpriteData.canine_white),
        ProjectileData("golem", CUSTOMEVENTS.ADDGOLEM, EnemiesSpriteData.golem),
        ProjectileData("rat", CUSTOMEVENTS.ADDRAT, EnemiesSpriteData.rat),
        ProjectileData("skull", CUSTOMEVENTS.ADDSKULL, EnemiesSpriteData.skull),
        ProjectileData("slime", CUSTOMEVENTS.ADDSLIME, EnemiesSpriteData.slime)
    ]

def handle_spawning(event_type):
    from .sprite_group import enemies
    from .game_state import GameState
    from .game_manager import GameManager

    if event_type == CUSTOMEVENTS.WAVEUPDATE:
        
        GameState.enemy_speed_multiplier += log10(GameState.enemy_speed_multiplier + 0.5) / 3.2
        GameState.enemy_health_multiplier += log10(GameState.enemy_health_multiplier + 0.5) / 1.4
        GameState.enemy_damage_multiplier += log10(GameState.enemy_damage_multiplier + 0.5) / 1.4
        GameState.enemy_value_multiplier += log10(GameState.enemy_value_multiplier + 0.5) / 1.4

        GameState.max_enemies_cap += log10(GameState.max_enemies_cap / 4)

        enemies_data = get_enemies_data()
        GameManager.clear_timers([enemy.event for enemy in enemies_data])
        
        enemy = None
        while not enemy:
            enemy = choice(enemies_data)
            if enemy.name in CUSTOMEVENTS.disabled: enemy = None
        GameManager.set_timer(enemy.event, GameState.sprite_timer[enemy.name])
        GameState.sprite_timer[enemy.name] -= 100
        if GameState.sprite_timer[enemy.name] < 100: GameState.sprite_timer[enemy.name] = 100

    elif event_type == CUSTOMEVENTS.ADDBULLET:
        target = find_closest_target(enemies)
        if target: Spawner.spawn_bullet(target)

    elif event_type == CUSTOMEVENTS.ADDLIGHTNING:
        target = find_on_screen_targets(enemies)
        if target: Spawner.spawn_lightning(target)
    
    elif event_type == CUSTOMEVENTS.ADDFIREBALL:
        target = find_random_target(enemies)
        if target: Spawner.spawn_animated_projectile(target, ProjectilesSpriteData.fire_ball)
    
    elif event_type == CUSTOMEVENTS.ADDFIRERING:
        target = find_random_target(enemies)
        if target: Spawner.spawn_animated_projectile(target, ProjectilesSpriteData.fire_ring)

    elif event_type == CUSTOMEVENTS.ADDFLAMEBALL:
        target = find_random_target(enemies)
        if target: Spawner.spawn_animated_projectile(target, ProjectilesSpriteData.flame_ball)
    
    elif event_type == CUSTOMEVENTS.ADDMAGICARROW:
        target = find_random_target(enemies)
        if target: Spawner.spawn_animated_projectile(target, ProjectilesSpriteData.magic_arrow)
    
    elif event_type == CUSTOMEVENTS.ADDMAGICORB:
        target = find_random_target(enemies)
        if target: Spawner.spawn_animated_projectile(target, ProjectilesSpriteData.magic_orb)
    
    elif event_type == CUSTOMEVENTS.ADDTHUNDERBALL:
        target = find_random_target(enemies)
        if target: Spawner.spawn_animated_projectile(target, ProjectilesSpriteData.thunder_ball)
    
    elif len(enemies) >= GameState.max_enemies_cap:
        return

    elif event_type == CUSTOMEVENTS.ADDENEMY:
        Spawner.spawn_enemy()

    elif event_type == CUSTOMEVENTS.ADDBAT:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.bat)
    
    elif event_type == CUSTOMEVENTS.ADDCANINEGRAY:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.canine_gray)
    
    elif event_type == CUSTOMEVENTS.ADDCANINEWHITE:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.canine_white)

    elif event_type == CUSTOMEVENTS.ADDGOLEM:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.golem)

    elif event_type == CUSTOMEVENTS.ADDRAT:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.rat)
    
    elif event_type == CUSTOMEVENTS.ADDSKULL:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.skull)
    
    elif event_type == CUSTOMEVENTS.ADDSLIME:
        Spawner.spawn_animated_enemy(EnemiesSpriteData.slime)

def format_minute_seconds(milliseconds):
    seconds = milliseconds // 1000
    minute = seconds // 60
    seconds = seconds % 60
    return f"{minute}:{seconds:02d}"
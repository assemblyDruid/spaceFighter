import pygame, math, time, pdb, sys, random
from random import randint

pygame.init()
pygame.key.set_repeat(1, 20)

# - # - # - # - #
#  G.VARIABLES  #
# - # - # - # - #

# independent vars
surface = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF)
sysInfo = pygame.display.Info()
CENTER_X = sysInfo.current_w / 2
CENTER_Y = sysInfo.current_h / 2
debris = [ [400, 0], ]
laser_speed = -15
asteroid_mod = 4
asteroid_speed = 10
asteroid_radius = 10
score = 0
font = pygame.font.Font(None, 30)
lasers = [ [CENTER_X, CENTER_Y] ]
debris = [ [400, 0] ]
fighter_lasers = []
foes = []
foes_mod = 30
foe_speed = 7
foe_weapon_speed = 30 # this is a quotient. smaller = faster
player1 = {
    "health" : 100,
    "sheild" : 50,
    "weapons" : 100,
    "agility" : 100,
    "weapons_heat" : 0
}

# dependent vars
Running = True
center_x = (sysInfo.current_w / 2)
center_y = (sysInfo.current_h / 2)
gameCounter = 0
moveDown = False
moveUp = False
moveRight = False
moveLeft = False
fireWeapons = False

# - # - # - # - # - # - #
#  GLOBAL DEFS & LISTS  #
# - # - # - # - # - # - #

# update window area
def updateWinArea():
    # called on resize
    sysInfo = pygame.display.Info()
    CENTER_X = (sysInfo.current_w / 2)
    CENTER_Y = (sysInfo.current_h / 2)
    center = (center_x, center_y)
# update window area end

# add new asteroid
def addAsteroid():
    x_pos = randint(2, (sysInfo.current_w) - 2)
    y_pos = 0
    debris.append(
        [
        x_pos,
        y_pos
        ]
        )
# end add new asteroid

# add new foe
def addFoe():
    foeType = [
    "suicider",
    "fighter"
    ]
    x_pos = randint(2, (sysInfo.current_w) - 2)
    y_pos = randint(15, 40)
    foe_weapon_x = 0
    foe_weapon_y = 0
    foe_weapon_deltas = []
    weapon_rate_mod = randint(0, 10)
    foes.append(
        [
        x_pos, #
        y_pos, #
        random.choice(foeType), # returns the form 'insert_random_type'
        foe_weapon_deltas # applies only to fighters
        ]
        )
# end add new foe

# - # - # - # - #
#   GAME LOOP   #
# - # - # - # - #

# game loop
while (Running):
    if pygame.event.peek:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                sys.exit()
                break
            if event.type == pygame.VIDEORESIZE:
                updateWinArea()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moveUp = True
                if event.key == pygame.K_DOWN:
                    moveDown = True
                if event.key == pygame.K_LEFT:
                    moveLeft = True
                if event.key == pygame.K_RIGHT:
                    moveRight = True
                if (event.key == pygame.K_SPACE) and (player1["weapons_heat"] < 100):
                    fireWeapons = True
                if event.key == pygame.K_ESCAPE:
                    Running = False
                    sys.exit()
                    break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    moveUp = False
                if event.key == pygame.K_DOWN:
                    moveDown = False
                if event.key == pygame.K_LEFT:
                    moveLeft = False
                if event.key == pygame.K_RIGHT:
                    moveRight = False
                if (event.key == pygame.K_SPACE):
                    fireWeapons = False

    # - # - # - # - # - #
    #    KEY BINDINGS   #
    # - # - # - # - # - #

    if moveDown:
        movement_speed = player1["agility"] / 20
        center_y += (movement_speed)
    if moveUp:
        movement_speed = player1["agility"] / 10
        center_y -= (movement_speed)
    if moveRight:
        movement_speed = player1["agility"] / 10
        center_x += (movement_speed)
    if moveLeft:
        movement_speed = player1["agility"] / 10
        center_x -= (movement_speed)
    if fireWeapons and (player1["weapons_heat"] < 100):
        movement_speed = player1["agility"] / 10
        lasers.append([center_x, center_y])
        player1["weapons_heat"] += 5.5
        print "added LASER"

    gameCounter += 1
    if gameCounter > 50:
        gameCounter = 0
        if (asteroid_mod - 1) < 1:
            asteroid_mod -= 1

    # - # - # - # - # - #
    #      PLAYER 1     #
    # - # - # - # - # - #

    # draw player 1

    pygame.draw.circle(
        surface,
        (255, 0 , 0),
        (center_x, center_y),
        10,
        1
        )

    # draw player 1 sheild
    if player1["sheild"] >= 90:
        sheild_width = 4
    elif player1["sheild"] >= 70:
        sheild_width = 3
    elif player1["sheild"] >= 50:
        sheild_width = 2
    else: sheild_width = 1
    if player1["sheild"] > 0:
        pygame.draw.circle(
            surface,
            (50, 100, 255),
            (center_x, center_y),
            (12 + sheild_width),
            sheild_width
            )

    # - # - # - # - #
    #   INFO BARS   #
    # - # - # - # - #

    # info bar(s) logic
        # begin health logic
    if player1["health"] > 90 : health_colorBar = (0, 255, 110)
    elif player1["health"] > 50 : health_colorBar = (255, 255, 0)
    else: health_colorBar = (255, 0, 0)
    pygame.draw.rect(
        surface,
        health_colorBar,
        pygame.Rect(
            (CENTER_X - player1["health"] / 2), # top left corner x pos
            (sysInfo.current_h - 25), # top left corner y pos
            player1["health"], # length of health bar
            10 # height of health bar
            )
        )
        # end health logic
        # begin sheild logic
    if player1["sheild"] > 0:
        pygame.draw.rect(
            surface,
            (0, 100, 255),
            pygame.Rect(
                (CENTER_X - player1["sheild"] / 2), # top left corner x pos
                (sysInfo.current_h - 15), # top left corner y pos
                player1["sheild"], # length of sheild bar
                10 # height of sheild bar
                )
        )
        # end sheild logic
        # weapons heat logic
    if player1["weapons_heat"] > 90: weapons_heat_colorBar = (255, 0, 0)
    else: weapons_heat_colorBar = (250, 80, 80)
    pygame.draw.rect(
        surface,
        weapons_heat_colorBar,
        pygame.Rect(
            ( (CENTER_X / 2) - (player1["weapons_heat"] / 2) ), # top left corner x pos
            (sysInfo.current_h - 15), # top left corner y pos
            player1["weapons_heat"], # length of weapons_heat bar
            10 # height of weapons_heat bar
            )
        )
        # end weapons heat logic
        # agility bar logic
    pygame.draw.rect(
        surface,
        (255, 50, 255),
        pygame.Rect(
            ( (CENTER_X / 2) - (player1["agility"] / 2) ), # top left corner x pos
            (sysInfo.current_h - 25), # top left corner y pos
            player1["agility"], # length of agility bar
            10 # height of agility bar
            )
        )
        # end agility bar logic
        # Score Board logic
            # time alive bonus
    if gameCounter % 90 == 0:
        score += 2
    score_display = "SCORE: " + str(score)
    score_render = font.render(score_display, 0, (255, 0, 0))
    surface.blit(
        score_render,
        ( (3 * CENTER_X / 2), # top left corner x pos
        (sysInfo.current_h - 35) ) # top left corner y pos
        )

    # weapons heat cooldown
    if player1["weapons_heat"] > 0:
        player1["weapons_heat"] -= 1

    # agility recharge
    if player1["agility"] < 100:
        player1["agility"] += 1

    # sheild regcharge
    if player1["sheild"] < 100:
        if gameCounter % 25 == 0:
            player1["sheild"] += 1
    # end info bar(s) logic

    # - # - # - # - #
    #      FOES     #
    # - # - # - # - #

    # foes logic
    foe_remove_list = []
    def foeCleanUp():
        if foe_remove_list > 0:
            for i in range(len(foe_remove_list)):
                del foes[foe_remove_list[i]]
    if (gameCounter % foes_mod) == 0 and len(foes) < 25:
        addFoe()
        print "added FOE"
    for i in range(len(foes)):
        breakLoop = False
        if breakLoop:
            break
        else:

            # - # - # - # - #
            #   SUICIDERS   #
            # - # - # - # - #

            if foes[i][2] == 'suicider':
                if(foes[i][1] <= center_y): # suicider is above player
                    if (foes[i][0] > (center_x + 10)): # foe is on player's right
                        foes[i][0] -= foe_speed
                        foes[i][1] += foe_speed
                    elif ((center_x - 10) > foes[i][0]): # foe is on player's left
                        foes[i][0] += foe_speed
                        foes[i][1] += foe_speed
                    else: foes[i][1] += foe_speed
                else: # suicider has passed player
                        foes[i][1] += foe_speed
                # draw suiciders
                pygame.draw.rect(
                    surface,
                    (255, 0, 0),
                    pygame.Rect(foes[i][0], foes[i][1], 8, 8),
                    0
                    )
                # end draw suiciders
                # suicider collision detection (with player)
                if (
                    abs(center_y - foes[i][1] < 10) and
                    (abs(center_x - foes[i][0]) < 12) and
                    (center_y >= foes[i][1])
                    ):
                    foe_remove_list.append(i)
                    if player1["sheild"] > 0:
                        if player1["sheild"] > 10:
                            player1["sheild"] -= 10
                        else: player1["sheild"] = 0
                        if player1["agility"] >= 50:
                            player1["agility"] -= 50
                        else: player1["agility"] = 0
                        print "+ kill list (collision : W/ sheild)"
                        breakLoop = True
                        break
                    elif player1["sheild"] <= 0:
                        if player1["health"] >= 30:
                            player1["health"] -= 30
                        else: player1["health"] = 0
                        if player1["agility"] >= 20:
                            player1["agility"] -= 20
                        else: player1["agility"] = 0
                        print "+ kill list (collision : W/O sheild)"
                        breakLoop = True
                        break
                    else:
                        print "[!] [!] NO CATCH ERROR (1) [!] [!]"
                # end suicider collision detection

            # - # - # - # - #
            #   FIGHTERS    #
            # - # - # - # - #

            if foes[i][2] == 'fighter':
                # add a laser to the weeapons list of each fighter on mod
                if ( gameCounter % (20 + randint(-10, 30)) ) == 0:
                    foes[i][3] = [
                    (center_x - foes[i][0]) / foe_weapon_speed,
                    (center_y - foes[i][1]) / foe_weapon_speed
                    ]
                    fighter_lasers.append(
                        [
                        foes[i][0],
                        foes[i][1],
                        foes[i][3]
                        ]
                        )
                # add random movement to fighters
                if ( gameCounter % 100 ):
                    fighter_movement_x = randint(-3, 3)
                    fighter_movement_y = randint(-1, 1)
                if ( gameCounter % 20 ):
                    foes[i][0] += fighter_movement_x
                    foes[i][1] += fighter_movement_y

                # draw fighters
                pygame.draw.circle(
                    surface,
                    (200, 40, 255),
                    (foes[i][0], foes[i][1]),
                    8,
                    0
                    )
    # fighter lasers logic
    fighter_laser_remove = []
    def fighterLaserCleanUp():
        if len(fighter_laser_remove) > 0:
            for i in range(len(fighter_laser_remove)):
                del [fighter_lasers[fighter_laser_remove[i]]]
                print "killed: (fighter laser)"
        # move lasers shot by fighters
    if len(fighter_lasers) > 0:
        for i in range(len(fighter_lasers)):
            fighter_lasers[i][0] += fighter_lasers[i][2][0]
            fighter_lasers[i][1] += fighter_lasers[i][2][1]

            # draw fighter lasers
            pygame.draw.circle(
                surface,
                (0, 255, 255),
                (fighter_lasers[i][0], fighter_lasers[i][1]),
                2,
                0
                )

            # remove lasers that are off the "map"
            if (
                (fighter_lasers[i][0] > sysInfo.current_w) or
                (fighter_lasers[i][1] > sysInfo.current_h)
                ):
                fighter_laser_remove.append(i)

    # fighter laser collsion detection (with player)
    if (len(fighter_lasers) > 0):
        breakLoop = False
        for i in range(len(fighter_lasers)):
            if breakLoop:
                break
            else:
                if (
                    abs(fighter_lasers[i][0] - center_x) < 12 and
                    abs(center_y - fighter_lasers[i][1]) < 10
                    ):
                    if player1["sheild"] > 0:
                        if player1["sheild"] >= 5:
                            player1["sheild"] -= 5
                        else: player1["sheild"] = 0
                        fighter_laser_remove.append(i)
                        print "+ kill list (collision : W/ sheild)"
                        breakLoop = True
                        break
                    elif player1["sheild"] <= 0:
                        if player1["health"] >= 5:
                            player1["health"] -= 5
                        else: player1["health"] = 0
                        if player1["agility"] >= 5:
                            player1["agility"] -= 5
                        else: player1["agility"] = 0
                        fighter_laser_remove.append(i)
                        print "+ kill list (collision : W/O sheild)"
                        breakLoop = True
                        break
                    else:
                        print "[!] [!] NO CATCH ERROR (2) [!] [!]"
    # end foes logic

    # - # - # - # - #
    #   ASTEROIDS   #
    # - # - # - # - #

    # asteroid logic
    if (gameCounter % asteroid_mod) == 0 and (len(debris) < 55):
        addAsteroid()
        print "added ASTEROID"
    asteroid_remove_list = []
    def asteroidCleanUp():
        if len(asteroid_remove_list) > 0:
            for i in range(len(asteroid_remove_list)):
                del debris[asteroid_remove_list[i]]
                print "killed: (asteroid)"
                break

    for i in range(len(debris)):
        x_pos = debris[i][0]
        y_pos = (debris[i][1] + asteroid_speed)
        debris[i][1] = y_pos # <-- change value of global var
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (x_pos, y_pos),
            asteroid_radius,
            1
            )

        # collision (ship & asteroid) detection logic
            # impact with sheild
        collisionRadius_player_x = center_x + asteroid_radius
        collisionRadius_player_y = center_y + asteroid_radius
        collisionRadius_asteroid_x = x_pos + asteroid_radius
        collisionRadius_asteroid_y = y_pos + asteroid_radius

        if (
            # imagine that player1's position is the origin
            # on a coordinate plane. Collisions will depend on the
            # quadrant that the incoming asteroid approaches from
            # as follows:

                ( # first quad
                    (collisionRadius_asteroid_x <= collisionRadius_player_x) and
                    (collisionRadius_asteroid_y <= collisionRadius_player_y) and
                    (math.sqrt(math.pow( (collisionRadius_player_x - collisionRadius_asteroid_x), 2) +
                            math.pow( (collisionRadius_player_y - collisionRadius_asteroid_y), 2) )) < 11
                )
                or
                ( # second quad
                    (collisionRadius_asteroid_x >= collisionRadius_player_x) and
                    (collisionRadius_asteroid_y <= collisionRadius_player_y) and
                    (math.sqrt(math.pow( (collisionRadius_asteroid_x - collisionRadius_player_x), 2) +
                            math.pow( (collisionRadius_player_y - collisionRadius_asteroid_y), 2) )) < 11
                )
                or
                ( # third quad
                    (collisionRadius_asteroid_x <= collisionRadius_player_x) and
                    (collisionRadius_asteroid_y >= collisionRadius_player_y) and
                    (math.sqrt(math.pow( (collisionRadius_player_x - collisionRadius_asteroid_x), 2) +
                            math.pow( (collisionRadius_asteroid_y - collisionRadius_player_y), 2) )) < 11
                )
                or
                ( # fourth quad
                    (collisionRadius_asteroid_x >= collisionRadius_player_x) and
                    (collisionRadius_asteroid_y >= collisionRadius_player_y) and
                     (math.sqrt(math.pow( (collisionRadius_asteroid_x - collisionRadius_player_x), 2) +
                            math.pow( (collisionRadius_asteroid_y - collisionRadius_player_y), 2) )) < 11
                )
            ):

            if player1["sheild"] > 0:
                if player1["sheild"] >= 20:
                    player1["sheild"] -= 20
                else: player1["sheild"] = 0
                if player1["agility"] >= 25:
                    player1["agility"] -= 50
                else: player1["agility"] = 0
                asteroid_remove_list.append(i)
                print "+ kill list (collision : W/ sheild)"
            elif player1["sheild"] <= 0:
                if player1["health"] >= 50:
                    player1["health"] -= 50
                else: player1["health"] = 0
                if player1["agility"] >= 25:
                    player1["agility"] -= 50
                else: player1["agility"] = 0
                asteroid_remove_list.append(i)
                print "+ kill list (collision : W/O sheild)"
            else:
                print "[!] [!] NO CATCH ERROR (3) [!] [!]"
            # impact without sheild
        # end collision (ship & asteroid) detection

        if player1["health"] == 0:
            Running = False
            sys.exit()

        if (debris[i][1] >= sysInfo.current_h):
            asteroid_remove_list.append(i)
            print "+ kill list (SCREEN END)"
    asteroidCleanUp()
    # end asteroid logic

    # - # - # - # - # - #
    #      LASERS       #
    # - # - # - # - # - #

    # laser logic
    laser_remove_list = []
    def laserCleanUp():
        if len(laser_remove_list) > 0:
            for i in range(len(laser_remove_list)):
                del lasers[laser_remove_list[i]]
                print "killed: (laser)"
                break

    for i in range(len(lasers)):
        x_pos = lasers[i][0]
        y_pos = (lasers[i][1] + laser_speed)
        lasers[i][1] = y_pos
        pygame.draw.circle(
            surface,
            (50, 255, 0),
            (x_pos, y_pos),
            2,
            1
            )
        if lasers[i][1] < 0:
            laser_remove_list.append(i)
        # laser collision logic (with asteroid)
    if (len(lasers) > 0 and len(debris) > 0):
        breakLoop = False
        for i in range(len(lasers)):
            if breakLoop:
                break
            else:
                for j in range(len(debris)):
                    if breakLoop:
                        break
                    else:
                        if (
                            abs( debris[j][0] - lasers[i][0] ) <= 10 and
                            debris[j][1] + asteroid_radius - lasers[i][1] + 2 > 1
                            ):
                            asteroid_remove_list.append(j)
                            laser_remove_list.append(i)
                            breakLoop = True
                            print "+ kill list (laser/asteroid collision)"
                            score += 10
                            print "score updated (+10)"
                            break
        # laser collision with foes
    if ( (len(lasers) > 0) and (len(foes) > 0) ):
        breakLoop = False
        for i in range(len(lasers)):
            if breakLoop:
                break
            else:
                for j in range(len(foes)):
                    if breakLoop:
                        break
                    else:
                        if foes[j][2] == 'suicider':
                            if (
                                (abs(lasers[i][0] - foes[j][0]) < 7) and
                                (abs(lasers[i][1] - foes[j][1]) < 7)
                                ):
                                foe_remove_list.append(j)
                                print "+ foe, rmList"
                                laser_remove_list.append(i)
                                breakLoop = True
                                print "+ laser, rmList"
                                break
                        if foes[j][2] == 'fighter':
                            if (
                                (abs(lasers[i][0] - foes[j][0]) < 8) and
                                (abs(lasers[i][1] - foes[j][1]) < 8)
                                ):
                                foe_remove_list.append(j)
                                print "+ foe, rmList"
                                laser_remove_list.append(i)
                                breakLoop = True
                                print "+ laser, rmList"
                                break
        # end laser collision with foes
    # end laser collision
    # end laser logic

    # - # - # - # - # - # - #
    #   CLEANUP / REFRESH   #
    # - # - # - # - # - # - #

    laserCleanUp()
    asteroidCleanUp()
    foeCleanUp()
    fighterLaserCleanUp()

    pygame.time.Clock().tick(30)
    pygame.display.flip()
    surface.fill((0, 0, 0))



import pygame
import string 

pygame.init()
res = (1024,768)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()
BLACK = (0, 0, 0, 0)
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 75, 5
lw = 1
divisions_x = 19
divisions_y = 16

alphabet = list(string.ascii_uppercase)
numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']

all_tiles = set([(x, y) for x in range(divisions_x) for y in range(divisions_y)])

forbidden_tiles = (
    (0,10),
    (0,11),
    (0,12),
    (0,13),
    (0,14),
    (0,15),
    (1,10),
    (1,11),
    (1,12),
    (1,13),
    (1,14),
    (1,15),
    (2,10),
    (2,11),
    (2,12),
    (2,13),
    (2,14),
    (2,15),
    (9,15),
    (10,14),
    (11,6),
    (12,14),
    (12,15),
    (13,15),
    (14,15),
    (15,15),
    (16,15),
)

land_tiles = (
    (0,4),
    (0,5),
    (0,6),
    (0,7),
    (0,8),
    (0,9),
    (1,4),
    (1,5),
    (1,9),
    (2,9),
    (3,9),
    (3,10),
    (3,11),
    (3,12),
    (3,13),
    (3,14),
    (3,15),
    # Cuba
    (2,3),
    (3,2),
    (3,3),
    (3,4),
    (4,2),
    (4,3),
    (4,6),
    (5,2),
    (5,3),
    (5,5),
    (6,3),
    (6,4),
    (7,3),
    (7,4),
    (7,5),
    (8,4),
    (8,5),
    (9,5),
    # Florida/Bahammas
    (4,0),
    (4,1),
    (5,0),
    (6,0),
    (6,1),
    (7,0),
    (7,1),
    (8,0),
    (8,1),
    (8,2),
    (9,1),
    (9,3),
    (9,4),
    (10,3),
    (10,4),
    # Jamica, Hispanola, Puerto Rico
    (6,7),
    (7,7),
    (8,7),
    (9,7),
    (10,7),
    (11,7),
    (12,7),
    (13,7),
    (14,7),
    (15,7),
    (16,7),
    (10,5),
    (11,5),
    (12,5),
    (10,6),
    (12,6),
    (13,6),
    # Panama, Columbia, Venezuala
    (4,15),
    (5,15),
    (6,15),
    (7,15),
    (8,15),
    (8,14),
    (9,14),
    (9,13),
    (10,13),
    (10,12),
    (11,12),
    (11,13),
    (11,14),
    (11,15),
    (10,15),
    (12,13),
    (13,13),
    (13,14),
    (12,12),
    (13,12),
    (14,14),
    (15,14),
    (16,14),
    (17,14),
    (17,15),
    (15,13),
    # Lower Antilles
    (17,13),
    (17,12),
    (17,11),
    (17,10),
    (17,9),
    (17,8),
    (17,7),
    (16,8),
    (18,13),
    (18,12),
)

ocean_tiles = all_tiles - set(land_tiles) - set(forbidden_tiles)

cant_move = (
    (0,4),
    (0,5),
    (2,3),
    (4,3),
    (3,2),
    (3,3),
    (4,2),
    (4,3),
    (5,2),
    (5,3),
    (6,3),
    (6,4),
    (4,0),
    (5,0),
    (7,4),
    (7,5),
    (8,4),
    (8,5),
    (10,5),
    (10,6),
    (10,7),
    (12,6),
    (12,7),
    (7,6),  
    (7,7),  
)

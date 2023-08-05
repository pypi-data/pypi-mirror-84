import pyframe, pygame, math
import numpy as np

def add_vectors(v1, v2):  # v[0] = Angle, v[1] = length
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length

def blur_surf(surface, amt):
    """
    Floutte une surface pygame (généralement une image)
    """
    if amt < 1.0:
        raise ValueError("L'agument 'amt' doit être plus grand que 1.0, la valeur était de %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def get_smallest(l) :
    assert type(l) is list
    val = math.inf
    for i in l :
        if i < val :
            val = i
    return val if val != math.inf or math.inf in l else None
def get_biggest(l) :
    assert type(l) is list
    val = -math.inf
    for i in l :
        if i > val :
            val = i
    return val if val != -math.inf or -math.inf in l else None

def falling_obj(x0,v0,g,t) :
    return x0 + v0*t + 0.5*g*t**2

def draw_grid(
        surface:pygame.surface.Surface,
        start_pos,
        color:tuple[int,int,int] = (0,0,0),
        rows:int = 5,
        cols:int = 5,
        cell_width:int = 50,
        cell_height:int = 50,
        line_width = 2
) :
    pygame.draw.line( surface,color,start_pos, (start_pos[0]+cell_width*cols,start_pos[1]),line_width ) # Haut
    pygame.draw.line( surface,color, (start_pos[0],start_pos[1]+cell_height*rows) , (start_pos[0]+cell_width*rows+round(line_width/2),start_pos[1]+cell_height*rows),line_width ) # Bas
    pygame.draw.line( surface,color,start_pos, (start_pos[0],start_pos[1]+cell_height*rows),line_width ) # Gauche
    pygame.draw.line( surface,color,(start_pos[0]+cell_width*rows,start_pos[1]), (start_pos[0]+cell_width*rows,start_pos[1]+cell_height*rows),line_width ) # Droite
    for col_nb in range(cols) :
        pygame.draw.line(
            surface,
            color,
            (
                start_pos[0]+col_nb*cell_width,
                start_pos[1]
            ),
            (
                start_pos[0]+col_nb*cell_width,
                start_pos[1]+rows*cell_height
            ),
            line_width
        )
    for row_nb in range(cols) :
        pygame.draw.line(
            surface,
            color,
            (
                start_pos[0],
                start_pos[1]+row_nb*cell_height
            ),
            (
                start_pos[0]+cols*cell_width,
                start_pos[1]+row_nb*cell_height
            ),
            line_width
        )
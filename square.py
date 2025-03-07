import pygame


def drawSquare(screen, center_x, center_y, side_length, triangle_position, mouth, color):
    # Calculate the coordinates of the square's top-left corner
    top_left_x = center_x - side_length // 2
    top_left_y = center_y - side_length // 2

    # Draw the square with a filled yellow background
    pygame.draw.rect(screen, color, (top_left_x, top_left_y, side_length, side_length))

    # Draw the black border
    pygame.draw.rect(screen, (0, 0, 0), (top_left_x, top_left_y, side_length, side_length), 2)

    # Calculate the coordinates of the vertices of the black triangle based on the specified position
    left_x = center_x - side_length // 2
    right_x = center_x + side_length // 2
    top_y = center_y - side_length // 2
    bottom_y = center_y + side_length // 2
    # Calculate the position of the eye
    eye_radius = side_length // 8
    if triangle_position == 'right':
        triangle_vertices = [(right_x, top_y), (right_x, bottom_y), (center_x, center_y)]
        eye_x = top_left_x + eye_radius * 2
        eye_y = top_left_y + eye_radius * 2
    elif triangle_position == 'bottom':
        triangle_vertices = [(right_x, bottom_y), (left_x, bottom_y), (center_x, center_y)]
        eye_x = right_x - eye_radius * 2
        eye_y = top_left_y + eye_radius * 2
    elif triangle_position == 'left':
        triangle_vertices = [(left_x, top_y), (left_x, bottom_y), (center_x, center_y)]
        eye_x = right_x - eye_radius * 2
        eye_y = top_left_y + eye_radius * 2
    elif triangle_position == 'top':
        triangle_vertices = [(right_x, top_y), (left_x, top_y), (center_x, center_y)]
        eye_x = left_x + eye_radius * 2
        eye_y = bottom_y - eye_radius * 2
    
    if mouth:
        pygame.draw.polygon(screen, (0, 0, 0), triangle_vertices)
    
    # Draw the black eye
    pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), eye_radius)
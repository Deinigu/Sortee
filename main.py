import math
import pygame
import random

pygame.init()


# Class with all the drawing information
class DrawInformation:
    # COLOURS
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = BLACK

    GRADIENTS = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]

    # FONTS
    FONT = pygame.font.SysFont("consolas", 15)

    # PADS SIZE
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sortee")
        self.set_lst(lst)

    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val)
        )
        self.start_x = self.SIDE_PAD // 2


# Main drawing function
def draw(draw_info, algo_name, ascending):
    # Draws background
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Draws the pad with information
    ascending_info = draw_info.FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
        1,
        draw_info.GREEN,
    )
    draw_info.window.blit(
        ascending_info, (draw_info.width / 2 - ascending_info.get_width() / 2, 25)
    )

    controls = draw_info.FONT.render(
        "N - New list | SPACE - Start Sorting | A - Ascending | D - Descending",
        1,
        draw_info.WHITE,
    )
    draw_info.window.blit(
        controls, (draw_info.width / 2 - controls.get_width() / 2, 55)
    )

    sorting = draw_info.FONT.render(
        "B - Bubble Sort | I - Insertion Sort | S - Selection Sort", 1, draw_info.WHITE
    )
    draw_info.window.blit(sorting, (draw_info.width / 2 - controls.get_width() / 2, 85))

    # Draws the list
    draw_list(draw_info)
    pygame.display.update()


# Draws the list
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (
            draw_info.SIDE_PAD // 2,
            draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD,
        )
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.block_width, draw_info.height)
        )

    if clear_bg:
        pygame.display.update()


# Returns a list with n random values going from min_val to max_val
def generate_starting_list(n, min_val, max_val):
    lst = random.sample(range(min_val,max_val),n)

    return lst

# Bubble Sort
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

                # Draw this bar with colors
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)

                # Generator yield (waits for the get method)
                yield True
    return lst

# Insertion Sort
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current

            # Draw this bar with colors
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)

            # Generator yield (waits for the get method)
            yield True
    return lst

# Selection Sort
def selectionSort(draw_info, ascending):
    
    array = draw_info.lst
    size = len(array)
    
    for ind in range(size):
        min_index = ind
 
        for j in range(ind + 1, size):
            if ascending == True:
                # select the minimum element in every iteration
                if array[j] < array[min_index]:
                    min_index = j
            elif ascending == False:
                if array[j] > array[min_index]:
                    min_index = j
                            
            # Draw this bar with colors
            draw_list(draw_info, {ind: draw_info.GREEN, j: draw_info.RED}, True)

            # Generator yield (waits for the get method)
            yield True
         # swapping the elements to sort the array
        (array[ind], array[min_index]) = (array[min_index], array[ind])
    return array

# Main loop
def main():
    run = True
    clock = pygame.time.Clock()

    # Variables for the generation of the list
    n = 100
    min_val = 0
    max_val = 100

    # Initialize list
    lst = generate_starting_list(n, min_val, max_val)

    # Initialize DrawInformation
    draw_info = DrawInformation(800, 600, lst)

    # Initialize variables
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algortihm_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sorting_algortihm_generator)  # type: ignore
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # EVENTOS
        for event in pygame.event.get():
            # Close application
            if event.type == pygame.QUIT:
                run = False

            # <--CONTROL KEYS-->
            if event.type != pygame.KEYDOWN:
                continue

            # Reset the list
            if event.key == pygame.K_n and not sorting:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_lst(lst)

            # Init sorting
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algortihm_generator = sorting_algorithm(draw_info, ascending)
            
            # Stops sorting
            elif event.key == pygame.K_SPACE and sorting:
                sorting = False

            # Control ascending or descending
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            # Chooses the algorithm
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selectionSort
                sorting_algo_name = "Selection Sort"

    pygame.quit()


if __name__ == "__main__":
    main()

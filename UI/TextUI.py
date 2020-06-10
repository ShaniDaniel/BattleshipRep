import pygame
BLACK = (0, 0, 0)
ANTIALIAS = 1
PADDING = 5


class TextUI:
    @staticmethod
    def write_title(screen, text, line_num, font=24):
        """displays the given text on the screen at the given line number"""
        title_font = pygame.font.Font(None, font)
        text_final = title_font.render(text, ANTIALIAS, BLACK)
        screen.blit(text_final, ((pygame.display.get_surface().get_size()[0] - text_final.get_width()) / 2,
                                 text_final.get_height() * line_num + PADDING))
        return "success"

    @staticmethod
    def clear_title(screen, line_num, font=24):
        """deletes the text from the screen at the given line number"""
        from UI.BoardUI import BoardUI
        title_font = pygame.font.Font(None, font)
        text_final = title_font.render(" ", ANTIALIAS, BLACK)
        pygame.draw.rect(screen, BoardUI.color_index["light blue"], (0, text_final.get_height() * line_num + PADDING,
                                                                     pygame.display.get_surface().get_size()[0],
                                                                     text_final.get_height()))
        return "success"

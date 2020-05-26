import pygame

from Classes.Cube import Cube


class GameUI:

    @staticmethod
    def write_title(screen, text, line_num, font=None):
        if font is None:
            title_font = pygame.font.Font(None, 24)
        else:
            title_font = pygame.font.Font(None, font)
        text_final = title_font.render(text, 1, (0, 0, 0))
        screen.blit(text_final, ((pygame.display.get_surface().get_size()[0] - text_final.get_width()) / 2,
                                 text_final.get_height() * line_num + 5))
        return "success"

    @staticmethod
    def clear_title(screen, line_num, font=None):
        if font is None:
            title_font = pygame.font.Font(None, 24)
        else:
            title_font = pygame.font.Font(None, font)
        text_final = title_font.render(" ", 1, (0, 0, 0))
        pygame.draw.rect(screen, (252, 168, 78), (0, text_final.get_height() * line_num + 5,
                         pygame.display.get_surface().get_size()[0], text_final.get_height()))
        return "success"



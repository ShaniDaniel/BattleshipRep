import pygame
import Constants


class TextUI:
    @staticmethod
    def write_title(screen, text, line_num, font=24):
        """displays the given text on the screen at the given line number"""
        title_font = pygame.font.Font(None, font)
        text_final = title_font.render(text, Constants.ANTIALIAS, Constants.BLACK)
        screen.blit(text_final, ((pygame.display.get_surface().get_size()[0] - text_final.get_width()) / 2,
                                 text_final.get_height() * line_num + Constants.LINE_PADDING))
        return "success"

    @staticmethod
    def clear_title(screen, line_num, font=24):
        """deletes the text from the screen at the given line number"""
        from UI.BoardUI import BoardUI
        title_font = pygame.font.Font(None, font)
        text_final = title_font.render(" ", Constants.ANTIALIAS, Constants.BLACK)
        pygame.draw.rect(screen, BoardUI.color_index["light blue"], (0, text_final.get_height() * line_num
                                                                     + Constants.LINE_PADDING,
                                                                     pygame.display.get_surface().get_size()[0],
                                                                     text_final.get_height()))
        return "success"

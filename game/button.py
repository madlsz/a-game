import pygame
import typing


class Button:
    def __init__(
        self,
        width: int,
        height: int,
        caption: str,
        on_click: typing.Callable,
        *args,
        font: str = "freesansbold.ttf",
        font_size: int = 20,
        font_color: typing.Tuple[int, int, int] = (255, 255, 255),
        background_color: typing.Tuple[int, int, int, int] = (0, 0, 0, 100),
    ) -> None:
        self.x = None
        self.y = None
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.font = pygame.font.Font(font, font_size)
        self.caption = self.font.render(caption, True, font_color)
        self.on_click = on_click
        self.args = args
        self.background_color = background_color

    def is_inside_point(self, pos: typing.Tuple[int, int]) -> bool:
        """
        True if the given point is inside the Button
        """
        x, y = pos
        if self.x <= x < self.width + self.x and self.y <= y < self.height + self.y:
            return True
        return False

    @property
    def surface(self) -> pygame.Surface:
        # if self.background_color:
        self.surf.fill(self.background_color)
        self.surf.blit(
            self.caption,
            (
                (self.surf.get_width() - self.caption.get_width()) // 2,
                (self.surf.get_height() - self.caption.get_height()) // 2,
            ),
        )
        return self.surf

    def click(self) -> bool:
        if self.is_inside_point(pygame.mouse.get_pos()) and callable(self.on_click):
            self.on_click(*self.args)
            return True
        return False

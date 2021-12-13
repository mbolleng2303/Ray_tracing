import pygame


class Button():
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        # Render new label
        self._text = t
        self.label = pygame.font.SysFont("monospace", 10).render(t, True, (0, 0, 0))

    def values(self):
        return self.x, self.y, self.width, self.height

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, self.color, self.values())
        # Draw label
        surface.blit(self.label, (self.x + (self.width / 2 - self.label.get_width() / 2),
                                  self.y + (self.height / 2 - self.label.get_height() / 2)))

    def clicked(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        else:
            return False
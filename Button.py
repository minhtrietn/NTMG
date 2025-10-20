import pygame


class AAfilledRoundedRect:
    def __init__(self, surface, rect=(0, 0, 0, 0), color: tuple or list = (0, 0, 0), radius: float = 1):
        rect = pygame.rect.Rect(rect)
        color = pygame.color.Color(color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0

        if radius > 1.0:
            raise ValueError("Max radius is 1.0")

        rectangle = pygame.surface.Surface(rect.size, pygame.constants.SRCALPHA).convert_alpha()
        circle = pygame.surface.Surface([min(rect.size) * 3] * 2, pygame.constants.SRCALPHA).convert_alpha()
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect())
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.constants.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.constants.BLEND_RGBA_MIN)

        surface.blit(rectangle, pos)


class Button_IMG:
    def __init__(self, x=0, y=0, image=None, scale=0, scale_change=0):
        self.check_disable = False
        self.x = x
        self.y = y
        self.image = image
        self.clicked = False
        self.scale = scale
        self.scaled = scale
        self.scale_change = scale_change
        self.width = image.get_width()
        self.height = image.get_height()
        self.imaged = pygame.transform.smoothscale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.imaged.get_rect()
        self.rect.center = (x, y)
        self.state = "normal"

    def draw(self, surface):
        if not self.check_disable:
            if self.state == "update":
                self.imaged = pygame.transform.smoothscale(self.image,
                                                           (int(self.width * self.scaled),
                                                            int(self.height * self.scaled)))
                self.state = "normal"
            surface.blit(self.imaged, (self.rect.x + (self.width * self.scale - int(self.width * self.scaled)) / 2,
                                       self.rect.y + (self.height * self.scale - int(self.height * self.scaled)) / 2))
            return self.check_click()
        else:
            surface.blit(self.imaged, (self.rect.x + (self.width * self.scale - int(self.width * self.scaled)) / 2,
                                       self.rect.y + (self.height * self.scale - int(self.height * self.scaled)) / 2))
            return self.check_click()

    def update_state(self, new_state):
        if self.state != new_state:
            self.state = "update"

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if not self.check_disable:
            if self.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    if self.scaled != self.scale:
                        self.scaled = self.scale
                        self.update_state("update")
                    self.clicked = True
                else:
                    if self.clicked:
                        self.clicked = False
                        return True
                    if self.scaled != self.scale + self.scale_change:
                        self.scaled = self.scale + self.scale_change
                        self.update_state("update")
            elif self.scaled != self.scale:
                self.scaled = self.scale
                self.update_state("update")
        else:
            return False

    def disable(self):
        self.check_disable = True

    def enable(self):
        self.check_disable = False

import pygame


class Button:
    def __init__(self, rect, text, font, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = (180, 140, 80) if self.hovered else (120, 80, 40)
        pygame.draw.rect(surface, color, self.rect, border_radius=16)
        pygame.draw.rect(surface, (60, 40, 20), self.rect, 3, border_radius=16)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()


class StartMenu:
    def __init__(self, surface, start_callback, exit_callback):
        self.surface = surface
        self.bg_img = pygame.image.load(
            "src/data/graphics/starting_screen.jpg"
        ).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, surface.get_size())
        self.font = pygame.font.SysFont("georgia", 36, bold=True)
        w, h = surface.get_size()
        menu_w, menu_h = 500, 320
        self.menu_rect = pygame.Rect(
            (w - menu_w) // 2, (h - menu_h) // 2, menu_w, menu_h
        )
        btn_w, btn_h = 370, 70
        btn_y = self.menu_rect.y + 120
        self.buttons = [
            Button(
                rect=(self.menu_rect.x + (menu_w - btn_w) // 2, btn_y, btn_w, btn_h),
                text="Start New Game",
                font=self.font,
                callback=start_callback,
            ),
            Button(
                rect=(
                    self.menu_rect.x + (menu_w - btn_w) // 2,
                    btn_y + btn_h + 20,
                    btn_w,
                    btn_h,
                ),
                text="Exit the Game",
                font=self.font,
                callback=exit_callback,
            ),
        ]

    def draw(self):
        # Dim background
        self.surface.blit(self.bg_img, (0, 0))
        s2 = pygame.Surface(self.menu_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s2, (180, 140, 80, 255), s2.get_rect(), border_radius=24)
        inner_rect = s2.get_rect().inflate(-12, -12)
        pygame.draw.rect(s2, (60, 40, 20, 220), inner_rect, border_radius=18)
        self.surface.blit(s2, self.menu_rect.topleft)
        # Title
        title_font = pygame.font.SysFont("georgia", 54, bold=True)
        title_surf = title_font.render("Dungeon Time", True, (255, 230, 180))
        title_rect = title_surf.get_rect(
            center=(self.menu_rect.centerx, self.menu_rect.y + 58)
        )
        self.surface.blit(title_surf, title_rect)
        # Buttons
        for btn in self.buttons:
            btn.draw(self.surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)


class LanguageMenu:
    def __init__(self, surface, start_callback, back_callback):
        self.surface = surface
        self.font = pygame.font.SysFont("georgia", 32, bold=True)
        w, h = surface.get_size()
        menu_w, menu_h = 500, 450
        self.menu_rect = pygame.Rect(
            (w - menu_w) // 2, (h - menu_h) // 2, menu_w, menu_h
        )
        btn_w, btn_h = 340, 60
        btn_y = self.menu_rect.y + 110
        self.buttons = [
            Button(
                rect=(self.menu_rect.x + (menu_w - btn_w) // 2, btn_y, btn_w, btn_h),
                text="English",
                font=self.font,
                callback=lambda: start_callback("en"),
            ),
            Button(
                rect=(
                    self.menu_rect.x + (menu_w - btn_w) // 2,
                    btn_y + btn_h + 18,
                    btn_w,
                    btn_h,
                ),
                text="Deutsch",
                font=self.font,
                callback=lambda: start_callback("de"),
            ),
            Button(
                rect=(
                    self.menu_rect.x + (menu_w - btn_w) // 2,
                    btn_y + 2 * btn_h + 36,
                    btn_w,
                    btn_h,
                ),
                text="Українська",
                font=self.font,
                callback=lambda: start_callback("ua"),
            ),
            Button(
                rect=(
                    self.menu_rect.x + (menu_w - btn_w) // 2,
                    btn_y + 3 * btn_h + 54,
                    btn_w,
                    btn_h,
                ),
                text="Back",
                font=self.font,
                callback=back_callback,
            ),
        ]

    def draw(self):
        # Dim background
        s = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        self.surface.blit(s, (0, 0))
        s2 = pygame.Surface(self.menu_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s2, (180, 140, 80, 255), s2.get_rect(), border_radius=24)
        inner_rect = s2.get_rect().inflate(-12, -12)
        pygame.draw.rect(s2, (60, 40, 20, 230), inner_rect, border_radius=18)
        self.surface.blit(s2, self.menu_rect.topleft)
        # Title
        title_font = pygame.font.SysFont("georgia", 40, bold=True)
        title_surf = title_font.render("Choose the language", True, (255, 230, 180))
        title_rect = title_surf.get_rect(
            center=(self.menu_rect.centerx, self.menu_rect.y + 58)
        )
        self.surface.blit(title_surf, title_rect)
        # Buttons
        for btn in self.buttons:
            btn.draw(self.surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)


class NameMenu:
    def __init__(self, surface, start_callback, back_callback):
        self.surface = surface
        self.font = pygame.font.SysFont("georgia", 32, bold=True)
        w, h = surface.get_size()
        menu_w, menu_h = 500, 300
        self.menu_rect = pygame.Rect(
            (w - menu_w) // 2, (h - menu_h) // 2, menu_w, menu_h
        )
        self.input_box = pygame.Rect(
            self.menu_rect.x + 80, self.menu_rect.y + 110, 340, 60
        )
        self.name = ""
        self.active = False
        self.start_callback = start_callback
        self.back_callback = back_callback
        self._start_btn = None
        self._back_btn = None

    def draw(self):
        # Dim background
        s = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        self.surface.blit(s, (0, 0))
        s2 = pygame.Surface(self.menu_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s2, (180, 140, 80, 255), s2.get_rect(), border_radius=24)
        inner_rect = s2.get_rect().inflate(-12, -12)
        pygame.draw.rect(s2, (60, 40, 20, 230), inner_rect, border_radius=18)
        self.surface.blit(s2, self.menu_rect.topleft)
        # Title
        title_font = pygame.font.SysFont("georgia", 40, bold=True)
        title_surf = title_font.render("Enter your name", True, (255, 230, 180))
        title_rect = title_surf.get_rect(
            center=(self.menu_rect.centerx, self.menu_rect.y + 48)
        )
        self.surface.blit(title_surf, title_rect)
        # Input box
        box_color = (255, 255, 255) if self.active else (220, 210, 180)
        border_color = (100, 180, 255) if self.active else (180, 140, 80)
        pygame.draw.rect(self.surface, box_color, self.input_box, 0, border_radius=12)
        pygame.draw.rect(
            self.surface, border_color, self.input_box, 3, border_radius=12
        )
        name_surf = self.font.render(
            self.name or "Type here...",
            True,
            (60, 40, 20) if self.name else (180, 140, 80),
        )
        name_rect = name_surf.get_rect(center=self.input_box.center)
        self.surface.blit(name_surf, name_rect)
        # Start and Back buttons
        btn_font = pygame.font.SysFont("georgia", 28, bold=True)
        mouse_pos = pygame.mouse.get_pos()
        start_btn_rect = pygame.Rect(
            self.menu_rect.x + 60, self.menu_rect.y + 200, 170, 50
        )
        back_btn_rect = pygame.Rect(
            self.menu_rect.x + 270, self.menu_rect.y + 200, 170, 50
        )
        self._start_btn = Button(
            start_btn_rect, "Start", btn_font, lambda: self.start_callback(self.name)
        )
        self._back_btn = Button(back_btn_rect, "Back", btn_font, self.back_callback)
        self._start_btn.hovered = start_btn_rect.collidepoint(mouse_pos)
        self._back_btn.hovered = back_btn_rect.collidepoint(mouse_pos)
        self._start_btn.draw(self.surface)
        self._back_btn.draw(self.surface)

    def handle_event(self, event):
        self._start_btn.handle_event(event)
        self._back_btn.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.input_box.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.start_callback(self.name)
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif len(self.name) < 16 and event.unicode.isprintable():
                self.name += event.unicode

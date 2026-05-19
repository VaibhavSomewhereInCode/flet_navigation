"""
Reusable navigation bar system for Flet apps.

Usage:
    from nav_bar import NavBar, NavDestination

    navbar = NavBar(
        destinations=[
            NavDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            NavDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"),
        ],
        on_change=lambda index: print(f"Switched to tab {index}"),
        bgcolor="#1a1a24",
        indicator_color="#7c5cfc33",
        shadow_color="#0f0f14",
        elevation=8,
    )

    # In your render function:
    page.navigation_bar = navbar.build(selected_index=current_tab)
"""

from dataclasses import dataclass, field
import flet as ft


@dataclass
class NavDestination:
    """A single tab destination in the navigation bar."""
    icon: str
    selected_icon: str
    label: str


class NavBar:
    """
    A generalized, reusable navigation bar wrapper.

    Parameters
    ----------
    destinations : list[NavDestination]
        The tabs to display.
    on_change : callable(int) -> None
        Called with the new index when the user taps a tab.
    bgcolor : str | None
        Background colour of the bar.
    indicator_color : str | None
        Colour of the selected-tab indicator pill.
    shadow_color : str | None
        Shadow colour underneath the bar.
    elevation : float
        Elevation (shadow depth) of the bar.
    """

    def __init__(
        self,
        destinations: list[NavDestination],
        on_change: callable,
        bgcolor: str | None = None,
        indicator_color: str | None = None,
        shadow_color: str | None = None,
        elevation: float = 8,
    ):
        self.destinations = destinations
        self._on_change = on_change
        self.bgcolor = bgcolor
        self.indicator_color = indicator_color
        self.shadow_color = shadow_color
        self.elevation = elevation

    # ── public API ───────────────────────────────────────────────────

    def build(self, selected_index: int = 0) -> ft.NavigationBar:
        """Build and return a fresh ``ft.NavigationBar`` control."""
        return ft.NavigationBar(
            selected_index=selected_index,
            bgcolor=self.bgcolor,
            indicator_color=self.indicator_color,
            shadow_color=self.shadow_color,
            elevation=self.elevation,
            on_change=self._handle_change,
            destinations=[
                ft.NavigationBarDestination(
                    icon=d.icon,
                    selected_icon=d.selected_icon,
                    label=d.label,
                )
                for d in self.destinations
            ],
        )

    # ── internals ────────────────────────────────────────────────────

    def _handle_change(self, e):
        """Unwrap the Flet event and forward just the index."""
        self._on_change(e.control.selected_index)

"""This module provides functionality for defining your site and registrering applications"""
from functools import wraps
from typing import Callable, Dict

import param

from .application import Application


class Site(param.Parameterized):
    """The Site provides meta data and functionality for registrering application meta data and
    views"""

    applications = param.List(
        doc="The list of applications to include in the site", constant=True
    )

    def __init__(self, **params):
        if "applications" not in params:
            params["applications"] = []

        super().__init__(**params)

    def register(self, application: Application):
        """Registers you application meta data and view
        >>> from awesome_panel_extensions.site import Author
        >>> from awesome_panel_extensions.site import Site, Application
        >>> site = Site(name="awesome-panel.org")
        >>> marc_skov_madsen = Author(
        ...     name="Marc Skov Madsen",
        ...     url="https://datamodelsanalytics.com",
        ...     avatar_url="https://avatars0.githubusercontent.com/u/42288570",
        ...     twitter_url="https://twitter.com/MarcSkovMadsen",
        ...     linkedin_url="https://www.linkedin.com/in/marcskovmadsen/",
        ...     github_url="https://github.com/MarcSkovMadsen",
        ... )
        >>> home = Application(
        ...     name="Home",
        ...     description="The home page of awesome-panel.org.",
        ...     url="home",
        ...     thumbnail_url="",
        ...     documentation_url="",
        ...     code_url="",
        ...     youtube_url="",
        ...     gif_url="",
        ...     author=marc_skov_madsen,
        ...     tags=["Site"],
        ... )
        >>> @site.register(application=home)
        ... def view():
        ...     return pn.pane.Markdown("# Home")
        >>> site.applications
        [Home]
        >>> site.routes
        {'home': <function view at...>}
        """

        def inner_function(view):
            application.view = view
            # pylint: disable=unsupported-membership-test
            if application not in self.applications:
                # pylint: disable=unsupported-assignment-operation
                self.applications.append(application)

            @wraps(view)
            def wrapper(*args, **kwargs):
                view(*args, **kwargs)

            return wrapper

        return inner_function

    @property
    def routes(self) -> Dict[str, Callable]:
        """Returns a dictionary with the url as key and the view as the value

        Returns:
            Dict[str, Callable]: [description]
        """
        # pylint: disable=not-an-iterable
        return {app.url: app.view for app in self.applications}

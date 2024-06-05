"""Developer frontpage for Digital Hospitals project."""

import os

import dash_mantine_components as dmc
from dash import Dash
from dash_compose import composition

IFM_LINK = "https://www.ifm.eng.cam.ac.uk/research/dial/research-projects/"\
    "current-projects/distributed-information-and-automation-laboratory/"

README_URL = f"https://github.com/{os.environ['DH_GITHUB']}/blob/main/README.md"


def color(col: str, variant: int) -> str:
    return dmc.DEFAULT_THEME['colors'][col][variant]


@composition
def layout(main_content: dmc.AppShellMain):
    """Page layout."""
    with dmc.MantineProvider(
        id='mantine-provider',
        forceColorScheme="dark"
    ) as container:
        with dmc.AppShell(
            [],
            header={"height": 53},
            footer={"height": 45},
            miw=600,
            py="lg",
            px="xl"
        ):
            with dmc.AppShellHeader(
                [], zIndex=2000, px="xl", py="sm", miw=600, bg=color('indigo', 9), id='header'
            ):
                with dmc.Container(fluid=True, p=0):
                    with dmc.Flex(
                        justify={"base": "space-between"},
                    ):
                        yield dmc.Text(
                            "University of Cambridge: Digital Hospitals Project",
                            size="xl",
                            fw=700
                        )
            yield main_content
            with dmc.AppShellFooter(
                [], zIndex=2000, px="xl", py="sm", miw=600, bg=color('dark', 9),
                id='footer'
            ):
                with dmc.Text(size="sm"):
                    yield "© 2024 "
                    yield dmc.Anchor("Digital Hospitals project", href=IFM_LINK,
                                     target='_blank', c='white', unstyled=True)
                    yield ", Institute for Manufacturing, University of Cambridge"

    return container


@composition
def body():
    """The main div of the webpage."""
    with dmc.AppShellMain([], miw=600, px='xl') as content:
        yield dmc.Title("Developer Portal", order=2, mb='sm',
                        style={'text-decoration-line': 'underline'})
        with dmc.List():
            with dmc.ListItem():
                yield dmc.Anchor(
                    "Project README.md (on Github)", href=README_URL, refresh=True, target='_self'
                )
            with dmc.ListItem():
                yield dmc.Anchor(
                    "Project documentation - main", href="/dev/specs/", refresh=True, target='_self'
                )
                yield ' (warning - unstable and subject to change)'
        yield dmc.Title('API documentaton (Swagger)', order=3)
        with dmc.List():
            with dmc.ListItem():
                yield dmc.Anchor(
                    "Example module", href="/api/example/docs", refresh=True, target='_self'
                )
            with dmc.ListItem():
                yield dmc.Anchor(
                    "BIM (Building information modelling) module",
                    href="/api/bim/docs", refresh=True, target='_self'
                )
    return content


app = Dash(
    __name__,
    title='Developer Portal',
    url_base_pathname='/dev/'
)
app.layout = layout(body())
server = app.server

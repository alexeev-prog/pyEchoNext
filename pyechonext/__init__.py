"""
EchoNext is a lightweight, fast and scalable web framework for Python
Copyright (C) 2024	Alexeev Bronislav (C) 2024

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
USA
"""

import requests
from rich import print
from rich.traceback import install

__version__ = "0.7.18"
install(show_locals=True)


def check_for_update():
    """
    Check for update in pypi
    """
    try:
        response = requests.get("https://pypi.org/pypi/pyechonext/json").json()

        latest_version = response["info"]["version"]

        latest_digits = [int(n) for n in latest_version.split(".")]
        current_digits = [int(n) for n in __version__.split(".")]

        if sum(latest_digits) > sum(current_digits):
            message = f"New version of library pyEchoNext available: {latest_version}"

            print(
                f"[red]{'#' * (len(message) + 4)}\n#[/red][bold yellow]"
                f" {message} [/bold yellow][red]#\n{'#' * (len(message) + 4)}[/red]\n"
            )
        elif sum(latest_digits) < sum(current_digits):
            print(
                "[yellow]You use [bold]UNSTABLE[/bold] branch of pyEchoNext. Stable"
                f" version: {latest_version}, your version: {__version__}[/yellow]\n"
            )
    except requests.RequestException:
        print(
            "[dim]Version updates information not available. Your version:"
            f" {__version__}[/dim]"
        )


check_for_update()

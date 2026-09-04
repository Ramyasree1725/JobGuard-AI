"""
Aetheris Command Line Interface: Terminal Formatting & ASCII Tables
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import List, Sequence


class TerminalFormatter:
    """ASCII Terminal Formatting, Colors, and Tables."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @classmethod
    def print_banner(cls) -> None:
        banner = r"""
   ___       __  __            _        ___                           _     
  / _ \___  / /_/ /  ___ ____ (_)__    / _ \___ ___ ___ ___ _________/ /    
 / // / _ \/ __/ _ \/ -_) __// (_-<   / , _/ -_|_-</ -_) _ `/ __/ __/ _ \   
/____/\___/\__/_//_/\__/_/  /_/___/  /_/|_|\__/___/\__/\_,_/_/  \__/_//_/   
                     AETHERIS AUTONOMOUS SIMULATION PLATFORM v1.0.0
        """
        print(cls.CYAN + cls.BOLD + banner + cls.ENDC)

    @classmethod
    def print_table(cls, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Header border
        sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
        print(sep)
        header_row = "| " + " | ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers)) + " |"
        print(cls.BOLD + header_row + cls.ENDC)
        print(sep)

        for row in rows:
            line = "| " + " | ".join(f"{str(cell):<{widths[i]}}" for i, cell in enumerate(row)) + " |"
            print(line)

        print(sep)

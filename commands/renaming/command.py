from commands.renaming.apply import apply_renaming
from commands.renaming.reverse import reverse_renaming

from core.options import Options

def rename_games(opts: Options) -> None:
    if opts.reverse_renaming:
        reverse_renaming(opts)
    else:
        apply_renaming(opts)
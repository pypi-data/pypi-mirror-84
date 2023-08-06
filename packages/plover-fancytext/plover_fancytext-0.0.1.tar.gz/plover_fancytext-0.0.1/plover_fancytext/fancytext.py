from threading import Thread
from plover.engine import StenoEngine
from plover import log

from plover.registry import registry
from plover.formatting import _Context

from .zalgo import Zalgo
from .sarcasm import Sarcasm
from .substitute import Substitute
from .character_helpers import \
    BUBBLE_MAP, MEDIEVAL_MAP, UPSIDE_DOWN_MAP, FULLWIDTH_MAP


class PloverPlugin(Thread):

    def __init__(self, engine: StenoEngine) -> None:
        super().__init__()

        log.info("FANCY_INIT")
        registry.register_plugin('meta', 'fancytext_set', self.fancy_set)

        self.formatter = None
        self.engine = engine
        self.transformers = {
            'bubble': Substitute(BUBBLE_MAP),
            'medieval': Substitute(MEDIEVAL_MAP),
            'fullwidth': Substitute(FULLWIDTH_MAP),
            'sarcasm': Sarcasm(),
            'upsidedown': Substitute(UPSIDE_DOWN_MAP),
            'zalgo': Zalgo()
        }

    def fancy_set(self, ctx: _Context, cmdline):
        if cmdline in self.transformers:
            self.formatter = self.transformers[cmdline]
        else:
            self.formatter = None

        return ctx.new_action()

    def start(self) -> None:
        log.info("FANCY_START")
        self.engine.hook_connect("translated", self.translated)
        super().start()

    def stop(self) -> None:
        self.engine.hook_disconnect("translated", self.translated)

    def translated(self, old, new):
        if self.formatter:

            log.info(old)
            log.info(new)

            for t in new:
                if t.text:
                    t.text = (self.formatter(t.text))
                if t.word:
                    t.word = (self.formatter(t.word))
                if t.prev_replace:
                    t.prev_replace = self.formatter(t.prev_replace)

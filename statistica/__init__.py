"""The 4th rewrite of Statistica"""

import re

import discord

from .command import CommandParser
from .config import grammar


class Statistica(discord.Client):
    """The custom bot class"""

    def __init__(self):
        discord.Client.__init__(self)
        self.parser = CommandParser(grammar_str=grammar.GRAMMAR)

    def show_presence(self):
        """Display's Statistica's status in the presence slot on Discord"""

    def assimilate(self, messages):
        """Learns a large number of messages"""

    def learn(self, message):
        """Learns a single message"""

    def generate(self, ctx):
        """Generates a sentence or passage"""

import socket
import belacomInfo
import json
import sys
import threading
import os

class ascii:
    def __init__(self):
        pass

    def asciiRender(self, gameState):
        os.system("cls" if os.name == "nt" else "clear")
        for i in range(len(gameState)):
            print("".join(gameState[i]))

    def asciiToList(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            grid = [list(line.rstrip("\n")) for line in f]
        return grid

#!/usr/bin/env python
#! -*- coding:utf-8 -*-

__author__ = 'psava, egrinstein, mbvaz'

import os, sys
import pygame

from pygame.locals import *
from GameMain import GameMain
from BackgroundMap import BackgroundMap


if __name__ == "__main__":
    
    MainWindow = GameMain()
    MainWindow.MainLoop()

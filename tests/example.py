#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ***DESCRIPTION***.
#
#  Copyright (C)
#  Honda Research Institute Europe GmbH
#  Carl-Legien-Str. 30
#  63073 Offenbach/Main
#  Germany
#
#  UNPUBLISHED PROPRIETARY MATERIAL.
#  ALL RIGHTS RESERVED.
#
#

from tulip_agent import CotTulipAgent, ToolLibrary


tulip = ToolLibrary(
    chroma_sub_dir="tmp/",
    file_imports=[("tools", [])],
    default_timeout=1,
)
cta = CotTulipAgent(tool_library=tulip)
cta.query(prompt="What is 2+2?")
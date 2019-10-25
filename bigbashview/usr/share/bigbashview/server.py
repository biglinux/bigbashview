#!/usr/bin/python3
from bbv.server.bbv2server import run_server
from bbv import globals as globaldata
if __name__ == "__main__":
	globaldata.COMPAT = True
	run_server(background=False)

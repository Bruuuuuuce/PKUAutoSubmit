from configparser import ConfigParser
import argparse

cfg = ConfigParser()
cfg.read("config.sample.ini")

parser = argparse.ArgumentParser(description="generate config.ini")

parser.add_argument("-u", type=str, help="学号")
parser.add_argument("-p", type=str, help="密码")
args = parser.parse_args()
cfg.set("login", "username", args.u)
cfg.set("login", "password", args.p)
cfg.write(open("config.ini", "w"))

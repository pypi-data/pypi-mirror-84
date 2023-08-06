from humbletray.systray import run_gui
import justpy as jp
from humbletray import systray
from pystray import MenuItem, Menu
# from loguru import logger
import schedule
import time

# logger.add("humble.log")
wp = jp.WebPage(delete_flag=False)


def start_server(iq):
    wp.q = iq
    wp.add(jp.Hello())
    jp.justpy(lambda: wp)


def open():
    print("open")
    # logger.info("open")


def job():
    # logger.info("I'm working!")
    time.sleep(10)


schedule.every(10).seconds.do(job)


# @logger.catch
def main():

    menu = [
        MenuItem("Remote Open", lambda: open()),
    ]

    systray.run_gui(start_server, menu, schedule=schedule)


if __name__ == "__main__":
    main()
### IMPORTS                 ###pip install more-properties
    ## Dependencies             ##
import pyscreenshot             as ss
import pyautogui                as ui
import win32.win32api           as win
import imagehash                as compare
import PIL.Image                as pil
import more_properties          as props
    ## Dependencies             ##
import collections
import typing
import os
import time
### IMPORTS                 ###
### RUN                     ###
    ## Class                    ##
class _Run(object):
    def __init__(self, path_to_exe): self.__path = path_to_exe
    def __enter__(self): os.system(self.__path)
    def __exit__(self, *args, **kwargs): os.system(f"TASKKILL /F /IM {self.__path}")
    ## Class                    ##
    ## Func                     ##
def _run(path_to_exe):
    """
    
    """
    return _Run(path_to_exe)
    ## Func                     ##
### RUN                     ###
### WINDOW                  ###
class _Window(object):
    class ImageChecks(object):
        image_cutoff = 20
        main_menu = (
            (512, 583), (1083, 734)
        )

    _BASE_RESOLUTION     = (1600, 900)
    _LOCAL_BTN           = (520, 552)
    _ONLINE_BTN          = (835, 559)
    _INSTRUCT_BTN        = (514, 680)
    _FREEPLAY_BTN        = (829, 685)
    _ANNOUCEMENT_BTN     = (490, 834)
    _SETTINGS_BTN        = (643, 807)
    _TUPLE_INT_DIV    = lambda i, j: tuple(e1 // e2 for e1, e2 in zip(i, j))
    _TUPLE_DIV        = lambda i, j: tuple(e1 /  e2 for e1, e2 in zip(i, j))

    class Freeplay(object):
        _SKELD_BTN          = (1157, 577)

    @props.staticproperty
    def resolution() -> typing.Tuple[int]:
        """
        Returns the resolution of your computer
        """
        return (win.GetSystemMetrics(0), win.GetSystemMetrics(1))

    @classmethod
    def _scale(cls, resol: tuple) -> typing.Tuple[int]: return cls._TUPLE_INT_DIV(
        cls._BASE_RESOLUTION,
        resol
    )
### WINDOW                  ###
### UTIL                    ###
class _Util(object):
    class Temp(object):
        def __init__(self, img, fn): self.__img, self.__fn = img, fn
        def __enter__(self): self.__img.save(self.__fn); return self
        def __exit__(self, *args, **kwargs): os.remove(self.__fn)
    @classmethod
    def temp_image(cls, img, fn): return cls.Temp(img, fn)
### UTIL                    ###
### API FUNCS               ###
class Api(_Window):
    """
    Api Class for interacting with Among Us 
    """
    RESOL = _Window.resolution
    SCALE = _Window._scale(RESOL)
    @staticmethod
    def run(path_to_exe: str) -> _Run:
        """
        
        """
        return _run(path_to_exe)
### API FUNCS               ###
### MAINMENU                ###
class MainMenu(Api):
    ## Documentation            ##
    """ For interacting with the main menu """
    ## Documentation            ##
    ## Button Positions         ##
    @props.classproperty
    def localBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of the local button
    """; return cls._TUPLE_DIV(cls._LOCAL_BTN, cls.SCALE)
    
    @props.classproperty
    def onlineBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of the online button
    """; return cls._TUPLE_DIV(cls._ONLINE_BTN, cls.SCALE)

    @props.classproperty
    def instructBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of the 'how to play' button
    """; return cls._TUPLE_DIV(cls._INSTRUCT_BTN, cls.SCALE)

    @props.classproperty
    def freeplayBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of the freeplay button
    """; return cls._TUPLE_DIV(cls._FREEPLAY_BTN, cls.SCALE)

    @props.classproperty
    def annoucementBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of the annoucements button
    """; return cls._TUPLE_DIV(cls._ANNOUCEMENT_BTN, cls.SCALE)

    @props.classproperty
    def settingsBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of the settings button
    """; return cls._TUPLE_DIV(cls._SETTINGS_BTN, cls.SCALE)
    ## Button Positions         ##
    ## Click Buttons            ##
    @classmethod
    def clickLocalBtn(cls): """ Clicks the local button """; ui.click(*cls.localBtnPos)
    
    @classmethod
    def clickOnlineBtn(cls): """ Clicks the online button """; ui.click(*cls.onlineBtnPos)
    
    @classmethod
    def clickInstructBtn(cls): """ Clicks the "How To Play" button """; ui.click(
        *cls.instructBtnPos
    )

    @classmethod
    def clickFreeplayBtn(cls): """ Clicks the freeplay button """; ui.click(
        *cls.freeplayBtnPos
    )

    @classmethod
    def clickAnnoucementBtn(cls): """ Clicks the annoucement button """; ui.click(
        *cls.annoucementBtnPos
    )

    @classmethod
    def clickSettingsBtn(cls): """ Clicks the settings button """; ui.click(
        *cls.settingsBtnPos
    )
    ## Click Buttons            ##
    ## Tests                    ##
    @props.staticproperty
    def inMainMenu():
        mainmenu = ss.grab(bbox=(
            *_Window.ImageChecks.main_menu[0],
            *_Window.ImageChecks.main_menu[1]
        ))
        mmf = os.path.join(os.getcwd(), 'amongUsAPI', 'mainmenu.png')
        with _Util.temp_image(mainmenu, "temp.jpg") as _:
            temphash = compare.average_hash(pil.open('temp.jpg'))
            mainmenu_hash = compare.average_hash(pil.open(mmf))
        return (temphash - mainmenu_hash) < _Window.ImageChecks.image_cutoff
    ## Tests                    ##
### MAINMENU                ###
### FREEPLAY MENU           ###
class FreeplayMenu(Api):
    ## Documentation            ##
    """ For interacting with the freeplay menu """
    ## Documentation            ##
    ## Button Positions         ##
    @props.classproperty
    def skeldBtnPos(cls) -> typing.Tuple[int]: """
    Returns the position of The Skeld Map
    """; return cls._TUPLE_DIV(cls.Freeplay._SKELD_BTN, cls.SCALE)
    ## Button Positions         ##
    ## Click Buttons            ##
    @classmethod
    def clickSkeldBtn(cls): """ Clicks the Skeld Map button """; ui.click(*cls.skeldBtnPos)
    ## Click Buttons            ##
### FREEPLAY MENU           ###
### DOCUMENTATION           ###
"""

"""
### DOCUMENTATION           ###
### TESTS                   ###
# time.sleep(5)
# ui.PAUSE = 1.1
# print(ui.position())
### TESTS                   ###
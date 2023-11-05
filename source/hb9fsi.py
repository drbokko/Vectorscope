# Use this template to start your VectorOS program:
import screennorm
import machine 
import gc
import vectoros
import asyncio
import keyleds
import keyboardcb
import timer
from vos_state import vos_state
from vectorscope_mock import VectorscopeMock
from dds import DDS
## Badge-specific classes 
from codec import Codec
from waveform import Waveform
from adc_reader import ADC_Reader

screen=screennorm.ScreenNorm()   # get the screen


task_name="hb9fsi"  # use this name in vos_launch.py, too
_run_every_ms=500   # how often to loop


_freeze=False
_exit=False
_menu_key=None

# Outsiders can call this to exit you
def exit(key=None):
    global _exit,task_name, _menu_key
    _exit=True
    vectoros.remove_task(task_name)
    _menu_key.detach()
    vos_state.show_menu=True
# do any cleanup (keyboard, timers) you need here
# or consider a "finally" in the main loop


# Outsiders can call this to pause you
def freeze(state=True):
    global _freeze
    _freeze=state

def play_morse(text):
    # Tone is connected to Y
    gc.collect()

    v = VectorscopeMock()
    d = DDS(v)
    d.increment = [1500, 1200]
    d.amplitude=[0.5, 0.5]
    d.recalculate_waveforms()

    for i in range(0,10):
        machine.Pin(22, machine.Pin.OUT).toggle()
        asyncio.sleep_ms(100)
    print(text)
    pass

def joycb(key):
    # A for morse code
    if (key==keyleds.A):
            oldpause=pauseflag
            pauseflag=False   # make sure it redraws
            play_morse("HB9FSI")
            pauseflag=oldpause


async def vos_main():
    global _freeze, _exit, _run_every_ms, task_name, _menu_key
    _freeze=False
    _exit=False
# exit on Menu
    _menu_key=keyboardcb.KeyboardCB({keyleds.KEY_MENU: exit})

# if you want to control keyboard and LED without running the whole OS
    if vectoros.vectoros_active()==False:
        keyboardcb.KeyboardCB.run(250)
        timer.Timer.run()
    while _exit==False:
        if _freeze==False:
# your code will mostly go here
            screen.jpg("hb9fsi_qr.jpg")

        await asyncio.sleep_ms(_run_every_ms)   

    _exit=False  # reset for next time
    vectoros.remove_task(task_name)   # make sure we are removed (also does this in exit)

def main():
    asyncio.run(vos_main())
# code here will never, ever run under VectorOS

# if you want the possibility to run directly without VectorOS
#if __name__=="__main__":
#    main()

# if you want to configure to run in vos_launch but still run this file
# add the main function to to vos_launch.py and use this:
if __name__=="__main__":
    vectoros.run()
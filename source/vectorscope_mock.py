import gc
import time
import gc9a01
import uctypes
import machine
import _thread

## Badge-specific classes 
from codec import Codec
from waveform import Waveform
from adc_reader import ADC_Reader
from pixel_pusher import Pixel_Pusher

## Misc helpers and defines
import dma_defs
import pin_defs

class VectorscopeMock():

    def __init__(self, screen_running = False):
       
        ## Couple buttons if you want to play with them
        # self.audio_shutdown_pin = machine.Pin(pin_defs.audio_shutdown, machine.Pin.OUT, value=1)
        self.user_button        = machine.Pin(pin_defs.user_button, machine.Pin.IN)
        
        ## Turn up the heat!
        machine.freq(250_000_000)
        
        ## start up I2S state machines
        self.codec = Codec()
        gc.collect()

        ## Fire up the I2S output feeder
        self.wave = Waveform() 
        gc.collect()

        ## sets up memory, DMAs to continuously read in ADC data into a 16-stage buffer
        self.adc_reader = ADC_Reader()
        gc.collect()

        ## automatically blits memory out to screen
        ## needs adc_reader b/c needs to know where samples go
        ## this is the real house of cards...
        self.pixel_pusher = Pixel_Pusher(self.adc_reader)
        gc.collect()

    def deinit(self):

        self.kill_phosphor = True
        machine.freq(125_000_000)

        self.adc_reader.deinit()
        self.wave.deinit()
        self.codec.deinit()

        ## doesn't seem to work.  
        ## Get OS Error 16 on next run
        ## brute force... grrr...
        machine.reset()
        

    def call_out(self):
        pass



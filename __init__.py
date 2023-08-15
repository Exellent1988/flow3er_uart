from st3m.application import Application, ApplicationContext
from st3m.ui.colours import PUSH_RED, GO_GREEN, BLACK
from st3m.goose import Dict, Any
from st3m.input import InputController, InputState

from ctx import Context
import leds
import badgelink

import machine
import math
import json
from st3m import logging
import st3m.run



log = logging.Log(__name__, level=logging.INFO)
log.info("Start UART DEMO")
class UART_SEND(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.input = InputController()
        self._scale = 1.0
        self._led = 0.0
        self._phase = 0.0
        self.text= None
        self.Display_Text = '-'
        jack = badgelink.right
        jack.enable()
        self.uart = machine.UART(1, baudrate=9600, tx=jack.tip.pin.num(), rx=jack.ring.pin.num())
        jackleft = badgelink.left
        jackleft.enable()
        self.uart2 = machine.UART(1, baudrate=9600, tx=jackleft.ring.pin.num(), rx=jackleft.tip.pin.num())

       


    def draw(self, ctx: Context) -> None:
        ctx.text_align = ctx.LEFT
        ctx.text_baseline = ctx.BOTTOM
        ctx.font_size = 20
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(*GO_GREEN)
        ctx.move_to(-60, -60)
        ctx.save()
        readline = self.uart2.readline()
        if  readline != bytes([00]) and readline != None:
            self.Display_Text = readline.decode()
            log.info('receive: '+ readline.decode())
            leds.set_all_rgb(0,255,0)
            ctx.text(self.Display_Text)
            self.text = None
        else:
            leds.set_all_rgb(255,0,0)
            
        if self.text != None:
            self.uart.write(self.text)
           
       
        else:
            self.uart.flush()
            # self.uart2.flush()
            
        ctx.text(self.Display_Text)
        ctx.restore()
        

        
        leds.update()
        # ctx.fill()


    def think(self, ins: InputController, delta_ms: int) -> None:
        super().think(ins, delta_ms)

        # self._phase += delta_ms / 1000
        # self._scale = math.sin(self._phase)
        self._led += delta_ms / 45
        if self._led >= 40:
            self._led = 0

        

        if self.input.buttons.app.left.pressed:
            self.text = 'left\r\n'
            log.info('send: left')
        elif self.input.buttons.app.right.pressed:
            self.text = 'right\r\n'
            log.info('send:right')

if __name__ == '__main__':
    # Continue to make runnable via mpremote run.
    st3m.run.run_view(UART_SEND(ApplicationContext()))


import RPi.GPIO as gpio
from robot_core.executor.executor import Executor


class Motor2wdExecutor(Executor):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

    def execute(self, **kwargs):
        if kwargs["command"] == "start_forward":
            return self.start_forward()
        elif kwargs["command"] == "stop_forward":
            return self.stop()
        elif kwargs["command"] == "start_backward":
            return self.start_backward()
        elif kwargs["command"] == "start_left":
            return self.start_left()
        elif kwargs["command"] == "start_right":
            return self.start_right()

    def start_forward(self):
        # roda esquerda frente
        gpio.setup(2, gpio.OUT)
        gpio.output(2, True)
        gpio.setup(3, gpio.OUT)
        gpio.output(3, False)

        # roda direta pra frente
        gpio.setup(18, gpio.OUT)
        gpio.output(18, True)
        gpio.setup(24, gpio.OUT)
        gpio.output(24, False)

    def stop(self):
        gpio.output(2, False)
        gpio.output(3, False)
        gpio.output(18, False)
        gpio.output(24, False)

    def start_backward(self):
        # roda esquerda tras
        gpio.setup(2, gpio.OUT)
        gpio.output(2, False)
        gpio.setup(3, gpio.OUT)
        gpio.output(3, True)

        # roda direita pra tras
        gpio.setup(18, gpio.OUT)
        gpio.output(18, False)
        gpio.setup(24, gpio.OUT)
        gpio.output(24, True)

    def start_left(self):
        # roda direta pra frente
        gpio.setup(18, gpio.OUT)
        gpio.output(18, True)
        gpio.setup(24, gpio.OUT)
        gpio.output(24, False)

        # roda esquerda tras
        gpio.setup(2, gpio.OUT)
        gpio.output(2, False)
        gpio.setup(3, gpio.OUT)
        gpio.output(3, True)

    def start_right(self):
        # roda esquerda frente
        gpio.setup(2, gpio.OUT)
        gpio.output(2, True)
        gpio.setup(3, gpio.OUT)
        gpio.output(3, False)

        # roda direita pra tras
        gpio.setup(18, gpio.OUT)
        gpio.output(18, False)
        gpio.setup(24, gpio.OUT)
        gpio.output(24, True)

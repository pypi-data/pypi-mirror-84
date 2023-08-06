import launchpad_py
from typing import List

class CustomButton:

    def __init__(self, x: int, y: int, pressed: bool):
        self.x: int = x
        self.y: int = y
        self.pressed: bool = pressed

    def __eq__(self, other):
        return other.replace(" ", "") == f"{self.x},{self.y},{self.pressed}"

    def __str__(self):
        return f"(X: {self.x}, Y: {self.y}, P: {self.pressed})"

    def __repr__(self):
        return f"(X: {self.x}, Y: {self.y}, P: {self.pressed})"


class CustomLP(launchpad_py.LaunchpadMk2):

    def GetButtonsXY(self) -> List[CustomButton]:

        result_list: list = []
        current_btn = self.ButtonStateXY()


        while current_btn:
            result_list.append(CustomButton(current_btn[0], current_btn[1], current_btn[2] != 0))
            current_btn = self.ButtonStateXY()


        return result_list


    def draw_list(self, raster: list):
        pixels_length = 9
        for i in range(pixels_length ** 2):
            if i == pixels_length - 1: continue

            x = i - int(i / pixels_length) * pixels_length
            y = int(i / pixels_length)

            self.LedCtrlXYByCode(x, y, raster[i])
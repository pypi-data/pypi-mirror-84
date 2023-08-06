#!/usr/bin/env python3
# coding: utf-8

from math import *
import shutil
from zencad import *
from dataclasses import dataclass


@dataclass
class MechanismObject:
    model: object
    use: bool = True,
    color: pyservoce.libservoce.Color = color(1, 1, 1)
    to_stl_name: str = None


def mechanism(
        objects: [MechanismObject],
        export_to_stl=True,
        to_stl_directory="./stl",
        to_stl_delta=0.01,
        use_mask=True,
        mask=halfspace().rotateX(pi / 2)
):
    stl_directory_was_initialized = False

    def initialize_stl_directory_if_need():
        nonlocal stl_directory_was_initialized
        if stl_directory_was_initialized:
            return
        if os.path.exists(to_stl_directory):
            shutil.rmtree(to_stl_directory)
        os.mkdir(to_stl_directory)
        stl_directory_was_initialized = True

    for obj in objects:
        if not obj.use:
            continue
        model_to_display = obj.model
        if use_mask:
            model_to_display ^= mask
        disp(model_to_display, obj.color)
        if export_to_stl and obj.to_stl_name is not None:
            initialize_stl_directory_if_need()
            to_stl_name = to_stl_directory + "/" + obj.to_stl_name + ".stl"
            to_stl(obj.model, to_stl_name, to_stl_delta)
            print(obj.to_stl_name, "exported as", to_stl_name)

    show()


if __name__ == '__main__':
    mechanism(
        objects=[
            MechanismObject(
                model=box(2),
                color=color(1, 0, 1),
                to_stl_name="box"
            ),
            MechanismObject(
                model=sphere(1),
                color=color(0, 1, 1),
                to_stl_name="sphere"
            )
        ],
        mask=halfspace().rotateX(-pi / 2).rotateZ(-3*pi / 4)
    )

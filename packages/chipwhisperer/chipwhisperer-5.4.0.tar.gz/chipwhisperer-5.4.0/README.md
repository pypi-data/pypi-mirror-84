# ChipWhisperer
[![Discord](https://img.shields.io/discord/747196318044258365?logo=discord)](https://discord.gg/chipwhisperer) | [Hardware Docs](https://rtfm.newae.com) | [Documentation](https://chipwhisperer.readthedocs.io) | [Forum](http://forum.newae.com) | [Store](https://store.newae.com) | [NewAE](http://newae.com)

ChipWhisperer is an open source toolchain dedicated to hardware security research. This toolchain consists of several layers of open source components:
* __Hardware__: The ChipWhisperer uses a _capture_ board and a _target_ board. Schematics and PCB layouts for the ChipWhisperer-Lite capture board and a number of target boards are freely available.
* __Firmware__: Three separate pieces of firmware are used on the ChipWhisperer hardware. The capture board has a USB controller (in C) and an FPGA for high-speed captures (in Verilog) with open-source firmware. Also, the target device has its own firmware; this repository includes many firmware examples for different targets.
* __Software__: The ChipWhisperer software is made up of a _capture_ program to control the hardware and an _analyzer_ program to process captured data.

---

## ChipWhisperer 5.0 Is Here

The biggest (and most breaking) change is here. ChipWhisperer 5.0 uses Python 3 & Juypter Notebooks. Here is a brief summary of improvements:

* Uses Jupyter Notebooks
* Python 3 
* Fully documented API (finally)
* 19 Jupyter notebook tutorials for side-channel analysis with ChipWhisperer
* 5x improved capture speed
* Tutorials all include output with three different targets (Nano, Lite (XMEGA), Lite (STM32F)), making it easier to compare your output to the tutorials output when you are following along.
* Fully usable as a standalone python package
* Project API supports import and export to zip file to move projects around.

An overview of the major changes can be found on the new ReadtheDocs [Overview Page](https://chipwhisperer.readthedocs.io/en/latest/getting-started.html).

We highly recommend you switch to CW5 as all development since last year has been for CW5, and will continue this way. The final tagged version of CW4 is 4.0.5, it can be found in the **develop** branch if you insist. 

## ChipWhisperer 5.3: Major tutorial/documentation overhaul

ChipWhisperer 5.3 comes with a lot of tutorial and documentation changes! https://wiki.newae.com is now deprecated
in favour of https://rtfm.newae.com. Beyond updated hardware documentation, this new website also has additional information
about tools and starter kits, as well as helpful comparisons between different hardware (such as different capture hardware and different targets).

Jupyter Notebook tutorials have been organized into different coureses which follow and compliment material
at https://learn.chipwhisperer.io. In general, tutorials have been redeveloped to include new information, as well
as better promote learning (less shift+enter). In addition, enitrely new tutorials are included.

Don't have ChipWhisperer hardware yet? No problem! Many of the SCA101 labs allow you to use prerecorded traces.

## Getting Started
First time using ChipWhisperer? Check out these links:
* [Getting started](https://chipwhisperer.readthedocs.io/en/latest/getting-started.html)
* [Installing ChipWhisperer](https://chipwhisperer.readthedocs.io/en/latest/installing.html) if you're trying to set up this software package
* [Hardware Docs](https://rtfm.newae.com) for hardware information. Also has helpful comparison between different NewAE products.

## GIT Source
Note all development occurs on the [develop](https://github.com/newaetech/chipwhisperer/tree/develop) branch. If you are looking for bleeding edge it's NOT on master - we push each release (and possibly any critical changes) to master. This means that "master" always gives you the latest known-working branch, but there may be new features on the "develop" branch.

## Help!
Stuck? If you need a hand, there are a few places you can ask for help:
* The [NewAE Forum](https://forum.newae.com/) is full of helpful people that can point you in the right direction
* If you find a bug, let us know through the [issue tracker](https://github.com/newaetech/chipwhisperer/issues)

---

ChipWhisperer is a trademark of NewAE Technology Inc., registered in the US, Europe, and China.

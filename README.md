# Morse Code Translator Using Blinking Artifacts in EEG Signals
## Introduction
This project involved building a Morse code translator that works in real-time. Blinking artefacts are common and easily
detectable in EEG signals. Different types of blinks are also distinguishable in the EEG signal. One can blink in
Morse code which can be translated into English.
The following algorithm considers a short blink as a dot and a long blink as a dash. It then identifies these in the
signal as Morse code character inputs and then translates them to English using a dictionary.

## Requirements
The program requires a LINUX interface to run. A USB-DUX box is essential to run the code. It executes it at a
specific sampling rate and processes the sample data in real-time. The pyusbdux library must be imported to
access the data from the box and process it further. Users should have prior knowledge of  Morse code or have a Morse code
dictionary in hand to be able to blink in Morse code. The following dictionary may be used:
https://www.researchgate.net/figure/International-Morse-code_fig5_308851059

## Installation
Ensure python3 is installed. The pyusbdux and py-iir-filter libraries are needed to process and implement the
code in real-time and further information regarding their installation and set-up can be found in the links below:
https://github.com/berndporr/pyusbdux/blob/master/README.rst
https://github.com/berndporr/py-iir-filter/blob/master/README.rst

## Usage
Three electrodes are utilised to detect the blinking artifacts. Two electrodes are placed above and below the eye
respectively and the third electrode (which acts as the ground) is placed at the mastoid (region behind the ear
lobes). 

<img align="centre" img width="374" alt="image" src="https://github.com/tanvik7072/morse-code-translator-using-eeg/assets/66367698/bc4196ea-614f-4099-9e04-e6bcb8ee0a87">


Ensure the electrodes are connected to the amplifier which is connected to the USB-DUX box and then
connected to the computer using a USB cable.
Once the set-up is complete run the Python file (from the directory in which the code is saved in) on the Linux
command line (BASH) to execute the code as follows:

```
python main.py
```

For a dot, blink how you normally would (short blink) and for a dash hold the blink for a second (long blink).
The code demonstrates efficiency in identifying dots; however, it exhibits limitations in detecting dashes, consequently restricting its ability to accurately identify certain alphabets in the dictionary.

Video demonstration: https://youtu.be/Lt7rQFrdUN0?feature=shared

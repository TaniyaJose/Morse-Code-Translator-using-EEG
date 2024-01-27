# Morse Code Translator Using Blinking Artifacts in EEG Signals
## Introduction
We have built a morse code translator that works in real time. Blinking artifacts are common and easily
detectable in EEG signals. Different types of blinks are also distinguishable in the EEG signal. One can blink in
morse code which can be translated into English.
The following algorithm considers a short blink as a dot and a long blink as a dash. It then identifies these in the
signal as morse code character inputs and then translates them using a Morse Code to English dictionary.

## Requirements
The program requires a LINUX interface to run. A USB-DUX box is essential to run the code. It executes it at a
specific sampling rate and processes the sample data in real time. The pyusbdux library must be imported to
access the data from the box and process it further. User should know morse code or at least have a morse code
dictionary in hand to blink in morse code. Can use the following dictionary:
https://www.researchgate.net/figure/International-Morse-code_fig5_308851059

## Installation
Ensure python3 is installed. The pyusbdux and py-iir-filter libraries are needed to process and implement the
code in real time and further information regarding their installation and set-up can be found in the links below:
https://github.com/berndporr/pyusbdux/blob/master/README.rst
https://github.com/berndporr/py-iir-filter/blob/master/README.rst
USAGE
Three electrodes are utilised to detect the blinking artifacts. Two electrodes are placed above and below the eye
respectively and the third electrode (which acts as the ground) is placed at the mastoid (region behind the ear
lobes). 

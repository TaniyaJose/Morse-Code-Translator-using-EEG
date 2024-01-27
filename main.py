import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyusbdux as c
from scipy.signal import butter
import iir_filter
import time

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Morse code decryptor
def decrypt(message):
    message += " "
    decipher = ""
    citext = ""
    i = 0
    for letter in message:
        if letter != " ":
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += " "
            else:
                for key, value in MORSE_CODE_DICT.items():
                    if citext == value:
                        decipher += key
                citext = ""
    return decipher

# Function to bandpass filter the signal
def bandpass_filter():
    lowcut = 1
    highcut = 20
    fs = 1000 
    order = 3
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], 'bandpass', output='sos')
    f = iir_filter.IIR_filter(sos)
    # Printing the coefficients
    print(sos)
    return f

# Converts detected peaks to binary data (1s and 0s)
def detect_peaks(data, threshold):
    peaks = (data > threshold).astype(int)
    return peaks

# Creates a scrolling data display
class RealtimePlotWindow:
    def __init__(self):
        # Create a plot window with three subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, sharex=True)

        # Subplot 1: Original Signal
        self.plotbuffer_original = np.zeros(500)
        self.line_original, = self.ax1.plot(self.plotbuffer_original)
        self.ax1.set_ylim(-2, 2)
        self.ax1.set_title('Original Signal')
        self.ax1.set_ylabel('Amplitude')
       
        # Real-timesampling rate
        self.start_time = time.time()
        self.end_time = time.time()
        self.num_samples = 0
        self.sampling_rate_interval = 1   # updates every 1 second

        # Subplot 2: Filtered signal
        self.plotbuffer_filtered = np.zeros(500)
        self.line_filtered, = self.ax2.plot(self.plotbuffer_filtered)
        self.ax2.set_ylim(-2, 2)
        self.ax2.set_title('Filtered signal')
        self.ax2.set_ylabel('Amplitude')

        # Displaying sampling rate in plot window
        self.sampling_rate_text = self.ax2.text(0.95,0.9,'', transform=self.ax2.transAxes,
                                           verticalalignment='top', horizontalalignment='right')

        # Subplot 3: Square wave of detected peaks
        self.plotbuffer_peaks = np.zeros(500)
        self.line_peaks, = self.ax3.step(np.arange(500), self.plotbuffer_peaks, where='mid')
        self.ax3.set_ylim(-0.5, 2)
        self.ax3.set_title('Square wave')
        self.ax3.set_xlabel('Number of Samples')
        self.ax3.set_ylabel('Amplitude')

        # Ringbuffers
        self.ringbuffer_original = []
        self.ringbuffer_filtered = []
        self.ringbuffer_peaks = []

        # Morse code accumulation
        self.morse_accumulator = []

        # Start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50)
   
    # Function to update the sampling rate in real time
    def update_sampling_rate(self, sampling_rate):
            self.sampling_rate_text.set_text(f'Sampling Rate: {sampling_rate: .2f} Hz')
   
    # Updates the plot
    def update(self, data):
        # Add new data to the buffer
        self.plotbuffer_original = np.append(self.plotbuffer_original, self.ringbuffer_original)
        self.plotbuffer_original = self.plotbuffer_original[-500:]
        self.ringbuffer_original = []
        # Update subplot 1: Original signal
        self.line_original.set_ydata(self.plotbuffer_original)

        # Detect peaks above a certain threshold and converts that to binary data (1s and 0s)
        peaks = detect_peaks(self.plotbuffer_filtered, threshold=0.5)

        # Update subplot 2: Filtered signal
        self.plotbuffer_filtered = np.append(self.plotbuffer_filtered, self.ringbuffer_filtered)
        self.plotbuffer_filtered = self.plotbuffer_filtered[-500:]
        self.ringbuffer_filtered = []
        self.line_filtered.set_ydata(self.plotbuffer_filtered)

        # Update sampling rate in real time  
        self.num_samples += 1
        self.end_time =  time.time()
        time_taken = self.end_time - self.start_time

        if time_taken >= self.sampling_rate_interval:
            current_sampling_rate = 2 * (self.num_samples / time_taken)
            self.update_sampling_rate(current_sampling_rate)

            # Reset variable for next second
            self.start_time = time.time()
            self.num_samples = 0

        # Update subplot 3: Square wave of detected peaks
        self.plotbuffer_peaks = np.append(self.plotbuffer_peaks, peaks)
        self.plotbuffer_peaks = self.plotbuffer_peaks[-500:]
        self.line_peaks.set_ydata(self.plotbuffer_peaks)

        # Conditions to identify and differentiate between a dot and a dash
        if np.sum(peaks[-100:]) > 80:  
            if np.sum(peaks[-100:]) > 70:    # Checks if the last 100 samples contains atleast 70 detected peaks
                self.morse_accumulator += "-"
            else:
                self.morse_accumulator += "."
        elif np.sum(peaks[-25:]) > 15 and np.sum(peaks[-40:-25]) < 5:  # Checks if the last 50 samples contains atleast 25 detected peaks &
                                                                       # checks if there are no peaks after a dot is flagged for the next 20 samples
                self.morse_accumulator += "."

        # Condtions to check for space between words
        if np.sum(peaks[-150:]) < 5:
            if self.morse_accumulator :
                self.morse_accumulator += " "

        # Print accumulated Morse code and translate it to English
        if len(self.morse_accumulator) >= 100 :
            morse_code_str = ''.join(self.morse_accumulator)
            morse_code_str = morse_code_str.strip()
            print("Morse Code:", morse_code_str)
            english = decrypt(self.morse_accumulator)
            print("English:", english)
            self.morse_accumulator = []

        return self.line_original, self.line_filtered, self.line_peaks

    # Appends data to the ringbuffer
    def addData(self, original_sample, filtered_sample, peak_value):
        self.ringbuffer_original.append(original_sample)
        self.ringbuffer_filtered.append(filtered_sample)
        self.ringbuffer_peaks.append(peak_value)

 # Creating an instance for the bandpass filter  
f = bandpass_filter()
# Create an instance for the real time plot window
realtimePlotWindow = RealtimePlotWindow()

class DataCallback(c.Callback):
    def hasSample(self, s):
        original_sample = s[0]
        filtered_sample = f.filter(original_sample)
        peak_value = detect_peaks(filtered_sample, threshold=0.5)
        realtimePlotWindow.addData(original_sample, filtered_sample, peak_value)

cb = DataCallback()
c.open()
print("ADC board:", c.get_board_name())
c.start(cb, 8, 250)
print("Actual samplingrate =", c.getSamplingRate(), "Hz")

# Starts the animation
plt.show()

c.stop()
c.close()

print("finished")
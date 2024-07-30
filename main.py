from machine import ADC, Pin, PWM
from utime import sleep, sleep_ms
import math

tones = {
"B0": 31,
"C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62,
"C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123,
"C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247,
"C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494,
"C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
"C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
"C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
"C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
}

# only cdefgab (no black notes) from 1st to 7th octave
tones_list = [
    [33, 37, 41, 44, 49, 55, 62],                   #1
    [65, 73, 82, 87, 98, 110, 123],                 #2
    [131, 147, 165, 175, 196, 220, 247],            #3
    [262, 294, 330, 349, 392, 440, 494],            #4
    [523, 587, 659, 698, 784, 880, 988],            #5
    [1047, 1175, 1319, 1397, 1568, 1760, 1976],     #6
    [2093, 2349, 2637, 2794, 3136, 3520, 3951],     #7
    [4186]                                          #8
]

def playtone(frequency, buzzer):
    buzzer.duty_u16(6000)
    print(f"playtone freq:{frequency}")
    buzzer.freq(frequency)


def octave_change(octave: int) -> int:
    sleep_ms(200)
    if octave < 7:
        print(f"octave to:{octave+1}")
        return octave + 1
    print("octave to:1")
    return 1

def playchords(pressed: list, octave: int, buzzer, nb: int):
    pow_div = 1.0 / nb
    value = 1.0
    print(f"playchords nb:{nb}")

    for i in range(len(pressed)):
        if pressed[i] == 1:
            value *= tones_list[octave-1][i] 
            # the minor do must be handled separetly
    chord_tone = math.pow(value, pow_div)
    print(f"chordtone:{chord_tone}")
    playtone(int(chord_tone), buzzer)


def do_action(pressed, octave, buzzer) -> int:
    nb = 0
    for x in pressed:
        if x == 1:
            nb+=1
    if nb == 0:
        bequiet(buzzer)
    elif nb == 1:
        if pressed[7] == 1:
            playtone(tones_list[octave][0], buzzer)
        else:
            playtone(tones_list[octave-1][pressed.index(1)], buzzer)
    elif nb == 2 and pressed[0] == 1 and pressed[-1] == 1:
        return octave_change(octave)
    else:
        playchords(pressed, octave, buzzer, nb)
    return octave

def bequiet(buzzer):
    buzzer.duty_u16(0)

def main():

    buzzer = PWM(Pin(0))
    do_ = Pin(2, Pin.IN)
    si = Pin(3, Pin.IN)
    la = Pin(4, Pin.IN)
    sol = Pin(5, Pin.IN)
    fa = Pin(6, Pin.IN)
    mi = Pin(7, Pin.IN)
    re = Pin(8, Pin.IN)
    do = Pin(9, Pin.IN)

    octave = 5
    bequiet(buzzer)
    while True:
        pressed = [0, 0, 0, 0, 0, 0, 0, 0]
        if do.value() == 1:
            pressed[0] = 1
        if re.value() == 1:
            pressed[1] = 1
        if mi.value() == 1:
            pressed[2] = 1
        if fa.value() == 1:
            pressed[3] = 1
        if sol.value() == 1:
            pressed[4] = 1
        if la.value() == 1:
            pressed[5] = 1
        if si.value() == 1:
            pressed[6] = 1
        if do_.value() == 1:
            pressed[7] = 1
        #pressed = [do.value(), re.value() etc]
        octave = do_action(pressed, octave, buzzer)

main()


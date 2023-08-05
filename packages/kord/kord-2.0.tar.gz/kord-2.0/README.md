# kord
kord is a python framework that provides programmers with a simple api for the creation of music-based applications. While it's mainly focused for theoretical purposes, some of it's more visually oriented features are well-suited for the generation of plucked-string instruments.


## installation

The only dependency for `kord` is the pip package `bestia`, my own library for creating command-line applications. It will be automatically downloaded when you install using pip:

```
$   python3 -m pip install kord
```



# api reference:

First, let me say that all of the following will only make sense to you if you already have some background on music theory|harmony.

## kord.notes module:

### Note() class
Note instances are the lowest-level objects of the framework and have 3 main attributes:

```
* chr: str   ('C', 'D', 'E', 'F', 'G', 'A', 'B')
* alt: str   ('b', 'bb', '', '#', '##')
* oct: int   (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```


Only the `chr` argument is required to create an instance. Arguments `alt` and `oct` will default to `''` and `3` respectively.

```
>>> from kord.notes import Note
>>> e3, f3 = Note('e'), Note('f')
>>> e3, f3
(E³, F³) 
>>> Note('B', 'b', 7)
B♭⁷
>>> Note('C', '#', 0)
C♯⁰
```

Notes with double alterations are supported but Notes with triple (or more) alterations raise InvalidAlteration Exceptions:

```
>>> n3 = Note('A', 'bb', 1)
>>> n3
A𝄫¹
>>> n4 = Note('F', '##', 1)
>>> n4
F𝄪¹
>>> Note('G', '###')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
kord.errors.InvalidAlteration: ###
```


 
Intervals between note objects can be evaluated using the following operators:  ```-   < >   <= >=   == !=   >>   ** ```
 
These allow calculation of semitone deltas between notes as well as insights into their enharmonic relationships. Let's take a quick look at each operator separately:

#### - operator

The substraction operator allows you to calculate the difference in semitones between two notes:

```
>>> f3 - e3
1
>>> Note('a', 'b', 2) - Note('g', '#', 2)
0
>>> Note('a', 8) - Note('c', 4)
57
>>> Note('a', 8) - Note('c', '##', 4)
55
```


####  < >   <= >=   == !=  operators

Comparison operators return boolean values based on the interval between 2 notes. 

```
>>> f3 > e3
True
>>> f3 >= e3
True
```

While the concept is seemingly straightforward, special attention needs to be taken when using `== !=` with enharmonic notes.

```
>>> n1 = Note('F', '#', 5)
>>> n2 = Note('G', 'b', 5)
>>> n1, n2
(F♯⁵, G♭⁵)
>>> n1 == n2
True
```

The notes F#5 and Gb5 are not the same but `==` checks their interval and since its a unison,  the comparison evaluates True. This might seem a bit counter-intuitive at first but `kord` uses different operators to check for exact note matches.

#### >> ** operators

The power and right-shift operators allow you to compare Notes for equality based not on their intervals, but on their internal properties. The strictest operator is `>>` which compares note, alteration and octave attributes while `**` is less strict and only compares note and alteration. 

```
>>> ab1, ab5 = Note('A', 'b', 1),  Note('A', 'b', 5)
>>> ab1 == ab5
False
>>> ab1 ** ab5
True
```

Notice that `**` evaluated True because both instances are A flat notes, even though there is a wide interval between them.

```
>>> ab1 >> ab5
False
>>> ab1.oct = 5
>>> ab1 >> ab5
True
```

For the `>>` operator to evaluate True, the octave of the notes has to match as well.



<hr/>




## kord.keys module:


### class MusicKey(object):

The best way to describe a MusicKey object is basically as a Note object generator. You can use this class to create any theoretical arrangement of musical notes (ie. chords, scales).

Let us take a look at 2 examples using the 2 main categories of child class that inherit from MusicKey class and how they are defined:


### class ChromaticKey(MusicKey):

The ChromaticScale class uses the MusicKey class as an interface while implementing it's own structure of intervals.

```
class ChromaticScale(MusicKey):

    root_intervals = (
        UNISON,
        MINOR_SECOND,
        MAJOR_SECOND,
        MINOR_THIRD,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH,
        MAJOR_SEVENTH,
    )
```

We can initialize ChromaticScale objects on any given note and use the ```degree()``` method to obtain one of it's degrees. We can achieve the same result using list index notation:

```
>>> from kord.keys import ChromaticScale
>>> c_chromatic = ChromaticScale('C')
>>> c_chromatic.degree(2)
C♯⁰
>>> c_chromatic[12]
B⁰
```

Perhaps the most interesting aspect of any MusicKey sub-class is it's ability to iterate over Note objects using one of their several generator methods. As an example, let's take a quick look at the ```scale()``` method:

```
>>> for note in c_chromatic.spell()
...   print(note, end=' ')
...
C⁰ C♯⁰ D⁰ D♯⁰ E⁰ F⁰ F♯⁰ G⁰ G♯⁰ A⁰ A♯⁰ B⁰ C¹ 
```

We can use the ```note_count=``` argument to specify to the scale generator the amount of notes to yield:

```
>>> for note in c_chromatic.spell(note_count=4):
...   print(note, end=' ')
...
C⁰ C♯⁰ D⁰ D♯⁰ 
```

The ```start_note=``` argument can be used to start yielding from a specific note. This can be done even if the note is not part of the scale:

```
>>> from kord.notes import Note
>>> Ab = Note('A', 'b', 0)
>>> for note in c_chromatic.spell(note_count=6, start_note=Ab):
...   print(note, end=' ')
...
G♯⁰ A⁰ A♯⁰ B⁰ C¹ C♯¹ 
```



### class DiatonicScale(MusicKey):

```
class MajorScale(DiatonicKey):

    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )
```


## fretboard sample application

A sample application `fretboard.py` comes built-in with the kord framework and gives some insight into it's possibilities. It displays a representation of the fretboard of your instrument, tuned to your preference along as where to find the notes for any given mode for any given root note.

```
usage: fretboard.py [-h] [-m] [-i] [-t] [-f] [-v] ROOT

<<< Fretboard visualizer sample tool for the kord music framework >>>

positional arguments:
  ROOT                select a root note

optional arguments:
  -h, --help          show this help message and exit
  -m , --mode         mode to visualize: ['major', 'minor', 'natural_minor', 'melodic_minor', 'harmonic_minor', 'ionian', 'lydian', 'mixo', 'aeolian', 'dorian', 'phrygian', 'chromatic']
  -i , --instrument   instrument fretboard to visualize: ['banjo', 'guitar', 'bass', 'ukulele']
  -t , --tuning       instrument tuning: check your .json files for available options
  -f , --frets        number of displayed frets: [0, 1, 2, .. , 36]
  -v , --verbosity    application verbosity: [0, 1, 2]

```

You will find some pre-defined instrument tunings in the `tunings` directory in the form of .json files. Feel free to modify these or add your own following the correct syntax and they will immediately become available to the fretboard tool.

I'm pretty sure guitar/bass players may find it very handy as a means to develop their knowledge of their instrument. Have fun!

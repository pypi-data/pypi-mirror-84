# kord
kord is a python framework that provides programmers with a simple api for the creation of music-based applications. While it's mainly intended for theoretical purposes, some of it's modules contain functionality specifically tailored for plucked-string instrument visualization.


## installation

The only dependency for `kord` is the pip package `bestia`, my own library for creating command-line applications. Both can be automatically installed by using pip:

```
$   python3 -m pip install kord
```



# api reference:

Please expect to understand the following documentation only if you have an above basic understanding of music theory|harmony.


## kord.notes module:

### class MusicNote(object):

Note instances are the lowest-level objects of the framework and have 3 main attributes:

```
* chr: str   ('C', 'D', 'E', 'F', 'G', 'A', 'B')
* alt: str   ('b', 'bb', '', '#', '##')
* oct: int   (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```


Only the `chr` argument is required to create an instance. Arguments `alt` and `oct` will default to `''` and `3` respectively.

```
>>> from kord.notes import Note
>>> e3, f3 = MusicNote('e'), MusicNote('f')
>>> e3, f3
(E³, F³) 
>>> MusicNote('B', 'b', 7)
B♭⁷
>>> MusicNote('C', '#', 0)
C♯⁰
```

Notes with double alterations are supported but Notes with triple (or more) alterations raise InvalidAlteration Exceptions:

```
>>> n3 = MusicNote('A', 'bb', 1)
>>> n3
A𝄫¹
>>> n4 = MusicNote('F', '##', 1)
>>> n4
F𝄪¹
>>> MusicNote('G', '###')
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
>>> MusicNote('a', 'b', 2) - MusicNote('g', '#', 2)
0
>>> MusicNote('a', 8) - MusicNote('c', 4)
57
>>> MusicNote('a', 8) - MusicNote('c', '##', 4)
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
>>> n1 = MusicNote('F', '#', 5)
>>> n2 = MusicNote('G', 'b', 5)
>>> n1, n2
(F♯⁵, G♭⁵)
>>> n1 == n2
True
```

The notes F#5 and Gb5 are NOT the same but since their interval is a unison, the `==` comparison evaluates True. This might seem a bit counter-intuitive at first but you can still check for exact note matches with the use of 2 other operators.

#### >> ** operators

The power and right-shift operators allow you to compare Notes for equality based not on their intervals, but on their intrinsic `chr, alt, oct` properties. The strictest operator `>>` compares all 3 attributes for equality while the looser `**` ignores `oct`: 

```
>>> ab1, ab5 = MusicNote('A', 'b', 1),  MusicNote('A', 'b', 5)
>>> ab1 == ab5
False
>>> ab1 ** ab5
True
```

Notice `**` evaluated True since both instances are A flat notes, even when there is a wide interval between them.

```
>>> ab1 >> ab5
False
>>> ab1.oct = 5
>>> ab1 >> ab5
True
```

For the `>>` operator to evaluate True, the octaves of the notes must match as well.


<hr/>




## kord.keys module:


### class MusicKey(object):

Think of MusicKey objects as generators of Note objects. You can define a new class which inherits MusicKey and use any theoretical arrangement of `intervals` from the root note in order to create chords, scales, modes. You can further restrict these child classes by restricting `degrees` to specific values.

These are a couple of pre-defined examples to give you an idea of how it works:

```
class ChromaticScale(MusicKey):
    intervals = (
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

class MajorScale(MusicKey):
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )
    
class MajorPentatonicScale(MajorScale):
    degrees = (1, 2, 3, 5, 6)

class MajorTriad(MajorScale):
    degrees = (1, 3, 5)
```

When we create an instance of a MusicKey subclass, we can then access it's items using list index notation:

```
>>> from kord.keys import ChromaticScale
>>> c_chromatic_scale = ChromaticScale('C')
>>> c_chromatic_scale[2]
C♯⁰
>>> c_chromatic_scale[12]
B⁰
```

### MusicKey.spell() method

Using list index notation is fine but perhaps it is more interesting to look at a different and more dynamic way of getting the items of our MusicKey instances. The `spell()` method provides a simple interface for generating Note instances on the fly. Let's take a look at a couple of examples and the several arguments that we can use when calling this method:

```
>>> for note in c_chromatic_scale.spell():
...     print(note, end=' ')
...
C⁰ C♯⁰ D⁰ D♯⁰ E⁰ F⁰ F♯⁰ G⁰ G♯⁰ A⁰ A♯⁰ B⁰ C¹ >>> 
```


The `note_count` argument is an `int` that allows us to specify the amount of notes we want:

```
>>> from kord.keys import MinorScale
>>> a_minor_scale = MinorScale('A')
>>> for note in a_minor_scale.spell(note_count=4):
...     print(note, end=' ')
...
A⁰ B⁰ C¹ D¹ >>> 
```

Be careful, ask for too many notes and kord will throw and Exception when the oct 9 has been exceeded.

The `yield_all` argument is a `bool` that will make the method yield not just Note instances, but also None instances for every non-diatonic semitone found:

```
>>> for note in a_minor_scale.spell(note_count=4, yield_all=True):
...     print(note, end=' ')
...
A⁰ None B⁰ C¹ None D¹ >>> 
```


The `start_note` argument is a `MusicNote` object that can be used to start getting notes from a specific note. This can be done even if the note is not part of the scale:

```
>>> Db1 = MusicNote('D', 'b', 1)
>>> for note in a_minor_scale.spell(note_count=4, yield_all=True, start_note=Db1):
...     print(note, end=' ')
...
None D¹ None E¹ F¹ None G¹ >>> 
```



## fretboard tool

A sample application `fretboard.py` comes built-in with `kord` and gives some insight into the possibilities of the framework. It displays a representation of your instrument's fretboard, tuned to your liking along with note patterns for any given mode (scale/chord) for any given root note. Installation path varies depending on your system but it's usually either `/usr/local/fretboard` or `~/.local/fretboard`. You will also find a `tunings` directory with some pre-defined instrument tunings in the form of .json files. Feel free to modify them or add your own following the correct syntax and they will immediately become available to the run-time.

```
> python3 fretboard.py --help
usage: fretboard.py [-h] [-s  | -c ] [-i] [-t] [-f] [-v] root

<<< Fretboard visualizer sample tool for the kord music framework >>>

positional arguments:
  root                select key ROOT note

optional arguments:
  -h, --help          show this help message and exit
  -s , --scale        major, minor, melodic_minor, harmonic_minor, major_pentatonic, minor_pentatonic, ionian, lydian, mixolydian, aeolian, dorian, phrygian, locrian, chromatic
  -c , --chord        maj, min, aug, dim, maj7, min7, 7, dim7, min7dim5, maj9, min9, 9
  -i , --instrument   banjo, guitar, bass, ukulele
  -t , --tuning       check .json files for available options
  -f , --frets        1, 2, .., 36
  -v , --verbosity    0, 1, 2
```

The only required parameter is the `root` note. 

The `--scale` and `--chord` options let you choose which note pattern to display for the selected root. They are mutually exclusive and the default value is `--chord maj` when left blank.

The `--instrument` and `--tuning` options refer to the json files you will find in the tunings directory. Default values are `--instrument guitar   --tuning standard`.

The `--frets` option let's you choose how many frets to visualize, maximum value is 36. Default value will fill your terminal screen.

The `--verbosity` option let's you choose how much information to see on-screen from 0 to 2. Default value is 1.

Keep on rocking!

# MakingMusicTool

## Introduction

The MakingMusicTool can create soundtracks out of a strict defined notation. 

## Table of Contents

1. [Introduction](#Introdurction)
2. [How to use](#Howtouse)
   1. [Class Description](#ClassDescription)
   2. [Usage](#Usage)
      1. [Soundtrack Information Input](#SoundtrackInformationInput)
      2. [MusicMaker](#MusicMaker)
3. [Contributing](#Contributing)
4. [Links](#Links)

## How to use

### Class Description

* **MusicMaker** **`MusicMakerTool.py`**
  Main Features:
  * imports the soundtrack information from `sound_pattern.csv`
  * analyses each row to create a soundtrack (instrument sound + volume + notes)
  * overlays the single soundtracks to one final soundtrack
  * exports the final soundtrack as `new_music.wav`

### Usage

#### Soundtrack Information Input

The csv file row must have the following notation (**without header**):

| instrument            | volume            | note 1           | ... | note n           |
| --------------------- | ----------------- | ---------------- | --- | ---------------- |
| $i \in$ sound files | $v \in [1,2,3]$ | $n\in  [1;16]$ |     | $n \in [1;16]$ |

The notes notation should be in a **4/4 time** and the notes correspond to the following notation:

|          note          |    meaning    | notation |
| :--------------------: | :------------: | :------: |
| **$&#119133$** |   whole note   |    1    |
| **$&#119134$** |   half note   |    2    |
|     $&#119135 $     |  quarter note  |    4    |
|      $&#119136$      |  eighth note  |    8    |
|      $&#119137$      | sixteenth note |    16    |

#### MusicMaker

If sou want to change the import csv file name:

```python
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
FILENAME = "sound_patter.csv"
```

Instance a **MusicMaker** object with the csv file name and the **B**eats **P**er **M**inutes (bpm, default 60).
Create a new soundtrack with the `makeMusic()` method and export it into `new_music.wav`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Links

Helpfull links:

* [all the answers](https://www.google.de/search?q=how+to+use+google&sxsrf=ALeKk01Pw_bxWGHPxYMFQxHBGvFGsr2o-Q%3A1624293592793&source=hp&ei=2MDQYOeDLsSAaaKmo8AH&iflsig=AINFCbYAAAAAYNDO6AEUucQ4syTqAp9GA4a02F4ETKfn&oq=how+to+use+google&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBOgcIIxDqAhAnOgQIIxAnOggIABDHARCjAjoCCAA6AgguOgUILhDLAVCG8ghY0oUJYKuHCWgBcAB4AIABwQGIAekLkgEEMTYuMZgBAKABAaoBB2d3cy13aXqwAQo&sclient=gws-wiz&ved=0ahUKEwjnz-2UlanxAhVEQBoKHSLTCHgQ4dUDCAk&uact=5)
* [free-sound-effects](https://mixkit.co/free-sound-effects/)

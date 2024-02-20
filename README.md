## About
A Python 3 script to convert tempo map data from a .chart (Clone Hero) file to a .tja (Taiko Simulator) file. Currently made to support BPM changes up to x/16 measures, to accomodate up to x/16 Time Signatures. (you should only put a BPM marker only in the white lines, through...)

The only graphical software avaliable for .tja charting (PeepoDrumKit) doesn't have a "BPM dragging" feature, like [Moonscraper Chart Editor](https://github.com/FireFox2000000/Moonscraper-Chart-Editor), so, with a bit of fiddling with ChatGPT, this script was made.

Also useful to quickly import tempo maps from already completed .chart files.

## Note
* It does not convert the note portion of the chart, as I don't think it would be useful to do the entire charting process in .chart.
* Time signature handler was disabled, as it is incomplete. It will consider all measures as 4/4. Despite this, as long a BPM change was made in x/(1,2,4,8 or 16) measure, it will work.
* MIDI files also work, you'll just need to convert to chart beforehand. Don't worry about resolution/ppq quirks through, this scripts should work with "any" resolution. (only tested with 192 atm)

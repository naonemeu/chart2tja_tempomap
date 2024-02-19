## About
Script to convert tempo map data from a .chart file to a .tja file. Currently made to support BPM changes up to x/16 measures, to accomodate up to x/16 Time Signatures. (you should only put a BPM marker only in the white lines, through...)

The only graphical software avaliable for .tja charting doesn't have a "BPM dragging" feature, like Moonscraper Chart Editor, so, with a bit of fiddling with ChatGPT, this script was made.

Also useful to quickly import tempo maps from already completed .chart files.

## Note
At the time, it does not convert the note portion of the chart, and the time signature handler was disabled, as it is incomplete. 
Despite this, as long a BPM change was made in x/(1,2,4,8 or 16) measure, it will work.

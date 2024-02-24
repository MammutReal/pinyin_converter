# Pinyin converter

A Pinyin converter for Hungarian, French and German.

Command line version usage:<br/>
`python.exe pinyin_converter.py [parameters]`<br/>

The settings can be adjusted as command line parameters or by editing the _config.json_ file.

GUI version usage:<br/>
`python.exe widget.py`<br/>

## Command line parameters

> [!TIP]
> The parameters can be added in any order.

_The target language_<br/>
**`h1`** &ensp; Hungarian (Popular) &emsp; ${\text{\color{red}default}}$<br/>
**`h2`** &ensp; Hungarian (Academic)<br/>
**`en`** &ensp; English (Wade-Giles)<br/>
**`fr`** &ensp; French (E.F.E.O)<br/>
**`de`** &ensp; German (Lessing-Othmer)<br/>
<br/>
_Clipboard_<br/>
**`copy`** &ensp; Copies the result to the clipboard. &emsp; `"copy": true` &emsp; ${\text{\color{red}default}}$<br />
**`nocopy`** &ensp; Does not copy the result to the clipboard. &emsp; `"copy": false`<br />
<br/>
_Hyphen options_<br/>
**`hyphen`** &ensp; Use hyphen between syllables of a first name. &emsp; ${\text{\color{red}default}}$<br/>
**`nohyphen`** &ensp; Do not use hyphens.<br/>
**`oneword`** &ensp; Use hyphens even if the name is only one word.<br/>
**`lastword`** &ensp; Use hyphens only if the name has more than one word. &emsp; ${\text{\color{red}default}}$<br/>
<br/>
**`save`** &ensp; Saves the command line parameters to the _config.json_ file.<br/>
<br/>
_`new_syllable_data_filename.json`_ &ensp; New data file containing syllables. (By default, the program works with _syllables.json_)<br/>



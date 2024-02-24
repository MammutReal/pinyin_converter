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
**`hyphen`** &ensp; Uses hyphen between syllables of a first name. &emsp; `"use_hyphen": true` &emsp; ${\text{\color{red}default}}$<br/>
**`nohyphen`** &ensp; Does not use hyphen. &emsp; `"use_hyphen": false`<br/>
**`oneword`** &ensp; Uses hyphen even if the name is only one word. &emsp; `"one_word": true`<br/>
**`lastword`** &ensp; Uses hyphen only if the name has more than one word. &emsp; `"one_word": false` &emsp; ${\text{\color{red}default}}$<br/>
<br/>
**`save`** &ensp; Saves the command line parameters to the _config.json_ file.<br/>
<br/>
_`new_syllable_data_filename.json`_ &ensp; New data file containing syllables. (By default, the program works with _syllables.json_)<br/>
<br/>
<br/>
> [!NOTE]
> The program uses [this syllable table](https://terebess.hu/keletkultinfo/atiras/atiras.html) for the conversion.

### Pocon
###### {Po} files {con}vert to Xml files

Pocon is a program for convert files with extension .po to files with extension .xml

#### Features

- Format the structure of files .po to convert to .xml
- The name of tags is adequate to mean translate
- Intent determine a possible name for the file [xml] output
- Deleted tags and translate word empty
- Convert individual files or multiples files of .po to .xml

#### Problem to solution

While I was refactor code of program's Gnome like Zenity, I see that Gnome based strongly
his translates in files .po, I wanna not lose the work realized in it translates, so that
I have two alternatives, write it translates to files xml manually or design an program that
to do it automatically.

The program actually, work fine for great part of file .po that Gnome use, the program can
realize conversions of file po to xml for any program design for Gnome and perhaps for other
more.

#### How to use

Pocon can use for convert individual files or multiples files.

##### Individual files

    > ./Pocon filename=<Path to file> (Without < and >)
    
##### Multiples files

    > ./Pocon directory=<Path to directory> (Without < and >)

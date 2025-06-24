# Initiative Plus 
##### (version 1.0.0)

![image](./assets/Initiative_Plus_Unedited_Icon.png)

## Description

Initiative Plus: A better tracker. This table built using python with the pyqt6 GUI framework keeps track of player and creature initiative and health when its 
time to battle in your favorite Table Top Role-Playing Game. This is my first large scale project so please feel free to share what you think of it.

## Downloads

[MacOS (Apple Silicon)](./dist/Initiative%20Plus.app/)

## Features (as of version 1.0.0)

- **Button Features**
    - Add Creature
    - Remove creature (individual or multiselect)
    - Table clearing
    - Turn tracker
    - Turn and Round display
    - Sort by Initiative 

- **Table Features**
    - Keeping track and display of names, initiative, HP, AC (Armor Class), and Conditions 
    - Damage and Heal popup with damage type selection
    - Vulnerability, Resistance, And Immunity Popup for each damage type. (select the shield icon in the AC column)
    - Damage type vulnerability, resistance, and immunity consideration upon damaging a creature
    - DND Condition checkbox with tooltips from the 5e ruleset

- **Additional Features** 
    - Save JSON formatted tracker data for when you want to continue battle later
        - Save: ```Cmd/Ctrl + S```
        - Open: ```Cmd/Ctrl + O```
    - Undo/Redo
    - Drag and drop creature row
        - Right click on row and drag and drop to desired location


Thank you so much for assisting me, in building this project on alternative operating systems. 

If you are not a contributor and desire to download this project (most likely because malware alerts are prohibiting you from running the app), please feel free to follow the steps
given below as well.

#### **Needed Systems (contributors only)**

- Currently there is support for MacOS (see 'Downloads' section)
- Windows 11 version needed
- Windows 10 version desired
- Linux is desired
    - Arch (btw) 
    - Ubuntu 
    - Any other distros that are desired

### Requirements for building

If you have an operating system that fits in the needed systems above, that's great. Here are the steps to build an executable file for this project

1. Have python installed. You may find installation and download instructions [here](https://www.python.org/downloads/)
2. Have pyinstaller installed. In the CLI input:
```bash 
pip install pyinstaller
```

### Pyinstaller command 

Once you have completed all those installations you may run the command below, if the spec file exists

```bash
pyinstaller Initiative_Plus.spec
```
If the spec file does not exists or does not work, try to run this command:

```bash
pyinstaller --onefile --windowed --paths=./src --paths=./assets -F --add-data="src/GUI/styles.css:." src/main.py 
```

### Finishing steps

Congrats, you should now have a working executable/app in the [dist](./dist) folder. If you are contributing to the building of this project, please send over that file to me or publish a pull request on github. Thank you very much. Your username will be forever remembered in the README

And finally, **ROLL INITIATIVE!**

## Contributors

Thank you contributors for building this project on your operating systems. This project's reach is extended thanks to you all.

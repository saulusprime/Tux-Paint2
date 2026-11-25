                                   Tux Paint
                                 version 0.9.22

  A simple drawing program for children

                Copyright 2002-2014 by Bill Kendrick and others
                         New Breed Software & Tux4Kids

                           bill@newbreedsoftware.com
                            http://www.tuxpaint.org/

                         June 14, 2002 - August 5, 2014

     ----------------------------------------------------------------------

   +------------------------------------------------------------------------+
   |Table of Contents                                                       |
   |------------------------------------------------------------------------|
   |  * About                                                               |
   |  * Using Tux Paint                                                     |
   |  * Loading Other Pictures into Tux Paint                               |
   |  * Further Reading                                                     |
   |  * How to Get Help                                                     |
   +------------------------------------------------------------------------+

     ----------------------------------------------------------------------

                                     About

What Is 'Tux Paint?'

       Tux Paint is a free drawing program designed for young children (kids
       ages 3 and up). It has a simple, easy-to-use interface, fun sound
       effects, and an encouraging cartoon mascot who helps guide children as
       they use the program. It provides a blank canvas and a variety of
       drawing tools to help your child be creative.

License:

       Tux Paint is an Open Source project, Free Software released under the
       GNU General Public License (GPL). It is free, and the 'source code'
       behind the program is available. (This allows others to add features,
       fix bugs, and use parts of the program in their own GPL'd software.)

       See COPYING.txt for the full text of the GPL license.

Objectives:

       Easy and Fun
               Tux Paint is meant to be a simple drawing program for young
               children. It is not meant as a general-purpose drawing tool.
               It is meant to be fun and easy to use. Sound effects and a
               cartoon character help let the user know what's going on, and
               keeps them entertained. There are also extra-large
               cartoon-style mouse pointer shapes.

       Extensibility
               Tux Paint is extensible. Brushes and "rubber stamp" shapes can
               be dropped in and pulled out. For example, a teacher can drop
               in a collection of animal shapes and ask their students to
               draw an ecosystem. Each shape can have a sound which is
               played, and textual facts which are displayed, when the child
               selects the shape.

       Portability
               Tux Paint is portable among various computer platforms:
               Windows, Macintosh, Linux, etc. The interface looks the same
               among them all. Tux Paint runs suitably well on older systems
               (like a Pentium 133), and can be built to run better on slow
               systems.

       Simplicity
               There is no direct access to the computer's underlying
               intricacies. The current image is kept when the program quits,
               and reappears when it is restarted. Saving images requires no
               need to create filenames or use the keyboard. Opening an image
               is done by selecting it from a collection of thumbnails.
               Access to other files on the computer is restricted.

     ----------------------------------------------------------------------

                                Using Tux Paint

Loading Tux Paint

  Linux/Unix Users

         Tux Paint should have placed a laucher icon in your KDE and/or GNOME
         menus, under 'Graphics.'

         Alternatively, you can run the following command at a shell prompt
         (e.g., "$"):

           $ tuxpaint

         If any errors occur, they will be displayed on the terminal (to
         "stderr").

     ----------------------------------------------------------------------

  Windows Users

                                                          [Icon]              
                                                         Tux Paint            

         If you installed Tux Paint on your computer using the
         'Tux Paint Installer,' it will have asked you whether you wanted a
         'Start' menu short-cut, and/or a desktop shortcut. If you agreed,
         you can simply run Tux Paint from the 'Tux Paint' section of your
         'Start' menu (e.g., under "All Programs" on Windows XP), or by
         double-clicking the "Tux Paint" icon on your desktop.

         If you installed Tux Paint using the 'ZIP-file' download, or if you
         used the 'Tux Paint Installer,' but chose not to have shortcuts
         installed, you'll need to double-click the "tuxpaint.exe" icon in
         the 'Tux Paint' folder on your computer.

         By default, the 'Tux Paint Installer' will put Tux Paint's folder in
         "C:\Program Files\", though you may have changed this when the
         installer ran.

         If you used the 'ZIP-file' download, Tux Paint's folder will be
         wherever you put it when you unzipped the ZIP file.

     ----------------------------------------------------------------------

  Mac OS X Users

         Simply double-click the "Tux Paint" icon.

     ----------------------------------------------------------------------

Title Screen

       When Tux Paint first loads, a title/credits screen will appear.

                               [Title Screenshot]

       Once loading is complete, press a key or click on the mouse to
       continue. (Or, after about 30 seconds, the title screen will go away
       automatically.)

     ----------------------------------------------------------------------

Main Screen

       The main screen is divided into the following sections:

       Left Side: Toolbar

               The toolbar contains the drawing and editing controls.

  [Tools: Paint, Stamp, Lines, Shapes, Text, Magic, Label, Learn, Undo,      
                  Redo, Eraser, New, Open, Save, Print, Quit]

       Middle: Drawing Canvas

               The largest part of the screen, in the center, is the drawing
               canvas. This is, obviously, where you draw!

                                   [(Canvas)]

               Note: The size of the drawing canvas depends on the size of
               Tux Paint. You can change the size of Tux Paint using the
               Tux Paint Config. configuration tool, or by other means. See
               the OPTIONS documentation for more details.

       Right Side: Selector

               Depending on the current tool, the selector shows different
               things. e.g., when the Paint Brush tool is selected, it shows
               the various brushes available. When the Rubber Stamp tool is
               selected, it shows the different shapes you can use.

                 [Selectors - Brushes, Letters, Shapes, Stamps]

       Lower: Colors

               A palette of available colors are shown near the bottom of the
               screen.

  [Colors - Black, White, Red, Pink, Orange, Yellow, Green, Cyan,       Blue,
                              Purple, Brown, Grey]

               (NOTE: You can define your own colors for Tux Paint. See the
               "Options" documentation.)

       Bottom: Help Area

               At the very bottom of the screen, Tux, the Linux Penguin,
               provides tips and other information while you draw.

 (For example: 'Pick a shape. Click to pick the center, drag, then       let go
when it is the size you want.  Move around to rotate it, and       click to draw
                                      it.)

     ----------------------------------------------------------------------

Available Tools

  Drawing Tools

         Paint (Brush)

                 The Paint Brush tool lets you draw freehand, using various
                 brushes (chosen in the Selector on the right) and colors
                 (chosen in the Color palette towards the bottom).

                 If you hold the mouse button down, and move the mouse, it
                 will draw as you move.

                 As you draw, a sound is played. The bigger the brush, the
                 lower the pitch.

     ----------------------------------------------------------------------

         Stamp (Rubber Stamp)

                 The Stamp tool is like a set of rubber stamps or stickers.
                 It lets you paste pre-drawn or photographic images (like a
                 picture of a horse, or a tree, or the moon) in your picture.

                 As you move the mouse around the canvas, an outline follows
                 the mouse, showing where the stamp will be placed, and how
                 big it will be.

                 There can be numerous categories of stamps (e.g., animals,
                 plants, outer space, vehicles, people, etc.). Use the Left
                 and Right arrows to cycle through the collections.

                 Some stamps can be colored or tinted. If the color palette
                 below the canvas is activated, you can click the colors to
                 change the tint or color of the stamp before placing it in
                 the picture.

                 Stamps can be shrunk and expanded, and many stamps can be
                 flipped vertically, or displayed as a mirror-image, using
                 controls at the bottom right of the screen.

                 Different stamps can have different sound effects and/or
                 descriptive (spoken) sounds. Buttons at the lower left (near
                 Tux, the Linux penguin) allow you to re-play the sound
                 effects and descriptive sounds for the currently-selected
                 stamp.

                 (NOTE: If the "nostampcontrols" option is set, Tux Paint
                 won't display the Mirror, Flip, Shrink and Grow controls for
                 stamps. See the "Options" documentation.)

     ----------------------------------------------------------------------

         Lines

                 This tool lets you draw straight lines using the various
                 brushes and colors you normally use with the Paint Brush.

                 Click the mouse and hold it to choose the starting point of
                 the line. As you move the mouse around, a thin 'rubber-band'
                 line will show where the line will be drawn.

                 Let go of the mouse to complete the line. A "sproing!" sound
                 will play.

     ----------------------------------------------------------------------

         Shapes

                 This tool lets you draw some simple filled, and un-filled
                 shapes.

                 Select a shape from the selector on the right (circle,
                 square, oval, etc.).

                 In the canvas, click the mouse and hold it to stretch the
                 shape out from where you clicked. Some shapes can change
                 proportion (e.g., rectangle and oval), others cannot (e.g.,
                 square and circle).

                 Let go of the mouse when you're done stretching.

                      Normal Mode

                              Now you can move the mouse around the canvas to
                              rotate the shape.

                              Click the mouse button again and the shape will
                              be drawn in the current color.

                      Simple Shapes Mode
                              If simple shapes are enabled (e.g., with the
                              "--simpleshapes" option), the shape will be
                              drawn on the canvas when you let go of the
                              mouse button. (There's no rotation step.)

     ----------------------------------------------------------------------

         Text and Label

                 Choose a font (from the 'Letters' available on the right)
                 and a color (from the color palette near the bottom). Click
                 on the screen and a cursor will appear. Type text and it
                 will show up on the screen.

                 Press [Enter] or [Return] and the text will be drawn onto
                 the picture and the cursor will move down one line.

                 Alternatively, press [Tab] and the text will be drawn onto
                 the picture, but the cursor will move to the right of the
                 text, rather than down a line, and to the left. (This can be
                 useful to create a line of text with mixed colors, fonts,
                 styles and sizes: Like this.)

                 Clicking elsewhere in the picture while the text entry is
                 still active causes the current line of text to move to that
                 location (where you can continue editing it).

                      Text versus Label

                              The Text tool is the original text-entry tool
                              in Tux Paint. Text entered using this tool
                              can't be modified or moved later, since it
                              becomes part of the drawing. However, because
                              the text becomes part of the picture, it can be
                              drawn over or modified using Magic tool effects
                              (e.g., smudged, tinted, embossed, etc.)

                              When using the Label tool (which was added to
                              Tux Paint in version 0.9.22), the text 'floats'
                              over the image, and the details of the label
                              (the text, the position of the label, the font
                              choice and the color) get stored separately.
                              This allows the label to be repositioned or
                              edited later.

                              The Label tool can be disabled (e.g., by
                              selecting "Disable 'Label' Tool" in
                              Tux Paint Config. or running Tux Paint with the
                              "--nolabel" command-line option).

                      International Character Input

                              Tux Paint allows inputting characters in
                              different languages. Most Latin characters
                              (A-Z, n, e, etc.) can by entered directly. Some
                              languages require that Tux Paint be switched
                              into an alternate input mode before entering,
                              and some characters must be composed using
                              numerous keypresses.

                              When Tux Paint's locale is set to one of the
                              languages that provide alternate input modes, a
                              key is used to cycle through normal (Latin
                              character) and locale-specific mode or modes.

                              Currently supported locales, the input methods
                              available, and the key to toggle or cycle
                              modes, are listed below. Note: Many fonts do
                              not include all characters for all languages,
                              so sometimes you'll need to change fonts to see
                              the characters you're trying to type.
                                 * Japanese - Romanized Hiragana and
                                   Romanized Katakana - right [Alt]
                                 * Korean - Hangul 2-Bul - right [Alt] or
                                   left [Alt]
                                 * Traditional Chinese - right [Alt] or
                                   left [Alt]
                                 * Thai - right [Alt]

     ----------------------------------------------------------------------

         Learn

                 The 'Learn' tool teaches you to draw a picture on paper,
                 step by step. It doesn't change your picture in Tux Paint:
                 you draw and color on a real sheet of paper, with a pencil,
                 an eraser and crayons.

                 Click the 'Learn' button and a dialog appears over the
                 canvas. At the top there are three tabs: "Easy" (one star),
                 "Medium" (two stars) and "Hard" (three stars). Below them
                 are the lessons of that level, each one showing the
                 finished, colored picture and its title. Click a lesson to
                 select it (its name is read aloud), then double-click it, or
                 click "Start", to begin. The "Voice" button turns reading
                 aloud on and off, and "Back" closes the dialog.

                 You can also use the keyboard: [1], [2] and [3] pick a
                 level, the arrow keys (or [F11], [F12], [F8] and [F7]) move
                 between the lessons, [Enter] starts the selected lesson,
                 [F2] renames it (in "Mine"), and [Escape] goes back.

                 The lesson is shown on a sheet of paper drawn on the screen,
                 with its title at the top left and, at the top right, dots
                 that show how far along you are. First comes the finished
                 picture, and Tux says: "Let's draw: (name)! Get a sheet of
                 paper, a pencil, an eraser and your crayons." Then the
                 lesson goes one step at a time. Tux shows the instruction
                 for the step, and a voice reads it aloud. The new lines of
                 the step are shown in orange-red, and blink; the lines of
                 the earlier steps are black. Next to the sheet, a picture
                 shows what to use:

                   * a pencil: draw the new lines;
                   * a paler pencil: draw a light 'guide' shape, softly
                     (e.g., a big oval that helps you place the other parts);
                   * an eraser: erase the guide shapes (on the screen, they
                     fade away);
                   * a crayon: color the blinking area, with the crayon's
                     color.

                 Click "Next" (or click the picture) to go to the next step,
                 "Previous" to go back one step, "Repeat" to hear the
                 instruction again and see the step blink again, or "Back" to
                 return to the list of lessons. On the keyboard, press
                 [Right], [Space], [Enter] or [Page Down] for the next step;
                 [Left], [Backspace] or [Page Up] for the previous one; [R]
                 to repeat; and [Escape] to go back.

                 After the last step, the finished picture is shown again,
                 and Tux says: "Well done! You finished: (name). Does your
                 drawing look like this one?"

                      Lessons

                              Tux Paint comes with 31 lessons. "Easy": apple,
                              balloon, fish, flower, house and sun (5 steps
                              each). "Medium": butterfly, cat, sailboat,
                              snail, tree and turtle (6 or 7 steps). "Hard",
                              with light guide shapes that are erased before
                              coloring (9 to 22 steps): biplane, car, cat
                              with a pumpkin, cat with friends (a short and a
                              long one), chicks in a nest, dinosaur, flying
                              vulture, fox with friends (a short and a long
                              one), garden chair, gumball machine, gummy
                              bears, horse with a foal, knitting friends,
                              owl, penguin, rocket and two foxes in the
                              woods.

                              Their texts are in English and Italian; in
                              other languages, the English ones are used.
                              (Translations can be added to the lesson
                              files.) To add your own lessons, see EXTENDING.

                      Your Own Pictures

                              A "Mine" tab (with a heart) appears when there
                              are pictures or lessons in the "custom" lessons
                              folder: "~/.tuxpaint/lessons/custom/" under
                              Linux and Unix (or "custom" in the data
                              directory's "lessons" folder). Tux Paint
                              doesn't come with any: it is for your own
                              drawings, or for pictures you got elsewhere
                              (mind their license).

                              Put SVG, PNG, JPEG or WebP pictures there. (EPS files
                              can't be read: convert them to SVG, e.g. with
                              Inkscape.) Each picture becomes a lesson that
                              copies it with a grid: look at it; draw a light
                              grid of 3 by 3 boxes on the paper; copy the
                              drawing one box at a time; erase the grid;
                              color it. Its title is the file's name, or the
                              one in a "NAME.txt" file next to it (just the
                              title, as in a lesson). Lessons with steps can
                              go there too (see EXTENDING).

                              The "Add" button of the Learn dialog puts a
                              picture there without leaving Tux Paint. It
                              shows, instead of the levels, the pictures in
                              your Downloads, Pictures and Desktop folders
                              (those you have; under Linux, as named in
                              "~/.config/user-dirs.dirs"). Pick one and press
                              "Add": it is copied to "custom", together with
                              the "NAME.txt" file next to it, if there is
                              one, with its steps or its title. Tux Paint
                              checks it first: a picture it can't read, or
                              steps whose groups aren't in the SVG, are not
                              added. Nothing is replaced: if the name is
                              taken, the copy gets another ("cat-2").

                              In the "Mine" tab, the "Rename" button (or the
                              [F2] key) gives the chosen picture another
                              name: type it on its card and press [Enter]
                              ([Escape] leaves it as it was; a click
                              elsewhere keeps what was typed). The name goes in its
                              "NAME.txt" file (made if missing), in place of
                              the title shown; the files keep their names.

                      The Voice

                              The instructions are read aloud by eSpeak NG,
                              in the language of the text, if its library
                              ("libespeak-ng.so.1") is installed. (On Debian
                              and Ubuntu it is in the "libespeak-ng1"
                              package, which is usually already installed
                              along with speech-dispatcher.) Another voice
                              program can be used instead, with the
                              "speechcommand" option.

                              The voice plays through Tux Paint's own sound,
                              so it is silent with the "--nosound" option, or
                              when sound is muted with [Alt] + [S]. The
                              "--nospeech" option turns it off altogether.
                              (See the "Options" documentation.)

                 The 'Learn' tool can be disabled (e.g., by running Tux Paint
                 with the "--nolessons" command-line option). It's also
                 disabled (greyed out) when no lessons are found.

     ----------------------------------------------------------------------

         Magic (Special Effects)

                 The 'Magic' tool is actually a set of special tools. Select
                 one of the "magic" effects from the selector on the right.
                 Then, depending on the tool, you can either click and drag
                 around the picture, and/or simply click the picture once, to
                 apply the effect.

                 If the tool can be used by clicking and dragging, a
                 'painting' button will be available on the left, below the
                 list of "magic" tools on the right side of the screen. If
                 the tool can affect the entire picture at once, an
                 'entire picture' button will be available on the right.

                 See the instructions for each Magic tool (in the
                 'magic-docs' folder).

     ----------------------------------------------------------------------

         Eraser

                 This tool is similar to the Paint Brush. Wherever you click
                 (or click and drag), the picture will be erased. (This may
                 be white, some other color, or to a background picture,
                 depending on the picture.)

                 A number of eraser sizes are available, both round and
                 square..

                 As you move the mouse around, a square outline follows the
                 pointer, showing what part of the picture will be erased to
                 white.

                 As you erase, a "squeaky clean" eraser/wiping sound is
                 played.

     ----------------------------------------------------------------------

  Other Controls

         Undo

                 Clicking this tool will undo the last drawing action. You
                 can even undo more than once!

                 Note: You can also press [Control]-[Z] on the keyboard to
                 undo.

     ----------------------------------------------------------------------

         Redo

                 Clicking this tool will redo the drawing action you just
                 "undid" with the 'Undo' button.

                 As long as you don't draw again, you can redo as many times
                 as you had "undone!"

                 Note: You can also press [Control]-[R] on the keyboard to
                 redo.

     ----------------------------------------------------------------------

         New

                 Clicking the "New" button will start a new drawing. A dialog
                 will appear where you may choose to start a new picture
                 using a solid background color, or using a 'Starter' image
                 (see below). You will first be asked whether you really want
                 to do this.

                 Note: You can also press [Control]-[N] on the keyboard to
                 start a new drawing.

                 'Starter' Images

                   'Starters' can be like a page from a coloring book (a
                   black-and-white outline of a picture, which you can then
                   color in), or like a 3D photograph, where you draw the
                   bits in between.

                   When you load a 'Starter,' draw on it, and then click
                   'Save,' it creates a new picture file (it doesn't
                   overwrite the original 'Starter,' so you can use it again
                   later).

     ----------------------------------------------------------------------

         Open

                 This shows you a list of all of the pictures you've saved.
                 If there are more than can fit on the screen, use the "Up"
                 and "Down" arrows at the top and bottom of the list to
                 scroll through the list of pictures.

                 Click a picture to select it, then...

                      * Click the green "Open" button at the lower left of
                        the list to load the selected picture.

                        (Alternatively, you can double-click a picture's icon
                        to load it.)

                      * Click the brown "Erase" (trash can) button at the
                        lower right of the list to erase the selected
                        picture. (You will be asked to confirm.)

                        Note: As of version 0.9.22, the picture will be
                        placed in your desktop's trash can, on Linux only.

                      * Click the blue "Slides" (slide projector) button at
                        the lower left to go to slideshow mode. See "Slides",
                        below, for details.

                      * Or click the red "Back" arrow button at the lower
                        right of the list to cancel and return to the picture
                        you were drawing.

                 If choose to open a picture, and your current drawing hasn't
                 been saved, you will be prompted as to whether you want to
                 save it or not. (See "Save," below.)

                 Note: You can also press [Control]-[O] on the keyboard to
                 get the 'Open' dialog.

     ----------------------------------------------------------------------

         Save

                 This saves your current picture.

                 If you haven't saved it before, it will create a new entry
                 in the list of saved images. (i.e., it will create a new
                 file)

                 Note: It won't ask you anything (e.g., for a filename). It
                 will simply save the picture, and play a "camera shutter"
                 sound effect.

                 If you HAVE saved the picture before, or this is a picture
                 you just loaded using the "Open" command, you will first be
                 asked whether you want to save over the old version, or
                 create a new entry (a new file).

                 (NOTE: If either the "saveover" or "saveovernew" options are
                 set, it won't ask before saving over. See the "Options"
                 documentation.)

                 Note: You can also press [Control]-[S] on the keyboard to
                 save.

     ----------------------------------------------------------------------

         Print

                 Click this button and your picture will be printed!

                 On most platforms, you can also hold the [Alt] key (called
                 [Option] on Macs) while clicking the 'Print' button to get a
                 printer dialog. Note that this may not work if you're
                 running Tux Paint in fullscreen mode. See below.

                      Disabling Printing

                              If the "noprint" option was set (either with
                              "noprint=yes" in Tux Paint's configuration
                              file, or using "--noprint" on the
                              command-line), the "Print" button will be
                              disabled.

                              See the "Options" documentation.)

                      Restricting Printing

                              If the "printdelay" option was used (either
                              with "printdelay=SECONDS" in the configuration
                              file, or using "--printdelay=SECONDS" on the
                              command-line), you can only print once every
                              SECONDS seconds.

                              For example, with "printdelay=60", you can
                              print only once a minute.

                              See the "Options" documentation.)

                      Printing Commands

                              (Linux and Unix only)

                              Tux Paint prints by generating a PostScript
                              representation of the drawing and sending it to
                              an external program. By default, the program
                              is:

                                lpr

                              This command can be changed by setting the
                              "printcommand" value in Tux Paint's
                              configuration file.

                              If the [Alt] key on the keyboard is being
                              pushed while clicking the 'Print' button, as
                              long as you're not in fullscreen mode, an
                              alternative program is run. By default, the
                              program is KDE's graphical print dialog:

                                kprinter

                              This command can be changed by setting the
                              "altprintcommand" value in Tux Paint's
                              configuration file.

                              For information on how to change the printing
                              commands, see the "Options" documentation.

                      Printer Settings

                              (Windows and Mac OS X)

                              By default, Tux Paint simply prints to the
                              default printer with default settings when the
                              'Print' button is pushed.

                              However, if you hold the [Alt] (or [Option])
                              key on the keyboard while pushing the button,
                              as long as you're not in fullscreen mode, your
                              operating system's printer dialog will appear,
                              where you can change the settings.

                              You can have the printer configuration changes
                              stored by using the "printcfg" option, either
                              by using "--printcfg" on the command-line, or
                              "printcfg=yes" in Tux Paint's own configuration
                              file ("tuxpaint.cfg").

                              If the "printcfg" option is used, printer
                              settings will be loaded from the file
                              "print.cfg" in your personal folder (see
                              below). Any changes will be saved there as
                              well.

                              See the "Options" documentation.)

                      Printer Dialog Options

                              By default, Tux Paint only shows the printer
                              dialog (or, on Linux/Unix, runs the
                              "altprintcommand", e.g., "kprinter" instead of
                              "lpr") if the [Alt] (or [Option]) key is held
                              while clicking the 'Print' button.

                              However, this behavior can be changed. You can
                              have the printer dialog always appear by using
                              "--altprintalways" on the command-line, or
                              "altprint=always" in Tux Paint's configuration
                              file. Or, you can prevent the [Alt]/[Option]
                              key from having any effect by using
                              "--altprintnever", or "altprint=never".

                              See the "Options" documentation.)

     ----------------------------------------------------------------------

         Slides (under "Open")

                 The "Slides" button is available in the "Open" dialog. It
                 displays a list of your saved files, just like the "Open"
                 dialog.

                 Click each of the images you wish to display in a
                 slideshow-style presentation, one by one. A digit will
                 appear over each image, letting you know in which order they
                 will be displayed.

                 You can click a selected image to unselect it (take it out
                 of your slideshow).

                 A sliding scale at the lower left of the screen (next to the
                 "Play" button) can be used to adjust the speed of the
                 slideshow, from slowest to fastest. Choose the leftmost
                 setting to disable automatic advancement - you will need to
                 press a key or click to go to the next slide (see below).

                 Note: The slowest setting does not automatically advance
                 through the slides. Use it for when you want to step through
                 them manually.

                 When you're ready, click the "Play" button to begin the
                 slideshow. (Note: If you hadn't selected ANY images, then
                 ALL images will be played in the slideshow.)

                 During the slideshow, press [Space], [Enter] or [Return] or
                 the [Right Arrow], or click the "Next" button at the lower
                 left, to manually advance to the next slide. Press [Left] to
                 go back to the previous slide.

                 Press [Escape], or click the "Back" button at the lower
                 right, to exit the slideshow and return to the slideshow
                 image selection screen.

                 Click "Back" in the slideshow image selection screen to
                 return to the "Open" dialog.

         Quit

                 Clicking the "Quit" button, closing the Tux Paint window, or
                 pushing the [Escape] key will quit Tux Paint.

                 You will first be prompted as to whether you really want to
                 quit.

                 If you choose to quit, and you haven't saved the current
                 picture, you will first be asked if wish to save it. If it's
                 not a new image, you will then be asked if you want to save
                 over the old version, or create a new entry. (See "Save"
                 above.)

                 NOTE: If the image is saved, it will be reloaded
                 automatically the next time you run Tux Paint!

                 NOTE: The "Quit" button and [Escape] key can be disabled
                 (e.g., by selecting "Disable 'Quit' Button" in
                 Tux Paint Config. or running Tux Paint with the "--noquit"
                 command-line option).

                 In that case, the "window close" button on Tux Paint's title
                 bar (if not in fullscreen mode) or the [Alt] + [F4] key
                 sequence may be used to quit.

                 If neither of those are possible, the key sequence of
                 [Shift] + [Control] + [Escape] may be used to quit. (See the
                 "Options" documentation.)

         Sound Muting

                 There is no on-screen control button at this time, but by
                 pressing [Alt] + [S], sound effects can be disabled and
                 re-enabled (muted and unmuted) while the program is running.

                 Note that if sounds are completely disabled (e.g., by
                 unselecting "Enable Sound Effects" in Tux Paint Config or
                 running Tux Paint with the "--nosound" command-line option),
                 the [Alt] + [S] key sequence has no effect. (i.e., it cannot
                 be used to turn on sounds when the parent/teacher wants them
                 disabled.)

     ----------------------------------------------------------------------

                     Loading Other Pictures into Tux Paint

     Since Tux Paint's 'Open' dialog only displays pictures you created with
     Tux Paint, what if you want to load some other picture or photograph
     into Tux Paint to edit?

     To do so, you simply need to convert the picture into a PNG (Portable
     Network Graphic) image file, and place it in Tux Paint's "saved"
     directory:

     Windows Vista
             Inside the user's "AppData" folder, e.g.:
             "C:\Users\(user name)\AppData\Roaming\TuxPaint\saved\"

     Windows 95, 98, ME, 2000, XP
             Inside the user's "Application Data" folder, e.g.: "C:\Documents
             and Settings\(user name)\Application Data\TuxPaint\saved\"

     Mac OS X
             Inside the user's "Library" folder:
             "/Users/(user name)/Library/Application
             Support/Tux Paint/saved/"

     Linux/Unix
             Inside a hidden ".tuxpaint" directory, in the user's home
             directory: "$(HOME)/.tuxpaint/saved/"

     Note: It is from this folder that you can copy or open pictures drawn in
     Tux Paint using other applications.

Using 'tuxpaint-import'

       Linux and Unix users can use the "tuxpaint-import" shell script which
       gets installed when you install Tux Paint. It uses some NetPBM tools
       to convert the image ("anytopnm"), resize it so that it will fit in
       Tux Paint's canvas ("pnmscale"), and convert it to a PNG ("pnmtopng").

       It also uses the "date" command to get the current time and date,
       which is the file-naming convention Tux Paint uses for saved files.
       (Remember, you are never asked for a 'filename' when you go to Save or
       Open pictures!)

       To use 'tuxpaint-import', simply run the command from a command-line
       prompt and provide it the name(s) of the file(s) you wish to convert.

       They will be converted and placed in your Tux Paint 'saved' directory.
       (Note: If you're doing this for a different user - e.g., your child,
       you'll need to make sure to run the command under their account.)

       Example:

         $ tuxpaint-import grandma.jpg
         grandma.jpg -> /home/username/.tuxpaint/saved/20020921123456.png
         jpegtopnm: WRITING A PPM FILE

       The first line ("tuxpaint-import grandma.jpg") is the command to run.
       The following two lines are output from the program while it's
       working.

       Now you can load Tux Paint, and a version of that original picture
       will be available under the 'Open' dialog. Just double-click its icon!

Doing it Manually

       Windows, Mac OS X and BeOS users must currently do the conversion
       manually.

       Load a graphics program that is capable of both loading your picture
       and saving a PNG format file. (See the documentation file "PNG.txt"
       for a list of suggested software, and other references.)

       When Tux Paint loads an image that's not the same size as its drawing
       canvas, it scales (and sometimes smears the edges of) the image so
       that it fits within the canvas.

       To avoid having the image stretched or smeared, you can resize it to
       Tux Paint's canvas size. This size depends on the size of the
       Tux Paint window, or resolution at which Tux Paint is run, if in
       fullscreen. (Note: The default resolution is 800x600.) See
       "Calculating Image Dimensions", below.

       Save the picture in PNG format. It is highly recommended that you name
       the filename using the current date and time, since that's the
       convention Tux Paint uses:

         YYYYMMDDhhmmss.png

         * YYYY = Year
         * MM = Month (01-12)
         * DD = Day (01-31)
         * HH = Hour, in 24-hour format (00-23)
         * mm = Minute (00-59)
         * ss = Second (00-59)

       e.g.:

         20020921130500 - for September 21, 2002, 1:05:00pm

       Place this PNG file in your Tux Paint 'saved' directory. (See above.)

  Calculating Image Dimensions

         The width of Tux Paint's canvas is simply the width of the window
         (e.g., 640, 800 or 1024 pixels), minus 192.

         Calculating the height of Tux Paint's canvas requires multiple
         steps:
          1. Take the height of the window (e.g, 480, 600 or 768 pixels) and
             subtract 144
          2. Take the result of Step 1 and divide it by 48
          3. Take the result of Step 2 and round it down (e.g., 9.5 becomes
             simply 9)
          4. Take the result of Step 3 and multiply it by 48
          5. Finally, take the result of Step 4 and add 40

         Example: Tux Paint running at fullscreen on a 1440x900 display.
           * The canvas width is simply 1440 - 192, or 1248.
           * The canvas height is calculated as:
               1. 900 - 144, or 756
               2. 756 / 48, or 15.75
               3. 15.75 rounded down, or 15
               4. 15 * 48, or 720
               5. 720 + 40, or 760
         So the canvas within a 1440x900 Tux Paint window is 1248x760.

     ----------------------------------------------------------------------

                                Further Reading

     Other documentation included with Tux Paint (in the "docs"
     folder/directory) include:
       * "Magic" Tool Documentation ("magic-docs")
         Documentation for each of the currently-installed "Magic" tools.
       * AUTHORS.txt
         List of authors and contributors.
       * CHANGES.txt
         Summary of changed between releases.
       * COPYING.txt
         Copying license (The GNU General Public License).
       * INSTALL.txt
         Instructions for compiling/installing, when applicable.
       * EXTENDING.html
         Detailed instructions on creating brushes, stamps and starters, and
         adding fonts, to extend Tux Paint.
       * OPTIONS.html
         Detailed instructions on command-line and configuration-file
         options, for those who don't want to use Tux Paint Config.
       * PNG.txt
         Notes on creating PNG format bitmapped images for use in Tux Paint.
       * SVG.txt
         Notes on creating SVG format vector images for use in Tux Paint.

     ----------------------------------------------------------------------

                                How to Get Help

     If you need help, feel free to contact New Breed Software:

       http://www.newbreedsoftware.com/

     You may also wish to participate in the numerous Tux Paint mailing
     lists:

       http://www.tuxpaint.org/lists/

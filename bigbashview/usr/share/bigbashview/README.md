<img src="https://github.com/biglinux/bigbashview/blob/master/bigbashview/usr/share/bigbashview/demos/documentation_images/bigbashview_logo.png" />
===================================

Graphical Frontends for shellscripts using HTML/JS/CSS

NEWS
----
*25/10/2019* - Version 3.3 released

About
-----

With BigBashView you will get:

  * Create powerfull frontend using common known languages as HTML, Javascrit and Shell!

  * Demo for all functions available!

  * Easy learn curve!

<img src="" />

Head over to the [http://code.google.com/p/bigbashview/downloads downloads] section to get it, and to the [http://code.google.com/p/bigbashview/wiki/Documentation wiki] section to see the documentation

Introduction
------------

Here you will find instructions on how to use `BigBashView` 3


Installing `BigBashView` 3
--------------------------

`BigBashView` 3 is not installable, you just need to download and extract the package.

To use it, you need:
  * python 3.x (http://www.python.org/) comes with Ubuntu
  * WebPy (http://webpy.org/) package python3-webpy on Ubuntu
  * PyQT5 (http://www.riverbankcomputing.co.uk/software/pyqt/intro) package python3-pyqt5 on Ubuntu 
  * Gtk3 (https://www.gtk.org/) package gir1.2-gtk-3.0

Usage
-----

to run `BigBashView`, you must execute the bigbashview.py script.
There are serveral command line arguments that can be used as following:
```bash

./bigbashview.py [-h|--help] [-s|--screen=widthxheight] [-v|--version] [-t|--toolkit=[gtk|qt|]] [-w|--window_state=[normal|maximized|fullscreen]] [-i|--icon image] [-c|--compatibility-mode] [-r|--root] [-d|--debug] URL
```

Where URL is a URL or a server path as documented bellow
```
|| Option || Description ||

|| -h, --help || Show the list of available options and exit ||
|| -s,--screen=widthxheight || Change the screen size for a specific widthxheight ||
|| -v, --version || Show version number and exit ||
|| -t, --toolkit=[gtk|qt] || Chooses the graphical toolkit to use. QT(5) or GTK(3) UI ||
|| -w, --window_state=[normal|maximized|fullscreen] || Change how the window will show, it can be normal, maximized or fullscreen ||
|| -i, --icon=image || Change `BigBashView` window icon ||
|| -c, --compatibility-mode || Enables `BigBashView` compatibility mode ||
|| -r, --root || Disable sandbox in QT UI for work as root. *only QT*
|| -d, --debug || Enable remote debugging *only QT*
```

Basic usage
-----------

To create a hello world window, just call `BigBashView` as follows:
```bash
$ ./bigbashview.py 'execute$echo Hello World!'
```

<img src="https://github.com/thor27/bigbashview/blob/python3/demos/documentation_images/hello01.png" />

To create a more fancy hello world, you coud try to create a script and call it, as follows:
```bash
$ vim hello.sh
```

```bash
#!/bin/bash
echo "
<html>
  <head>
    <title>Hello World at `BigBashView` 3</title>
  </head>
  <body>
    <h1>Hello $USER!</h1>
    <p>`date`</p>
  </body>
</html>
"
```

```bash
$chmod +x hello.sh
$./bigbashview.py 'execute$hello.sh'
```

<img src="" />

Server Options 
---------

As you saw above, to execute the *hello.sh* script, we used *execute$*

This syntax works like this:

```bash
command <options>$ <value>
```

The available commands are:

|| Command || Description ||
|| execute || execute `<value>` in your shell environment, and returns to the page everything that was printed to stdout ||
|| content || returns the contents of the file at `<value>` ||

The available options are:

|| Option || Description ||
|| plain || Set the web header Content type to text/plain ||
|| close || *only for execute command* Closes `BigBashView` after `<value>` execution ||

This same syntax can be used in URLs on links, images and everything on your webpage, just remember to put a */* before to use it.

To get some examples on how to use server options, see the folder *server_options* inside the demos folder of your `BigBashView` package

Creating Forms 
---------

After creating a form, set it on the action to send to server to execute the script. for example:

```html
<form action="execute$./process_form.sh">
```

in the process_form.sh you will get all post (or get) values in system variables named like:

```bash
p_fieldname
```

To get an example on how to create a form, see the folder *form* inside the demos folder of your `BigBashView` package

Common javascript and HTML tips 
---------

Some html and javascript window manipulations will work on `BigBashView` windows.

|| on HTML/Javascript || behavior on `BigBashView` Window ||
|| html `<title>` tag on head || Change window title ||
|| html `<link REL="SHORTCUT ICON" HREF="">` tag on head || Change window icon || *only QT*
|| javascript window.close || Closes the window ||
|| javascript window.resizeTo || Resizes the window || *only GTK*
|| javascript window.moveTo || Moves the window || *only GTK*

To see those javascript and HMTL tips in action, see the folder *javascript_html_tips* inside the demos folder of your `BigBashView` package

Closing the window
------------------

As you can see [http://code.google.com/p/bigbashview/issues/detail?id=2 here], there are some issues related to javascript window.close when the window has navigated.

To workaround this, you can tell server to shutdown the application, calling the *close* option like this:

```html
<a href="execute close$">Close the window</a>
```

This option will only work with the execute command.
Optionally you can, in your script, print "False" to stderr so the server will not close the window, like that:

```html
<a href="execute close$echo False">This does not close the window</a>
```

This way you can show a dialog confirmation before closing the window.

To get some examples on how to use this syntax, see the folder *window_close* inside the demos folder of your `BigBashView` package.

Advanced Usage
--------------

Compatibility Mode
------------------

To enable the compatibility mode, you need to use the *-c* or *--compatibility-mode* argument option when starting the application.

  The urls cannot contain *`file://`*, only the absolute path for the file.
  You need to use the absolute path for the file. Relative paths wont work.
  The old HTML tag *`<scripttool>`* is not available even in compatibility mode.

In comptibility mode, the URLs will not contain commands, just the path for the file. `BigBashView` will try to guess what to do with the file according its extension.

|| Extension || BBV Action ||
|| .sh,.sh.html,.sh.htm || Execute the file and return the result as HTML ||
|| .htm, .html || Open the file and return its content as HTML ||
|| .txt || Open the file and return its content as TXT ||

To get some examples on how to use compatibility mode, see the folder *compatibility_mode* inside the demos folder of your `BigBashView` package.

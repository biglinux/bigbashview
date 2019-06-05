#!/usr/bin/env python3
import gtk


def format_color_string(Color):
    return "rgb(%s,%s,%s)" % (Color.red / 256, Color.green/256,  Color.blue/256)


def format_color_key(key, Color):
    return "%s%s}\n" % (key, format_color_string(Color))


invisible1 = gtk.Invisible()
style1 = invisible1.style

button1 = gtk.Button()
buttonstyle = button1.style

scroll1 = gtk.VScrollbar()
scrollbarstyle = scroll1.style

menu1 = gtk.Menu()
menuitem1 = gtk.MenuItem()
menu1.add(menuitem1)
menustyle = menuitem1.style

user_reg = """<style><!--

a:hover {text-decoration:underline;}
"""

# http://ubuntuforums.org/showthread.php?p=5506889
# http://www.moeraki.com/pygtkreference/pygtk2reference/class-gtkstyle.html
# http://lists.ximian.com/pipermail/mono-winforms-list/2003-August/000469.html


user_reg += format_color_key('a:link {color: ', style1.bg[gtk.STATE_SELECTED])
user_reg += format_color_key('body {background-color:',
                             style1.bg[gtk.STATE_NORMAL])
user_reg += format_color_key('body {color:', style1.fg[gtk.STATE_NORMAL])
user_reg += format_color_key(
    'table.kdecolor {background-color:', style1.fg[gtk.STATE_INSENSITIVE])


print(user_reg)

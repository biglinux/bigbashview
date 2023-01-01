# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2009  Bruno Goncalves Araujo
#  Copyright (C) 2022 Elton Fabrício Ferreira <eltonfabricio10@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout,
    QSplitter, QApplication
)
from PySide6.QtGui import (
    QIcon, QColor, QKeySequence,
    QShortcut, QCursor
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage as QEP
from bbv.globaldata import ICON, TITLE

# Import gettext module
import gettext
lang_translations = gettext.translation(
    'bigbashview',
    localedir='/usr/share/locale',
    fallback=True
)
lang_translations.install()

# define _ shortcut for translations
_ = lang_translations.gettext


class Window(QWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.web = QWebEngineView()
        self.inspector = QWebEngineView()
        self.inspector.page().windowCloseRequested.connect(self.devpage)
        self.setWindowIcon(QIcon(ICON))
        if TITLE:
            self.app.setApplicationName(TITLE)
            self.setWindowTitle(TITLE)
        else:
            self.web.titleChanged.connect(self.title_changed)
        self.web.page().windowCloseRequested.connect(self.close_window)
        self.web.page().featurePermissionRequested.connect(self.onFeature)
        self.web.iconChanged.connect(self.icon_changed)
        self.web.loadFinished.connect(self.add_script)
        self.key_f5 = QShortcut(QKeySequence(Qt.Key_F5), self.web)
        self.key_f5.activated.connect(self.web.reload)
        self.key_f12 = QShortcut(QKeySequence(Qt.Key_F12), self.web)
        self.key_f12.activated.connect(self.devpage)

        # contextmenu translations
        back = self.web.pageAction(QEP.Back)
        back.setText(_('Voltar'))
        forward = self.web.pageAction(QEP.Forward)
        forward.setText(_('Avançar'))
        update = self.web.pageAction(QEP.Reload)
        update.setText(_('Recarregar'))
        copy = self.web.pageAction(QEP.Copy)
        copy.setText(_('Copiar'))
        cut = self.web.pageAction(QEP.Cut)
        cut.setText(_('Recortar'))
        paste = self.web.pageAction(QEP.Paste)
        paste.setText(_('Colar'))
        select_all = self.web.pageAction(QEP.SelectAll)
        select_all.setText(_('Selecionar tudo'))
        undo = self.web.pageAction(QEP.Undo)
        undo.setText(_('Desfazer'))
        redo = self.web.pageAction(QEP.Redo)
        redo.setText(_('Refazer'))
        paste_style = self.web.pageAction(QEP.PasteAndMatchStyle)
        paste_style.setVisible(False)
        copy_link = self.web.pageAction(QEP.CopyLinkToClipboard)
        copy_link.setText(_('Copiar endereço do link'))
        inspect_element = self.web.pageAction(QEP.InspectElement)
        inspect_element.setText(_('Inspecionar'))
        copy_img = self.web.pageAction(QEP.CopyImageToClipboard)
        copy_img.setText(_('Copiar imagem'))
        copy_link_img = self.web.pageAction(QEP.CopyImageUrlToClipboard)
        copy_link_img.setText(_('Copiar endereço da imagem'))
        save_page = self.web.pageAction(QEP.SavePage)
        save_page.setVisible(False)
        view_source = self.web.pageAction(QEP.ViewSource)
        view_source.setVisible(False)
        open_new_tab = self.web.pageAction(QEP.OpenLinkInNewTab)
        open_new_tab.setVisible(False)
        open_new_window = self.web.pageAction(QEP.OpenLinkInNewWindow)
        open_new_window.setVisible(False)
        save_link = self.web.pageAction(QEP.DownloadLinkToDisk)
        save_link.setVisible(False)
        save_img = self.web.pageAction(QEP.DownloadImageToDisk)
        save_img.setVisible(False)

        # pagesplitter
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.web)
        self.splitter2 = QSplitter(Qt.Horizontal)
        self.hbox.addWidget(self.splitter)
        self.setLayout(self.hbox)

    def onFeature(self, url, feature):
        if feature in (
            QEP.MediaAudioCapture,
            QEP.MediaVideoCapture,
            QEP.MediaAudioVideoCapture,
        ):
            self.web.page().setFeaturePermission(
                url,
                feature,
                QEP.PermissionGrantedByUser
            )
        else:
            self.web.page().setFeaturePermission(
                url,
                feature,
                QEP.PermissionDeniedByUser
            )

    def devpage(self):
        if self.splitter.count() == 1 or self.splitter2.count() == 1:
            self.inspector.page().setInspectedPage(self.web.page())
            self.splitter2.hide()
            self.splitter.addWidget(self.web)
            self.splitter.addWidget(self.inspector)
            self.splitter.setSizes([(self.width()/3)*2, self.width()/3])
            self.splitter.show()
            self.hbox.addWidget(self.splitter)
            self.setLayout(self.hbox)
        else:
            self.splitter.hide()
            self.splitter2.addWidget(self.web)
            self.splitter2.show()
            self.hbox.addWidget(self.splitter2)
            self.setLayout(self.hbox)

    def add_script(self, event):
        script = '''
        function _run(run){
        //https://dmitripavlutin.com/javascript-fetch-async-await/#4-canceling-a-fetch-request

            // Step 1: instantiate the abort controller
            const controller = new AbortController();
            setTimeout(() => controller.abort(), 1000);

            // Step 2: make the fetch() aware of controller.signal
            fetch('/execute$'+run, { signal: controller.signal });
        };
        '''
        if event:
            self.web.page().runJavaScript(script)

    def viewer(self, window_state):
        if window_state == "maximized":
            self.setWindowState(Qt.WindowMaximized)
            self.show()
        elif window_state == "fullscreen":
            self.setWindowState(Qt.WindowFullScreen)
            self.show()
        elif window_state == "maximizedTop":
            self.setWindowState(Qt.WindowMaximized)
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        elif window_state == "frameless":
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.show()
        elif window_state == "framelessTop":
            self.setWindowFlags(
                Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
            )
            self.show()
        elif window_state == "fixedTop":
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.show()

    def run(self):
        self.app.exec_()

    def close_window(self):
        self.app.quit()

    def title_changed(self, title):
        os.system('''
        xprop -id "$(xprop -root '\t$0' _NET_ACTIVE_WINDOW | cut -f2)" \
              -f WM_CLASS 8s -set WM_CLASS "%s"''' % title)
        self.setWindowTitle(title)

    def icon_changed(self, icon):
        self.setWindowIcon(QIcon(icon))

    def load_url(self, url):
        self.url = QUrl.fromEncoded(url.encode("utf-8"))
        self.web.load(self.url)

    def set_size(self, width, height, window_state):
        display = self.app.screenAt(QCursor().pos())
        size = display.availableGeometry()
        if width <= 0:
            width = size.width()/2
        if height <= 0:
            height = size.height()/2

        self.resize(width, height)
        qr = self.frameGeometry()
        cp = display.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        if window_state in ("fixed", "fixedTop"):
            self.setFixedSize(width, height)

    def style(self, colorful):
        if colorful == 'black':
            self.web.page().setBackgroundColor(QColor.fromRgbF(0, 0, 0, 1))

        elif colorful == 'none':
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.web.page().setBackgroundColor(QColor.fromRgbF(0, 0, 0, 0))

        elif os.environ.get('XDG_CURRENT_DESKTOP') == 'KDE':
            rgb = os.popen('''
            kreadconfig5 --group WM --key activeBackground
            ''').read().split(',')

            if len(rgb) > 1:
                r, g, b = rgb if len(rgb) == 3 else rgb[:-1]
                r = float(int(r)/255)
                g = float(int(g)/255)
                b = float(int(b)/255)
                self.web.page().setBackgroundColor(QColor.fromRgbF(r, g, b, 1))
            else:
                self.web.page().setBackgroundColor(QColor.fromRgbF(0, 0, 0, 0))
        else:
            self.web.page().setBackgroundColor(QColor.fromRgbF(0, 0, 0, 0))

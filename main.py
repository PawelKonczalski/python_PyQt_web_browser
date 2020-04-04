import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter


class address_bar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mouse_press_event(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Web Browser')
        self.layout = QVBoxLayout()
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout()
        self.addressbar = address_bar()
        self.add_tab_button = QPushButton('+')
        self.back_button = QPushButton('<')
        self.forward_button = QPushButton('>')
        self.reload_button = QPushButton('⟳')
        self.container = QWidget()
        self.tabs = []
        self.tab_count = 0
        self.create_app()
        self.setFixedSize(1366, 768)

    def create_app(self):
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.tabbar.tabCloseRequested.connect(self.close_tab)
        self.tabbar.tabBarClicked.connect(self.switch_tab)
        self.add_tab_button.clicked.connect(self.add_tab)
        self.addressbar.setObjectName('Addressbar')
        self.addressbar.returnPressed.connect(self.browse_to)
        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button.clicked.connect(self.reload_page)

        self.toolbar.setObjectName('Toolbar')
        self.toolbar.setLayout(self.toolbar_layout)
        self.toolbar_layout.addWidget(self.back_button)
        self.toolbar_layout.addWidget(self.forward_button)
        self.toolbar_layout.addWidget(self.reload_button)
        self.toolbar_layout.addWidget(self.addressbar)
        self.toolbar_layout.addWidget(self.add_tab_button)
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)
        self.add_tab()
        self.show()

    def close_tab(self, i):
        self.tabbar.removeTab(i)
        self.tab_count -= 1

    def add_tab(self):
        i = self.tab_count
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)
        self.tabs[i].setObjectName('tab' + str(i))
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput('https://google.com'))
        self.tabs[i].content.titleChanged.connect(lambda: self.set_tab_text(i, 'title'))
        self.tabs[i].content.iconChanged.connect(lambda: self.set_tab_text(i, 'icon'))
        self.tabs[i].content.urlChanged.connect(lambda: self.set_tab_text(i, 'url'))
        self.tabs[i].splitview = QSplitter()
        self.tabs[i].layout.addWidget(self.tabs[i].splitview)
        self.tabs[i].splitview.addWidget(self.tabs[i].content)
        self.tabs[i].setLayout(self.tabs[i].layout)
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])
        self.tabbar.addTab('New tab')
        self.tabbar.setTabData(i, {'object': 'tab' + str(i), 'initial': i})
        self.tabbar.setCurrentIndex(i)
        self.tab_count += 1

    def switch_tab(self, i):
        if self.tabbar.tabData(i)['object']:
            tab_data = self.tabbar.tabData(i)['object']
            tab_content = self.findChild(QWidget, tab_data)
            self.container.layout.setCurrentWidget(tab_content)
            new_url = tab_content.content.url().toString()
            self.addressbar.setText(new_url)

    def browse_to(self):
        text = self.addressbar.text()
        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        wv = self.findChild(QWidget, tab).content

        if 'http' not in text:
            if '.' not in text:
                url = 'https://www.google.com/search?q=' + text
            else:
                url = 'http://' + text
        else:
            url = text
        wv.load(QUrl.fromUserInput(url))

    def set_tab_text(self, i, type):
        tab_name = self.tabs[i].objectName()
        count = 0
        running = True
        current_tab = self.tabbar.tabData(self.tabbar.currentIndex())['object']

        if current_tab == tab_name and type == 'url':
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.addressbar.setText(new_url)
            return False

        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False

            if tab_name == tab_data_name['object']:
                if type == 'title':
                    new_title = self.findChild(QWidget, tab_name).content.title()
                    self.tabbar.setTabText(count, new_title)
                elif type == 'icon':
                    new_icon = self.findChild(QWidget, tab_name).content.icon()
                    self.tabbar.setTabIcon(count, new_icon)
                running = False
            else:
                count += 1

    def go_back(self):
        active_index = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(active_index)['object']
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.back()

    def go_forward(self):
        active_index = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(active_index)['object']
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.forward()

    def reload_page(self):
        active_index = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(active_index)['object']
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.reload()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '667'
    window = App()
    with open('style.css', 'r') as style:
        app.setStyleSheet(style.read())
    sys.exit(app.exec_())


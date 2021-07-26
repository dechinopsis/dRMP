import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings


class Screenshot(QWebEngineView):

    def capture(self, url, output_file):
        self.output_file = output_file
        self.load(QUrl(url))
        self.loadFinished.connect(self.on_loaded)
        # Create hidden view without scrollbars
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.show()

    def on_loaded(self):
        # size = self.page().contentsSize().toSize()
        ##self.setFixedHeight(750)
        # self.resize(size)
        # self.setZoomFactor(0.5)
        # Wait for resize
        QTimer.singleShot(4000, self.remove_inputs)

    def remove_inputs(self):
        self.page().runJavaScript(
            """
            function remove(elem){
                if(elem.parentNode)
                     elem.parentNode.removeChild(elem);
            }
            remove(document.getElementById("layers"));
            remove(document.querySelector('header[role="banner"]'));
            //document.querySelector('article[role="article"]').style='font-color:white;background-color:#15202B;';

            (function(){
                var article = document.querySelector('article[role=\"article\"]');
                if(article)
                    return document.querySelector('article[role=\"article\"]').offsetHeight;
                return 'null';
            })();
        """, self.callbackJs)

    def callbackJs(self, wtfit):
        def representsInt(s):
            try:
                int(s)
                print('valid integer height', s, type(s))
                return True
            except ValueError:
                print('error parsing height ',s)
                return False

        if representsInt(wtfit):
            self.setFixedHeight(wtfit)

        QTimer.singleShot(4000, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')
        self.app.quit()


print('capturing tweet---->>>' + sys.argv[1])

tweetId = sys.argv[1]
app = QApplication(sys.argv)
s = Screenshot()
s.app = app
s.capture('https://twitter.com/i/web/status/' + str(tweetId),
          '/Users/dtorres/Documents/RMPSS/'+str(tweetId)+'.png')
sys.exit(app.exec_())


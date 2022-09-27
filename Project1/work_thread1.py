from PyQt5.QtCore import QRunnable, pyqtSlot
from work_signals import WorkerSignals
import traceback,sys


class GenPDF(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self,fn, getid = None,*args,**kwargs):
        super(GenPDF,self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.getid = getid
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @staticmethod
    def test(getstr):
        print(getstr)


    '''
    Worker thread
    '''
    @pyqtSlot()
    def run(self):
        self.test("hello")
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
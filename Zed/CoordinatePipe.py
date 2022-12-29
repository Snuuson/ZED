import win32pipe
import win32file

class CoordinatePipe:
    _BUFFER_SIZE = 1024 * 30
    def __init__(self) -> None:
        self._create_pipe()
        self._connect()
        
    def _create_pipe(self):
        print("Creating Pipe")
        self.pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\CoordinatePipe',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, self._BUFFER_SIZE, self._BUFFER_SIZE,
        0,
        None)
        
    def _connect(self):
        print("Waiting for Client")
        win32pipe.ConnectNamedPipe(self.pipe, None)
        print("Connected to Client")

    def _close(self):
        print("Closing pipe")
        win32file.CloseHandle(self.pipe)

    def Write(self,data):
        try:
            win32file.FlushFileBuffers(self.pipe)
            win32file.WriteFile(self.pipe, data)
            
            
        except Exception as ex:
            print(ex)
            self._close()
            self._create_pipe()
            self._connect()

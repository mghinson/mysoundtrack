import SocketServer
import SimpleHTTPServer

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")        

    def do_GET(self):           
        self.send_response(200)
        self.wfile.write(self.path)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type',    'text/html')                                    
        self.end_headers()              
        self.wfile.write(self.path)
        self.connection.shutdown(1) 
        return(self.path)

def main():
  SocketServer.ForkingTCPServer(('', 8000), MyHandler).serve_forever()

main()
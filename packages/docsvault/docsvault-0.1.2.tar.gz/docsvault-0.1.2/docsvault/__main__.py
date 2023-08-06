import sys, os
import argparse
import webbrowser
import subprocess


def parse_args(args=None):    
    parser = argparse.ArgumentParser('docsvault')
    subparsers = parser.add_subparsers(dest='command')

    server_parser = subparsers.add_parser('server', help='control docsvault server state')
    server_parser.add_argument('--host', type=str, default='localhost', help='ip or name on which server listen')
    server_parser.add_argument('--port', type=str, default='8024', help='port on which server listen')
    server_parser.add_argument('--debug', action='store_true', help='if set, enable hot reload')
   
    webui_parser = subparsers.add_parser('webui', help='open docsvault web ui in your browser')

    args = parser.parse_args(args)
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    return args


def start_server(host='localhost', port=8025, debug=False):
    python_bin = os.path.dirname(sys.executable)

    if debug:
        command = [
            os.path.join(python_bin, 'uvicorn'),
            'docsvault.wsgi:app', '--reload',
            '--port', str(port)
        ]
        print(command)
    else:
        command = [
            os.path.join(python_bin, 'gunicorn'),
            'docsvault.wsgi:app',
            '--bind', '{}:{}'.format(host, port),
            '-k', 'uvicorn.workers.UvicornWorker'
        ]
        if not debug:
            command.append('--daemon')
            print('Server listening on http://{}:{}'.format(host, port))
        print(command)

    subprocess.call(command)


def main(args=None):
    """
    Dispatch parsed command to the
    corresponding docsvault function.
    """
    args = parse_args(args)
    
    if args.command == 'server':
        print(args.port, args.host)
        start_server(host=args.host, port=args.port)
    elif args.command == 'webui':
        webbrowser.open('http://localhost:8025')  


if __name__ == '__main__':
    main()

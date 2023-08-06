import asyncio
from biolib.pyppeteer.pyppeteer import launch, command
from biolib.pyppeteer.pyppeteer.launcher import resolveExecutablePath, __chromium_revision__
import http.server
import socketserver
import threading
import base64
import os
import sys
import subprocess
import re
import requests

# fix required for async to work in notebooks
import nest_asyncio
nest_asyncio.apply()

# import sys, logging
# logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
#                     level=logging.INFO, stream=sys.stdout)
# logger = logging.getLogger('DEV')
# logger.setLevel(logging.DEBUG)

class BioLibError(Exception):
    def __init__(self, message):
        self.message = message


class CompletedProcess:
    def __init__(self, stdout, stderr, exitcode):
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode

    def ipython_markdown(self):
        from IPython.display import display, Markdown
        markdown_str = self.stdout.decode("utf-8")
        # prepend ./biolib_results/ to all paths
        # ie [SeqLogo](./SeqLogo2.png) test ![SeqLogo](./SeqLogo.png)
        # ![SeqLogo](SeqLogo.png)  ![SeqLogo](/SeqLogo.png)
        # is transformed to ![SeqLogo](./biolib_results/SeqLogo2.png) test ![SeqLogo](./biolib_results/SeqLogo.png)
        # ![SeqLogo](./biolib_results/SeqLogo.png)  ![SeqLogo](./biolib_results/SeqLogo.png)
        markdown_str_modified = re.sub('\!\[([^\]]*)\]\((\.\/|\/|)([^\)]*)\)', '![\\1](./biolib_results/\\3)', markdown_str)
        display(Markdown(markdown_str_modified))

class BioLibServer(socketserver.TCPServer):
    debug = False

class BioLibHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if self.server.debug:
            http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)


def js_to_python_byte_array_converter(js_encoded):
    return bytes(list([js_encoded[str(i)] for i in range(len(js_encoded))]))


def python_bytes_to_byte64(data):
    return base64.b64encode(data).decode('ascii')


class BioLib:
    executable_path = None
    no_sandbox = True
    debug = True

    @staticmethod
    def set_chrome_path(path):
        BioLib.executable_path = path

    @staticmethod
    def set_sandbox(use_sandbox):
        BioLib.no_sandbox = not use_sandbox

    @staticmethod
    def set_debug(use_debug):
        BioLib.debug = use_debug

class BioLibApp:

    def __init__(self, author, name):
        if BioLib.debug:
            print("Loading package...")
        api_url = f"https://biolib.com/api/apps/?account_handle={author}&app_name={name}"
        r = requests.get(api_url)
        results = r.json()['results']
        if len(results) == 0:
            raise Exception(f"Application '{author}/{name}' was not found. "
                            f"Make sure you have spelled the application name correctly, "
                            f"and that you have the required permissions.")
        app = results[0]
        app_version_uuid = app["public_id"]
        semantic_version = f"{app['active_version']['major']}.{app['active_version']['minor']}.{app['active_version']['patch']}"
        self.app_version_uuid = app_version_uuid
        self.semantic_version = semantic_version
        if BioLib.debug:
            print("Loaded package:", f"{author}/{name}")

    async def call_pyppeteer(self, port, args, stdin, files, output_path):
        if not BioLib.executable_path:
            mac_chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if os.path.isfile(mac_chrome_path):
                BioLib.set_chrome_path(mac_chrome_path)

        if not BioLib.executable_path:
            linux_chrome_path = "/usr/lib/chromium-browser/chromium-browser"

            # special install for google colab
            if not os.path.isfile(linux_chrome_path) and 'google.colab' in sys.modules:
                subprocess.run("apt-get update", shell=True, check=True)
                subprocess.run("apt install chromium-chromedriver", shell=True, check=True)

            if os.path.isfile(linux_chrome_path):
                BioLib.set_chrome_path(linux_chrome_path)

        resolved_path = resolveExecutablePath(None, __chromium_revision__)
        if not BioLib.executable_path and resolved_path[1]:
            # if executable_path is not set explicit,
            # and resolveExecutablePath failed (== we got an error message back in resolved_path[1])
            if BioLib.debug:
                print("Installing dependencies...")
            os.environ['PYPPETEER_NO_PROGRESS_BAR'] = "true"
            command.install()

        chrome_arguments = [
                '--disable-web-security',
            ]
        if BioLib.no_sandbox:
            chrome_arguments.append('--no-sandbox')
        browser = await launch(args=chrome_arguments, executablePath=BioLib.executable_path
        )

        # start new page
        page = await browser.newPage()

        await page.goto("http://localhost:" + str(port))

        def getCode():
            return python_bytes_to_byte64(b"code")

        def getData():
            data = {}
            data["stdin"] = stdin
            data["parameters"] = args
            data["files"] = files
            return data

        def setProgressCompute(x):
            if BioLib.debug:
                print("Compute progress:", x)

        def setProgressInitialization(x):
            if BioLib.debug:
                print("Initialization progress:", x)

        def addLogMessage(x):
            if BioLib.debug:
                print("Log message:", x)

        await page.exposeFunction("getCode", getCode)
        await page.exposeFunction("getData", getData)
        await page.exposeFunction("setProgressCompute", setProgressCompute)
        await page.exposeFunction("setProgressInitialization", setProgressInitialization)
        await page.exposeFunction("addLogMessage", addLogMessage)

        result = await page.evaluate("""
        async function() {
          const refreshToken = undefined;
          window.BioLib.BioLibSingleton.setConfig({ baseUrl: 'https://biolib.com', refreshToken });
          window.BioLib.AppClient.setApiClient(window.BioLib.BioLibSingleton.get());
          var data = await window.getData()
          data["stdin"] = Uint8Array.from(atob(data["stdin"]), c => c.charCodeAt(0))
          for(var i = 0; i<data["files"].length; i++) {
              data["files"][i].data = Uint8Array.from(atob(data["files"][i].data), c => c.charCodeAt(0))
          }
          var jobUtils = {}
          jobUtils["setProgressCompute"] = window.setProgressCompute
          jobUtils["setProgressInitialization"] = window.setProgressInitialization
          jobUtils["addLogMessage"] = window.addLogMessage

          try {
            return await window.BioLib.AppClient.runApp(""" + f"\"{self.app_version_uuid}\",\"{self.semantic_version}\"" + """, data, jobUtils)
          } catch(err) {
            return err.toString()
          }
        }
        """)
        if BioLib.debug:
            print("Closing browser")
        await browser.close()

        if isinstance(result, dict):
            if len(result["files"]) > 0:
                if BioLib.debug:
                    print("Writing output files to:", output_path)
                os.makedirs(output_path, exist_ok=True)
                for f in result["files"]:
                    filename = output_path + f["pathWithoutFilename"] + f["name"]
                    data = js_to_python_byte_array_converter(f["data"])
                    fp = open(filename, "wb")
                    fp.write(data)
                    fp.close()
            return CompletedProcess(
                stdout=js_to_python_byte_array_converter(result["stdout"]),
                stderr=js_to_python_byte_array_converter(result["stderr"]),
                exitcode=result["exitcode"]
            )
        else:
            raise BioLibError(result)

    def __call__(self, args=[], stdin=None, files=None, output_path="biolib_results"):
        cwd = os.getcwd()

        if stdin is None:
            stdin = b""

        if not output_path.startswith("/"):
            # output_path is relative, make absolute
            output_path = f"{cwd}/{output_path}"

        if isinstance(args, str):
            args = list(filter(lambda p: p != "", args.split(" ")))

        if not isinstance(args, list):
            raise Exception("The given input arguments must be list or str")

        if isinstance(stdin, str):
            stdin = stdin.encode("utf-8")

        if files is None:
            files = []
            for idx, arg in enumerate(args):
                if os.path.isfile(arg):
                    files.append(arg)
                    args[idx] = arg.split("/")[-1]

        files_data = []
        for f in files:
            path = f
            if not f.startswith("/"):
                # make path absolute
                path = cwd + "/" + f

            arg_split = path.split("/")
            file = open(path, "rb")
            files_data.append({
                "pathWithoutFilename": "/",
                "name": arg_split[-1],
                "data": python_bytes_to_byte64(file.read())
            })
            file.close()

        stdin = python_bytes_to_byte64(stdin)

        BioLibServer.debug = BioLib.debug
        with BioLibServer(("127.0.0.1", 0), BioLibHandler) as httpd:
            port = httpd.server_address[1]
            thread = threading.Thread(target=httpd.serve_forever)
            # TODO: figure out how we can avoid changing the current directory
            os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/biolib-js/")
            try:
                thread.start()
                res = asyncio.get_event_loop().run_until_complete(
                    self.call_pyppeteer(port=port, args=args, stdin=stdin, files=files_data, output_path=output_path))
            finally:
                os.chdir(cwd)
            httpd.shutdown()
            thread.join()
            return res

        raise BioLibError("Failed to start TCPServer")

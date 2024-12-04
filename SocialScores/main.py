
def hello_world():
    return "Hello, World!"

import os
import locale
print(f"Preferred encoding: {locale.getpreferredencoding()}")

print(hello_world())

import Database.InitializationJob as InitializationJob

# init database
InitializationJob.start()


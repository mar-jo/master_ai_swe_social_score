
def hello_world():
    return "Hello, World!"

print(hello_world())

import Database.InitializationJob as InitializationJob

# init database
InitializationJob.start()


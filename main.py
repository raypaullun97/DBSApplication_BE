from core import app
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)



if (__name__ == "__main__"):

    logging.debug("Hello World")
    app.runner()
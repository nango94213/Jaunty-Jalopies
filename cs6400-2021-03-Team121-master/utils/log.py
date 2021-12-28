import logging

from conf.config import LOG_LEVEL

# Create a custom logger
LOG = logging.getLogger(__name__)
LOG.setLevel(level=LOG_LEVEL)

# Create handlers
handler = logging.StreamHandler()

# Create formatters and add it to handlers
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s:%(pathname)s:%(lineno)s %(message)s')
handler.setFormatter(formatter)

# Add handlers to the logger
LOG.addHandler(handler)

LOG.propagate = False

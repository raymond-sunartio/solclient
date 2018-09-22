import logging
import logging.config
import settings
from solclient import solclient

logger = logging.getLogger(__name__)


#
# main()
#
def main():
    logging.config.dictConfig(settings.LOGGING)


if __name__ == '__main__':
    main()


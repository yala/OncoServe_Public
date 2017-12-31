import oncoserve.logger
logger = oncoserve.logger.get_logger('oncologger.oncoserve', 'errors.log')

NO_AGGREGATOR_ERR = "Aggregator {} not in AGGREGATOR_REGISTRY! Available datasets are {}"
AGGREGATOR_SUCCESS_MSG = "Aggregator {} succesfuly retrieved from aggregator factory"

AGGREGATOR_REGISTRY = {}

def RegisterExamAggregator(name):
    def decorator(f):
        AGGREGATOR_REGISTRY[name] = f
        return f

    return decorator

def get_exam_aggregator(name):

    if not name in AGGREGATOR_REGISTRY:
        error_msg = NO_AGGREGATOR_ERR.format(name, AGGREGATOR_REGISTRY.keys())
        logger.error(error_msg)
        raise Exception(error_msg)
    logger.info(AGGREGATOR_SUCCESS_MSG.format(name))
    return AGGREGATOR_REGISTRY[name]

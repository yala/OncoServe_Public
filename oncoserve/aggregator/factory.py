logger = logging.getLogger('oncologger.oncoserve')

NO_AGGREGATOR_ERR = "Aggregator {} not in AGGREGATOR_REGISTRY! Available datasets are {}"

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

    return AGGREGATOR_REGISTRY[name]
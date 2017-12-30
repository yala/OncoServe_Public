from oncoserve.aggregator.factory import RegisterExamAggregator
import numpy as np

@RegisterExamAggregator("max")
def aggregate_max(preds):
    return np.max(preds)

@RegisterExamAggregator("vote")
def aggregate_vote(preds):
    counts = np.bincount(preds)
    max_indx = np.argmax(counts)
    return preds[max_indx]



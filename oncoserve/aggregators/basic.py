from oncoserve.aggregators.factory import RegisterExamAggregator
import numpy as np

@RegisterExamAggregator("max")
def aggregate_max(preds):
    return np.max(preds)

@RegisterExamAggregator("vote")
def aggregate_vote(preds):
    counts = np.bincount(preds)
    max_vote = np.argmax(counts)
    return max_vote



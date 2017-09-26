DEBUG=True
SERVER_NAME="localhost:5000"

# Custom configuration parameters
MODEL="alexnet"         # model to use for the task: "alexnet", "resnet18",
                        # "resnet34", "resnet50", "resnet101", "resnet152",
                        # "squeezenet1.0", "squeezenet1.1"
AGGREGATION="none"          # method of aggregating the results: "first", "last",
                            # "min", "max", "none"

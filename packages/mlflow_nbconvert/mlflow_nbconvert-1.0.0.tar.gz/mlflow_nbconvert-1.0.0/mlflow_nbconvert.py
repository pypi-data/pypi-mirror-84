"""mlflow-nbconvert"""
__version__ = "1.0.0"

import mlflow
from nbconvert.postprocessors import PostProcessorBase


class MLFlowPostProcessor(PostProcessorBase):
    def postprocess(self, input):
        mlflow.log_artifact(input)


def main(path):
    """allow running this module to serve the slides"""
    postprocessor = MLFLowPostProcessor()
    postprocessor(path)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])

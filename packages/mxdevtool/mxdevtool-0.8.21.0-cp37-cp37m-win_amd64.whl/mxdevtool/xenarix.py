import mxdevtool as mx


def test_xenarix():
    print('now testing...')


def max(models, name=None):
    if name is None:
        name = '_'.join([m.name() for m in models]) + 'max'
    return mx.MultaryFunctionWrapperCalc(name, models, 'max')
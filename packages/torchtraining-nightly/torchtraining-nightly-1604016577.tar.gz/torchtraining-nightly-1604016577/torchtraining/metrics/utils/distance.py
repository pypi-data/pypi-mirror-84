from . import docs_general


def docstring(header, reduction=None):
    def arguments():
        return r"""
Arguments
---------
data: Tuple[torch.Tensor, torch.Tensor]
    Tuple containing `outputs` from neural network and regression `targets`.
    `outputs` should be of shape :math:`(N, F)`, where :math:`N` is the number of samples,
    :math:`F` is the number of features.
    Should contain `floating` point values.
    `targets` should be in the same shape `outputs` and be of `float` data type as well.

        """

    def wrapper(klass):
        docstring = r"""{}

        """.format(
            header
        )
        if reduction is not None:
            docstring += r"""
Parameters
----------
            """
            docstring += docs_general.reduction_parameter(reduction)

        klass.__doc__ = docstring
        klass.forward.__doc__ = arguments() + docs_general.returned(reduction)
        return klass

    return wrapper

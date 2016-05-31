import numpy as np
from scipy import integrate
from scipy.stats import rv_continuous


class ContinuousFactor(rv_continuous):
    """
    Class for continuous node representation. This is a subclass of
    scipy.stats.rv_continuous.
    
    This allows representation of user defined continuous random variables
    by associating these continuous factors.
    It requires a function to compute the probability density function
    of the distribution.
    
    All methods of the scipy.stats.rv_continuous class can be used on
    the objects.
    This supports an extra method to discretize the continuous distribution
    into a discrete factor using various methods.
    
    """
    def __init__(self, pdf, lb=None, ub=None):
        """
        Parameters
        ----------
        pdf : function
        The user defined probability density function.

        lb : float, optional
        Lower bound of the support of the distribution, default is minus
        infinity.

        ub : float, optional
        Upper bound of the support of the distribution, default is plus
        infinity.

        Examples
        --------
        >>> from pgmpy.factors import ContinuousFactor
        >>> custom_pdf = lambda x : 0.5 if x > -1 and x < 1 else 0
        >>> node = ContinuousFactor(custom_pdf, -3, 3)
        """
        self.pdf = pdf
        super(ContinuousFactor, self).__init__(momtype=0, a=lb, b=ub)

    def _pdf(self, *args):
        """
        Defines the probability density function of the given
        continuous variable.
        """
        return self.pdf(*args)

    def discretize(self, method, *args, **kwargs):
        """
        Discretizes the continuous distribution into discrete
        probability masses using various methods.

        Parameters
        ----------
        method : A Discretizer Class from pgmpy.continuous.discretize

        *args, **kwargs:
            The parameters to be given to the Discretizer Class.

        Examples
        --------
        >>> from pgmpy.factors import ContinuousFactor
        >>> exp_pdf = lambda x: 2*np.exp(-2*x) if x>=0 else 0
        >>> exp_node = ContinuousFactor(exp_pdf)
        >>> from pgmpy.continuous.discretize import UnbiasedDiscretizer
        >>> exp_node.discretize(UnbiasedDiscretizer, exp_node, 0, 5, 10)
        [0.39627368905806137, 0.4049838434034298, 0.13331784003148325,
         0.043887287876647259, 0.014447413395300212, 0.0047559685431339703,
         0.0015656350182896128, 0.00051540201980112557, 0.00016965346326140994,
         3.7867260839208328e-05]

        (Refer the various Discretization methods, in pgmpy.continuous.discretize
         for details regarding the input parameters.)

        """
        from pgmpy.continuous.discretize import BaseDiscretizer

        if not issubclass(method, BaseDiscretizer):
            raise TypeError("{} must be Discretizer class.".format(method))

        return method(self, *args, **kwargs).get_discrete_values()

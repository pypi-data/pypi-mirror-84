from scipy.stats import moment
import math as math
import mgt2001.per as per


def outlier(data, base=per):
    """
    The default is set to per.percentile()

    Usages
    ------
    >>> df = whatever DataFrame you construct
    >>> per.outlier(df["column_name"], per) # to use per.percentile (textbook) to compute quartiles
    >>> per.outlier(df["column_name"], np) # to use np.percentile to compute quartiles

    Examples
    ------
    In HW04, 4.73, the results could be different:
    >>> per.outlier(df["Time_Public"].dropna(), np)
    Quartiles for playing on a public course:

    Q1 = 279.5
    Q2 = 296.0
    Q3 = 307.0
    IQR = 27.5

    Outliers are listed as follows:
    [238.0, 359.0]

    >>> per.outlier(df["Time_Public"].dropna()) # default = per
    Quartiles for playing on a public course:

    Q1 = 279.0
    Q2 = 296.0
    Q3 = 307.0
    IQR = 28.0

    Outliers are listed as follows:
    [359.0]

    """
    Q1 = base.percentile(data, 25)
    Q2 = base.percentile(data, 50)
    Q3 = base.percentile(data, 75)
    IQR = Q3 - Q1  # IQR is interquartile range.
    filter = (data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)
    if (len(data.loc[filter].to_list()) != 0):
        outlier_prompt = "Outliers are listed as follows:\n{}".format(
            data.loc[filter].to_list())
    else:
        outlier_prompt = "There are no outliers."

    description = """
Q1 = {}
Q2 = {}
Q3 = {}
IQR = {}

{}
    """.format(Q1, Q2, Q3, IQR, outlier_prompt)

    return description


def kurtosis(df):
    """
    How to read the kurtosis value?

    K > 3 : Leptokurtic (Narrow-tall)
    K = 3 : Mesokurtic (Regular)
    K < 3 : Platykurtic (Wide-low)
    -------
    To convert excel kurtosis to a real one, please consider the function "convert_excel_kurtosis(K, n)"

    """
    m2 = moment(df, moment=2)
    m4 = moment(df, moment=4)
    kurtosis_f = m4 / pow(m2, 2)
    return kurtosis_f


def convert_excel_kurtosis(K, n):
    """
    K is the kurtosis you get from Excel.

    The function will return (n-2) * (n-3) * K / ((n + 1) * (n - 1)) + 3 * (n - 1) / (n + 1).
    """
    if (n < 3):
        return None
    return (n-2) * (n-3) * K / ((n + 1) * (n - 1)) + 3 * (n - 1) / (n + 1)


def skew(df):
    """
    How to read skew value?

    g > 0 : Skewed to right
    g = 0 : Symmetric
    g < 0 : Skewed to left
    -------
    To convert excel skewness to a real one, please consider the function "convert_excel_skew(G, n)"
    """
    m2 = moment(df, moment=2)
    m3 = moment(df, moment=3)
    skew_f = m3 / pow(pow(m2, 0.5), 3)
    return skew_f


def convert_excel_skew(G, n):
    """
    G is the skewness you get from Excel.

    The function will return (n-2) * G / math.sqrt(n * (n - 1)).
    """
    if (n < 2):
        return None
    return (n-2) * G / math.sqrt(n * (n - 1))

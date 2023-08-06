import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import textwrap

from sklearn import metrics, linear_model, neighbors
import scipy.stats as st
import warnings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def summarise_ts(dfs):
    """Gets summary on timeseries
    
    :param dfs: MxN DataFrame with M = length of dataframe, N = number of columns
    :type dfs: pandas.DataFrame
    :return: Summary of time series characteristics
    :rtype: pandas.DataFrame
    """
    
    summaries = []
    
    for col_name in dfs.columns:
        df = dfs[[col_name]]
        
        start_date = df.dropna().index[0]
        end_date = df.dropna().index[-1]
        num_samples = len(df.dropna())
    
        summary = pd.DataFrame(
            data=[start_date, end_date, num_samples], 
            index=['Start Date', 'End Date', 'Num Samples'], 
            columns=df.columns)
        summaries.append(summary)

    return pd.concat(summaries, axis=1).T

def freq_name_to_abbr(freq_name):
    if freq_name == 'daily':
        return 'D'
    elif freq_name == 'weekly':
        return 'W'
    elif freq_name == 'monthly':
        return 'M'
    elif freq_name == 'quarterly':
        return 'Q'
    elif freq_name == 'annually' or freq_name =='yearly':
        return 'A'
    else:
        logger.warning(
            '`%s` is not a recognisable `freq_name`. Program will continue running but assumes %s is the frequency abbreviation.' % 
            (freq_name, freq_name)
        )
        return freq_name

def filter_ts(data, start_date=None, end_date=None, freq='B'):
    if not start_date:
        start_date = data.index[0]
    if not end_date:
        end_date = data.index[-1]
    data = data.loc[start_date:end_date]

    freq_abbr = freq_name_to_abbr(freq)
    return data.resample(freq_abbr).last()

def shade_chart(ax, bools, y_min=None, y_max=None, **kwargs):
    """Shade axis for positive areas

    :param ax: Axis to shade
    :type ax: matplotlib.axes.Axes
    :param bools: Time series for shading
    :type bools: pd.DataFrame
    :param y_min: Smallest y value to shade
    :type y_min: See `y1 arg <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.fill_between.html>`_
    :param y_max: Maximum y value to shade
    :type y_max: See `y2 arg <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.fill_between.html>`_
    :param kwargs: Other keyword arguments from `yyfill_between <https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.fill_between.html>`_
    """

    if y_min is None:
        y_min = ax.get_ylim()[0]
    
    if y_max is None:
        y_max = ax.get_ylim()[1]
        
    return ax.fill_between(x=bools.index, y1=y_min, y2=y_max, where=bools==1, **kwargs)

def plot_explained_var_ratio_curve(X, ax=None):
    """Plots cumulative explained variance ratio vs components"""

    num_cols = len(X.columns)
    pca = PCA(num_cols)
    pca.fit(X.values)
    var_ratio_df = pd.DataFrame(data=pca.explained_variance_ratio_, 
                                index=range(1, num_cols + 1), 
                                columns=['Explained Variance Ratio'])
    var_ratio_df['Cum. Explained Variance Ratio'] = var_ratio_df['Explained Variance Ratio'].cumsum()
    ax = var_ratio_df['Cum. Explained Variance Ratio'].plot(ax=ax, title='Cum. Explained Variance Ratio')
    ax.set_xlabel('Num. of components')
    ax.set_ylabel('Explained Variance Ratio')
    return ax

def _determine_ts_freq(ts):
    # Compute the average days diff between each sample
    dates_diff = ts.index[1:] - ts.index[:-1]
    days_diff = [
        date_diff / np.timedelta64(1, 'D') for date_diff in dates_diff
    ]
    days_diff_mean = round(np.mean(days_diff))

    # Match the above computation to the most likely days diff
    recognised_days_diffs = [
        1,         # day
        7,         # week
        21, 30,    # month
        63, 92,    # quarter
        126, 183,  # semi-annual
        252, 365   # year
    ]
    diff_betw_mean_and_recognised_days_diffs = [
        abs(recognised_duration - days_diff_mean) for recognised_duration in recognised_days_diffs
    ]
    smallest_diff_betw_mean_and_recognised_days_diffs = min(diff_betw_mean_and_recognised_days_diffs)
    smallest_diff_pos = diff_betw_mean_and_recognised_days_diffs.index(smallest_diff_betw_mean_and_recognised_days_diffs)
    likely_days_diff = recognised_days_diffs[smallest_diff_pos]

    # Match to most likely days diff to the most likely freq 
    recognised_freqs = [
        'B',
        'W',
        'BM', 'M',
        'BQ', 'Q',
        'BSA', 'SA',
        'BA', 'A'
    ]
    likely_freq = recognised_freqs[smallest_diff_pos]

    return likely_freq

def _pct_change(ts, window, transformation_name):
    if isinstance(ts, pd.DataFrame):
        _ts = ts.pct_change(window)
        _ts.columns = ['%s(%s)' % (transformation_name, col) for col in ts.columns]
    elif isinstance(ts, pd.Series):
        _ts = ts.pct_change(window)
    else:
        raise NotImplementedError('Cannot perform %s transformation on type `%s`.' % (transformation_name, type(ts)))

    return _ts

def WoW(ts):
    transformation_name = 'WoW'
    likely_freq = _determine_ts_freq(ts)

    if likely_freq == 'B':
        return _pct_change(ts, 5, transformation_name)
    elif likely_freq == 'W':
        return _pct_change(ts, 1, transformation_name)
    else:
        raise ValueError('Cannot perform %s transformation on data with frequency %s.' % (transformation_name, likely_freq))

def MoM(ts):
    transformation_name = 'MoM'
    likely_freq = _determine_ts_freq(ts)

    if likely_freq == 'B':
        return _pct_change(ts, 21, transformation_name)
    elif likely_freq == 'W':
        return _pct_change(ts, 4, transformation_name)
    elif likely_freq == 'M' or likely_freq == 'BM':
        return _pct_change(ts, 1, transformation_name)
    else:
        raise ValueError('Cannot perform %s transformation on data with frequency %s.' % (transformation_name, likely_freq))

def QoQ(ts):
    transformation_name = 'QoQ'
    likely_freq = _determine_ts_freq(ts)

    if likely_freq == 'B':
        return _pct_change(ts, 63, transformation_name)
    elif likely_freq == 'W':
        return _pct_change(ts, 13, transformation_name)
    elif likely_freq == 'M' or likely_freq == 'BM':
        return _pct_change(ts, 3, transformation_name)
    elif likely_freq == 'Q' or likely_freq == 'BQ':
        return _pct_change(ts, 1, transformation_name)
    else:
        raise ValueError('Cannot perform %s transformation on data with frequency %s.' % (transformation_name, likely_freq))

def SAoSA(ts):
    transformation_name = 'SAoSA'
    likely_freq = _determine_ts_freq(ts)

    if likely_freq == 'B':
        return _pct_change(ts, 126, transformation_name)
    elif likely_freq == 'W':
        return _pct_change(ts, 26, transformation_name)
    elif likely_freq == 'M' or likely_freq == 'BM':
        return _pct_change(ts, 6, transformation_name)
    elif likely_freq == 'Q' or likely_freq == 'BQ':
        return _pct_change(ts, 2, transformation_name)
    elif likely_freq == 'SA' or likely_freq == 'BSA':
        return _pct_change(ts, 1, transformation_name)
    else:
        raise ValueError('Cannot perform %s transformation on data with frequency %s.' % (transformation_name, likely_freq))

def YoY(ts):
    transformation_name = 'YoY'
    likely_freq = _determine_ts_freq(ts)

    if likely_freq == 'B':
        return _pct_change(ts, 252, transformation_name)
    elif likely_freq == 'W':
        return _pct_change(ts, 52, transformation_name)
    elif likely_freq == 'M' or likely_freq == 'BM':
        return _pct_change(ts, 12, transformation_name)
    elif likely_freq == 'Q' or likely_freq == 'BQ':
        return _pct_change(ts, 4, transformation_name)
    elif likely_freq == 'SA' or likely_freq == 'BSA':
        return _pct_change(ts, 2, transformation_name)
    elif likely_freq == 'A' or likely_freq == 'BA':
        return _pct_change(ts, 1, transformation_name)
    else:
        raise ValueError('Cannot perform %s transformation on data with frequency %s.' % (transformation_name, likely_freq))

def run_linear_regression(X_train, y_train, X_test, y_test, scoring='mse', return_axes=False):
    """Runs a linear regression on a separated dataset, and plots the results

    :param X_train:
    :type X_train:
    :param y_train:
    :type y_train:
    :param X_test:
    :type X_test:
    :param y_test:
    :type y_test:
    :param scoring:
    :type scoring:
    :param return_axes:
    :type return_axes:
    """

    model = LinearRegression()
    model.fit(X_train.values, y_train.values)

    # Run train preds
    train_preds = pd.DataFrame(data=model.predict(X_train.values), index=X_train.index, columns=['Train Preds'])
    train_errors = (y_train.iloc[:, 0] / train_preds['Train Preds'] - 1).to_frame('Train Errors')
    # Run test preds
    test_preds = pd.DataFrame(data=model.predict(X_test.values), index=X_test.index, columns=['Test Preds'])
    test_errors = (y_test.iloc[:, 0] / test_preds['Test Preds'] - 1).to_frame('Test Errors')

    fig, axes = plt.subplots(1, 2, figsize=(18, 4))

    # 1st plot
    title_1st_line = 'Predictions vs Actual'
    title_2nd_line = ''
    for feature_name, coef in zip(X_train.columns, model.coef_[0]):
        title_2nd_line += '%f %s + ' % (coef, feature_name)
    title_2nd_line = title_2nd_line.rstrip(' + ')
    title_2nd_line = '\n'.join(textwrap.wrap(title_2nd_line, width=70))
    title = '%s\n%s' % (title_1st_line, title_2nd_line)

    _ = train_preds.plot(ax=axes[0])
    _ = test_preds.plot(ax=axes[0])
    _ = (y_train.iloc[:, 0].append(y_test.iloc[:, 0])).to_frame('Actual').plot(ax=axes[0], title=title)
    # 2nd plot
    if scoring == 'mse':
        train_opt_error = mean_squared_error(y_train.values, train_preds.values)
        test_opt_error = mean_squared_error(y_test.values, test_preds.values)
    elif scoring == 'mae':
        train_opt_error = mean_absolute_error(y_train.values, train_preds.values)
        test_opt_error = mean_absolute_error(y_test.values, test_preds.values)
    else:
        raise ValueError('The scoring `%s` is not recognised.' % scoring)

    train_error_mean, train_error_std, train_error_skew, train_error_kurt = \
        train_errors.mean().item(), train_errors.std().item(), train_errors.skew().item(), train_errors.kurtosis().item()
    test_error_mean, test_error_std, test_error_skew, test_error_kurt = \
        test_errors.mean().item(), test_errors.std().item(), test_errors.skew().item(), test_errors.kurtosis().item()

    title_1st_line = 'Errors(Pct)'
    title_2nd_line = 'Train: %s = %.2f, Moments = (%.2f, %.2f, %.2f, %.2f)' % \
        (scoring.upper(), train_opt_error, train_error_mean, train_error_std, train_error_skew, train_error_kurt)
    title_3rd_line = 'Test: %s = %.2f, Moments = (%.2f, %.2f, %.2f, %.2f)' % \
        (scoring.upper(), test_opt_error, test_error_mean, test_error_std, test_error_skew, test_error_kurt)
    title = '%s\n%s\n%s' % (title_1st_line, title_2nd_line, title_3rd_line)

    _ = train_errors.plot(ax=axes[1])
    _ = test_errors.plot(ax=axes[1], title=title)

    if return_axes:
        return model, axes
    else:
        return model

def choose_dists(dist_type):
    """Chooses a group of distributions to test against depending on chosen category"""

    if dist_type == 'all':
        return [        
            st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
            st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
            st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
            st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
            st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
            st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
            st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
            st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
            st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
            st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
        ]
    elif dist_type == 'std':
        return [
            st.expon, st.genextreme, st.gumbel_r, st.gumbel_l, st.logistic, st.lognorm, st.norm, st.pareto, st.t, st.uniform 
        ]
    else:
        raise NotImplementedError('Does not recognise this category of distributions')

def get_frozen_dist(dist, params):
    """Gets a frozen distribution
    
    :param dist_name: Distribution to freeze
    :type dist_name: scipy.stats.<rv_continuous>
    :params params: Parameters required for initializing distribution
    :type params: tuple
    :returns: Frozen distribution
    :rtype: scipy.stats.<rv_frozen>
    """

    # Extract params
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    # Prepare distribution
    return dist(*arg, loc=loc, scale=scale)

def _best_fit_dist(data, dists=None, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""

    # Get defaults
    if dists is None:
        dists = choose_dists('std')
    
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    # Initialize best holders
    best_dist = st.norm
    best_params = (0.0, 1.0)
    best_mse = np.inf

    # Estimate distribution parameters from data
    for dist in dists:
        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                # fit dist to data
                params = dist.fit(data)
                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
                # Calculate fitted PDF and error with fit in distribution
                pdf = dist.pdf(x, loc=loc, scale=scale, *arg)
                mse = mean_squared_error(y_true=y, y_pred=pdf)
                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                except Exception:
                    pass
                # identify if this distribution is better
                if best_mse > mse > 0:
                    best_dist = dist
                    best_params = params
                    best_mse = mse
        except Exception:
            pass

    return best_dist.name, best_params

def make_dist_pdf(dist, size=10000):
    """Generate distribution's probability distribution function
    
    :param dist: Freezed distrubition
    :type dist: Distribution in scipy.stats
    :param size: Number of values to use for histogram X values
    :type size: int
    :returns: Probability distribution function with 
    :rtype: pd.Series
    """

    # Get sane start and end points of distribution
    start = dist.ppf(0.01)
    end = dist.ppf(0.99)
    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x)
    pdf = pd.Series(y, x)

    return pdf

def best_fit_dist(data, dists=None, bins=200):
    """Find the best fit distribution
    
    ..example::
        dists = distribution.choose_dist('usual')

        title = 'SPY Rets'
        ylabel = 'Density'
        xlabel = 'Rets'

        best_pdf = distribution.best_fit_dist(
            data=spy['Rets'].dropna(), dist_names=dists)
    
    :param data: Data to find best fit distribution of
    :type data: pd.Series
    :param dist_names: Distributions to choose from. If None, 
    :type dist_names: List of scipy.stats._cont_dists, optional
    :param bins: Number of bins for data histogram
    :type bins: int, optional
    :return: Probability distribution function
    :rtype: pd.Series
    """

    best_dist_name, best_fit_params = _best_fit_dist(data, dists, bins)
    best_dist_cls = getattr(st, best_dist_name)
    best_dist = get_frozen_dist(best_dist_cls, best_fit_params)
    return best_dist   

def plot_best_fit_dist(data, dists=None, bins=200, title='', xlabel='', ylabel=''):
    """Find the best fit distribution and plot it
    
    ..example::
        dists = distribution.choose_dist('usual')

        title = 'SPY Rets'
        ylabel = 'Density'
        xlabel = 'Rets'

        best_pdf = distribution.plot_best_fit_dist(
            data=spy['Rets'].dropna(), dist_names=dists, title=title, xlabel=xlabel, ylabel=ylabel)
    
    :param data: Data to find best fit distribution of
    :type data: pd.Series
    :param dist_names: Distributions to choose from. If None, 
    :type dist_names: List of scipy.stats._cont_dists, optional
    :param bins: Number of bins for data histogram
    :type bins: int, optional
    :param title: Main title for charts
    :type title: str, optional
    :param xlabel: X-axis label for both charts
    :type xlabel: str, optional
    :param ylabel: Y-axis label for both charts
    :type ylabel: str, optional
    :return: Probability distribution function
    :rtype: pd.Series
    """

    # Plot for comparison
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    ax0 = data.plot(ax=axes[0], kind='hist', bins=50, density=True, alpha=0.5)
    # Save plot limits
    dataYLim = ax0.get_ylim()
    # Find best fit distribution
    best_dist_name, best_fit_params = _best_fit_dist(data, dists, bins, ax0)
    best_dist_cls = getattr(st, best_dist_name)
    best_dist = get_frozen_dist(best_dist_cls, best_fit_params)
    # Update plots
    ax0.set_ylim(dataYLim)
    ax0.set_title(title + '\n All Fitted Distributions')
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel(ylabel)

    # Make PDF with best params 
    pdf = make_dist_pdf(best_dist)
    # Display
    ax1 = pdf.plot(ax=axes[1], lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=50, density=True, alpha=0.5, label='Data', legend=True, ax=ax1)
    # Make suffix for plot title to display distribution params
    param_names = (best_dist_cls.shapes + ', loc, scale').split(', ') if best_dist_cls.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
    dist_str = '{}({})'.format(best_dist_cls.name, param_str)
    # Update plots
    ax1.set_title(title + ' with best fit distribution \n' + dist_str)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    return best_dist

def choose_kernels():
    return ['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']

def best_fit_kernel(data, kernels=None, bins=200, ax=None, **kwargs):
    """
    Fit kernel to a series of observations, and derive the probability of observation

    :param data: Observations to fit kernel to
    :type data: numpy.ndarray
    :param kwargs: Keyword arguments used to init KernelDensity class as labelled in 'sklearn <https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KernelDensity.html#sklearn.neighbors.KernelDensity>_`, except for kernel
    :type kwargs: dict
    :return: Best kernel density estimator
    :rtype: sklearn.neighbors.KernelDensity
    """

    # Change to 2d if it is 1d
    if len(data.shape) == 1:
        data = data.reshape(-1, 1)
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    # Initialize best holders
    best_kde = None
    best_kde_name = None
    best_mse = np.inf
    
    # Iterate over each kernel available
    for kernel in kernels:
        # Fit kernel density estimator
        kde = KernelDensity(kernel=kernel, **kwargs).fit(data)
        # Compute density
        log_dens = kde.score_samples(x.reshape((-1, 1)))
        pdf = np.exp(log_dens)
        # Compute error with fit in distribution
        mse = mean_squared_error(y_true=y, y_pred=pdf)
        # If axis is available, pass in to plot
        try:
            if ax:
                pd.Series(pdf, x).plot(ax=ax)
        except Exception:
            pass
        # Identify if this distribution is better
        if best_mse > mse > 0:
            best_kde = kde
            best_kde_name = kernel
            best_mse = mse

    return best_kde, best_kde_name

def make_kernel_pdf(kde, x):
    """Generate distribution's probability distribution function
    
    :param kde: Fitted kernel density estimator
    :type kde: sklearn.neighbors.KernelDensity
    :param x: Values to score density
    :type x: numpy.ndarray
    :returns: Probability distribution function with 
    :rtype: pd.Series
    """

    # Change to 2d if it is 1d
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    # Score density
    log_dens = kde.score_samples(x)
    pdf = pd.Series(data=np.exp(log_dens), index=x.flatten()).sort_index()

    return pdf

def plot_best_fit_kernel(data, kernels=None, bins=200, title='', xlabel='', ylabel='', **kwargs):
    """Find the best fit kernel and plot it
    
    :param data: Data to find best fit kernel of
    :type data: pd.Series
    :param kernels: Kernels to choose from. If None, 
    :type kernels: List of strings, optional
    :param bins: Number of bins for data histogram
    :type bins: int, optional
    :param title: Main title for charts
    :type title: str, optional
    :param xlabel: X-axis label for both charts
    :type xlabel: str, optional
    :param ylabel: Y-axis label for both charts
    :type ylabel: str, optional
    :return: Probability distribution function
    :rtype: pd.Series
    """

    # Plot for comparison
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    ax0 = data.plot(ax=axes[0], kind='hist', bins=50, density=True, alpha=0.5)
    # Save plot limits
    dataYLim = ax0.get_ylim()
    # Find best fit distribution
    best_kde, best_kde_name = best_fit_kernel(data.values, kernels, bins, ax0, **kwargs)
    # Update plots
    ax0.set_ylim(dataYLim)
    ax0.set_title(title + '\n All Fitted Kernels')
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel(ylabel)

    # Make PDF with best params 
    pdf = make_kernel_pdf(best_kde, data.values)
    # Display
    ax1 = pdf.plot(ax=axes[1], lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=50, density=True, alpha=0.5, label='Data', legend=True, ax=ax1)
    # Update plots
    ax1.set_title(title + '\nBest fit kernel = %s' + best_kde_name)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    return best_kde

def monte_carlo(pdf, pdf_type, num_periods, num_paths=500):
    """Monte Carlo simulations with probability distribution function
    
    :param pdf: Probability distribution function
    :type pdf:
    :param pdf_type: The type of probability distribution function being used
    :type pdf_type: str
    :param num_periods: Number of timestamps to simulate in a single path
    :type num_periods: int
    :param num_paths: Number of Monte Carlo simulations
    :type num_paths: int, optional
    """
    
    if pdf_type == 'dist':
        paths = tuple([pdf.rvs(size=num_periods).reshape((-1, 1)) for _ in range(num_paths)])
    elif pdf_type == 'kernel':
        paths = tuple([pdf.sample(n_samples=num_periods).reshape((-1, 1)) for _ in range(num_paths)])
    else:
        raise NotImplementedError

    return np.concatenate(paths, axis=1)

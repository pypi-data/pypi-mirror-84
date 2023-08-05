import time
from functools import wraps

from IPython import get_ipython
from IPython.display import display
from ipywidgets import HTML, IntProgress, VBox
from tqdm import tqdm as _tqdm

from pymove.utils.datetime import deltatime_str


def timer_decorator(func):
    """A decorator that prints how long a function took to run."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_total = deltatime_str(time.time() - t_start)
        message = '%s took %s' % (func.__name__, t_total)
        print('*' * len(message))
        print(message)
        print('*' * len(message))
        return result

    return wrapper


def _log_progress(sequence, desc=None, total=None, miniters=None):
    """
    Make and display a progress bar.

    Parameters
    ----------
    sequence : list or iterable.
        Represents a sequence of elements.
    desc : String, optional, default None.
        Represents the description of the operation.
    total : int, optional, default None.
        Represents the total/number elements in sequence.
    miniters : int, optional, default None.
        Represents the steps in which the bar will be updated

    """
    if desc is None:
        desc = ''
    is_iterator = False
    if total is None:
        try:
            total = len(sequence)
        except TypeError:
            is_iterator = True
    if total is not None:
        if miniters is None:
            if total <= 200:
                miniters = 1
            else:
                miniters = int(total / 200)
    else:
        if miniters is None:
            miniters = 1

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=total, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % miniters == 0:
                if is_iterator:
                    label.value = '%s: %s / ?' % (desc, index)
                else:
                    progress.value = index
                    label.value = u'%s: %s / %s' % (desc, index, total)
            yield record
    except Exception:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = '%s: %s' % (desc, str(index or '?'))


try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        progress_bar = _log_progress
    else:
        raise NameError
except NameError:
    progress_bar = _tqdm

====================
DataStax Tech Review
====================

***************
Installation
***************

To install the DataStax metric collector, first you must install ``python-tk``::

    epeters:~$ sudo apt-get install -y python-tk

It is suggested that you use a python virtual environment to install the remaining python packages (I tend to use virtualenvwrapper - more on that `here <https://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_
)::

    epeters:~$ cd delivery
    epeters:~/delivery$ mkvirtualenv datastax
    (@datastax) epeters:~/delivery$ pip install -r requirements
    (@datastax) epeters:~/delivery$ pip install .

After installation, there will be an executable named ``ds-metrics`` on the path.

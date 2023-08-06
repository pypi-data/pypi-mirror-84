pytest-tipsi-testing
====================

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

pytest-tipsi-testing is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 3.5+.

.. code-block:: bash

    $ pip install pytest-tipsi-testing

License
-------

pytest-tipsi-testing is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.


Motivation and features
-----------------------

We want to make fixtures more predictable in pytest. So this plugin ensures that only loaded fixtures will be available when test is running.

Currently pytest allows fixtures with bigger scopes (session, module and etc.) to be instantiated even if test doesn't directly require them. This may cause some troubles in several cases, for example if you wan't to create some kind of cache in bigger fixture.

This means that all not required fixtures will be finished before test is started: even with bigger scope. So if you want to have some fixtures always awailable (eg. docker_start fixture with session scope) - you should make it autoused.


Also we're forcing correct order for fixtures with different scopes: session -> module -> class -> function.


Usecase
^^^^^^^

In conjunction with `pytest-tipsi-django <https://github.com/tipsi/pytest-tipsi-django>`_ you can make fixtures on different level than scope and share the same database state across different tests. It's quit helpful when you perform complex and long database setup and want to have small and readable test cases.

Please see ``pytest-tipsi-django`` documentation for more detailed description.


Fixtures
--------

vprint
^^^^^^

Print that works only when verbose mode is enabled ``-v``.

*Note*: you should add ``-s`` to see the output.


log_requests
^^^^^^^^^^^^

Use it when you want to write down all request/responses made with `requests <http://docs.python-requests.org/en/master/>`_ library. By default it will put docs into ``.doc`` dir or other directory supplied by ``DOCS_ROOT`` environmental variable.

.. code-block:: python

  def example(log_requests):
    import requests
    with log_request('out_file'):
      r = requests.get('http://echo.jsontest.com/key/value/one/two')
      assert r.status_code == 200, r


It will put json file into your ``.doc/{MODULE_PATH}.out_file.json``, in my case it was a ``.doc/tests.test_log_requests.out.json`` your case may be different depending on module you have used it in.

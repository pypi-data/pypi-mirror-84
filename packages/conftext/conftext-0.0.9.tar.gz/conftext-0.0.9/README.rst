========
conftext
========
This package contains a couple of mudules:

* conftext - a helper for managing configuration contexts.
* conf_ini - unified configuration handling for ini files.


conftext
========

Motivation
----------
Imagine handling multi-tenant services, that each require certain config contexts to be specified
for using them (think db connection information for instance). A "configuration matrix" if you like.
The parameters of these config options are the same, but their values differ. You are creating CLI
tools for working with these services and find yourself doing:

.. code-block:: shell

   $ some_task1(db_host=service_A_ip, db_name=service_A_name, param1, param2)
   $ some_task2(db_host=service_A_ip, db_name=service_A_name)
   $ some_task3(db_host=service_A_ip, db_name=service_A_name, param1)
   
   $ some_task1(db_host=service_B_ip, db_name=service_B_name, param1, param2)
   $ some_task2(db_host=service_B_ip, db_name=service_B_name)
   $ some_task3(db_host=service_B_ip, db_name=service_B_name, param1)

This small library intends to help bring things back to:

.. code-block:: shell

   $ some_task1(param1, param2)
   $ some_task2()
   $ some_task3(param1)

This is just an example. The tool is meant to be generic and is not nescessarily only made for this
particular use case.

Operation
---------
This tool works by providing a way to persist configuration coordinates that can be used to look up
the appropriate configuration in the "configuarion matrix". The configuration coordinates are stored
in a file at well-known location (look at current dir, then traverse upwards in file hierarchy until
`/` or `~/.config/conftext.ini`).

A command-line tool, also called conftext, can be used to show and manipulate the conftext file.

Usage
-----
Use `get_config` in code where context-aware config should be loaded. The conftext invoke task can
then be used to switch the context config.

Example in code:

.. code-block:: python

   defaults = dict(
       service='dummy',
       context='local')
   
   config = Conftext(section='package.module', default_config=defaults)

Command-line usage:

.. code-block:: shell

   $ conftext show
   $ conftext set --service <someservice>
   $ conftext set --service <someservice> --context <somecontext>

Ideas
-----
* add a enter task for the CLI tool that will enter the conf context?
   - when inside conf context, consider modifying the prompt to show vital context config
   - add exit task as well
* add python prompt with config context as well?


conf_ini
========

Provides unified configuarion for ini files.

Currently, this means that the configuration for a given package/module is expected to be found in::

    ~/.config/<package>/<module>.ini

and that the file is expected to in a `.ini` format that can be parsed by the configparser of the
python standard library.

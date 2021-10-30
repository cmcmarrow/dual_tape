##################
dual tape - v1.0.0
##################

*****
About
*****
This python module "dual_tape" is an `Esolang <https://esolangs.org/wiki/Main_Page>`_.

*******************
Python Installation
*******************
.. code-block:: bash

   pip install dual_tape

*****************
Console Interface
*****************
.. code-block:: bash

   dual_tape hello_world.dt

.. code-block:: text

   dual_tape

   positional arguments:
     file           path to dual_tape script

   optional arguments:
     -h, --help     show this help message and exit
     -a, --author   get author of dual_tape
     -v, --version  get version of dual_tape
     -l, --log      enables debug log
     --timeout TIMEOUT  max number of instructions that can run

*************
Documentation
*************
* `Documentation <https://esolangs.org/wiki/dual_tape>`_
* `Raw Documentation <https://github.com/cmcmarrow/dual_tape/blob/master/DOCUMENTATION.txt>`_

****************
Build Executable
****************
.. code-block:: bash

   git clone https://github.com/cmcmarrow/dual_tape.git
   pip install -e .[dev]
   python build.py

***
API
***
``dual_tape_api.py``

.. code-block:: text

   info: API to dual_tape
   :param: inputs: Optional[Union[Tuple[str, ...], List[str]]]
   :param: sys_output: bool
   :param: catch_output: bool
   :param: log: bool
   :return: Generator[vm.VMState, None, None]

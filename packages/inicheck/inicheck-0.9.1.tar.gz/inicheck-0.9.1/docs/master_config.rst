.. _MasterConfig:

=========================
Master Configuration File
=========================

Basic Entry
-----------
To accurately check files, every entry and section must be provided in the
master configuration file. Every entry must belong to a section. However, if an
option is not registered (in the master config), inicheck will simply produce a
warning to alert the user.

Consider the following entry for a configuration file:

.. code-block:: ini

  [time]

  time_step:
            default = 60,
            type = int,
            description = Time interval that SMRF distributes data at in minutes

The example above specifies that the section **time** has an entry **time_step**
with a default of 60 and should always be an integer. The end outcome is
that inicheck requires all provided options for time_step are integers. If the
user didn't provide it, inicheck will add the default.

The attributes describing/constraining an entry are:

  * default - the default value to use for this entry when not provided
  * type - the type the value should be casted into, if it is not castable, then throw an error
  * options - a list of options that the entry value must be in.
  * description- a description of the entry to be used for documentation and self help
  * max - A Maximum value used for checking if a numeric input is under it.
  * min - A minimum value used for checking if a numeric input is over it.
  * allow_none - A Bool to check if None is an acceptable input

While these are the available attributes they are not required but always exist for each entry. If
it is not provided in the master configuration file the following defaults are used.

  * default - None
  * type - str
  * options - None
  * description- ''
  * max - None
  * min - None
  * allow_none - True

if your options are set to none then inicheck assumes the entry can be
unconstrained e.g. filenames are a great example where a user would not want a
set list of available options.

Available Types
---------------

Each entry in the master config file can provide a type. If no type is provided,
then the default is type string.

Available types:

  * Bool - :class:`~inicheck.checkers.CheckBool`
  * String - :class:`~inicheck.checkers.CheckString`
  * Float - :class:`~inicheck.checkers.CheckFloat`
  * Integer - :class:`~inicheck.checkers.CheckInt`
  * Datetime - :class:`~inicheck.checkers.CheckDatetime`
  * Ordered datetime pair - :class:`~inicheck.checkers.CheckDatetimeOrderedPair`
  * Filename - :class:`~inicheck.checkers.CheckFilename`
  * CriticalFilename - :class:`~inicheck.checkers.CheckCriticalFilename`
  * Discretionary Critical Filename - :class:`~inicheck.checkers.CheckDiscretionaryCriticalFilename`
  * Directory - :class:`~inicheck.checkers.CheckDirectory`
  * CriticalDirectory - :class:`~inicheck.checkers.CheckCriticalDirectory`

The following example required the users input to be a string, and must match
nearest, linear, or cubic.

.. code-block:: ini

    [interpolation]
      method:
            default = linear,
            options = [nearest linear cubic],
            description = interpolation method to use for this variable

Notes on Types
^^^^^^^^^^^^^^

Paths
+++++

All paths (filenames and directories) in inicheck are
assumed to be either relative to the config file or absolute. e.g.

.. code-block:: ini

  [path_management]
    log:
          default = ../log.txt,
          type = filename,
          description = path to log file

This will default to a path up one directory from the location of the config.

Any path options with critical prepended just means that inicheck will throw
an error instead of a warning.

Lists
+++++

Listed input checking can be performed. To assign a type
as a list, simply add the keyword list to the type name. This will force the
output to be a list and still check every entry in a provided list. To provide
a list in inicheck master configs use bracketed space separated lists. An
example of adding the list keyword and a list default is below

.. code-block:: ini

  [financial_plots]
    quarterly_dates:
          default = [01-01 04-01 07-01 10-01] ,
          type = datetimelist
          description = List of datetimes to plot up for earnings


Dates
+++++

All datetime types will be checked by the |dateparser_link| library, whether
the given string can be converted into a valid datetime object. All dates
given are assumed to be in UTC timezone. Dates can be given in any combination
that the library supports.

Care must be taken when there is a timezone given.
For instance:

.. code-block::

  2020-01-01 00:00 MST

will be parsed using the UTC timezone and results in

.. code-block::

  2020-01-01 07:00

The returned datetime object will be timezone unaware.

.. |dateparser_link| raw:: html

  <a href="https://dateparser.readthedocs.io/en/latest/" target="_blank">
    dateparser
  </a>

Recipes
--------
The master config can have recipes to generate certain adding or removing of
entries in the users configuration file automatically.This can really help with
config file bloat on the users end by only entering the information that matters
to them. The the information that matters to the software can be added later by
use of recipes.

Recipes are entered like sections **but** they must have the keyword **recipe** in
the section name. Each recipe is composed of triggers and edits.

Recipe Triggers
^^^^^^^^^^^^^^^

A trigger describes the conditions for which you want to apply the edits to a
configuration file. So you can think of a trigger as a conditional statement.
Every trigger is distinguished from edits by having **trigger** in its entry
name. This is required for inicheck to see the triggers!

Triggers can be defined using keywords and to create complex scenarios you can
add more keywords. Recipe triggers have only a couple key words available:

* **has_section** - if the configuration file has this section
* **has_item** -  It is provded using a bracketed, **space delimited** list in
  section > item order
* **has_value** - This is the most flexible trigger provided. It is provded
  using a bracketed, **space delimited** list in section > item > value order.

Below is an example showing how a trigger can have multiple criteria that can
create very specific conditions. Trigger entries can be provided in a comma
separated fashion indicating that the conditions are compounded such that the
recipe is applied only if all the entries are true. This allows developers to
create highly specific scenarios to apply changes to a users configuration file.

.. code-block:: ini

  [my_specific_recipe]
         specific_trigger:  has_value = [cool_section cool_item],
                            has_section = test_section,
                            has_value = [super_section awesome_item crazy_value]

If a developer wants more broad conditions to apply changes this can be
accomplished by providing another trigger which will be apply a recipe if
either trigger is true.

.. code-block:: ini

  [my_specific_recipe]
         trigger_1:         has_value = [cool_section cool_item]
         trigger_2:         has_section = test_section
         trigger_3:         has_value = [super_section awesome_item crazy_value]

**Summary**:

* Triggers need to have the word trigger in its name
* Triggers can compounded by using comma separated values (like an AND statement)
* Triggers can be broadened by using multiple triggers (like an OR statement)

Recipe Edits
^^^^^^^^^^^^

Recipe edits are simply anything in the recipe thats not a trigger and are the
edits that will be made to the users configuration file if the recipe is
triggered. If a keyword is not used then values are treated like section > item
> value and assigned to the users configuration file.

Edits can be prescribed by section and item names under a recipe:

.. code-block:: ini

  [my_recipe]
    some_trigger:   has_section = test_section

    test_section:
      module = module_name

The example above will assign the value **module_name** to the item **module** in the
users section **test_section** if the configuration file has the section **test_section**

To simplify some entries there are a couple keywords available to reduce repeated
actions. Available keywords for entries are:

* **apply_defaults** - apply the defaults set in the section
* **remove_item** - remove an item in this section
* **remove_section** - remove an section in this section
* **default_item** - Applies defaults to all the items provided in a space
                     delimited list


.. code-block:: ini

  [topo_ipw_recipe]
  trigger_type:       has_value = [topo type ipw]

  topo:               type = ipw,
                      apply_defaults = [dem mask],
                      remove_item = filename

Using the entryword default
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Any item can have the value default given to it which triggers inicheck to look
for the default value specified in the master config file and apply during the
application of a recipe.

Using the entryword ANY
^^^^^^^^^^^^^^^^^^^^^^^
To provide a little more flexibility and again avoid repeated entries, a developer
can use the keyword any to capture more generic scenarios. This can be particularly
useful when an item is repeated in multiple sections and the developer wants to
have the same behavior.

Consider the following configuration file:

.. literalinclude:: ../examples/any/config.ini

Let's say in the above example we want to have **dk_threads** everytime a
section has **distribution: dk**. So in the master configuration file we can add
a recipe that uses the **any**  keyword to use the same recipe for everytime this
happens.

.. literalinclude:: ../examples/any/master.ini


Recipe Example and Breakdown
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following example shows a recipe:

.. code-block:: ini

  [csv_recipe]
  test_trigger:      has_section = csv
  csv:          apply_defaults= true
  mysql:        remove_section = true
  gridded:      remove_section = true

1. The section name here is identified as a recipe by having the recipe in the name.
2. The trigger is identified by having a name with the word trigger in it and is
   triggered when the user's configuration file has a the section csv.
3. If the test_trigger condition is met then all the defaults will be applied to
   the csv section in the user's configuration file because of the keyword
   **apply_defaults**
4. If the users config file contains the sections **mysql** and or **gridded** then
   they will be removed due to the keywords **remove_section**

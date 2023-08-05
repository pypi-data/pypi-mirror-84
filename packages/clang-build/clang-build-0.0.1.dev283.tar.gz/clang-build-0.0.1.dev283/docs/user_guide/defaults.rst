Defaults
==============================================


General
----------------------------------------------

By default:

- all relative paths in a toml are interpreted as relative to that toml file
- if only one target is built from source, it is built into `build/<build_type>`
- if more than one target is built from source, they are built into `build/<target_name>/<build_type>`
- an external target's sources will be copied/downloaded into `build/<target_name>/external_sources`
- targets for which sources are found will be built as `executable`
- targets for which no sources are found will be `header-only`


Search Paths
----------------------------------------------

**Include directories**

  Default system directories for `#include`-searches are given by Clang.

  `clang-build`'s include directories will be added to the search paths and will be searched
  for header files for a target.
  In your project file, you can add an `include_directories` array to specify a target's header directories,
  where by default `clang-build` will try the target's root directory and an "include" subdirectory.

**Source directories**

  `clang-build`'s source directories will be searched for source files for a target.
  In your project file, you can add a `sources` array of patterns to specify a target's sources,
  where by default `clang-build` will try the target's root directory and a "src" subdirectory.


Build Type and Flags
----------------------------------------------

For ".cpp" files, the newest available C++ standard will be used by automatically adding e.g. `-std=c++17`.

The `default` build type contains the flags, which are used in all build configurations,
i.e. the minimum set of flags which `clang-build` enforces.

:`default`:        contains `-Wall -Wextra -Wpedantic -Werror`
:`release`:        adds `-O3 -DNDEBUG`
:`relwithdebinfo`: adds `-O3 -g3 -DNDEBUG`
:`debug`:          adds `-O0 -g3 -DDEBUG`
:`coverage`:       adds debug flags and `--coverage -fno-inline`

By activating all warnings and turning them into errors, the default flags ensure that unrecommended
code needs to be explicitly allowed by the author.


Build Directories
----------------------------------------------

.. code-block:: text

  build
  ├── myproject
  |   ├── targetname
  |   |   ├── external_sources
  |   |   ├── release
  |   |   |   ├── obj
  |   |   |   ├── dep
  |   |   |   ├── bin
  |   |   |   ├── lib
  |   |   |   └── include
  |   |   ├── debug
  |   |   | └── ...
  |   |   ├── default
  |   |   | └── ...
  |   |   └── ...
  |   └── othertargetname
  |       └── ...
  └── mysubproject
      └── ...

*Note:*

  If there is only one project, the target build folders will be placed directly into "build".
  Analogously, if there is only one target, the "release", "debug", etc. directories will be
  placed directly into "build".
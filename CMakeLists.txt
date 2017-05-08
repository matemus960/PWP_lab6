cmake_minimum_required(VERSION 2.8.9)

project(PWPLab)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/PWPLab")
set(EXTENSION_CATEGORY "lab")
set(EXTENSION_CONTRIBUTORS "Mateusz Muszer (PolSl)")
set(EXTENSION_DESCRIPTION "example")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/PWPLab.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/PWPLab/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(lab6)
add_subdirectory(lab6)
add_subdirectory(labor6)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})

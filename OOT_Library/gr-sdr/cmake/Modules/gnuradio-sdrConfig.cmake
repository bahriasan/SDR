find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_SDR gnuradio-sdr)

FIND_PATH(
    GR_SDR_INCLUDE_DIRS
    NAMES gnuradio/sdr/api.h
    HINTS $ENV{SDR_DIR}/include
        ${PC_SDR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_SDR_LIBRARIES
    NAMES gnuradio-sdr
    HINTS $ENV{SDR_DIR}/lib
        ${PC_SDR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-sdrTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_SDR DEFAULT_MSG GR_SDR_LIBRARIES GR_SDR_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_SDR_LIBRARIES GR_SDR_INCLUDE_DIRS)

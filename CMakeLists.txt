cmake_minimum_required(VERSION 3.7.0 FATAL_ERROR)

find_package(IRODS REQUIRED)
set(IRODS_PLUGIN_REVISION "0")
set(IRODS_PLUGIN_VERSION "${IRODS_VERSION}.${IRODS_PLUGIN_REVISION}")

set(IRODS_PACKAGE_REVISION "1")

include(IrodsCXXCompiler)
set(CMAKE_CXX_STANDARD ${IRODS_CXX_STANDARD})
set(CMAKE_MODULE_LINKER_FLAGS_INIT "-Wl,--enable-new-dtags -Wl,--as-needed -Wl,-z,defs")
set(CMAKE_SHARED_LINKER_FLAGS_INIT "-Wl,--enable-new-dtags -Wl,--as-needed -Wl,-z,defs")
set(CMAKE_MODULE_LINKER_FLAGS_RELEASE_INIT "-Wl,--gc-sections -Wl,-z,combreloc")
set(CMAKE_SHARED_LINKER_FLAGS_RELEASE_INIT "-Wl,--gc-sections -Wl,-z,combreloc")

project(irods_rule_engine_plugin-metadata_guard
  VERSION "${IRODS_PLUGIN_VERSION}"
  LANGUAGES CXX)

set(CMAKE_SKIP_BUILD_RPATH OFF)
set(CMAKE_SKIP_INSTALL_RPATH OFF)
set(CMAKE_SKIP_RPATH OFF)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH ON)
set(CMAKE_BUILD_WITH_INSTALL_RPATH OFF)
set(CMAKE_BUILD_RPATH_USE_ORIGIN ON)

include(${IRODS_TARGETS_PATH})

include(GNUInstallDirs)
include(UseLibCXX)

if (NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build {Debug, Release}." FORCE)
    message(STATUS "Setting unspecified CMAKE_BUILD_TYPE to '${CMAKE_BUILD_TYPE}'")
endif()

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  add_compile_options($<$<COMPILE_LANGUAGE:CXX>:-fpermissive>)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

set(PLUGIN irods_rule_engine_plugin-metadata_guard)

add_library(${PLUGIN} MODULE ${CMAKE_SOURCE_DIR}/src/main.cpp)

target_compile_options(${PLUGIN} PRIVATE -Wno-write-strings)

target_compile_definitions(${PLUGIN} PRIVATE ${IRODS_COMPILE_DEFINITIONS}
                                             IRODS_QUERY_ENABLE_SERVER_SIDE_API
                                             IRODS_ENABLE_SYSLOG
                                             IRODS_FILESYSTEM_ENABLE_SERVER_SIDE_API
                                             IRODS_USER_ADMINISTRATION_ENABLE_SERVER_SIDE_API)
                                             #IRODS_IO_TRANSPORT_ENABLE_SERVER_SIDE_API
                                             #FMT_HEADER_ONLY
                                             #SPDLOG_FMT_EXTERNAL)

target_include_directories(${PLUGIN} PRIVATE ${IRODS_INCLUDE_DIRS}
                                             ${IRODS_EXTERNALS_FULLPATH_BOOST}/include
                                             ${IRODS_EXTERNALS_FULLPATH_SPDLOG}/include
                                             ${IRODS_EXTERNALS_FULLPATH_FMT}/include
                                             ${IRODS_EXTERNALS_FULLPATH_JSON}/include)

target_link_libraries(${PLUGIN} PRIVATE irods_server
                                        irods_common
                                        ${IRODS_EXTERNALS_FULLPATH_BOOST}/lib/libboost_filesystem.so
                                        ${IRODS_EXTERNALS_FULLPATH_BOOST}/lib/libboost_system.so
                                        ${IRODS_EXTERNALS_FULLPATH_FMT}/lib/libfmt.so
                                        dl)

install(TARGETS ${PLUGIN} LIBRARY DESTINATION ${IRODS_PLUGINS_DIRECTORY}/rule_engines)

install(FILES ${CMAKE_SOURCE_DIR}/packaging/test_rule_engine_plugin_metadata_guard.py
        DESTINATION ${IRODS_HOME_DIRECTORY}/scripts/irods/test
        PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)

install(FILES ${CMAKE_SOURCE_DIR}/packaging/run_metadata_guard_test.py
        DESTINATION ${IRODS_HOME_DIRECTORY}/scripts
        PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)

set(PLUGIN_PACKAGE_NAME irods-rule-engine-plugin-metadata-guard)

set(CPACK_PACKAGE_VERSION ${IRODS_PLUGIN_VERSION})
set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY OFF)
set(CPACK_COMPONENT_INCLUDE_TOPLEVEL_DIRECTORY OFF)
set(CPACK_COMPONENTS_GROUPING IGNORE)
set(CPACK_PACKAGE_CONTACT "Renaissance Computing Institute <info@irods.org>")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "The integrated Rule-Oriented Data System")
set(CPACK_PACKAGE_VENDOR "Renaissance Computing Institute <info@irods.org>")

set(CPACK_DEB_COMPONENT_INSTALL OFF)
set(CPACK_DEBIAN_PACKAGE_SECTION "contrib/science")
set(CPACK_DEBIAN_COMPRESSION_TYPE "gzip")
set(CPACK_DEBIAN_PACKAGE_PRIORITY "extra")
set(CPACK_DEBIAN_PACKAGE_HOMEPAGE "https://irods.org")
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS OFF)
set(CPACK_DEBIAN_PACKAGE_CONTROL_STRICT_PERMISSION ON)
set(CPACK_DEBIAN_PACKAGE_CONTROL_EXTRA "${CMAKE_SOURCE_DIR}/packaging/postinst;")
set(CPACK_DEBIAN_PACKAGE_BREAKS ${PLUGIN_PACKAGE_NAME})
set(CPACK_DEBIAN_PACKAGE_REPLACES ${PLUGIN_PACKAGE_NAME})
set(CPACK_DEBIAN_PACKAGE_RELEASE "${IRODS_PACKAGE_REVISION}")
if (IRODS_LINUX_DISTRIBUTION_VERSION_CODENAME)
  set(CPACK_DEBIAN_PACKAGE_RELEASE "${CPACK_DEBIAN_PACKAGE_RELEASE}~${IRODS_LINUX_DISTRIBUTION_VERSION_CODENAME}")
endif()
set(CPACK_DEBIAN_FILE_NAME DEB-DEFAULT)

set(CPACK_RPM_COMPONENT_INSTALL OFF)
set(CPACK_RPM_PACKAGE_LICENSE "BSD-3-Clause")
set(CPACK_RPM_PACKAGE_VENDOR "iRODS Consortium")
set(CPACK_RPM_PACKAGE_URL "https://irods.org")
set(CPACK_RPM_PACKAGE_AUTOREQ 0)
set(CPACK_RPM_PACKAGE_AUTOPROV 0)
set(CPACK_RPM_PACKAGE_OBSOLETES ${PLUGIN_PACKAGE_NAME})
set(CPACK_RPM_POST_INSTALL_SCRIPT_FILE "${CMAKE_SOURCE_DIR}/packaging/postinst")
set(CPACK_RPM_PACKAGE_RELEASE "${IRODS_PACKAGE_REVISION}")
set(CPACK_RPM_FILE_NAME RPM-DEFAULT)

set(CPACK_ARCHIVE_COMPONENT_INSTALL OFF)

set(CPACK_DEBIAN_PACKAGE_NAME ${PLUGIN_PACKAGE_NAME})
set(CPACK_DEBIAN_PACKAGE_DEPENDS "${IRODS_PACKAGE_DEPENDENCIES_STRING}, irods-server (= ${IRODS_VERSION}), irods-runtime (= ${IRODS_VERSION}), libc6")

set(CPACK_RPM_PACKAGE_NAME ${PLUGIN_PACKAGE_NAME})
if (IRODS_LINUX_DISTRIBUTION_NAME STREQUAL "centos" OR
    IRODS_LINUX_DISTRIBUTION_NAME STREQUAL "centos linux" OR
    IRODS_LINUX_DISTRIBUTION_NAME STREQUAL "opensuse")
    set(CPACK_RPM_PACKAGE_REQUIRES "${IRODS_PACKAGE_DEPENDENCIES_STRING}, irods-server = ${IRODS_VERSION}, irods-runtime = ${IRODS_VERSION}")
endif()

if (NOT CPACK_GENERATOR)
    set(CPACK_GENERATOR ${IRODS_CPACK_GENERATOR} CACHE STRING "CPack generator to use, e.g. {DEB, RPM, TGZ}." FORCE)
    message(STATUS "Setting unspecified CPACK_GENERATOR to ${CPACK_GENERATOR}. This is the correct setting for normal builds.")
endif()

include(CPack)

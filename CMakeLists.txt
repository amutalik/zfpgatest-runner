cmake_minimum_required(VERSION 3.14)

project(zfpgatest-operator LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

#Automoc and RCC ON. Needed in QT projects
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

#C++ 14 Flag
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#Set project Version
set(ZFPGATEST_OPERATOR_VERSION_MAJOR "0")
set(ZFPGATEST_OPERATOR_VERSION_MINOR "1")
set(ZFPGATEST_OPERATOR_VERSION_PATCH "0")

set(PROJECT_VERSION "${ZFPGATEST_OPERATOR_VERSION_MAJOR}.${ZFPGATEST_OPERATOR_VERSION_MINOR}.${ZFPGATEST_OPERATOR_VERSION_PATCH}")

#Adding cmake functions like feature_summary()
include(FeatureSummary)
include(GNUInstallDirs)

#Find dependecies
find_package(Qt5 COMPONENTS Core CONFIG REQUIRED)
find_package(simpleautorunlib REQUIRED)

add_subdirectory(src)

enable_testing()

# spawn out some info on configuration
feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)



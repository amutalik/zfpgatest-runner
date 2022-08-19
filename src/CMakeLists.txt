set(CMAKE_INCLUDE_CURRENT_DIR ON)

#sum up project Files
set(SOURCES
    main.cpp
    testmessagehandler.cpp
)

set(HEADERS
    testmessagehandler.h
)

add_executable(${PROJECT_NAME}
    ${SOURCES}
    ${HEADERS}
)

#set target Version
set_target_properties(${PROJECT_NAME} PROPERTIES VERSION ${PROJECT_VERSION})
set_target_properties(${PROJECT_NAME} PROPERTIES SOVERSION ${ZFPGATEST_RUNNER_VERSION_MAJOR})

#link dependencies
target_link_libraries(${PROJECT_NAME}
    PUBLIC
    Qt5::Core
    simpleautorunlib
)

#install executable to bin
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )

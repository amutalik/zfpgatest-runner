set(CMAKE_INCLUDE_CURRENT_DIR ON)

#sum up project Files
set(SOURCES
    main.cpp
)

add_executable(${PROJECT_NAME}
    ${SOURCES}
)

#set target Version
set_target_properties(${PROJECT_NAME} PROPERTIES VERSION ${PROJECT_VERSION})
set_target_properties(${PROJECT_NAME} PROPERTIES SOVERSION ${ZFPGATEST_OPERATOR_VERSION_MAJOR})

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

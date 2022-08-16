#include "cmdhandlerfile.h"
#include "cmdparserfile.h"
#include "testmessagehandler.h"
#include <QCoreApplication>
#include <QCommandLineOption>
#include <QCommandLineParser>
#include <iostream>

int main(int argc, char *argv[]) {
    qInstallMessageHandler(TestMessageHandler::MessageHandler);
    QCoreApplication a(argc, argv);
    QCommandLineParser parser;

    parser.addHelpOption();

    // option execution file
    QCommandLineOption optExecFile(QStringList() << "x" << "exec-file", "fill path execution file", "path");
    parser.addOption(optExecFile);

    parser.process(a);
    QString strExecFile = parser.value(optExecFile);

    std::cout << "Input file is : " << strExecFile.toStdString() << std::endl;

    CmdParserFile parserFile;
    CmdHandlerFile handlerFile;
    parserFile.SetCmdHandler(&handlerFile);

    // Ensure event loop up
    QTimer::singleShot(300, &parserFile, [&]
                       () {
        QObject::connect(&parserFile, &CmdParserFile::done, &a, &QCoreApplication::exit );
        QObject::connect(&handlerFile, &CmdHandlerFile::kill, &a, &QCoreApplication::exit );

        parserFile.StartFileExecution(strExecFile, &handlerFile);
    });

    int ret = a.exec();

    TestMessageHandler::DisplayTestSummary();

    return ret;
}

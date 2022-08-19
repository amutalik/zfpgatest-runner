#include "testmessagehandler.h"

quint32 TestMessageHandler::m_ReadCount = 0;
quint32 TestMessageHandler::m_ReadErrorCount = 0;
quint32 TestMessageHandler::m_ReadSuccessCount = 0;
quint32 TestMessageHandler::m_WriteCount = 0;
quint32 TestMessageHandler::m_WriteErrorCount = 0;
quint32 TestMessageHandler::m_WriteSuccessCount = 0;
quint32 TestMessageHandler::m_ResponseCheckCount = 0;
quint32 TestMessageHandler::m_ResponseErrorCount = 0;
quint32 TestMessageHandler::m_ResponseSuccessCount = 0;

void TestMessageHandler::MessageHandler(QtMsgType type, const QMessageLogContext &context, const QString &msg)
{
    QByteArray localMsg = DecodeMessageInfo(msg).toLocal8Bit();

    fprintf(stderr, "%s\n", localMsg.constData());
}

void TestMessageHandler::DisplayTestSummary()
{
    QTextStream stream(stdout);
    stream << "\nTest summary of Read, Write and Check Response commands : \n";

    stream << qSetFieldWidth(20) << Qt::left << "Read =>" << qSetFieldWidth(0)
           << "\tTotal: " << m_ReadCount
           << "\tPassed: " << m_ReadSuccessCount
           << "\tFailed: " << m_ReadErrorCount << "\n";

    stream << qSetFieldWidth(20) << Qt::left << "Write =>" << qSetFieldWidth(0)
           << "\tTotal: " << m_WriteCount
           << "\tPassed: " << m_WriteSuccessCount
           << "\tFailed: " << m_WriteErrorCount << "\n";

    stream << qSetFieldWidth(20) << Qt::left << "Check Response =>" << qSetFieldWidth(0)
           << "\tTotal: " << m_ResponseCheckCount
           << "\tPassed: " << m_ResponseSuccessCount
           << "\tFailed: " << m_ResponseErrorCount << "\n";

    qInfo("%s", qPrintable(stream.readAll()));
}

QString TestMessageHandler::DecodeMessageInfo(const QString &msg)
{
    MessageType msgType = DecodeMessageType(msg);
    QString msgInfo = msg;

    if (msg.contains("READ", Qt::CaseInsensitive)) {
        msgInfo = ReadMessageHandler(msgType, msg);
    }
    else if (msg.contains("WRITE", Qt::CaseInsensitive)) {
        msgInfo = WriteMessageHandler(msgType, msg);
    }
    else if (msg.contains("CHECK", Qt::CaseInsensitive)) {
        msgInfo = CheckResponseMessageHandler(msgType, msg);
    }
    else {
    }

    return msgInfo;
}

MessageType TestMessageHandler::DecodeMessageType(const QString &msg)
{
    MessageType msgType = MessageType::NOT_DEFINED;

    if (msg.contains("OK", Qt::CaseInsensitive)) {
        msgType = MessageType::RESPONSE_OK;
    }
    else if (msg.contains("ERROR", Qt::CaseInsensitive)) {
        msgType = MessageType::RESPONSE_ERROR;
    }
    else if (msg.contains("STARTING", Qt::CaseInsensitive)) {
        msgType = MessageType::COMMAND;
    }
    else {
        msgType = MessageType::NOT_DEFINED;
    }

    return msgType;
}

QString TestMessageHandler::ReadMessageHandler(MessageType msgType, const QString &msg)
{
    QString msgInfo = msg;

    if (msgType == MessageType::RESPONSE_OK) {
        //supress the display of values read
        int posOK = msg.lastIndexOf(',');
        msgInfo = msg.left(posOK);
        m_ReadSuccessCount++;
    }

    if (msgType == MessageType::RESPONSE_ERROR) {
        m_ReadErrorCount++;
    }

    if (msgType == MessageType::COMMAND) {
        m_ReadCount++;
    }

    return msgInfo;
}

QString TestMessageHandler::WriteMessageHandler(MessageType msgType, const QString &msg)
{
    if (msgType == MessageType::RESPONSE_OK) {
        m_WriteSuccessCount++;
    }

    if (msgType == MessageType::RESPONSE_ERROR) {
        m_WriteErrorCount++;
    }

    if (msgType == MessageType::COMMAND) {
        m_WriteCount++;
    }

    return msg;
}

QString TestMessageHandler::CheckResponseMessageHandler(MessageType msgType, const QString &msg)
{
    QString msgInfo = msg;

    if (msgType == MessageType::RESPONSE_OK) {
        m_ResponseSuccessCount++;
    }

    if (msgType == MessageType::RESPONSE_ERROR) {
        if (msg.contains("CHECK FAILED", Qt::CaseInsensitive)) {
            //suppress the display of expected and actual values
            int posOK = msg.indexOf("expected", Qt::CaseInsensitive);
            msgInfo = msg.left(posOK);
        }
        m_ResponseErrorCount++;
    }

    if (msgType == MessageType::COMMAND) {
        m_ResponseCheckCount++;
    }

    return msgInfo;
}

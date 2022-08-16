#ifndef MESSAGEHANDLER_H
#define MESSAGEHANDLER_H

#include <QDebug>

enum class MessageType {
    COMMAND = 0,
    RESPONSE_OK,
    RESPONSE_ERROR,
    NOT_DEFINED
};

class TestMessageHandler {

public:
    static void MessageHandler(QtMsgType type, const QMessageLogContext &context, const QString &msg);
    static void DisplayTestSummary();

private:
    //private constructor: objects of this class can't be created
    TestMessageHandler() {}

    static QString DecodeMessageInfo(const QString &msg);
    static MessageType DecodeMessageType(const QString &msg);

    static QString ReadMessageHandler(MessageType msgType, const QString &msg);
    static QString WriteMessageHandler(MessageType msgType, const QString &msg);
    static QString CheckResponseMessageHandler(MessageType msgType, const QString &msg);

    static quint32 m_ReadCount;
    static quint32 m_ReadErrorCount;
    static quint32 m_ReadSuccessCount;
    static quint32 m_WriteCount;
    static quint32 m_WriteErrorCount;
    static quint32 m_WriteSuccessCount;
    static quint32 m_ResponseCheckCount;
    static quint32 m_ResponseErrorCount;
    static quint32 m_ResponseSuccessCount;
};

#endif // MESSAGEHANDLER_H

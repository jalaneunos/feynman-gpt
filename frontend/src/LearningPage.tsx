// LearningPage.tsx

import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import ChatBar from "./Chatbar";
import Message from "./Message";
import StartSessionButton from "./StartSessionButton";
import Loading from "./Loading";
import LoadingSpinner from "./LoadingSpinner";

interface Message {
    text: string;
    sender: "You" | "Timmy" | "Richie";
}

const LearningPage: React.FC = () => {
    const [learningSession, setLearningSession] = useState<any>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLearningStarted, setIsLearningStarted] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const chatContainerRef = useRef<HTMLDivElement>(null);
    console.log(learningSession);

    const startLearningSession = useCallback(async () => {
        try {
            const response = await axios.get("http://localhost:8000/start_learning");
            setLearningSession(response.data.data.learning_session);
        } catch (error) {
            console.error("Error starting learning session:", error);
        }
    }, []);

    useEffect(() => {
        startLearningSession();
    }, [startLearningSession]);

    const handleStartLearning = async () => {
        try {
            const questionResponse = await axios.post("http://localhost:8000/question", {
                question_index: 0,
                learning_session: learningSession,
            });
            const message = questionResponse.data.data.question;
            setMessages((prevMessages) => [...prevMessages, { text: message, sender: "Timmy" }]);
            setIsLearningStarted(true);
        } catch (error) {
            console.error("Error fetching first question:", error);
        }
    };

    const handleSendMessage = async (message: string) => {
        setMessages((prevMessages) => [...prevMessages, { text: message, sender: "You" }]);
        setIsLoading(true);
        try {
            const response = await axios.post("http://localhost:8000/answer", {
                user_answer: message,
                question_index: learningSession.current_question_index,
                learning_session: learningSession,
            });

            if (response.data.status === "success") {
                if (response.data.data.next_question_index !== undefined) {
                    const nextQuestionIndex = response.data.data.next_question_index;
                    setLearningSession((prevSession: any) => ({
                        ...prevSession,
                        current_question_index: nextQuestionIndex,
                    }));
                    const questionResponse = await axios.post("http://localhost:8000/question", {
                        question_index: nextQuestionIndex,
                        learning_session: learningSession,
                    });
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { text: response.data.message, sender: "Timmy" },
                        { text: questionResponse.data.data.question, sender: "Timmy" },
                    ]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { text: "Congratulations! You have completed the learning session.", sender: "Richie" },
                    ]);
                }
            } else {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: response.data.message, sender: "Richie" },
                    { text: response.data.data.guidance, sender: "Richie" },
                ]);
            }
            setIsLoading(false);
        } catch (error) {
            setIsLoading(false);
            console.error("Error submitting answer:", error);
        }
    };

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    if (!learningSession) {
        return <Loading />;
    }

    return (
        <div className="flex flex-col h-screen">
            <div className="flex-1 overflow-y-auto">
                <div className="max-w-2xl mx-auto w-full px-4">
                    <div className="flex justify-center pt-3">
                        <h2 className="text-xl mb-4">{learningSession.title}</h2>
                    </div>
                    <div ref={chatContainerRef} className="mb-20">
                        {messages.map((msg, index) => (
                            <Message key={index} text={msg.text} sender={msg.sender} />
                        ))}
                        {isLoading && <LoadingSpinner />}
                    </div>
                </div>
            </div>
            <div className="fixed bottom-0 left-0 right-0 p-4">
                <div className="max-w-2xl mx-auto flex justify-center">
                    {!isLearningStarted ? (
                        <StartSessionButton onClick={handleStartLearning} />
                    ) : (
                        <ChatBar onSendMessage={handleSendMessage} messages={messages} />
                    )}
                </div>
            </div>
        </div>
    );
};

export default LearningPage;

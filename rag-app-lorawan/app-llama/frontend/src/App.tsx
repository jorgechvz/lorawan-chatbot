import React, { useState, useRef, useEffect } from "react";
import { Send, User } from "lucide-react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { ClipLoader } from "react-spinners";
import rehypeSanitize from "rehype-sanitize";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

type Message = {
  id: number;
  content: string;
  sender: "user" | "ai";
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async () => {
    if (inputMessage.trim() === "") return;

    const newMessage: Message = {
      id: Date.now(),
      content: inputMessage,
      sender: "user",
    };

    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_PUBLIC_CHAT_API}`,
        {
          query: inputMessage,
        }
      );

      const aiResponse: Message = {
        id: Date.now() + 1,
        content: response.data.response,
        sender: "ai",
      };

      setMessages((prevMessages) => [...prevMessages, aiResponse]);
    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        content: "Sorry, an error occurred.",
        sender: "ai",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Efecto para hacer scroll al final cuando los mensajes cambian
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-gray-100">
      <div className="flex flex-col justify-between bg-white border border-gray-300 rounded-lg shadow-lg w-full max-w-7xl h-[80vh]">
        <div className="p-6 bg-blue-600 text-white text-center rounded-t-lg">
          <h1 className="text-2xl font-bold">
            LoRa Chatbot: Intelligent Conversations for IoT Networks
          </h1>
        </div>
        {/* Chat Area */}
        <div
          ref={chatContainerRef} // Referencia para el scroll
          className="flex-grow p-6 overflow-y-auto"
        >
          {messages.map((message) => (
            <div
              key={message.id}
              className={`mb-4 flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`p-4 rounded-lg shadow-md ${
                  message.sender === "user"
                    ? "bg-blue-500 text-white rounded-tr-none max-w-xs md:max-w-md"
                    : "bg-gray-200 text-gray-900 rounded-tl-none max-w-full md:max-w-[80%]"
                }`}
              >
                <div className="flex items-center space-x-2 mb-2">
                  {message.sender === "user" ? (
                    <User className="w-6 h-6" />
                  ) : (
                    <Send className="w-6 h-6" />
                  )}
                  <span className="font-semibold">
                    {message.sender === "user" ? "You" : "Assistant"}
                  </span>
                </div>
                {message.sender === "ai" ? (
                  <ReactMarkdown
                    rehypePlugins={[rehypeSanitize]}
                    className="prose prose-sm"
                  >
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  <p>{message.content}</p>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-xs md:max-w-md p-4 rounded-lg shadow-md bg-gray-200 text-gray-900">
                <div className="flex items-center space-x-2">
                  <ClipLoader color="#4A90E2" loading={true} size={24} />
                  <span className="font-semibold">Assistant is typing...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-300 bg-gray-50">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center space-x-2"
          >
            <Input
              type="text"
              placeholder="Type your message..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-grow p-3 border border-gray-300 rounded-full shadow-sm focus:ring focus:ring-blue-500"
            />
            <Button
              type="submit"
              disabled={isLoading}
              className="bg-blue-600 text-white rounded-full p-3 shadow-md"
            >
              <Send className="w-5 h-5" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}

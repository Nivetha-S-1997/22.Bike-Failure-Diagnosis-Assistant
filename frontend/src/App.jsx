
import { useState, useEffect, useRef } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  // 1. State variables
  const [message, setMessage] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  // 2. References
  const chatBoxRef = useRef(null);
  const latestBotRef = useRef(null);

  // 3. Automatically scroll to the latest message
  useEffect(() => {
    if (loading) {
      // Show the typing indicator
      if (chatBoxRef.current) {
        chatBoxRef.current.scrollTop =
          chatBoxRef.current.scrollHeight;
      }
    } else if (latestBotRef.current) {
      // Show the beginning of the latest bot response
      latestBotRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [chatMessages, loading]);

  // 4. Start a new chat
  const startNewChat = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/new-chat", {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error("Failed to create a new chat");
    }

    const data = await response.json();

    setSessionId(data.session_id);
    setChatMessages([]);
    setMessage("");
  } catch (error) {
    console.error(error);
    alert("Unable to start a new chat.");
  }
};

  // 5. Automatically create a session
  useEffect(() => {
    startNewChat();
  }, []);

  // 6. Send the user's message to FastAPI
  const sendMessage = async () => {
    if (!message.trim() || loading || !sessionId) return;

    const userMessage = message.trim();

    // Display user's message immediately
    setChatMessages((previousMessages) => [
      ...previousMessages,
      { role: "user", text: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
          errorData.detail || "Unable to get a response. Please try again."
        );
      }

      const data = await response.json();

      // Add bot response to conversation
      setChatMessages((previousMessages) => [
        ...previousMessages,
        { role: "bot", text: data.response },
      ]);
    } 
    
    catch (error) {
    console.error(error);

    setChatMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "bot",
        text: error.message || "Unable to connect to the chatbot. Please try again.",
      },
    ]);
    }
    
    finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1>Bike Failure Diagnosis Assistant</h1>
      <p>Describe your bike problem and I'll help you diagnose it.</p>

      <div className="chat-actions">
        <button onClick={startNewChat} disabled={loading}>
        + New Chat </button>
      </div>

      <div className="chat-box" ref={chatBoxRef}>
        {chatMessages.map((chat, index) => (
          <div
            key={index}
            ref={
              chat.role === "bot" &&
              index === chatMessages.length - 1
                ? latestBotRef
                : null
            }
            className={`chat-message ${chat.role}`}
          >
            <strong>{chat.role === "user" ? "You" : "Bot"}</strong>

            {chat.role === "bot" ? (
              <ReactMarkdown>{chat.text}</ReactMarkdown>
            ) : (
              <p>{chat.text}</p>
            )}
          </div>
        ))}

        {loading && (
          <div className="chat-message bot">
            <p>Bot is typing...</p>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Describe your bike problem..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button onClick={sendMessage} disabled={loading || !sessionId}>
          {loading ? "Sending..." : "Send"}</button>
      </div>
    </div>
  );
}

export default App;
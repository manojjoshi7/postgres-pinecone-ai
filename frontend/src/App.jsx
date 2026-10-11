import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! 👋 I'm your E-Commerce AI Assistant. Ask me anything about the customer data.",
    },
  ]);

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: trimmedQuestion,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the AI server. Please check that FastAPI is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✦</div>

          <div>
            <h2>Insight AI</h2>
            <span>Customer Intelligence</span>
          </div>
        </div>

        <button
          className="new-chat"
          onClick={() =>
            setMessages([
              {
                role: "assistant",
                content:
                  "Hello! 👋 Start a new conversation by asking a question about the customer data.",
              },
            ])
          }
        >
          + New conversation
        </button>

        <div className="sidebar-section">
          <span className="section-title">
            AI capabilities
          </span>

          <div className="capability">
            <span>⌕</span>
            Semantic Search
          </div>

          <div className="capability">
            <span>◈</span>
            Customer Insights
          </div>

          <div className="capability">
            <span>⌁</span>
            RAG Answers
          </div>
        </div>

        <div className="sidebar-footer">
          <span className="status-dot"></span>
          Local AI • Ollama
        </div>
      </aside>

      <main className="chat-container">

        <header className="chat-header">
          <div>
            <h1>E-Commerce AI Assistant</h1>
            <p>
              Ask questions about your customer data
            </p>
          </div>

          <div className="model-badge">
            <span className="status-dot"></span>
            Llama 3.2 3B
          </div>
        </header>

        <section className="messages">

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.role}`}
            >

              {message.role === "assistant" && (
                <div className="avatar ai-avatar">
                  ✦
                </div>
              )}

              <div className="message">
                {message.content}
              </div>

              {message.role === "user" && (
                <div className="avatar user-avatar">
                  U
                </div>
              )}

            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar ai-avatar">
                ✦
              </div>

              <div className="message typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

        </section>

        <div className="suggestions">

          <button
            onClick={() =>
              setQuestion(
                "How many customers spent more than $100?"
              )
            }
          >
            💰 Spending insights
          </button>

          <button
            onClick={() =>
              setQuestion(
                "What products are customers interested in?"
              )
            }
          >
            🛍 Product interests
          </button>

          <button
            onClick={() =>
              setQuestion(
                "Which product categories are popular?"
              )
            }
          >
            📊 Popular categories
          </button>

        </div>

        <div className="input-area">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your customer data..."
            rows="1"
          />

          <button
            className="send-button"
            onClick={sendMessage}
            disabled={loading || !question.trim()}
          >
            {loading ? "..." : "↑"}
          </button>

        </div>

        <p className="disclaimer">
          AI-generated answers are based on your connected
          customer data.
        </p>

      </main>
    </div>
  );
}

export default App;
import { useState, useRef, useEffect } from "react";
import { Bot, User, ArrowUp, Plus, Smile, Mic } from "lucide-react";

// Use environment variable for production, fallback to localhost for development
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

interface Message {
  id: number;
  content: string;
  role: "user" | "ai";
}

const ChatWindow = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = input.trim();
    const userMsg: Message = { id: Date.now(), content: userMessage, role: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => null);
        throw new Error(errorData?.detail || `Server error (${res.status})`);
      }

      const data = await res.json();
      const aiMsg: Message = {
        id: Date.now() + 1,
        content: data.response,
        role: "ai",
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (error: any) {
      const errMsg: Message = {
        id: Date.now() + 1,
        content: `⚠️ ${error.message || "Failed to connect to the server. Make sure the backend is running on port 8000."}`,
        role: "ai",
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="min-h-screen gradient-bg flex flex-col">
      {/* Main content area */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 pb-32">
        {!hasMessages ? (
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-semibold text-foreground tracking-tight">
              What's on your mind?
            </h1>
          </div>
        ) : (
          <div
            ref={scrollRef}
            className="w-full max-w-2xl flex-1 overflow-y-auto scrollbar-thin space-y-4 py-8"
            style={{ maxHeight: "calc(100vh - 200px)" }}
          >
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-3 animate-fade-in ${msg.role === "user" ? "flex-row-reverse" : ""}`}
              >
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${msg.role === "user" ? "user-bubble" : "ai-bubble"
                    }`}
                >
                  {msg.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                </div>
                <div
                  className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${msg.role === "user" ? "user-bubble" : "ai-bubble"
                    }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex gap-3 animate-fade-in">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full ai-bubble">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="ai-bubble rounded-2xl px-4 py-3 text-sm">
                  <span className="inline-flex gap-1">
                    <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "300ms" }} />
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Fixed input area at bottom */}
      <div className="fixed bottom-0 left-0 right-0 p-4 pb-6 flex justify-center">
        <div className="w-full max-w-2xl chat-card rounded-2xl">
          <div className="chat-input rounded-2xl flex items-end gap-2 p-3 transition-all">
            <button type="button" className="icon-btn p-2 rounded-lg hover:bg-secondary/50">
              <Plus className="h-5 w-5" />
            </button>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask Lovable to create a landing page for my..."
              rows={1}
              className="flex-1 bg-transparent text-foreground placeholder:text-muted-foreground text-sm resize-none outline-none py-2 max-h-32"
              style={{ minHeight: "24px" }}
            />
            <div className="flex items-center gap-1">
              <button type="button" className="icon-btn p-2 rounded-lg hover:bg-secondary/50">
                <Smile className="h-5 w-5" />
              </button>
              <button type="button" className="icon-btn p-2 rounded-lg hover:bg-secondary/50">
                <Mic className="h-5 w-5" />
              </button>
              <button
                onClick={handleSend}
                disabled={!input.trim()}
                className="send-btn rounded-lg p-2 disabled:opacity-40 disabled:cursor-not-allowed ml-1"
              >
                <ArrowUp className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;

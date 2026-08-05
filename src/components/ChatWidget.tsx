import { useEffect, useRef, useState } from "react";
import { usePlantData } from "@/hooks/use-plant-data";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

interface ChatWidgetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  isRaining: boolean;
  forecastRainProbability: number;
}

// Chat message structure used by this component
interface ChatMessage {
  role: "user" | "assistant";
  text: string;
  crop?: string;
  score?: number;
  timestamp: string; // ISO string
}

const ChatWidget = ({
  open,
  onOpenChange,
  isRaining,
  forecastRainProbability,
}: ChatWidgetProps) => {
  const [question, setQuestion] = useState<string>("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const { data } = usePlantData();

  // Refs for input focus and auto-scroll
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Keep the view scrolled to newest message on updates (smooth)
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Clear conversation when widget fully closes (preserve while open)
  useEffect(() => {
    if (!open) {
      setMessages([]);
      setQuestion("");
    } else {
      // focus input when opened
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [open]);


    const API_URL = import.meta.env.VITE_API_URL;
  // Centralized send handler: avoids duplicated fetch logic.
    const handleSend = async () => {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    const userMessage: ChatMessage = {
      role: "user",
      text: trimmed,
      timestamp: new Date().toISOString(),
    };

    setMessages((m) => [...m, userMessage]);
    setLoading(true);

    try {
      console.log("Sending sensor data:", {
        crop: data.type,
        moisture: data.moisture,
        threshold: data.threshold,
        temperature: data.temperature,
        humidity: data.humidity,
        pump: data.pump,
      });
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmed,
          crop: data.type ?? "wheat",
          moisture: data.moisture ?? 0,
          temperature: data.temperature ?? 0,
          humidity: data.humidity ?? 0,
          pumpStatus: data.pump ?? "OFF",
          threshold: data.threshold ?? 40,

          // Weather context
          isRaining,
          forecastRainProbability,
        }),
      });

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const responseData = await res.json();

      const assistantMessage: ChatMessage = {
        role: "assistant",
        text:
          responseData.response ??
          "I couldn't generate a reliable answer.",
        crop: responseData.best_crop,
        score: responseData.best_score,
        timestamp: new Date().toISOString(),
      };

      setMessages((m) => [...m, assistantMessage]);

      setQuestion("");
      setTimeout(() => inputRef.current?.focus(), 20);
    } catch (err) {
      console.error(err);

      const errMsg: ChatMessage = {
        role: "assistant",
        text: "Unable to contact the AI server. Please try again.",
        timestamp: new Date().toISOString(),
      };

      setMessages((m) => [...m, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Handle Enter to send, Shift+Enter to newline
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void handleSend();
    }
  };

  // Small helper to format timestamps
  const formatTimestamp = (iso?: string) => {
    if (!iso) return "";
    try {
      return new Date(iso).toLocaleString();
    } catch (e) {
      return iso;
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="bottom"
        className="h-[80vh] rounded-t-3xl flex flex-col"
      >
        <SheetHeader>
          <SheetTitle>🌱 KrishiMitra AI</SheetTitle>
        </SheetHeader>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto mt-6 px-4 py-2 space-y-4">

          <div className="bg-muted rounded-xl p-4">
            <p className="text-sm font-medium">👋 Hello! I'm KrishiMitra AI.</p>
            <p className="text-sm text-muted-foreground mt-2">Ask me anything about:</p>
            <ul className="mt-3 text-sm space-y-2">
              <li>🌾 Crop diseases</li>
              <li>💧 Irrigation advice</li>
              <li>🌱 Fertilizers</li>
              <li>🌦 Weather-based farming</li>
            </ul>
          </div>

          {/* Messages list */}
          <div className="flex flex-col gap-4">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className={`${m.role === "user" ? "bg-primary text-primary-foreground rounded-xl text-sm px-4 py-2 max-w-[80%]" : "bg-white/70 border border-gray-200 rounded-xl text-sm px-4 py-2 max-w-[80%]"}`}>
                  <div className="whitespace-pre-wrap">{m.text}</div>

                  {/* Retrieval info displayed for assistant messages */}
                  {m.role === "assistant" && (m.crop || typeof m.score === "number") && (
                    <div className="mt-2 text-xs text-gray-600">
                      {m.crop && <div><strong>Retrieved Crop:</strong> {m.crop}</div>}
                      {typeof m.score === "number" && (
                        <div>Confidence: {m.score.toFixed(2)}</div>
                      )}
                    </div>
                  )}

                  <div className="text-[11px] text-gray-500 mt-2 text-right">{formatTimestamp(m.timestamp)}</div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

        </div>

        {/* Input Area */}
        <div className="border-t pt-4 mt-4 px-4 pb-4">
          <textarea
            ref={inputRef}
            placeholder="Ask your question... (Shift+Enter for new line)"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={2}
            className="w-full rounded-xl border px-4 py-3 outline-none mb-3 resize-none"
          />

          <button
            onClick={() => void handleSend()}
            disabled={
              loading || question.trim() === "" || data.moisture === null
            }
            className="w-full rounded-xl bg-primary text-primary-foreground py-3 font-medium disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default ChatWidget;
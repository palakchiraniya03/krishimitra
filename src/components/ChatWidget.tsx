import { useState } from "react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

interface ChatWidgetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const ChatWidget = ({ open, onOpenChange }: ChatWidgetProps) => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");

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
        <div className="flex-1 overflow-y-auto mt-6 space-y-4">

          <div className="bg-muted rounded-xl p-4">
            <p className="text-sm font-medium">
              👋 Hello! I'm KrishiMitra AI.
            </p>

            <p className="text-sm text-muted-foreground mt-2">
              Ask me anything about:
            </p>

            <ul className="mt-3 text-sm space-y-2">
              <li>🌾 Crop diseases</li>
              <li>💧 Irrigation advice</li>
              <li>🌱 Fertilizers</li>
              <li>🌦 Weather-based farming</li>
            </ul>
          </div>

          {response && (
            <div className="bg-green-50 border border-green-200 rounded-xl p-4">
              <p className="text-sm font-semibold mb-2">
                🌱 KrishiMitra AI
              </p>

              <p className="text-sm whitespace-pre-wrap">
                {response}
              </p>
            </div>
          )}

        </div>

        {/* Input Area */}
        <div className="border-t pt-4 mt-4">
          <input
            type="text"
            placeholder="Ask your question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full rounded-xl border px-4 py-3 outline-none mb-3"
          />

          <button
            onClick={async () => {
              const response = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  question: question,
                }),
              });

              const data = await response.json();

              setResponse(data.response);

              console.log(data);
            }}
            className="w-full rounded-xl bg-primary text-primary-foreground py-3 font-medium"
          >
            Send
          </button>
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default ChatWidget;
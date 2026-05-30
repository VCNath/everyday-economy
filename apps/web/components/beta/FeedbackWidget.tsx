"use client";

import { MessageSquare, X } from "lucide-react";
import { usePathname } from "next/navigation";
import { useState } from "react";
import type { FormEvent } from "react";

import { useAuth } from "@/hooks/useAuth";
import { submitFeedback } from "@/lib/api-client";
import type { FeedbackType } from "@/lib/types";

const TYPES: Array<{ value: FeedbackType; label: string }> = [
  { value: "bug", label: "Bug" },
  { value: "data_issue", label: "Data issue" },
  { value: "confusing", label: "Confusing" },
  { value: "feature_request", label: "Feature request" },
  { value: "design_feedback", label: "Design feedback" },
  { value: "general", label: "General" },
];

export function FeedbackWidget() {
  const pathname = usePathname();
  const auth = useAuth();
  const [open, setOpen] = useState(false);
  const [feedbackType, setFeedbackType] = useState<FeedbackType>("general");
  const [rating, setRating] = useState<number | "">("");
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error">("idle");

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setStatus("sending");
    try {
      await submitFeedback({
        feedback_type: feedbackType,
        rating: rating === "" ? null : rating,
        message,
        email: auth.isAuthenticated ? null : email || null,
        page_path: pathname,
        metadata: {
          viewport: typeof window !== "undefined" ? `${window.innerWidth}x${window.innerHeight}` : undefined,
          userAgent: typeof navigator !== "undefined" ? navigator.userAgent : undefined,
        },
      }, auth.token);
      setStatus("sent");
      setMessage("");
      setEmail("");
    } catch {
      setStatus("error");
    }
  }

  return (
    <>
      <button className="feedback-fab" type="button" onClick={() => setOpen(true)} aria-label="Send beta feedback">
        <MessageSquare size={18} />
        <span>Feedback</span>
      </button>
      {open ? (
        <div className="feedback-backdrop" role="presentation">
          <form className="feedback-dialog" onSubmit={onSubmit} aria-labelledby="feedback-title">
            <div className="row between">
              <div>
                <p className="eyebrow">Public beta</p>
                <h2 id="feedback-title">Send feedback</h2>
              </div>
              <button className="icon-button" type="button" onClick={() => setOpen(false)} aria-label="Close feedback form">
                <X size={18} />
              </button>
            </div>
            {status === "sent" ? (
              <div className="empty-state compact">
                <h3>Thanks. That helps.</h3>
                <p>Your feedback is now in the beta review queue.</p>
                <button className="button" type="button" onClick={() => { setStatus("idle"); setOpen(false); }}>Done</button>
              </div>
            ) : (
              <>
                <label className="field">
                  <span>Type</span>
                  <select value={feedbackType} onChange={(event) => setFeedbackType(event.target.value as FeedbackType)}>
                    {TYPES.map((type) => <option key={type.value} value={type.value}>{type.label}</option>)}
                  </select>
                </label>
                <label className="field">
                  <span>Rating, optional</span>
                  <select value={rating} onChange={(event) => setRating(event.target.value ? Number(event.target.value) : "")}>
                    <option value="">No rating</option>
                    {[1, 2, 3, 4, 5].map((value) => <option key={value} value={value}>{value}</option>)}
                  </select>
                </label>
                {!auth.isAuthenticated ? (
                  <label className="field">
                    <span>Email, optional</span>
                    <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" placeholder="you@example.com" />
                  </label>
                ) : null}
                <label className="field">
                  <span>Message</span>
                  <textarea value={message} onChange={(event) => setMessage(event.target.value)} minLength={10} maxLength={4000} required placeholder="What felt broken, confusing, useful, or missing?" />
                </label>
                <p className="muted">Page: {pathname}. Please avoid sharing sensitive personal information.</p>
                {status === "error" ? <p className="form-error">Could not submit feedback. Please try again.</p> : null}
                <button className="button primary" type="submit" disabled={status === "sending"}>{status === "sending" ? "Sending..." : "Submit feedback"}</button>
              </>
            )}
          </form>
        </div>
      ) : null}
    </>
  );
}

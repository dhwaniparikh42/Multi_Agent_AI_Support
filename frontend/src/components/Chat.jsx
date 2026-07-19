import { useEffect, useRef, useState } from 'react'
import { chatAPI } from '../services/api'
import MessageBubble, { TypingIndicator } from './MessageBubble'

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'assistant',
  content: "Hello! I'm your AI Support Assistant. I can help you with:\n\n• 💳 Billing & Payments\n• 🔧 Technical Support\n• 📦 Product Information\n• 📝 Complaints & Escalation\n• ❓ General FAQs\n\nHow can I assist you today?",
  agent_type: 'general',
  created_at: new Date().toISOString()
}

export default function Chat({ sessionId, onSessionCreated }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [typing, setTyping] = useState(false)
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    if (!sessionId) {
      setMessages([WELCOME_MESSAGE])
      return
    }
    setLoading(true)
    chatAPI.getMessages(sessionId)
      .then((res) => setMessages(res.data.length ? res.data : [WELCOME_MESSAGE]))
      .finally(() => setLoading(false))
  }, [sessionId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, typing])

  const sendMessage = async (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text || typing) return
    setInput('')

    // Optimistically add user message
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      created_at: new Date().toISOString()
    }
    setMessages((prev) => [...prev.filter((m) => m.id !== 'welcome'), userMsg])
    setTyping(true)

    try {
      let sid = sessionId
      if (!sid) {
        const res = await chatAPI.createSession(text.slice(0, 50))
        sid = res.data.id
        onSessionCreated(sid)
      }
      const res = await chatAPI.sendMessage(sid, text)
      const aiMsg = res.data.message
      setMessages((prev) => [...prev, aiMsg])
    } catch {
      setMessages((prev) => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        agent_type: 'general',
        created_at: new Date().toISOString()
      }])
    } finally {
      setTyping(false)
      inputRef.current?.focus()
    }
  }

  return (
    <div className="flex flex-col flex-1 h-full overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-3 px-6 py-4 bg-white border-b border-gray-200 shadow-sm">
        <div className="w-9 h-9 bg-blue-600 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <p className="font-semibold text-gray-900 text-sm">AI Support Assistant</p>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 bg-green-500 rounded-full" />
            <span className="text-xs text-gray-500">Online · Multi-Agent System</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-6 py-4 bg-gray-50">
        {loading ? (
          <div className="flex justify-center py-16">
            <svg className="animate-spin h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {typing && <TypingIndicator />}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 px-4 py-4">
        <form onSubmit={sendMessage} className="flex items-end gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  sendMessage(e)
                }
              }}
              placeholder="Type your message… (Enter to send, Shift+Enter for new line)"
              rows={1}
              className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none text-sm transition"
              style={{ minHeight: '46px', maxHeight: '120px' }}
              onInput={(e) => {
                e.target.style.height = 'auto'
                e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
              }}
            />
          </div>
          <button
            type="submit"
            disabled={!input.trim() || typing}
            className="w-11 h-11 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-2xl flex items-center justify-center flex-shrink-0 transition shadow-sm"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
        <p className="text-center text-xs text-gray-400 mt-2">
          Routed by intent to specialized agents — Billing · Technical · Product · Complaints · FAQ
        </p>
      </div>
    </div>
  )
}

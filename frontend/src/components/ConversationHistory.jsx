import { useEffect, useState } from 'react'
import { chatAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'

const AGENT_COLORS = {
  billing: 'bg-yellow-100 text-yellow-700',
  technical: 'bg-blue-100 text-blue-700',
  product: 'bg-green-100 text-green-700',
  complaint: 'bg-red-100 text-red-700',
  faq: 'bg-purple-100 text-purple-700',
  general: 'bg-gray-100 text-gray-700'
}

function formatDate(iso) {
  const d = new Date(iso)
  const now = new Date()
  const diffDays = Math.floor((now - d) / 86400000)
  if (diffDays === 0) return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return d.toLocaleDateString([], { weekday: 'short' })
  return d.toLocaleDateString([], { month: 'short', day: 'numeric' })
}

export default function ConversationHistory({ activeSessionId, onSelectSession, onNewSession }) {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const { user, logout } = useAuth()

  useEffect(() => {
    chatAPI.getSessions()
      .then((res) => setSessions(res.data))
      .finally(() => setLoading(false))
  }, [activeSessionId])

  const handleDelete = async (e, sessionId) => {
    e.stopPropagation()
    await chatAPI.deleteSession(sessionId)
    setSessions((prev) => prev.filter((s) => s.id !== sessionId))
    if (activeSessionId === sessionId) onSelectSession(null)
  }

  return (
    <aside className="w-72 flex-shrink-0 bg-gray-900 text-white flex flex-col h-full">
      {/* Brand */}
      <div className="px-4 py-5 border-b border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-blue-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <p className="font-bold text-sm">AI Support</p>
            <p className="text-xs text-gray-400">Multi-Agent System</p>
          </div>
        </div>
      </div>

      {/* New Chat */}
      <div className="px-3 py-3">
        <button
          onClick={onNewSession}
          className="w-full flex items-center gap-2 px-3 py-2.5 bg-blue-600 hover:bg-blue-700 rounded-xl text-sm font-medium transition"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          New Conversation
        </button>
      </div>

      {/* Sessions list */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-2 pb-2">
        {loading ? (
          <div className="flex justify-center py-8">
            <svg className="animate-spin h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
          </div>
        ) : sessions.length === 0 ? (
          <p className="text-center text-gray-500 text-xs py-8">No conversations yet</p>
        ) : (
          <div className="space-y-1">
            {sessions.map((s) => (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                className={`group flex items-start gap-2 px-3 py-2.5 rounded-xl cursor-pointer transition ${
                  activeSessionId === s.id ? 'bg-gray-700' : 'hover:bg-gray-800'
                }`}
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-100 truncate">{s.title}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    {s.agent_type && (
                      <span className={`text-xs px-1.5 py-0.5 rounded-full font-medium ${AGENT_COLORS[s.agent_type] || AGENT_COLORS.general}`}>
                        {s.agent_type}
                      </span>
                    )}
                    <span className="text-xs text-gray-500">{formatDate(s.updated_at)}</span>
                  </div>
                </div>
                <button
                  onClick={(e) => handleDelete(e, s.id)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-600 rounded-lg transition flex-shrink-0 mt-0.5"
                >
                  <svg className="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* User footer */}
      <div className="px-3 py-3 border-t border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
            {user?.name?.[0]?.toUpperCase() || 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.name}</p>
            <p className="text-xs text-gray-400 truncate">{user?.email}</p>
          </div>
          <button onClick={logout} className="p-1.5 hover:bg-gray-700 rounded-lg transition" title="Sign out">
            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>
  )
}

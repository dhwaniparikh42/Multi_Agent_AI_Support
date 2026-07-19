const AGENT_BADGE = {
  billing: { label: 'Billing Agent', color: 'bg-yellow-100 text-yellow-700 border-yellow-200' },
  technical: { label: 'Technical Agent', color: 'bg-blue-100 text-blue-700 border-blue-200' },
  product: { label: 'Product Agent', color: 'bg-green-100 text-green-700 border-green-200' },
  complaint: { label: 'Complaint Agent', color: 'bg-red-100 text-red-700 border-red-200' },
  faq: { label: 'FAQ Agent', color: 'bg-purple-100 text-purple-700 border-purple-200' },
  general: { label: 'General Agent', color: 'bg-gray-100 text-gray-700 border-gray-200' }
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function renderMarkdown(text) {
  return text
    .split('\n')
    .map((line, i) => {
      // Replace **text** with <strong>
      const parts = line.split(/(\*\*[^*]+\*\*)/g).map((part, j) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={j}>{part.slice(2, -2)}</strong>
        }
        return part
      })
      return <span key={i}>{parts}<br /></span>
    })
}

export function TypingIndicator() {
  return (
    <div className="flex gap-3 mb-4">
      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 self-end">
        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      </div>
      <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
        <div className="flex gap-1 items-center h-5">
          <span className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
          <span className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
          <span className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
        </div>
      </div>
    </div>
  )
}

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const badge = message.agent_type ? AGENT_BADGE[message.agent_type] : null

  if (isUser) {
    return (
      <div className="flex gap-3 mb-4 justify-end">
        <div className="max-w-[75%]">
          <div className="bg-blue-600 text-white rounded-2xl rounded-br-sm px-4 py-3 shadow-sm">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          </div>
          <p className="text-xs text-gray-400 mt-1 text-right">{formatTime(message.created_at)}</p>
        </div>
        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 self-end text-blue-700 font-bold text-sm">
          U
        </div>
      </div>
    )
  }

  return (
    <div className="flex gap-3 mb-4">
      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 self-end">
        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      </div>
      <div className="max-w-[75%]">
        {badge && (
          <span className={`inline-block text-xs font-medium px-2 py-0.5 rounded-full border mb-1 ${badge.color}`}>
            {badge.label}
          </span>
        )}
        <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
          <p className="text-sm leading-relaxed text-gray-800">
            {renderMarkdown(message.content)}
          </p>
        </div>
        <p className="text-xs text-gray-400 mt-1">{formatTime(message.created_at)}</p>
      </div>
    </div>
  )
}

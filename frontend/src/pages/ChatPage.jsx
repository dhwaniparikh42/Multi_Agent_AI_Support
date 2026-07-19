import { useState } from 'react'
import ConversationHistory from '../components/ConversationHistory'
import Chat from '../components/Chat'

export default function ChatPage() {
  const [activeSessionId, setActiveSessionId] = useState(null)

  const handleNewSession = () => setActiveSessionId(null)

  return (
    <div className="flex h-screen overflow-hidden">
      <ConversationHistory
        activeSessionId={activeSessionId}
        onSelectSession={setActiveSessionId}
        onNewSession={handleNewSession}
      />
      <main className="flex-1 flex flex-col overflow-hidden">
        <Chat
          sessionId={activeSessionId}
          onSessionCreated={(id) => setActiveSessionId(id)}
        />
      </main>
    </div>
  )
}

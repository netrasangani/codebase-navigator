import { useState } from "react"
import "./App.css"

function App() {
  const [repoUrl, setRepoUrl] = useState("")
  const [repoName, setRepoName] = useState("")
  const [repoStats, setRepoStats] = useState(null)
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const [repoIndexed, setRepoIndexed] = useState(false)

  const API_URL = "http://127.0.0.1:8000"

  async function indexRepository() {
    if (!repoUrl.trim()) {
      setMessage("Enter a GitHub repository URL first.")
      setRepoIndexed(false)
      return
    }

    setLoading(true)
    setMessage("")
    setRepoIndexed(false)

    try {
      const response = await fetch(`${API_URL}/repository`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: repoUrl,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setRepoIndexed(true)
        setMessage("")
        setMessages([])

        const parts = repoUrl
          .replace(/\/$/, "")
          .split("/")

        setRepoName(
          `${parts[parts.length - 2]}/${parts[parts.length - 1]}`
        )

        setRepoStats(data.stats)
      } else {
        setMessage(
          data.error || "Failed to index repository."
        )
      }
    } catch (error) {
      setMessage("Could not connect to the backend.")
    }

    setLoading(false)
  }

  function clearChat() {
    setMessages([])
    setMessage("")
    setQuestion("")
  }

  async function askQuestion(customQuestion = question) {
    if (!repoIndexed) {
      setMessage("Index a repository before asking questions.")
      return
    }

    if (!customQuestion.trim()) {
      setMessage("Enter a question first.")
      return
    }

    const currentQuestion = customQuestion.trim()

    setQuestion("")
    setMessage("")
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setMessages((previousMessages) => [
          ...previousMessages,
          {
            question: currentQuestion,
            answer: data.answer,
            sources: data.sources,
          },
        ])
      } else {
        setMessage(
          data.error || "Something went wrong."
        )
      }
    } catch (error) {
      setMessage("Could not connect to the backend.")
    }

    setLoading(false)
  }

  function getSources(sourceText) {
    if (!sourceText) {
      return []
    }

    return sourceText
      .split("\n\n--- CODE CHUNK ---\n\n")
      .filter((source) => source.trim())
  }

  function getFileName(source) {
    const firstLine = source.split("\n")[0]

    if (firstLine.startsWith("FILE:")) {
      const filePath = firstLine
        .replace("FILE:", "")
        .trim()

      const parts = filePath.split("/")

      return parts[parts.length - 1]
    }

    return "Repository source"
  }

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div className="brand">

          <div className="brand-mark">
            &lt;/&gt;
          </div>

          <div>
            <div className="logo">
              Codebase <span>Navigator</span>
            </div>

            <div className="brand-subtitle">
              AI-powered repository explorer
            </div>
          </div>

        </div>

        <div className="header-status">
          <span className="status-dot"></span>
          Local AI
        </div>

      </header>


      <div className="workspace">

        {/* SIDEBAR */}

        <aside className="sidebar">

          <div className="sidebar-heading">
            <span>01</span>
            Repository
          </div>

          <div className="repo-card">

            <label className="label">
              GitHub URL
            </label>

            <input
              type="text"
              placeholder="https://github.com/user/repo"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
            />

            <button
              className="primary-button"
              onClick={indexRepository}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Indexing
                </>
              ) : (
                <>
                  Index Repository
                  <span>→</span>
                </>
              )}
            </button>


            {/* REPOSITORY STATUS */}

            {repoIndexed && (
              <div className="success-status">

                <span className="check">
                  ✓
                </span>

                <div>
                  <strong>
                    {repoName || "Repository ready"}
                  </strong>

                  <small>
                    Codebase indexed successfully
                  </small>
                </div>

              </div>
            )}


            {/* REPOSITORY STATS */}

            {repoIndexed && repoStats && (
              <div className="repo-stats">

                <div className="stats-row">

                  <div className="stat-item">

                    <span className="stat-value">
                      {repoStats.files}
                    </span>

                    <span className="stat-label">
                      FILES
                    </span>

                  </div>


                  <div className="stat-divider"></div>


                  <div className="stat-item">

                    <span className="stat-value">
                      {repoStats.chunks}
                    </span>

                    <span className="stat-label">
                      CHUNKS
                    </span>

                  </div>

                </div>


                <div className="embedding-info">

                  <span className="embedding-label">
                    EMBEDDING MODEL
                  </span>

                  <span className="embedding-model">
                    {repoStats.embedding_model}
                  </span>

                </div>

              </div>
            )}


            {message && (
              <div className="status">
                {message}
              </div>
            )}

          </div>


          <div className="sidebar-divider"></div>


          {/* PIPELINE */}

          <div className="sidebar-heading">
            <span>02</span>
            How it works
          </div>

          <div className="pipeline">

            <div className="pipeline-item">

              <div className="pipeline-number">
                1
              </div>

              <div>
                <strong>
                  Clone
                </strong>

                <small>
                  Fetch repository
                </small>
              </div>

            </div>


            <div className="pipeline-line"></div>


            <div className="pipeline-item">

              <div className="pipeline-number">
                2
              </div>

              <div>
                <strong>
                  Embed
                </strong>

                <small>
                  Create code vectors
                </small>
              </div>

            </div>


            <div className="pipeline-line"></div>


            <div className="pipeline-item">

              <div className="pipeline-number">
                3
              </div>

              <div>
                <strong>
                  Retrieve
                </strong>

                <small>
                  Find relevant code
                </small>
              </div>

            </div>


            <div className="pipeline-line"></div>


            <div className="pipeline-item">

              <div className="pipeline-number">
                4
              </div>

              <div>
                <strong>
                  Answer
                </strong>

                <small>
                  Generate response
                </small>
              </div>

            </div>

          </div>

        </aside>


        {/* MAIN */}

        <main className="main">

          {/* HERO */}

          <section className="hero">

            <div className="hero-eyebrow">
              CODE INTELLIGENCE
            </div>

            <h1>
              Understand your
              <span> codebase.</span>
            </h1>

            <p>
              Ask questions in plain English and navigate your
              repository using AI-powered semantic search.
            </p>

          </section>


          {/* QUESTION CARD */}

          <section className="question-card">

            <div className="question-top">

              <div>

                <div className="question-label">
                  Ask your codebase
                </div>

                <div className="question-hint">
                  Search through indexed source code
                </div>

              </div>

              <div className="rag-indicator">
                <span></span>
                RAG SEARCH
              </div>

            </div>


            <div className="question-row">

              <input
                type="text"
                placeholder="e.g. Where is authentication handled?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    askQuestion()
                  }
                }}
              />

              <button
                className="ask-button"
                onClick={() => askQuestion()}
                disabled={loading}
              >
                {loading ? "Searching..." : "Ask AI"}

                {!loading && (
                  <span>
                    ↗
                  </span>
                )}

              </button>

            </div>


            <div className="suggestions">

              <span>
                Try asking:
              </span>

              <button
                onClick={() =>
                  askQuestion(
                    "Where is authentication handled?"
                  )
                }
              >
                Where is authentication handled?
              </button>

              <button
                onClick={() =>
                  askQuestion(
                    "What are the main classes?"
                  )
                }
              >
                What are the main classes?
              </button>

              <button
                onClick={() =>
                  askQuestion(
                    "How does this project work?"
                  )
                }
              >
                How does this project work?
              </button>

            </div>

          </section>


          {/* EMPTY STATE */}

          {messages.length === 0 && !loading && (
            <section className="empty-state">

              <div className="empty-icon">

                <span>&lt;</span>
                <span>/</span>
                <span>&gt;</span>

              </div>

              <h2>
                Your codebase, ready to explore
              </h2>

              <p>
                Index a repository and start asking questions.
                Your conversation and relevant source code will
                appear here.
              </p>

            </section>
          )}


          {/* LOADING */}

          {loading && (
            <section className="loading-card">

              <div className="loading-animation">

                <span></span>
                <span></span>
                <span></span>

              </div>

              <strong>
                Searching your codebase
              </strong>

              <p>
                Finding the most relevant code...
              </p>

            </section>
          )}


          {/* CONVERSATION */}

          {messages.length > 0 && (
            <div className="conversation">

              <div className="conversation-header">

                <div>

                  <strong>
                    Conversation
                  </strong>

                  <small>
                    {messages.length} question
                    {messages.length !== 1 ? "s" : ""}
                  </small>

                </div>

                <button
                  className="clear-button"
                  onClick={clearChat}
                >
                  Clear Chat
                </button>

              </div>


              {messages.map((item, index) => {

                const sources = getSources(
                  item.sources
                )

                return (
                  <div
                    className="conversation-item"
                    key={index}
                  >

                    {/* USER */}

                    <div className="user-message">

                      <div className="message-avatar">
                        You
                      </div>

                      <div className="message-content">
                        {item.question}
                      </div>

                    </div>


                    {/* AI */}

                    <div className="ai-message">

                      <div className="message-avatar ai-avatar">
                        AI
                      </div>

                      <div className="ai-content">

                        <div className="ai-label">
                          Codebase Navigator
                        </div>

                        <div className="answer">
                          {item.answer}
                        </div>

                      </div>

                    </div>


                    {/* SOURCES */}

                    {sources.length > 0 && (
                      <div className="sources-section">

                        <div className="sources-section-header">

                          <div>

                            <strong>
                              Retrieved Sources
                            </strong>

                            <small>
                              Top {sources.length} relevant code chunks
                              from FAISS
                            </small>

                          </div>

                          <span className="result-badge">
                            {sources.length} RESULTS
                          </span>

                        </div>


                        <div className="source-list">

                          {sources.map(
                            (source, sourceIndex) => {

                              const fileName =
                                getFileName(source)

                              return (
                                <div
                                  className="source-card"
                                  key={sourceIndex}
                                >

                                  <div className="source-header">

                                    <div className="source-title">

                                      <span>
                                        &lt;/&gt;
                                      </span>

                                      <div>

                                        <strong>
                                          {fileName}
                                        </strong>

                                        <small>
                                          Retrieved code chunk
                                        </small>

                                      </div>

                                    </div>

                                    <span className="source-number">
                                      #{sourceIndex + 1}
                                    </span>

                                  </div>

                                  <div className="source-container">

                                    <pre>
                                      {source}
                                    </pre>

                                  </div>

                                </div>
                              )
                            }
                          )}

                        </div>

                      </div>
                    )}

                  </div>
                )
              })}

            </div>
          )}

        </main>

      </div>

    </div>
  )
}

export default App
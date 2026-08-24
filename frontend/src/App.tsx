import { useMemo, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import redsoftLogo from './assets/brand/logo-dark.png'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ''
const ACCEPTED_TYPES = '.pdf,.jpg,.jpeg,.png,.txt,.md'

type SummarizeResponse = {
  filename: string
  contentType: string
  summary: string
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [textPreview, setTextPreview] = useState<string | null>(null)
  const [result, setResult] = useState<SummarizeResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const isTextFile = useMemo(
    () => file?.type.startsWith('text/') || /\.(txt|md)$/i.test(file?.name ?? ''),
    [file],
  )

  function resetForNewFile(selected: File | null) {
    setResult(null)
    setError(null)
    setTextPreview(null)
    if (previewUrl) URL.revokeObjectURL(previewUrl)

    if (!selected) {
      setFile(null)
      setPreviewUrl(null)
      return
    }

    setFile(selected)
    if (selected.type.startsWith('text/') || /\.(txt|md)$/i.test(selected.name)) {
      selected.text().then(setTextPreview)
      setPreviewUrl(null)
    } else {
      setPreviewUrl(URL.createObjectURL(selected))
    }
  }

  async function handleSummarize() {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await fetch(`${API_BASE}/api/summarize`, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail ?? `Request failed with status ${response.status}`)
      }
      setResult(data as SummarizeResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1>AI Powered IVF Report Summary</h1>
          <p>Upload a report and get accurate summary in seconds!</p>
        </div>
        <img src={redsoftLogo} alt="Redsoft" className="brand-logo" />
      </header>

      <main className="layout">
        <section className="panel">
          <h2>Report</h2>
          <div className="upload-controls">
            <input
              ref={fileInputRef}
              type="file"
              accept={ACCEPTED_TYPES}
              onChange={(e) => resetForNewFile(e.target.files?.[0] ?? null)}
            />
            <button
              type="button"
              className="generate-btn"
              disabled={!file || loading}
              onClick={handleSummarize}
            >
              {loading && <span className="spinner" aria-hidden="true" />}
              {loading ? 'Summarizing…' : 'Generate Summary'}
            </button>
          </div>

          <div className="preview">
            {!file && <p className="hint">No file selected.</p>}
            {file && previewUrl && file.type === 'application/pdf' && (
              <iframe
                src={previewUrl}
                title="Report preview"
                className="pdf-preview fade-in"
              />
            )}
            {file && previewUrl && file.type.startsWith('image/') && (
              <img
                src={previewUrl}
                alt="Report preview"
                className="image-preview fade-in"
              />
            )}
            {file && isTextFile && textPreview !== null && (
              <pre className="text-preview fade-in">{textPreview}</pre>
            )}
          </div>
        </section>

        <section className="panel">
          <h2>Summary</h2>
          {error && <p className="error fade-in">{error}</p>}
          {loading && (
            <p className="hint loading-hint fade-in">
              <span className="spinner" aria-hidden="true" />
              Generating summary…
            </p>
          )}
          {!loading && !error && !result && (
            <p className="hint">Upload a report and click Generate Summary.</p>
          )}
          {result && (
            <div className="summary fade-in">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {result.summary}
              </ReactMarkdown>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App

import { useRef, useState } from 'react'

export function useAudioRecorder() {
  const recorderRef = useRef<MediaRecorder | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const [isRecording, setIsRecording] = useState(false)

  async function start() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    streamRef.current = stream
    chunksRef.current = []
    recorderRef.current = new MediaRecorder(stream)
    recorderRef.current.ondataavailable = event => {
      chunksRef.current.push(event.data)
    }
    recorderRef.current.start()
    setIsRecording(true)
  }

  function stop(): Promise<File> {
    return new Promise((resolve, reject) => {
      const recorder = recorderRef.current
      if (!recorder) {
        reject(new Error('Gravador não iniciado.'))
        return
      }

      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        const file = new File([blob], 'recording.webm', { type: 'audio/webm' })
        cleanup()
        resolve(file)
      }

      recorder.stop()
    })
  }

  function cancel() {
    if (recorderRef.current?.state === 'recording') {
      recorderRef.current.stop()
    }
    cleanup()
  }

  function cleanup() {
    setIsRecording(false)
    streamRef.current?.getTracks().forEach(track => track.stop())
    streamRef.current = null
    recorderRef.current = null
    chunksRef.current = []
  }

  return { isRecording, start, stop, cancel }
}

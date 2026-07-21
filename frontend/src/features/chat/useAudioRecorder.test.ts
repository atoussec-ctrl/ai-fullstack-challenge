import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { useAudioRecorder } from './useAudioRecorder'

class FakeMediaRecorder {
  state: 'inactive' | 'recording' = 'inactive'
  ondataavailable: ((event: { data: Blob }) => void) | null = null
  onstop: (() => void) | null = null
  stream: MediaStream

  constructor(stream: MediaStream) {
    this.stream = stream
  }

  start() {
    this.state = 'recording'
  }

  stop() {
    this.state = 'inactive'
    this.ondataavailable?.({ data: new Blob(['chunk']) })
    this.onstop?.()
  }
}

function stubMicrophoneAccess() {
  const track = { stop: vi.fn() }
  const stream = { getTracks: () => [track] } as unknown as MediaStream
  const getUserMedia = vi.fn().mockResolvedValue(stream)

  vi.stubGlobal('navigator', { ...navigator, mediaDevices: { getUserMedia } })
  vi.stubGlobal('MediaRecorder', FakeMediaRecorder)

  return { track, getUserMedia }
}

describe('useAudioRecorder', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('starts recording and exposes isRecording', async () => {
    stubMicrophoneAccess()
    const { result } = renderHook(() => useAudioRecorder())

    await act(async () => {
      await result.current.start()
    })

    expect(result.current.isRecording).toBe(true)
  })

  it('stops the microphone stream when the component unmounts mid-recording', async () => {
    const { track } = stubMicrophoneAccess()
    const { result, unmount } = renderHook(() => useAudioRecorder())

    await act(async () => {
      await result.current.start()
    })
    unmount()

    expect(track.stop).toHaveBeenCalledTimes(1)
  })

  it('does not attempt to stop any track on unmount if recording was never started', () => {
    const { unmount } = renderHook(() => useAudioRecorder())

    expect(() => unmount()).not.toThrow()
  })

  it('does not stop the microphone twice when unmounting after an explicit stop()', async () => {
    const { track } = stubMicrophoneAccess()
    const { result, unmount } = renderHook(() => useAudioRecorder())

    await act(async () => {
      await result.current.start()
    })
    await act(async () => {
      await result.current.stop()
    })
    unmount()

    expect(track.stop).toHaveBeenCalledTimes(1)
  })
})

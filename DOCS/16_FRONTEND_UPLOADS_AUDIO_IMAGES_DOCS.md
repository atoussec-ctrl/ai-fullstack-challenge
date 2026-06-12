# Uploads — Áudio, Imagens e Documentos

## Objetivo

Permitir que o usuário envie contexto adicional para o assistente Python.

## Tipos suportados

| Tipo | MIME/extensão | Uso |
|---|---|---|
| Documento | `.txt`, `.md`, `.py`, `.json`, `.pdf` | Contexto textual |
| Imagem | `png`, `jpg`, `webp` | Prints e diagramas |
| Áudio | `webm`, `wav`, `mp3` | Perguntas faladas |

## Validação no frontend

- Tamanho máximo por arquivo: 10 MB no MVP.
- Quantidade máxima: 5 arquivos por mensagem.
- Bloquear extensões perigosas.
- Mostrar erro antes de enviar.
- Permitir remover arquivo antes do envio.

## Hook de seleção de arquivo

```tsx
import { useState } from "react";

export interface PendingAttachment {
  id: string;
  file: File;
  previewUrl?: string;
}

export function usePendingAttachments() {
  const [attachments, setAttachments] = useState<PendingAttachment[]>([]);

  function addFiles(files: FileList | File[]) {
    const next = Array.from(files).map((file) => ({
      id: crypto.randomUUID(),
      file,
      previewUrl: file.type.startsWith("image/")
        ? URL.createObjectURL(file)
        : undefined,
    }));

    setAttachments((current) => [...current, ...next]);
  }

  function removeAttachment(id: string) {
    setAttachments((current) => current.filter((item) => item.id !== id));
  }

  return {
    attachments,
    addFiles,
    removeAttachment,
  };
}
```

## Gravação de áudio

Usar `MediaRecorder` do browser.

Fluxo:

```txt
Usuário clica no microfone
  ↓
Browser solicita permissão
  ↓
Gravação começa
  ↓
Usuário para ou cancela
  ↓
Arquivo de áudio vira attachment
  ↓
Mensagem é enviada
```

## Hook de áudio

```tsx
import { useRef, useState } from "react";

export function useAudioRecorder() {
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const [isRecording, setIsRecording] = useState(false);

  async function start() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    chunksRef.current = [];
    recorderRef.current = new MediaRecorder(stream);

    recorderRef.current.ondataavailable = (event) => {
      chunksRef.current.push(event.data);
    };

    recorderRef.current.start();
    setIsRecording(true);
  }

  function stop(): Promise<File> {
    return new Promise((resolve) => {
      const recorder = recorderRef.current;

      if (!recorder) {
        throw new Error("Gravador não iniciado.");
      }

      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const file = new File([blob], "recording.webm", { type: "audio/webm" });
        setIsRecording(false);
        resolve(file);
      };

      recorder.stop();
    });
  }

  return {
    isRecording,
    start,
    stop,
  };
}
```

## Segurança

- Não renderizar PDF diretamente sem sandbox.
- Não executar arquivos enviados.
- Não confiar no MIME informado pelo browser.
- Backend deve revalidar tudo.
- Remover previews com `URL.revokeObjectURL`.

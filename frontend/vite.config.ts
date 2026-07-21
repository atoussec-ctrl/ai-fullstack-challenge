import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  // VITE_BASE_URL is set by the deploy workflow for GitHub Pages (e.g. /AI_PYTHON_TEST_FULLSTACK/)
  // Falls back to '/' for local development
  base: process.env.VITE_BASE_URL ?? '/',
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3002,
    strictPort: true,
    proxy: {
      '/api': {
        target: process.env.VITE_API_PROXY_TARGET ?? 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: true,
    include: ['src/**/*.test.{ts,tsx}'],
    exclude: ['node_modules', 'dist', 'e2e'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'text-summary'],
      include: ['src/features/**/*.{ts,tsx}', 'src/shared/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.test.{ts,tsx}',
        'src/test/**',
        'src/**/*.stories.tsx',
        'src/features/chat/useAudioRecorder.ts',
        // types.ts contains only TypeScript type declarations — no executable code to cover
        'src/shared/api/types.ts',
      ],
      // Alvo é 95% (ver plano de melhorias). branches fica em 90% porque
      // handleDragEnd em ChatSessionRow.tsx só é acionado pelo prop sintético
      // onDragEnd do Framer Motion (não um evento DOM real) — não dá para
      // exercitar via fireEvent sem reintroduzir hacks de fiber do React.
      // A lógica de decisão em si (resolveSwipeAction) já é 100% testada;
      // o gesto de arrastar real fica coberto pelo Playwright E2E.
      thresholds: {
        lines: 94,
        functions: 93,
        branches: 90,
        statements: 92,
      },
    },
  },
})

"use client"

import { LoginForm } from "@/components/auth/LoginForm"

export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900">CareerNavigator</h1>
        <p className="mt-2 text-gray-600">Your AI-powered career transition platform</p>
      </div>
      <LoginForm />
    </main>
  )
}

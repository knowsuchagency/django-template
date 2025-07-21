import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">Welcome Home</h1>
      <Button>Click me</Button>
    </div>
  )
}
export default function Contact() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">Contact Us</h1>
      <div className="max-w-md w-full space-y-4">
        <p className="text-gray-600">Get in touch with us:</p>
        <ul className="space-y-2">
          <li>Email: hello@example.com</li>
          <li>Phone: +1 (555) 123-4567</li>
          <li>Address: 123 Main St, City, State 12345</li>
        </ul>
      </div>
    </div>
  )
}
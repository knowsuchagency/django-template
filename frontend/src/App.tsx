import { Routes, Route } from "react-router"
import Layout from "@/components/Layout"
import Home from "@/pages/Home"
import About from "@/pages/About"
import Contact from "@/pages/Contact"

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="contact" element={<Contact />} />
      </Route>
    </Routes>
  )
}

export default App

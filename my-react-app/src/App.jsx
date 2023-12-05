//import Navbar from "./Navbar"
import Art from "./pages/Art"
import Home from "./pages/Home"
import Profile from "./pages/Profile"
import Header from "./Header"
import { Route, Routes } from "react-router-dom"

function App() {
  return (
    <>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/Art" element={<Art />} />
        </Routes>
      </div>
    </>
  )
}

export default App
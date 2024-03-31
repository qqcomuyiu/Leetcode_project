//import Navbar from "./Navbar"
import Art from "./pages/Art"
import Home from "./pages/Home"
import RoutePlanner from "./pages/RoutePlanner"
import Header from "./Header"
import { Route, Routes } from "react-router-dom"

function App() {
  return (
    <>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/route" element={<RoutePlanner />} />
          <Route path="/account" element={<Art />} />
        </Routes>
      </div>
    </>
  )
}

export default App
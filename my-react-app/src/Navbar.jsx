import { Link, useMatch, useResolvedPath } from "react-router-dom"
import './Navbar.css'

export default function Navbar() {
  return (
    <nav className="nav">
      <ul>
        <Link to="/route">Route Planner</Link>
        <Link to="/account">Account</Link>
      </ul>
    </nav>
  )
}


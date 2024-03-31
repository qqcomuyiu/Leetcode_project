import './Header.css'
import Navbar from './Navbar';
import { Link} from "react-router-dom"

//import {Route , Routes} from "react-router-dom "


function Header(){
    return (
        <header>
            <Link to="/" className="site-title"> NYC Transit App</Link>
            <Navbar/>
        </header>
    );

}

export default Header
import {useState} from 'react'
import './Profile.css'

function Profile(){
   const [Movies, setMovies] = useState([])
   const [Books, setBooks] = useState([])
   const [TV, setTV] = useState([])
   const [Albums, setAlbums] = useState([])
   const [inputValue, setInputValue] = useState('');
   const [selectedMedium, setSelectedMedium] = useState('');
   const MAX_LENGTH = 3;

   const handleInputChange = (e) => {
      setInputValue(e.target.value);
   };
  
   const addTo = () => {
       if(inputValue){
         if(selectedMedium == 'TV' && TV.length< MAX_LENGTH){
             setTV([...TV, inputValue])
         }
         if(selectedMedium == 'Albums' && Albums.length< MAX_LENGTH){
            setAlbums([...Albums, inputValue])
         }
         if(selectedMedium == 'Movie' && Movies.length< MAX_LENGTH){
            setMovies([...Movies, inputValue])
         }
         if(selectedMedium == 'Books' && Books.length< MAX_LENGTH){
            setBooks([...Books, inputValue])
         }
       }

    }

   const Add = () =>{    
      return(
         <>
         <form >
         <label>Enter a movie:
         <input
            type="text" 
            value={inputValue}
            onChange={handleInputChange}
         />
         </label>
         </form>
         <label for="artMedium">Medium of Art:</label>
         <select 
            value = {selectedMedium}
            onChange ={e=> setSelectedMedium(e.target.value)} >
            <option value="TV">TV</option>
            <option value="Movie">Movie</option>
            <option value="Albums">Albums</option>
            <option value="Books">Books</option>
         </select>
         <br></br>
         <button onClick={addTo} >
            Add
         </button>
         </>
      )
    }
  

   return( 
      <>      
      <h1>Profile</h1>
      {Add()}
      <div>

      </div>
      <div className='movies'>
         <h2>Movie List</h2>
         <ul>
         {Movies.map((movie) => <li>{movie}</li> )}
         </ul>
      </div>
      <div className='books'>
         <h2>Book List</h2>
         <ul>
         {Books.map((book) => <li>{book}</li> )}
         </ul>
      </div>
      <div className='TV'>
         <h2>TV List</h2>
         <ul>
         {TV.map((tv) => <li>{tv}</li> )}
         </ul>
      </div>
      <div className='Albums'>
         <h2>Albums List</h2>
         <ul>
         {Albums.map((album) => <li>{album}</li> )}
         </ul>
      </div>
      </>
   )


}

export default Profile
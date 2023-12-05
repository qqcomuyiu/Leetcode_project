import { useEffect, useState } from "react"
import TableComponent from './TableComponent.jsx';
import './Art.css'
import { DeleteButton } from './DeleteButton.jsx';


function Art(){
   const [inputValue, setInputValue] = useState('')
   const [selectedMedium, setSelectedMedium] = useState('TV')
   const [rating, setRating] = useState('10')
   const [art, setArt] = useState([])
   const [status, setStatus] =useState('Completed')

   useEffect(() => {
      localStorage.setItem("ITEMS", JSON.stringify(art))
   }, [art])
  

   const handleInputChange = (e) => {
      setInputValue(e.target.value);
   };

   const handleRatingChange = (e) => {
      setRating(e.target.value);
   };


   const Add = () => {
      return(
         <>
         <form>
            <label>Enter the Title </label>
            <input
            type="text" 
            value={inputValue}
            onChange={handleInputChange}
            />
         </form>
         <form>
            <label>Enter Rating </label>
            <input
            type="number" 
            min="1"
            max ="10"
            step = "0.5"
            value={rating}
            onChange={handleRatingChange}
            />
         </form>
         <label htmlFor="artMedium">Medium of Art:</label>
         <select 
            value = {selectedMedium}
            onChange ={e=> setSelectedMedium(e.target.value)} >
            <option value="TV">TV</option>
            <option value="Movie">Movie</option>
            <option value="Albums">Albums</option>
            <option value="Books">Books</option>
         </select>
         <label htmlFor="artStatus">Status:</label>
         <select 
            value = {status}
            onChange ={e=> setStatus(e.target.value)} >
            <option value="Completed">Completed</option>
            <option value="Plan To Watch">Plan To Watch</option>
            <option value="Watching">Watching</option>
         </select>
         <br></br>
         <button onClick={addTo} >
            Add
         </button>
         </>
      )
   }

   const addTo = () => {
         if(inputValue){
            let art_thing= {id: inputValue, Title: inputValue, Medium: selectedMedium, Rating: rating, Status: status, delete: <DeleteButton id = {inputValue} deleteTodo={deleteTodo}/>}
            setArt([...art, art_thing])
            //alert("added")
            setInputValue("")
         }
  
   }

   function deleteTodo(id) {
      setArt(currentTodos => {
        return currentTodos.filter(todo => todo.id !== id)
      })
    }

   return( 
      <>
      <h1> Art</h1>
      {Add()}
      <h1> My art</h1>
      <TableComponent data={art} />

      </> 
   )


}


export default Art

import React from 'react';


export function DeleteButton({id, deleteTodo}){

    return(
        <>
        <button
        onClick={() => deleteTodo(id)}>
            Delete
        </button>
        </>
    )

}

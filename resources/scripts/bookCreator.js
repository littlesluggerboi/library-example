import Book from "./Book.js";

export default function BookCreator(){
    const form = document.querySelector("form");
    let currentId = 0;
    //getFormElement
    const getFormElement = () =>{
        return form;
    }
    
    //create
    const create = () =>{
        const title = form.elements["title"].value;
        const author = form.elements["author"].value;
        const description = form.elements["description"];
        const genre = form.elements["genre"];
        const year = form.elements["year"];
        const newBook = new Book(title, author, description, genre, year, currentId++);
        form.reset();
        return newBook;
    }

    return {create, getFormElement};
    
}
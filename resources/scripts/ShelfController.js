import Shelf from "./Shelf.js";
import BookController from "./BookContoller.js";

export default function ShelfController(){
    const bookShelf = new Shelf();
    const bookDisplay = document.querySelector(".book");
    const bookDisplays = new Map();
    
    //removeBook;
    const deleteBookDisplay = (bookId)=>{
        bookDisplays.get(bookId).deleteDisplay();
    }

    const removeBook = (event) =>{
        const targetElement = event.target;
        const bookId = targetElement.id;
        deleteBookDisplay(bookId);
        bookDisplays.delete(bookId);
        bookShelf.removeBook(bookId);
    }

    //addBook;
    const addBook = (book) =>{
        const newBookDisplay = new BookController(book);
        const bookId = book.getId();
        bookShelf.addBook(book);
        bookDisplays.set(bookId, newBookDisplay);
        newBookDisplay.createDisplay();
        const bookHtmlElement = newBookDisplay.getDisplay();
        //TODO addevent listener removeBook to the book html element.
        bookDisplay.prepend(bookHtmlElement);
    }

    return {addBook};
}
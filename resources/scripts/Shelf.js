import Book from "./Book.js";
export default function Shelf(){
    const bookShelf = new Map();
    
    const getBook = (value)=>{
        const book = bookShelf.get(value);
        if(book == null){
            throw new Error("Cannot find book with specified id: " + value);
        }
        return book;
    }

    const addBook = (value) =>{
        if(value instanceof Book){
            bookShelf.set(value.getId(), value);
            return true;
        }
        return false;
    }
    
    const removeBook = (value) =>{
        return bookShelf.delete(value);
    }

    const clearShelf = () =>{
        bookShelf.clear();
    }

    return {getBook, addBook, removeBook, clearShelf};
}
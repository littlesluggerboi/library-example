import Book from "./Book.js";

export default function BookController(book) {
  if (!(book instanceof Book)) {
    throw new Error("Pass a Book instance");
  }
  const bookReference = book;
  let htmlElementReference;
  //createDisplay;
  const createDisplay = () => {
    if (htmlElementReference != null) {
      throw new Error("Book already got a display");
    }
    const newDisplay = document.createElement("div");
    newDisplay.id = book.getId();
    newDisplay.classList.add("book");
    htmlElementReference = newDisplay;
  };

  //deleteDisplay;
  const deleteDisplay = () => {
    if (htmlElementReference != null) {
      htmlElementReference.remove();
    }
  };
  //hoverOverDisplay

  //getDisplay;
  const getDisplay = ()=>{
    if(htmlElementReference == null){
        throw new Error("Display not yet created");
    }
    return htmlElementReference;
  }

  return {createDisplay, deleteDisplay, getDisplay};
}

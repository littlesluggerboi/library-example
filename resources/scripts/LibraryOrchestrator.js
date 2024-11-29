function Book(
  bookTitle,
  bookAuthor,
  bookDescription,
  bookGenre,
  bookYear,
  bookNumber
) {
  let title;
  let author;
  let description;
  let read = false;
  let genre;
  let year;
  let id;

  const validateStringInput = (value, errorMessage) => {
    if (value != null && value.toString().length > 0) {
      return value.toString();
    } else {
      throw new Error(errorMessage);
    }
  };

  const checkField = (value, fieldName) => {
    if (value == null) {
      throw new Error(fieldName + " field is undefined");
    }
  };

  const setTitle = (value) => {
    title = validateStringInput(value, "A bad title");
  };

  const getTitle = () => {
    checkField(title, "Title");
    return title;
  };

  const setAuthor = (value) => {
    author = validateStringInput(value, "Bad author");
  };

  const getAuthor = () => {
    checkField(author, "Author");
    return author;
  };

  const setDescription = (value) => {
    description = validateStringInput(value, "Bad description");
  };

  const getDescription = () => {
    checkField(description, "Description");
  };

  const toggleIsRead = () => {
    read = !read;
  };
  const isRead = () => {
    return read;
  };

  const setGenre = (value) => {
    genre = validateStringInput(value, "Bad Genre");
  };

  const getGenre = () => {
    checkField(genre, "Genre");
    return genre;
  };

  const validIntInput = (value) => {
    console.log(value);
    value = parseInt(value);
    console.log(value);
    if(isNaN(value)){
        throw new Error("Not a number");
    }
    return value;
  };

  const setYear = (value) => {
    value = validIntInput(value);
    if (value < 1900 || value > 2040) {
      throw new Error("Year out of Range");
    }
    year = value;
  };

  const getYear = () => {
    checkField(year, "Year");
    return year;
  };

  const setId = (value) => {
    if (value == null) {
      throw new Error("bookNumber Cannot be null");
    }
    id = value;
  };

  const getId = () => {
    checkField(id, "bookNumber");
    return id;
  };
  setId(bookNumber);
  setTitle(bookTitle);
  setAuthor(bookAuthor);
  setDescription(bookDescription);
  setGenre(bookGenre);
  setYear(bookYear);

  return {
    setTitle,
    getTitle,
    getAuthor,
    setAuthor,
    getDescription,
    setDescription,
    getGenre,
    setGenre,
    toggleIsRead,
    isRead,
    setYear,
    getYear,
    getId,
  };
}

function Shelf() {
  const bookShelf = new Map();

  const getBook = (value) => {
    const book = bookShelf.get(value);
    if (book == null) {
      throw new Error("Cannot find book with specified id: " + value);
    }
    return book;
  };

  const addBook = (value) => {
    if (value instanceof Book) {
      bookShelf.set(value.getId(), value);
      return true;
    }
    return false;
  };

  const removeBook = (value) => {
    return bookShelf.delete(value);
  };

  const clearShelf = () => {
    bookShelf.clear();
  };

  return { getBook, addBook, removeBook, clearShelf };
}

function BookController(book) {
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
      htmlElementReference = null;
    }
  };
  //hoverOverDisplay

  //getDisplay;
  const getDisplay = () => {
    if (htmlElementReference == null) {
      throw new Error("Display not yet created");
    }
    return htmlElementReference;
  };

  return { createDisplay, deleteDisplay, getDisplay };
}

function ShelfController() {
  const bookShelf = new Shelf();
  const shelfDisplay = document.querySelector(".shelf");
  const bookDisplays = new Map();

  //removeBook;
  const deleteBookDisplay = (bookId) => {
    bookDisplays.get(bookId).deleteDisplay();
  };

  const removeBook = (event) => {
    const targetElement = event.target;
    const bookId = targetElement.id;
    deleteBookDisplay(bookId);
    bookDisplays.delete(bookId);
    bookShelf.removeBook(bookId);
  };

  //addBook;
  const addBook = (book) => {
    const newBookDisplay = new BookController(book);
    const bookId = book.getId();
    bookShelf.addBook(book);
    bookDisplays.set(bookId, newBookDisplay);
    newBookDisplay.createDisplay();
    const bookHtmlElement = newBookDisplay.getDisplay();
    //TODO addevent listener removeBook to the book html element.
    shelfDisplay.prepend(bookHtmlElement);
  };

  return { addBook };
}

function BookCreator() {
  const form = document.querySelector("form#book-form");
  console.log(form);
  let currentId = 0;
  //getFormElement
  const getFormElement = () => {
    return form;
  };

  //create
  const create = () => {

    const title = form.elements["title"].value;
    const author = form.elements["author"].value;
    const description = form.elements["description"].value;
    const genre = form.elements["genre"].value;
    const year = form.elements["year"].value;
    console.log(title, author, description, genre, year);
    const newBook = new Book(
      title,
      author,
      description,
      genre,
      year,
      currentId++
    );
    form.reset();
    return newBook;
  };

  return { create, getFormElement };
}

function LibraryOrchestrator() {
  const bookCreator = new BookCreator();
  const bookShelf = new ShelfController();

  const addBook = (e) => {
    e.preventDefault();
    const newBook = bookCreator.create();
    bookShelf.addBook(newBook);
  };
  const form = document.querySelector("form#book-form")
  form.onsubmit = addBook;
  return{bookCreator, bookShelf};
}

const lib = new LibraryOrchestrator();

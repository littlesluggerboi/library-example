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
    value = parseInt(value);
    if (isNaN(value)) {
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
    bookShelf.set(value.getId(), value);
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

  const showBookActions = () => {
    htmlElementReference.querySelector(".book-actions").style.visibility =
      "visible";
  };
  const hideBookAction = () => {
    htmlElementReference.querySelector(".book-actions").style.visibility =
      "hidden";
  };

  const readBook = () => {
    const button = htmlElementReference.querySelector("button.read");
    if (!bookReference.isRead()) {
      greenButton(button);
    } else {
      whiteButton(button);
    }
    bookReference.toggleIsRead();
  };

  const greenButton = (buttonElement) => {
    buttonElement.textContent = "unread";
    buttonElement.style.backgroundColor = "green";
    buttonElement.style.color = "white";
  };

  const whiteButton = (buttonElement) => {
    buttonElement.textContent = "read";
    buttonElement.style.backgroundColor = "white";
    buttonElement.style.color = "black";
  };

  const createDisplay = () => {
    if (htmlElementReference != null) {
      throw new Error("Book already got a display");
    }
    const newDisplay = document.createElement("div");
    newDisplay.id = book.getId();

    const img_container = document.createElement("div");
    img_container.classList.add("img-container");

    const book_actions = document.createElement("div");
    book_actions.classList.add("book-actions");
    const remove_buttton = document.createElement("button");
    remove_buttton.classList.add("remove");
    remove_buttton.textContent = "remove";

    const read_button = document.createElement("button");
    read_button.classList.add("read");
    read_button.textContent = "read";

    book_actions.append(remove_buttton, read_button);
    img_container.append(book_actions);
    img_container.addEventListener("mouseover", showBookActions);
    img_container.addEventListener("mouseout", hideBookAction);

    const title = document.createElement("h4");
    title.textContent = bookReference.getTitle();
    const author = document.createElement("p");
    author.textContent = bookReference.getAuthor();
    newDisplay.classList.add("book");
    newDisplay.append(img_container, title, author);

    htmlElementReference = newDisplay;
  };

  //deleteDisplay;
  const deleteDisplay = () => {
    if (htmlElementReference != null) {
      htmlElementReference.remove();
      htmlElementReference = null;
    }
  };

  //getDisplay;
  const getDisplay = () => {
    if (htmlElementReference == null) {
      throw new Error("Display not yet created");
    }
    return htmlElementReference;
  };

  return { createDisplay, deleteDisplay, getDisplay, readBook };
}

function RecentlyController(){
  const recentlyAddedContainer = document.querySelector(".recently-added-container");
  const recentActivityContainer = document.querySelector(".recent-activity-container");

  const createActivityElement = (book)=>{
    const viewedElement = document.createElement("div");
    viewedElement.classList.add("viewed");
    
    const title = document.createElement("h4");
    title.textContent = book.getTitle();

    const author = document.createElement("p");
    author.textContent = book.getAuthor();
    
    viewedElement.append(title, author);
    return viewedElement;
  }
  
  const maintainContainerSize = (element)=>{
    if(element.children.length == 3){
      element.children[2].remove();
    }
  }

  const addRecentActivity = (book)=>{
    
    const newActivity = createActivityElement(book);
    maintainContainerSize(recentActivityContainer);
    recentActivityContainer.prepend(newActivity);
  }

  const addRecentlyAdded = (book)=>{
    const newlyAdded = createActivityElement(book);
    maintainContainerSize(recentlyAddedContainer);
    recentlyAddedContainer.prepend(newlyAdded);
  }

  return {addRecentActivity, addRecentlyAdded};
}

function ShelfController() {
  const bookShelf = new Shelf();
  const shelfDisplay = document.querySelector(".shelf");
  const bookDisplays = new Map();
  const recentController = new RecentlyController();

  //removeBook;
  const deleteBookDisplay = (bookId) => {
    const bookDisplay = bookDisplays.get(bookId);
    if (bookDisplay != null) {
      bookDisplay.deleteDisplay();
    }
  };

  const removeBook = (event) => {
    const targetElement =
      event.target.parentElement.parentElement.parentElement;
    const bookId = parseInt(targetElement.id);
    deleteBookDisplay(bookId);
    bookDisplays.delete(bookId);
    bookShelf.removeBook(bookId);
  };

  const readBook = (event) => {
    const targetElement =
      event.target.parentElement.parentElement.parentElement;
    const bookId = parseInt(targetElement.id);
    bookDisplays.get(bookId).readBook();
    //TODO add book to recently viewed
    recentController.addRecentActivity(bookShelf.getBook(bookId));
  };

  //addBook;
  const addBook = (book) => {
    const newBookDisplay = new BookController(book);
    const bookId = book.getId();
    bookShelf.addBook(book);
    bookDisplays.set(bookId, newBookDisplay);
    newBookDisplay.createDisplay();
    const bookHtmlElement = newBookDisplay.getDisplay();
    bookHtmlElement
      .querySelector("button.remove")
      .addEventListener("click", removeBook);
    bookHtmlElement
      .querySelector("button.read")
      .addEventListener("click", readBook);
    shelfDisplay.prepend(bookHtmlElement);
    //TODO add book to recently added.
    recentController.addRecentlyAdded(book);
  };

  return { addBook };
}

function BookCreator() {
  const form = document.querySelector("form#book-form");
  let currentId = 0;
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

function modalContoller() {
  const bookFormModal = document.querySelector("dialog");
  const show = () => {
    bookFormModal.showModal();
  };
  const hide = () => {
    bookFormModal.close();
  };
  return { show, hide };
}

function LibraryOrchestrator() {
  const bookCreator = new BookCreator();
  const bookShelf = new ShelfController();
  const formModal = new modalContoller();

  const addBook = (e) => {
    e.preventDefault();
    const newBook = bookCreator.create();
    bookShelf.addBook(newBook);
    formModal.hide();
  };

  const form = bookCreator.getFormElement();
  form.onsubmit = addBook;

  const addBookButton = document.querySelector("button.add-book");
  addBookButton.addEventListener("click", formModal.show);
}

const lib = new LibraryOrchestrator();

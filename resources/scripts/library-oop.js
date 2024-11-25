class Book {
  constructor(title, author, yearPublished, genre, description) {
    this.title = title;
    this.author = author;
    this.yearPublished = yearPublished;
    this.genre = genre;
    this.description = description;
    this.read = false;
    this.isRead = function () {
      return this.read;
    };
  }
}

class HTMLFactory {
  createParagraph(p) {
    const header_para = document.createElement("p");
    header_para.textContent = p;
    return header_para;
  }
  createH4(h) {
    const h4 = document.createElement("h4");
    h4.textContent = h;
    return h4;
  }
  createSpan(s) {
    const span = document.createElement("span");
    span.textContent = s;
    return span;
  }
}

class BookPartsFactory extends HTMLFactory {
  createBookRim() {
    const rim = document.createElement("div");
    rim.classList.add("rim");
    return rim;
  }

  createGroupTag() {
    const tagGroup = document.createElement("div");
    tagGroup.classList.add("tag-group");
    return tagGroup;
  }
}

class SelectedBookPartsFactory extends HTMLFactory {
  createRemoveButton() {
    const removeButton = document.createElement("button");
    removeButton.classList.add("remove");
    removeButton.textContent = "Delete";
    return removeButton;
  }
}

class BookDisplayBuilder {
  constructor(bookPartsFactory) {
    if (bookPartsFactory instanceof HTMLFactory) {
      this.factory = bookPartsFactory;
    }
  }
  buildDisplay(book) {
    if (book instanceof Book) {
      const bookElement = document.createElement("div");
      bookElement.classList.add("book");

      const header = this.factory.createGroupTag();
      header.appendChild(this.factory.createBookRim());
      header.appendChild(this.factory.createParagraph(book.genre));
      header.appendChild(this.factory.createBookRim());

      const title = this.factory.createH4(book.title);
      const author = this.factory.createParagraph(book.author);

      const footer = this.factory.createGroupTag();
      footer.appendChild(this.factory.createBookRim());
      footer.appendChild(this.factory.createParagraph(book.yearPublished));
      footer.appendChild(this.factory.createBookRim());

      const span = this.factory.createSpan("x");

      bookElement.appendChild(header);
      bookElement.appendChild(title);
      bookElement.appendChild(author);
      bookElement.appendChild(footer);
      bookElement.appendChild(span);
      return bookElement;
    }
  }
}

class SelectedBookDisplayBuilder {
  constructor(selectedBookPartsFactory) {
    this.factory = selectedBookPartsFactory;
  }
  buildDisplay(book) {
    const display = document.createElement("div");
    display.classList.add("full-description");
    display.appendChild(this.factory.createH4("Title"));
    display.appendChild(this.factory.createParagraph(book.title));
    display.appendChild(this.factory.createH4("Description"));
    display.appendChild(this.factory.createParagraph(book.description));
    display.appendChild(this.factory.createH4("Author"));
    display.appendChild(this.factory.createParagraph(book.author));
    display.appendChild(this.factory.createH4("Genre"));
    display.appendChild(this.factory.createParagraph(book.genre));
    display.appendChild(this.factory.createH4("Published Year"));
    display.appendChild(this.factory.createParagraph(book.year));
    display.appendChild(this.factory.createH4("Status"));
    if (!book.isRead) {
      display.appendChild(this.factory.createParagraph("Read"));
    } else {
      display.appendChild(this.factory.createParagraph("Unread"));
    }
    display.appendChild(this.factory.createRemoveButton());
    return display;
  }
  buildEmptyDisplay() {
    const emplyDisplay = document.createElement("div");
    emplyDisplay.classList.add("full-description");
    emplyDisplay.textContent = "Select A Book";
    return emplyDisplay;
  }
}

class BookCreator {
  constructor(input) {
    this.input = input;
  }
  create() {
    let newBook = new Book(
      this.input.elements.title.value,
      this.input.elements.author.value,
      this.input.elements.year.value,
      this.input.elements.genre.value,
      this.input.elements.description.value
    );
    this.input.reset();
    return newBook;
  }
}

class Shelf {
  constructor(display) {
    this.display = display;
    this.collection = new Map();
    this.add = function (key, value) {
      this.collection.set(key, value);
      this.display.appendChild(value);
    };
  }

  remove(targetItem) {
    this.collection.get(targetItem).remove();
    this.collection.delete(targetItem);
  }
  findByDisplay(display) {
    const values = this.collection.keys();
    for (let key of values) {
      if (this.collection.get(key) == display) {
        return key;
      }
    }
  }
  getElementDisplay(key) {
    return this.collection.get(key);
  }

  isFull() {
    if (this.collection.size >= 10) {
      return true;
    }
    return false;
  }
}

function removeStyleSelected() {
  const selectedBook = document.querySelector(".book.selected");
  if (selectedBook != null) {
    selectedBook.classList.remove("selected");
  }
}

function isolateBookElement(htmlElement) {
  if (htmlElement.classList.contains("book")) {
    return htmlElement;
  } else if (
    htmlElement.offsetParent != null &&
    htmlElement.offsetParent.classList.contains("book")
  ) {
    return htmlElement.offsetParent;
  } else {
    return null;
  }
}

function selectBook(element) {
  const htmlElement = isolateBookElement(element.srcElement);
  if (htmlElement != null) {
    const selected = shelf.findByDisplay(htmlElement);
    removeStyleSelected();
    selectedBook = selected;
    htmlElement.classList.add("selected");
    const newDisplay = selectedBookDisplayBuilder.buildDisplay(selected);
    newDisplay
      .querySelector("button.remove")
      .addEventListener("click", removeBook);
    document.querySelector(".full-description").replaceWith(newDisplay);
  }
}

function removeBook() {
  shelf.remove(selectedBook);
  selectedBook = null;
  document
    .querySelector(".full-description")
    .replaceWith(selectedBookDisplayBuilder.buildEmptyDisplay());
}

function createBook() {
  return bookCreator.create();
}

function showSpan(element) {
  const htmlElement = isolateBookElement(element.srcElement);
  if(htmlElement != null){
    const span = htmlElement.querySelector("span");
    span.style.display = "block";
    
    // add functionality to the x span
    
  }
}

function removeSpan(element) {
  const htmlElement = isolateBookElement(element.srcElement);
  if(htmlElement != null){
    const span = htmlElement.querySelector("span");
    span.style.display = "none";
  }
}

function addBookToShelf() {
  if (!shelf.isFull()) {
    const newBook = createBook();
    const newBookDisplay = bookDisplayBuilder.buildDisplay(newBook);
    newBookDisplay.addEventListener("click", selectBook);
    newBookDisplay.addEventListener("mouseenter", showSpan);
    newBookDisplay.addEventListener("mouseleave", removeSpan);

    shelf.add(newBook, newBookDisplay);
  } else {
    alert("The Bookshelf is FULL!! Remove a one to add another.");
  }
}

const formElement = document.querySelector("form");
const bookCreator = new BookCreator(formElement);

const shelfDisplay = document.querySelector(".shelf");
const shelf = new Shelf(shelfDisplay);

let selectedBook = null;

const bookPartsFactory = new BookPartsFactory();
const bookDisplayBuilder = new BookDisplayBuilder(bookPartsFactory);

const selectedBookPartsFactory = new SelectedBookPartsFactory();
const selectedBookDisplayBuilder = new SelectedBookDisplayBuilder(
  selectedBookPartsFactory
);

const addButton = document.querySelector("button.submit");
addButton.addEventListener("click", addBookToShelf);

const ele = document.createElement("div");

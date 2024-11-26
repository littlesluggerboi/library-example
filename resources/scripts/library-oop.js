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
    span.innerHTML = s;
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
      let icon = "&#9697";
      if (book.isRead()) {
        icon = "👁";
      }
      const spanRead = this.factory.createSpan(icon);
      spanRead.classList.add("read");
      //&#9697
      //"👁"
      //&#10060
      const spanRemove = this.factory.createSpan("&#10060");
      spanRemove.classList.add("take");

      bookElement.appendChild(header);
      bookElement.appendChild(title);
      bookElement.appendChild(author);
      bookElement.appendChild(footer);
      bookElement.appendChild(spanRead);
      bookElement.appendChild(spanRemove);

      return bookElement;
    }
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
      this.display.prepend(value);
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

function log(e) {
  console.log(e.target.parentElement);
}

function removeBook(e) {
  const bookDisplay = e.target.parentElement;
  const book = shelf.findByDisplay(bookDisplay);
  shelf.remove(book);
}

function showSpan(element) {
  const htmlElement = element.target;
  if (htmlElement != null && htmlElement.classList.contains("book")) {
    const spanRead = htmlElement.querySelector("span.read");
    spanRead.style.display = "block";

    const spanTake = htmlElement.querySelector("span.take");
    spanTake.style.display = "block";

    spanRead.addEventListener("click", readBook);
    spanTake.addEventListener("click", removeBook);
  }
}

function removeSpan(element) {
  const htmlElement = element.target;
  if (htmlElement != null && htmlElement.classList.contains("book")) {
    for (let span of htmlElement.querySelectorAll("span")) {
      span.style.display = "none";
    }
  }
}

function addBookToShelf(e) {
  e.preventDefault();
  if (!shelf.isFull()) {
    const newBook = createBook();
    const newBookDisplay = bookDisplayBuilder.buildDisplay(newBook);
    newBookDisplay.addEventListener("mouseenter", showSpan);
    newBookDisplay.addEventListener("mouseleave", removeSpan);

    shelf.add(newBook, newBookDisplay);
  } else {
    fullDialog.showModal();
    fullDialog.style.visibility = "visible";
    // alert("The Bookshelf is FULL!! Remove a one to add another.");
  }
}

function updateReadingModal(book){
  const readingModal = document.querySelector("dialog.reading");
  const title = readingModal.querySelector("h4");
  const description = readingModal.querySelector("p:nth-of-type(1)");
  const author = readingModal.querySelector("p:nth-of-type(2)");
  const publishedYear = readingModal.querySelector("p:nth-of-type(3)");
  const genre = readingModal.querySelector("p:nth-of-type(4)");
  title.textContent = book.title;
  description.textContent = book.description;
  author.textContent = book.author;
  publishedYear.textContent = book.yearPublished;
  genre.textContent = book.genre;
}
function openReadingModal(){
  const readingModal = document.querySelector("dialog.reading");
  readingModal.showModal();
  readingModal.style.visibility = "visible";
}
function closeReadingModal(){
  const readingModal = document.querySelector("dialog.reading");
  readingModal.close();
  readingModal.style.visibility = "hidden";
}

function readBook(e) {
  const span = e.target;
  const bookDisplay = e.target.parentElement;
  const book = shelf.findByDisplay(bookDisplay);
  if (book != null) {
    book.read = true;  
    span.innerHTML = "👁";
    openReadingModal();
    updateReadingModal(book); 
  }
}

const formElement = document.querySelector("form");
const bookCreator = new BookCreator(formElement);

const shelfDisplay = document.querySelector(".shelf");
const shelf = new Shelf(shelfDisplay);

const bookPartsFactory = new BookPartsFactory();
const bookDisplayBuilder = new BookDisplayBuilder(bookPartsFactory);

const addButton = document.querySelector('button[type="submit"]');
addButton.addEventListener("click", addBookToShelf, false);


const fullDialog = document.querySelector("dialog.full");
const closeModalButton = fullDialog.querySelector("button.close");
closeModalButton.addEventListener("click", ()=> {fullDialog.close(); fullDialog.style.visibility = "hidden";});


const readingModal = document.querySelector("dialog.reading");
const closeReadingModalButton = readingModal.querySelector("button.close");
closeReadingModalButton.addEventListener("click", closeReadingModal);
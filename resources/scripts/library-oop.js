function Book(title, author, yearPublished, genre, description) {
  this.title = title;
  this.author = author;
  this.yearPublished = yearPublished;
  this.genre = genre;
  this.description = description;
  this.isRead = false;
}

function HTMLFactory() {
  this.createParagraph = function (p) {
    const header_para = document.createElement("p");
    header_para.textContent = p;
    return header_para;
  };
  this.createH4 = function (h) {
    const h4 = document.createElement("h4");
    h4.textContent = h;
    return h4;
  };
}

function BookPartsFactory() {
  this.createBookRim = function () {
    const rim = document.createElement("div");
    rim.classList.add("rim");
    return rim;
  };

  this.createGroupTag = function () {
    const tagGroup = document.createElement("div");
    tagGroup.classList.add("tag-group");
    return tagGroup;
  };
}

function SelectedBookPartsFactory() {
  this.createRemoveButton = function () {
    const removeButton = document.createElement("button");
    removeButton.classList.add("remove");
    removeButton.textContent = "Delete";
    return removeButton;
  };
}

function BookDisplayBuilder(bookPartsFactory) {
  this.factory = bookPartsFactory;
  this.buildDisplay = function (book) {
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
    footer.appendChild(this.factory.createParagraph(book.year));
    footer.appendChild(this.factory.createBookRim());

    bookElement.appendChild(header);
    bookElement.appendChild(title);
    bookElement.appendChild(author);
    bookElement.appendChild(footer);

    return bookElement;
  };
}

function SelectedBookDisplayBuilder(selectedBookPartsFactory) {
  this.factory = selectedBookPartsFactory;
  this.buildDisplay = function (book) {
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
    if (this.book.isRead) {
      display.appendChild(this.factory.createParagraph("Read"));
    } else {
      display.appendChild(this.factory.createParagraph("Unread"));
    }
    display.appendChild(this.factory.createRemoveButton());
    return display;
  };
  this.buildEmptyDisplay = function () {
    const emplyDisplay = document.createElement("div");
    emplyDisplay.classList.add("full-description");
    emplyDisplay.textContent = "Select A Book";
    return emplyDisplay;
  };
}

function BookCreator(input) {
  this.input = input;
  this.create = function () {
    let newBook = new Book(
      input.elements.title.value,
      input.elements.author.value,
      input.elements.year.value,
      input.elements.genre.value,
      input.elements.description.value
    );
    input.reset();
    return newBook;
  };
}

function Shelf(display) {
  this.display = display;
  (this.collection = new Map() < Book), HTMLElement > {};
  this.add = function (key, value) {
    this.collection.add(key, value);
    this.display.appendChild(display);
  };
  this.remove = function (targetItem) {
    this.collection.get(targetItem).remove();
    this.collection.remove(targetItem);
  };
  this.findByDisplay = function (display) {
    const values = this.collection.keys();
    for (let key of values) {
      if (this.collection.get(key) == display) {
        return key;
      }
    }
  };
  this.getElementDisplay = function (key) {
    return this.collection.get(key);
  };
}

function Library(
  bookCreator,
  shelfDisplay,
  bookPartsFactory,
  selectedBookPartsFactory,
  selectedBookDisplay
) {
  this.bookCreator = bookCreator;
  this.bookDisplayBuilder = new BookDisplayBuilder(bookPartsFactory);
  this.selectedBookDisplayBuilder = new selectedBookPartsFactory();
  this.shelf = new Shelf(shelfDisplay);
  this.shelfDisplay = shelfDisplay;
  this.selectedBook = null;
  this.selectedBookDisplay = selectedBookDisplay;

  this.addBook = function () {
    const newBook = this.bookCreator.create();
    const newBookDisplay = this.bookDisplayBuilder.buildDisplay(newBook);
    newBook.addEventListener("click", this.selectBook(newBookDisplay));
    this.shelf.add(newBook, newBookDisplay);
  };

  this.selectBook = function (htmlElement) {
    this.selectedBook = this.shelf.findByDisplay(htmlElement);
    this.selectedBookDisplay.replaceWith(
      this.selectedBookDisplayBuilder.buildDisplay()
    );
    const previouslySelectedBookDisplay = document.querySelector(".selected");
    if (previouslySelectedBookDisplay != null) {
      previouslySelectedBookDisplay.classList.remove("selected");
    }
    htmlElement.classList.add("selected");
  };

  this.removeBook = function () {
    this.shelf.remove(this.selectedBook);
    this.selectedBook = null;
    this.selectedBookDisplay.replaceWith(
      this.SelectedBookDisplayBuilder.buildEmptyDisplay()
    );
  };
}

function selectBook(e) {
  library.selectBook(e);
}

let formElement = document.querySelector("form");
let bookCreator = new BookCreator(formElement);
let shelfDisplay = document.querySelector("shelf");
let bookPartsFactory = new BookPartsFactory();
let selectedBookPartsFactory = new SelectedBookPartsFactory();
let selectedBookDisplay = document.querySelector("full-description");

let library = new Library(
  bookCreator,
  shelfDisplay,
  bookPartsFactory,
  selectedBookPartsFactory,
  selectedBookDisplay
);

const addButton = document.querySelector("button.submit");
addButton.addEventListener("click", library.addBook);
const removeButton = document.querySelector("button.remove");
removeButton.addEventListener("click", library.removeBook);

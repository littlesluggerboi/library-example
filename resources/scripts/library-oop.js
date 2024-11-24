class Book {
  constructor(title, author, yearPublished, genre, description) {
    this.title = title;
    this.author = author;
    this.yearPublished = yearPublished;
    this.genre = genre;
    this.description = description;
    this.isRead = false;
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
    if(bookPartsFactory instanceof HTMLFactory){
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
      footer.appendChild(this.factory.createParagraph(book.year));
      footer.appendChild(this.factory.createBookRim());

      bookElement.appendChild(header);
      bookElement.appendChild(title);
      bookElement.appendChild(author);
      bookElement.appendChild(footer);

      return bookElement;
    }
  }
}

class SelectedBookDisplayBuilder {
  constructor(selectedBookPartsFactory) {
    this.factory = selectedBookPartsFactory;
  }
  buildDisplay(book) {
    if (book instanceof Book) {
      const display = document.createElement("div");
      display.classList.add("full-description");
      display.appendChild(this.htmlFactory.createH4("Title"));
      display.appendChild(this.htmlFactory.createParagraph(book.title));
      display.appendChild(this.htmlFactory.createH4("Description"));
      display.appendChild(this.htmlFactory.createParagraph(book.description));
      display.appendChild(this.htmlFactory.createH4("Author"));
      display.appendChild(this.htmlFactory.createParagraph(book.author));
      display.appendChild(this.htmlFactory.createH4("Genre"));
      display.appendChild(this.htmlFactory.createParagraph(book.genre));
      display.appendChild(this.htmlFactory.createH4("Published Year"));
      display.appendChild(this.htmlFactory.createParagraph(book.year));
      display.appendChild(this.htmlFactory.createH4("Status"));
      if (this.book.isRead) {
        display.appendChild(this.htmlFactory.createParagraph("Read"));
      } else {
        display.appendChild(this.htmlFactory.createParagraph("Unread"));
      }
      display.appendChild(this.factory.createRemoveButton());
      return display;
    }
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
}

class Library {
  constructor(
    shelfDisplay,
    bookPartsFactory,
    selectedBookPartsFactory,
    selectedBookDisplay
  ) {
    this.bookDisplayBuilder = new BookDisplayBuilder(
      bookPartsFactory
    );
    this.selectedBookDisplayBuilder = new SelectedBookDisplayBuilder(
      selectedBookPartsFactory
    );
    this.shelf = new Shelf(shelfDisplay);
    this.shelfDisplay = shelfDisplay;
    this.selectedBook = null;
    this.selectedBookDisplay = selectedBookDisplay;
  }

  addBook(newBook) {
    let newBookDisplay = this.bookDisplayBuilder.buildDisplay(newBook);
    newBookDisplay.addEventListener("click", this.selectBook);
    this.shelf.add(newBook, newBookDisplay);
  }


  selectBook(htmlElement) {
    this.selectedBook = this.shelf.findByDisplay(htmlElement);
    this.selectedBookDisplay.replaceWith(
      this.selectedBookDisplayBuilder.buildDisplay()
    );
    const previouslySelectedBookDisplay = document.querySelector(".selected");
    if (previouslySelectedBookDisplay != null) {
      previouslySelectedBookDisplay.classList.remove("selected");
    }
    htmlElement.classList.add("selected");
  }

  removeBook() {
    this.shelf.remove(this.selectedBook);
    this.selectedBook = null;
    this.selectedBookDisplay.replaceWith(
      this.SelectedBookDisplayBuilder.buildEmptyDisplay()
    );
  }
}


const formElement = document.querySelector("form");
const bookCreator = new BookCreator(formElement);

const shelfDisplay = document.querySelector(".shelf");
const shelf = new Shelf()

const selectedBook = null;
const selectedBookDisplay = document.querySelector(".full-description");

const bookPartsFactory = new BookPartsFactory();
const bookDisplayBuilder = new BookDisplayBuilder(bookPartsFactory);

const selectedBookPartsFactory = new SelectedBookPartsFactory();
const selectedBookDisplayBuilder = new SelectedBookDisplayBuilder(selectedBookPartsFactory);



const addButton = document.querySelector("button.submit");
addButton.addEventListener("click", createBook);
const removeButton = document.querySelector("button.remove");
// removeButton.addEventListener("click", library.removeBook());
function selectBook(e) {
  library.selectBook(e);
}
function createBook(){
  library.addBook(bookCreator.create());
}
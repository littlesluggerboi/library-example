function Book(book_title, author, year, genre, description) {
  this.title = book_title;
  this.author = author;
  this.year = year;
  this.genre = genre;
  this.isRead = false;
  this.description = description;
  this.display = null;
}

function Library(library_name) {
  this.library_name = library_name;
  this.books = [];

  this.addBook = function (book) {
    if (!this.isFull()) {
      this.books.push(book);
    }
  };

  this.isFull = function () {
    return this.books.length >= 10;
  };

  this.findByDisplay = function (target) {
    for (let book of this.books) {
      if (book.display == target) {
        return book;
      }
    }
    return null;
  };

  this.remove = function (book) {
    let iterator= 0;
    while(iterator < this.books.length && this.books[iterator] != book){
      iterator++;
    }
    if(iterator < this.books.length){
      this.books[iterator].display.remove();
      this.books.splice(iterator,1);
    }
  };
}

function Description(book){
  this.book = book;
  this.createDescriptionElement = function () {
    const fullDescriptionElement = document.createElement("div");
    fullDescriptionElement.classList.add("full-description");
    fullDescriptionElement.appendChild(createH4Element("Title"));
    fullDescriptionElement.appendChild(createParaElement(this.book.title));
    fullDescriptionElement.appendChild(createH4Element("Description"));
    fullDescriptionElement.appendChild(createParaElement(this.book.description));
    fullDescriptionElement.appendChild(createH4Element("Author"));
    fullDescriptionElement.appendChild(createParaElement(this.book.author));
    fullDescriptionElement.appendChild(createH4Element("Genre"));
    fullDescriptionElement.appendChild(createParaElement(this.book.genre));
    fullDescriptionElement.appendChild(createH4Element("Published Year"));
    fullDescriptionElement.appendChild(createParaElement(this.book.year));
    fullDescriptionElement.appendChild(createH4Element("Status"));
    if (this.book.isRead) {
      fullDescriptionElement.appendChild(createParaElement("Read"));
    } else {
      fullDescriptionElement.appendChild(createParaElement("Unread"));
    }
    fullDescriptionElement.appendChild(createRemoveBookButton());
    this.description = fullDescriptionElement;
  }
  this.description = null;
  this.deleteElementSelectedElement = function (){
    standard_lib.remove(this.book);
    this.book = null;
    const emptyDescription = document.createElement("div");
    emptyDescription.classList.add("full-description");
    emptyDescription.textContent = "Select A Book";
    this.description.replaceWith(emptyDescription);
  }
}

function createRemoveBookButton(){
  const removeButton = document.createElement("button");
  removeButton.classList.add("remove");
  removeButton.textContent = "Delete";
  removeButton.addEventListener("click", removeBook);
  return removeButton;
}

function createBookFromFormInput() {
  console.log("Created a book from input form");
  let form = document.getElementById("form");
  let newBook = new Book(
    form.elements.title.value,
    form.elements.author.value,
    form.elements.year.value,
    form.elements.genre.value,
    form.elements.description.value
  );
  form.reset();
  return newBook;
}

function removeBook(){
  highlightedElement.deleteElementSelectedElement();
}

function showFullDescription(e) {
  const book = standard_lib.findByDisplay(e.srcElement);
  removeStyleSelected();
  highlightedElement.book = book;
  highlightedElement.createDescriptionElement();
  e.srcElement.classList.add("selected");
  let container = document.querySelector(".container");
  container.firstElementChild.replaceWith(highlightedElement.description);
}

function removeStyleSelected(){
  const selectedBook = document.querySelector(".book.selected");
  if(selectedBook!=null){
    selectedBook.classList.remove("selected");
  }

}

function showSpan(element){
  console.log(element);
  const spanInElement = element.srcElement.querySelector("span");
  spanInElement.style.display = "block";
}

function removeSpan(element){
  const el = document.querySelector("span");
  el.classList.contains("book");
  const sourceElement = element.srcElement;
  // console.log(sourceElement.offsetParent);  
  console.log(sourceElement);
  const spanInElement = element.srcElement.querySelector("span");
}

function addBook() {
  if (!standard_lib.isFull()) {
    let newBook = createBookFromFormInput();
    const shelf = document.querySelector(".shelf");
    const bookElement = createBookElement(newBook);
    bookElement.addEventListener("click", showFullDescription);
    bookElement.addEventListener("mouseover", showSpan);
    bookElement.addEventListener("mouseout", removeSpan);
    newBook.display = bookElement;
    standard_lib.addBook(newBook);
    shelf.appendChild(bookElement);
  } else {
    alert("The bookshelf is full. Remove one to add another.")
  }
}

function createRimElement() {
  const rim = document.createElement("div");
  rim.classList.add("rim");
  return rim;
}
function createParaElement(p) {
  const header_para = document.createElement("p");
  header_para.textContent = p;
  return header_para;
}
function createH4Element(h) {
  const h4 = document.createElement("h4");
  h4.textContent = h;
  return h4;
}
function createTagGroupElement() {
  const tagGroup = document.createElement("div");
  tagGroup.classList.add("tag-group");
  return tagGroup;
}
function createBookElement(book) {
  const bookElement = document.createElement("div");
  bookElement.classList.add("book");

  const header = createTagGroupElement();
  header.appendChild(createRimElement());
  header.appendChild(createParaElement(book.genre));
  header.appendChild(createRimElement());

  const title = createH4Element(book.title);
  const author = createParaElement(book.author);

  const footer = createTagGroupElement();
  footer.appendChild(createRimElement());
  footer.appendChild(createParaElement(book.year));
  footer.appendChild(createRimElement());

  bookElement.appendChild(header);
  bookElement.appendChild(title);
  bookElement.appendChild(author);
  bookElement.appendChild(footer);
  bookElement.appendChild(createSpan());

  return bookElement;
}
function createSpan(){
  const span = document.createElement("span");
  span.textContent = "x";
  return span;
}

const submitFormButton = document.querySelector(".submit");
submitFormButton.addEventListener("click", addBook);

let standard_lib = new Library("The Library");
let highlightedElement = new Description(null);


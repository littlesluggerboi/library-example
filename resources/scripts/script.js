function Book(book_title, author, year, genre, description) {
  this.title = book_title;
  this.author = author;
  this.year = year;
  this.genre = genre;
  this.red = false;
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
    return this.books.length >= 16;
  };

  this.find = function (target){
    for(let book of this.books){
      if(book.display == target){
        return book;
      }
    }
    return null;
  }

  this.remove = function (target){
    
  }
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

function createFullDescriptionElement(){
  
}

function showFullDescription(e){
  const book = standard_lib.find(e.srcElement);
  console.log(book);
}

function addBook() {
  if (!standard_lib.isFull()) {
    let newBook = createBookFromFormInput();
    const shelf = document.querySelector(".shelf");
    const bookElement = createBookElement(newBook);
    bookElement.addEventListener("click",showFullDescription);
    newBook.display = bookElement;
    standard_lib.addBook(newBook);
    shelf.appendChild(bookElement);
  } else{

  }
}

function showBooks() {
  
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

  return bookElement;
}

const submitFormButton = document.querySelector("button");
submitFormButton.addEventListener("click", addBook);

let standard_lib = new Library("The Library");

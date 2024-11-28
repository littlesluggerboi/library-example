export default function Book(bookTitle, bookAuthor, bookDescription, bookGenre, bookYear, bookNumber) {
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
    if (typeof value != "number" || Math.floor(value) != value) {
      throw new Error("Not an Integer");
    }
    return value;
  };

  const setYear = (value) => {
    value = validIntInput(value);
    if (value < 1900 || value > 2040) {
      throw new Error("Year out of Range");
    }
    return value;
  };

  const getYear = () => {
    checkField(year, "Year");
    return year;
  };

  const setId = (value) =>{
    if(value == null){
      throw new Error("bookNumber Cannot be null");
    }
    id = value;
  }

  const getId = () =>{
    checkField(id, "bookNumber");
    return id;
  }
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
    getId
  };
}


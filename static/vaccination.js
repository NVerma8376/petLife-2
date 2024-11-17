const datesContainer = document.getElementById('dates');
const monthYearDisplay = document.getElementById('monthYear');
const notePopup = document.getElementById('notePopup');
const noteInput = document.getElementById('noteInput');
const notesList = document.getElementById('notesList');

let currentDate = new Date();
let activeDate = null;
let notes = JSON.parse(localStorage.getItem('notes')) || {}; // Load saved notes from localStorage

function renderCalendar() {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  monthYearDisplay.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${year}`;

  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();

  datesContainer.innerHTML = '';

  for (let i = 0; i < firstDay; i++) {
    datesContainer.innerHTML += `<div></div>`;
  }

  for (let date = 1; date <= lastDate; date++) {
    const dateDiv = document.createElement('div');
    dateDiv.classList.add('date');
    dateDiv.textContent = date;

    const dateKey = `${year}-${month + 1}-${date}`; // Format: YYYY-M-D
    if (notes[dateKey]) {
      dateDiv.classList.add('active');
    }

    dateDiv.addEventListener('click', () => openNotePopup(dateKey));
    datesContainer.appendChild(dateDiv);
  }
}

function openNotePopup(dateKey) {
  activeDate = dateKey;
  noteInput.value = notes[dateKey] || '';
  notePopup.style.display = 'block';
}

function closeNotePopup() {
  notePopup.style.display = 'none';
}

function saveNote() {
  const noteText = noteInput.value.trim();
  if (noteText) {
    notes[activeDate] = noteText;
  } else {
    delete notes[activeDate];
  }

  localStorage.setItem('notes', JSON.stringify(notes)); // Save notes to localStorage
  renderCalendar();
  updateNotesList();
  closeNotePopup();
}

function deleteNote(dateKey) {
  delete notes[dateKey]; // Remove the note from the object
  localStorage.setItem('notes', JSON.stringify(notes)); // Update localStorage
  renderCalendar();
  updateNotesList(); // Refresh the notes list
}

function updateNotesList() {
  notesList.innerHTML = '';
  Object.keys(notes).forEach(dateKey => {
    const noteItem = document.createElement('li');
    noteItem.classList.add('note-item');
    noteItem.innerHTML = `
      <span>${dateKey}: ${notes[dateKey]}</span>
      <button class="delete-note" data-date="${dateKey}">Delete</button>
    `;

    notesList.appendChild(noteItem);
  });

  // Add event listeners to the delete buttons
  document.querySelectorAll('.delete-note').forEach(button => {
    button.addEventListener('click', (e) => {
      const dateKey = e.target.getAttribute('data-date');
      deleteNote(dateKey);
    });
  });
}

document.getElementById('prev').addEventListener('click', () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar();
});

document.getElementById('next').addEventListener('click', () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar();
});

document.getElementById('saveNote').addEventListener('click', saveNote);
document.getElementById('cancelNote').addEventListener('click', closeNotePopup);

renderCalendar();
updateNotesList();
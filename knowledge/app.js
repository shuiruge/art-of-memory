const fetchNotes = () => {
  fetch('/notes')
    .then(response => response.json())
    .then(notes => {
      const noteInput = document.getElementById('note-input');
      const noteList = document.getElementById('note-list');

      noteList.innerHTML = '';
      notes.forEach(note => {
        const li = document.createElement('li');
        li.textContent = note;
        noteList.appendChild(li);
      });
    });
};

const addNote = () => {
  const noteInput = document.getElementById('note-input');
  const note = noteInput.value.trim();
  if (note) {
    fetch('/notes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ note })
    })
    .then(response => response.json())
    .then(data => {
      noteInput.value = '';
      fetchNotes();
    });
  }
};

const searchNote = () => {
  const noteInput = document.getElementById('note-input');
  const searchInput = document.getElementById('search-input');
  const noteList = document.getElementById('note-list');

  const searchTerm = searchInput.value.trim();
  if (searchTerm) {
    const matchingNotes = noteList.querySelectorAll('.note');
    let found = false;
    for (let i = 0; i < matchingNotes.length; i++) {
      if (matchingNotes[i].textContent.includes(searchTerm)) {
        matchingNotes[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
        found = true;
        break;
      }
    }
    if (!found) {
      alert('No matching notes found');
    }
  }
};

const removeNote = (event) => {
  const li = event.target.parentNode;
  li.remove();
  fetchNotes();
};

document.getElementById('note-input').addEventListener('input', addNote);
document.getElementById('note-input').addEventListener('@', searchNote);
document.getElementById('search-input').addEventListener('input', searchNote);
document.getElementById('note-list').addEventListener('click', removeNote);

fetchNotes();

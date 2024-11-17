const calendar = document.getElementById('calendar');
const monthYear = document.getElementById('month-year');
const detailedInfo = document.getElementById('detailed-info');

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

let dietData = {}; // Store diet details for each date

// Function to render calendar
function renderCalendar() {
  const firstDay = new Date(currentYear, currentMonth, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

  // Clear calendar
  calendar.querySelector('tbody').innerHTML = ''; 

  let row = document.createElement('tr');
  // Add empty cells before the first day of the month
  for (let i = 0; i < firstDay; i++) {
    row.appendChild(document.createElement('td'));
  }

  // Loop through days in the month and create cells
  for (let day = 1; day <= daysInMonth; day++) {
    const cell = document.createElement('td');
    cell.innerText = day;
    cell.onclick = () => showDayDetails(day);

    // Highlight today's date
    const today = new Date();
    if (today.getDate() === day && today.getMonth() === currentMonth && today.getFullYear() === currentYear) {
      cell.classList.add('current-day');
    }

    row.appendChild(cell);

    // Start new row after Saturday
    if ((firstDay + day) % 7 === 0) {
      calendar.querySelector('tbody').appendChild(row);
      row = document.createElement('tr');
    }
  }

  // Append the last row if any cells exist
  if (row.children.length > 0) {
    calendar.querySelector('tbody').appendChild(row);
  }

  monthYear.innerText = `${getMonthName(currentMonth)} ${currentYear}`;
}

// Get full month name
function getMonthName(month) {
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  return months[month];
}

// Function to change month
function changeMonth(offset) {
  currentMonth += offset;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  } else if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar();
}

// Function to show details of selected day
function showDayDetails(day) {
  const date = `${currentYear}-${currentMonth + 1}-${day}`;
  const details = dietData[date] || {};

  document.getElementById('detail-date').innerText = date;
  document.getElementById('detail-food').innerHTML = details.food ? `<li>${details.food}</li>` : '<li>No items recorded.</li>';
  document.getElementById('detail-calories').innerText = details.calories ? `${details.calories} kcal` : '0 kcal';
  document.getElementById('detail-notes').innerText = details.notes || 'No additional details.';
}

// Add diet data
function addDiet() {
  const date = document.getElementById('date').value;
  const food = document.getElementById('food').value;
  const calories = document.getElementById('calories').value;
  const notes = document.getElementById('notes').value;

  if (!date || !food || !calories) return alert('Please fill in all fields');

  dietData[date] = { food, calories, notes };
  
  // Clear input fields after adding
  document.getElementById('diet-form').reset();
  renderCalendar();
}

renderCalendar();

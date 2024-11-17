// Function to update the current time
function updateCurrentTime() {
    const currentTimeElement = document.getElementById('currentTime');
    const currentTime = new Date();
    const hours = currentTime.getHours().toString().padStart(2, '0');
    const minutes = currentTime.getMinutes().toString().padStart(2, '0');
    const seconds = currentTime.getSeconds().toString().padStart(2, '0');
    currentTimeElement.textContent = `Time: ${hours}:${minutes}:${seconds}`;
}

// Function to add a medicine reminder
function addReminder() {
    const medicineSelect = document.getElementById('medicineName');
    const medicineName = medicineSelect.value;
    const reminderTime = document.getElementById('reminderTime').value;

    if (!medicineName || !reminderTime) {
        alert("Please select a medicine and time!");
        return;
    }

    // Create reminder item
    const reminderItem = document.createElement('li');
    reminderItem.classList.add('reminder-item');

    // Display the reminder information
    reminderItem.innerHTML = `
        <div>${medicineName} - ${reminderTime}</div>
        <button class="delete-btn" onclick="deleteReminder(this)">Delete</button>
    `;

    // Add the reminder to the list
    const remindersList = document.getElementById('reminders');
    remindersList.appendChild(reminderItem);

    // Set up the alarm for the reminder
    setupAlarm(reminderTime);

    // Reset the dropdown and input
    medicineSelect.value = '';
    document.getElementById('reminderTime').value = '';
}

// Function to delete a reminder
function deleteReminder(buttonElement) {
    const reminderItem = buttonElement.parentElement;
    const remindersList = document.getElementById('reminders');
    remindersList.removeChild(reminderItem);
}

// Function to set up the alarm for the reminder
function setupAlarm(reminderTime) {
    const currentTime = new Date();
    const [hours, minutes] = reminderTime.split(':');
    const reminderDate = new Date();
    reminderDate.setHours(hours, minutes, 0, 0);

    const timeDifference = reminderDate.getTime() - currentTime.getTime();

    if (timeDifference > 0) {
        setTimeout(() => {
            alert('Time to take your medicine!');
        }, timeDifference);
    }
}

// Update the current time every second
setInterval(updateCurrentTime, 1000);

// Update the current time immediately on page load
updateCurrentTime();

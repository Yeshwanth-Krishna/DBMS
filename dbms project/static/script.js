let selectedDate = null;
// Removed duplicate declaration of filterYear

function hideMenus(e) {
  if (!e.target.closest('#editEventBox') && !e.target.closest('.day')) {
    const editEventBox = document.getElementById("editEventBox");
    if (editEventBox.classList.contains('show')) {
      editEventBox.classList.remove('show');
    }
  }
  if (!e.target.closest('#dashboardMenu') && !e.target.closest('#hamburger')) {
    const menu = document.getElementById("dashboardMenu");
    menu.style.display = "none";
  }
}

function toggleMenu() {
  const menu = document.getElementById("dashboardMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function setFilter(year) {
  console.log('setFilter called with year:', year);
  filterYear = year;
  document.querySelectorAll('.year-button').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.year-button').forEach(btn => {
    if (btn.textContent === year) btn.classList.add('active');
  });

  // Synchronize yearSelect dropdown with filterYear
  const yearSelect = document.getElementById('yearSelect');
  if (year === 'All') {
    // Disable yearSelect or set to a default valid year
    yearSelect.disabled = true;
  } else {
    yearSelect.disabled = false;
    // Extract year number from filterYear string like "Year 2"
    const yearNumber = year.replace('Year ', '').trim();
    // Find matching option and select it
    for (let option of yearSelect.options) {
      if (option.value === yearNumber || option.text === yearNumber) {
        option.selected = true;
        break;
      }
    }
  }

  // Submit the filter form with year filter as query param
  const form = document.getElementById('filterForm');
  // Remove existing filterYear input if any
  const existingInput = document.querySelector('input[name="filterYear"]');
  if (existingInput) {
    existingInput.value = year;
  } else {
    const yearInput = document.createElement('input');
    yearInput.type = 'hidden';
    yearInput.name = 'filterYear';
    yearInput.value = year;
    form.appendChild(yearInput);
  }
  form.submit();
}

document.addEventListener('DOMContentLoaded', () => {
  console.log('Page loaded, current filterYear:', filterYear);
});

function showEvents(day) {
  const modal = document.getElementById('eventModal');
  const modalDay = document.getElementById('modalDay');
  const modalEvents = document.getElementById('modalEvents');
  modalDay.textContent = day;
  modalEvents.innerHTML = '';

  if (eventsByDay[day]) {
    eventsByDay[day].forEach(event => {
      modalEvents.innerHTML += `<li>
        <strong>${event.name}</strong><br>
        ${event.time} @ ${event.venue}<br>
        <em>${event.description}</em>
      </li>`;
    });
  } else {
    modalEvents.innerHTML = '<li>No events on this day.</li>';
  }

  modal.classList.add('show');
}

function closeModal() {
  const modal = document.getElementById('eventModal');
  modal.classList.remove('show');
}

function previewImage(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      document.getElementById("eventImagePreview").src = e.target.result;
      document.getElementById("eventImagePreview").style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

let selectedEventId = null;
let filterYear = "All";

function deleteEvent() {
  if (!selectedEventId) {
    alert("No event selected to delete.");
    return;
  }
  if (!confirm("Are you sure you want to delete this event?")) {
    return;
  }
  // Redirect to delete event URL with event ID
  window.location.href = `/delete_event/${selectedEventId}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const filterForm = document.getElementById('filterForm');
  const prevMonthBtn = document.getElementById('prevMonthBtn');
  const nextMonthBtn = document.getElementById('nextMonthBtn');
  const monthSelect = document.getElementById('monthSelect');
  const yearSelect = document.getElementById('yearSelect');

  prevMonthBtn.addEventListener('click', () => {
    let month = parseInt(monthSelect.value);
    let year = parseInt(yearSelect.value);
    month -= 1;
    if (month < 1) {
      month = 12;
      year -= 1;
    }
    monthSelect.value = month;
    yearSelect.value = year;
    filterForm.submit();
  });

  nextMonthBtn.addEventListener('click', () => {
    let month = parseInt(monthSelect.value);
    let year = parseInt(yearSelect.value);
    month += 1;
    if (month > 12) {
      month = 1;
      year += 1;
    }
    monthSelect.value = month;
    yearSelect.value = year;
    filterForm.submit();
  });

  // Show editEventBox form on calendar date click for faculty/admin
  const calendar = document.getElementById('calendar');
  const editEventBox = document.getElementById('editEventBox');
  const editDate = document.getElementById('editDate');
  const eventDateInput = document.getElementById('eventDate');
  const eventSemSelect = document.getElementById('eventSem');
  const eventForm = document.getElementById('eventForm');

  calendar.querySelectorAll('.day:not(.header):not(.empty)').forEach(dayEl => {
    dayEl.addEventListener('click', (event) => {
      event.stopPropagation();
      const day = dayEl.querySelector('.date-number')?.textContent;
      alert('Clicked day: ' + day);
      if (!day) return;

      console.log('User role:', window.userRole);
      console.log('Current filterYear:', filterYear);
      if (window.userRole && (window.userRole === 'faculty' || window.userRole === 'admin')) {
        let year = yearSelect.value;
        const month = String(monthSelect.value).padStart(2, '0');
        console.log('yearSelect.value:', year);
        console.log('monthSelect.value:', monthSelect.value);
        const dayPadded = String(day).padStart(2, '0');
        // If filterYear is 'All' or yearSelect is disabled, use current year as fallback
        if (filterYear === 'All' || !year || yearSelect.disabled) {
          year = new Date().getFullYear();
          console.log('Using fallback year:', year);
        }
        const selectedDateStr = `${year}-${month}-${dayPadded}`;

        selectedDate = selectedDateStr;
        selectedEventId = null; // Reset selected event ID on new date selection
        editDate.textContent = `Selected Date: ${selectedDateStr}`;
        eventDateInput.value = selectedDateStr;

        // Reset semester select to default on new date selection
        if (eventSemSelect) {
          eventSemSelect.value = "";
        }

        // Reset form action to add_event for new event
        eventForm.action = "/add_event";
        // Clear hidden event ID input
        document.getElementById('eventId').value = "";

        // Clear other form fields
        document.getElementById('eventTitle').value = "";
        document.getElementById('eventTime').value = "";
        document.getElementById('eventVenue').value = "";
        document.getElementById('eventDescription').value = "";
        document.getElementById('eventYear').value = "";

        editEventBox.classList.add('show');
        console.log('Event form shown');
      } else {
        console.log('User role not authorized to add events');
      }
    });
  });

  // Hide editEventBox when clicking outside
  document.addEventListener('click', (e) => {
    if (!editEventBox.contains(e.target) && !e.target.closest('.day')) {
      editEventBox.classList.remove('show');
      selectedDate = null;
      selectedEventId = null;
      editDate.textContent = '';
    }
  });

  // Add click listeners to event list items to allow editing and selecting event for deletion
  document.querySelectorAll('.event-list li').forEach(eventLi => {
    eventLi.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!(window.userRole && (window.userRole === 'faculty' || window.userRole === 'admin'))) {
        return;
      }
      const eventName = eventLi.querySelector('strong')?.textContent || '';
      const eventDetails = eventLi.textContent || '';
      const eventTimeVenue = eventDetails.match(/(\d{2}:\d{2}) @ (.+)/);
      const eventTime = eventTimeVenue ? eventTimeVenue[1] : '';
      const eventVenue = eventTimeVenue ? eventTimeVenue[2] : '';
      const eventDescription = eventLi.querySelector('em')?.textContent || '';
      const eventIdForm = eventLi.querySelector('form');
      const eventId = eventIdForm ? eventIdForm.action.match(/\/delete_event\/(\d+)/)[1] : null;

      // Get event date from data attribute
      const eventDate = eventLi.getAttribute('data-event-date') || '';

      selectedEventId = eventId;
      selectedDate = null;
      editDate.textContent = `Editing Event: ${eventName}`;
      eventDateInput.value = eventDate; // Set the date input value from data attribute
      document.getElementById('eventTitle').value = eventName;
      document.getElementById('eventTime').value = eventTime;
      document.getElementById('eventVenue').value = eventVenue;
      document.getElementById('eventDescription').value = eventDescription;
      if (eventSemSelect) {
        eventSemSelect.value = ""; // No semester info in event list, reset
      }

      // Set form action to edit_event for editing
      eventForm.action = "/edit_event";
      // Set hidden event ID input
      document.getElementById('eventId').value = eventId;

      editEventBox.classList.add('show');
    });
  });
});

// Removed duplicate 'DOMContentLoaded' event listener block

function toggleProfileMenu(event) {
  event.preventDefault();
  const profileMenu = document.getElementById('profileMenu');
  const settingsMenu = document.getElementById('settingsMenu');
  if (profileMenu.style.display === 'block') {
    profileMenu.style.display = 'none';
  } else {
    profileMenu.style.display = 'block';
    settingsMenu.style.display = 'none';
  }
}

function toggleSettingsMenu(event) {
  event.preventDefault();
  const settingsMenu = document.getElementById('settingsMenu');
  const profileMenu = document.getElementById('profileMenu');
  if (settingsMenu.style.display === 'block') {
    settingsMenu.style.display = 'none';
  } else {
    settingsMenu.style.display = 'block';
    profileMenu.style.display = 'none';
  }
}

function previewProfilePhoto(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      document.getElementById('profilePhoto').src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function saveProfilePhoto() {
  alert('Profile photo saved (functionality to be implemented)');
}

function saveSettings(event) {
  event.preventDefault();
  alert('Settings saved (functionality to be implemented)');
}

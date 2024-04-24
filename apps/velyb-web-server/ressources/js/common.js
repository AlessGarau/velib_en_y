// Notification should disappear after 3 seconds
notificationElement = document.getElementById('notification');

if (notificationElement) {
    setTimeout(() => {
        notificationElement.classList.add('hide');
        notificationElement.remove()
    }, 3000);

}
